#!/usr/bin/env python3
"""ASTRID Stage 1 photometric baseline fitter for RMDC26 Experienced data.

Purpose
-------
Fit a fast, reproducible 1S1L/PSPL photometric baseline to each event, solve
source/blend fluxes analytically per band, and route poor fits to later
binary/higher-order analysis. The routing label is triage metadata, not a
final scientific classification.

Designed for the Roman Research Nexus dataset:
    /data/data-challenge/rges/RMDC26_Experienced_Data.parquet

Outputs are checkpointed as Parquet and CSV and are shaped for later conversion
to ``microlens-submit`` CSV imports.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import duckdb
import numpy as np
import pandas as pd
from scipy import __version__ as scipy_version
from scipy.optimize import minimize

SCRIPT_VERSION = "0.2.2"
DEFAULT_SOURCE = Path("/data/data-challenge/rges/RMDC26_Experienced_Data.parquet")
DEFAULT_OUTPUT_DIR = Path.home() / "Stellar_Intelligence" / "outputs" / "fits"


@dataclass(frozen=True)
class FitConfig:
    max_fit_points: int = 6000
    t0_candidates: int = 5
    coarse_starts: int = 12
    maxiter: int = 240
    anomaly_red_chi2: float = 2.0
    anomaly_p99_abs_sigma: float = 5.0
    anomaly_fraction_gt5: float = 0.002
    anomaly_max_run_gt4: int = 8


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--event-id", action="append", default=[], help="Repeat for multiple events.")
    parser.add_argument("--limit", type=int, default=5, help="Number of unprocessed events; 0 means all.")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--max-fit-points", type=int, default=6000)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--memory-limit", default="4GB")
    parser.add_argument("--checkpoint-every", type=int, default=5)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def pspl_magnification(t: np.ndarray, t0: float, u0: float, t_e: float) -> np.ndarray:
    tau = (t - t0) / t_e
    u2 = u0 * u0 + tau * tau
    u = np.sqrt(np.maximum(u2, 1.0e-18))
    return (u2 + 2.0) / (u * np.sqrt(u2 + 4.0))


def robust_scale(values: np.ndarray) -> float:
    med = float(np.median(values))
    mad = float(np.median(np.abs(values - med)))
    return max(1.4826 * mad, np.finfo(float).eps)


def standardized_excess(flux: np.ndarray, err: np.ndarray, band_codes: np.ndarray) -> np.ndarray:
    z = np.zeros_like(flux, dtype=float)
    for band in np.unique(band_codes):
        mask = band_codes == band
        baseline = float(np.median(flux[mask]))
        scatter = robust_scale(flux[mask])
        denom = np.sqrt(np.square(err[mask]) + scatter * scatter)
        z[mask] = (flux[mask] - baseline) / denom
    return z


def choose_fit_subset(t: np.ndarray, z: np.ndarray, max_points: int) -> np.ndarray:
    n = t.size
    if n <= max_points:
        return np.arange(n, dtype=int)

    # Preserve anomalous/high-information epochs, then fill deterministically.
    priority = np.flatnonzero(np.abs(z) >= 3.0)
    if priority.size > max_points // 2:
        ranked = priority[np.argsort(np.abs(z[priority]))[::-1]]
        priority = ranked[: max_points // 2]

    remaining_count = max_points - priority.size
    regular = np.linspace(0, n - 1, remaining_count, dtype=int)
    selected = np.unique(np.concatenate([priority, regular]))

    if selected.size > max_points:
        selected = selected[:max_points]
    elif selected.size < max_points:
        missing = np.setdiff1d(np.arange(n), selected, assume_unique=False)
        selected = np.sort(np.concatenate([selected, missing[: max_points - selected.size]]))
    return selected


def candidate_t0s(t: np.ndarray, z: np.ndarray, count: int) -> list[float]:
    order = np.argsort(z)[::-1]
    selected: list[float] = []
    span = float(np.ptp(t))
    separation = max(0.05, min(1.0, span / 5000.0))
    for idx in order:
        if not np.isfinite(z[idx]):
            continue
        value = float(t[idx])
        if all(abs(value - prior) >= separation for prior in selected):
            selected.append(value)
            if len(selected) >= count:
                break
    if not selected:
        selected = [float(np.median(t))]
    return selected


def solve_band_fluxes(
    magnification: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    band_codes: np.ndarray,
) -> tuple[np.ndarray, dict[int, tuple[float, float]]]:
    model = np.empty_like(flux, dtype=float)
    coefficients: dict[int, tuple[float, float]] = {}

    for band in np.unique(band_codes):
        mask = band_codes == band
        a = magnification[mask]
        y = flux[mask]
        sigma = err[mask]
        w = 1.0 / np.square(sigma)

        s_aa = float(np.sum(w * a * a))
        s_a1 = float(np.sum(w * a))
        s_11 = float(np.sum(w))
        s_ay = float(np.sum(w * a * y))
        s_1y = float(np.sum(w * y))

        normal = np.array([[s_aa, s_a1], [s_a1, s_11]], dtype=float)
        rhs = np.array([s_ay, s_1y], dtype=float)
        ridge = max(np.trace(normal), 1.0) * 1.0e-12
        normal.flat[::3] += ridge
        fs, fb = np.linalg.solve(normal, rhs)
        coefficients[int(band)] = (float(fs), float(fb))
        model[mask] = fs * a + fb

    return model, coefficients


def constant_chi2(flux: np.ndarray, err: np.ndarray, band_codes: np.ndarray) -> float:
    chi2 = 0.0
    for band in np.unique(band_codes):
        mask = band_codes == band
        w = 1.0 / np.square(err[mask])
        baseline = float(np.sum(w * flux[mask]) / np.sum(w))
        chi2 += float(np.sum(np.square((flux[mask] - baseline) / err[mask])))
    return chi2


def objective(
    theta: np.ndarray,
    t: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    band_codes: np.ndarray,
) -> float:
    t0, log_u0, log_t_e = map(float, theta)
    u0 = math.exp(log_u0)
    t_e = math.exp(log_t_e)
    try:
        magnification = pspl_magnification(t, t0, u0, t_e)
        model, coefficients = solve_band_fluxes(magnification, flux, err, band_codes)
    except (FloatingPointError, ValueError, np.linalg.LinAlgError):
        return 1.0e100

    # Keep the objective finite even when a trial produces negative source flux.
    # A negative fitted source is retained as explicit anomaly evidence instead of
    # creating a flat penalty plateau that can make L-BFGS-B report false success.
    if any(not np.isfinite(fs) or not np.isfinite(fb) for fs, fb in coefficients.values()):
        return 1.0e100
    residual = (flux - model) / err
    value = float(np.dot(residual, residual))
    return value if np.isfinite(value) else 1.0e100


def centered_objective(
    theta: np.ndarray,
    t_ref: float,
    t: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    band_codes: np.ndarray,
) -> float:
    dt0, log_u0, log_t_e = map(float, theta)
    return objective(
        np.array([t_ref + dt0, log_u0, log_t_e], dtype=float),
        t,
        flux,
        err,
        band_codes,
    )


def max_consecutive_threshold(values: np.ndarray, threshold: float) -> int:
    longest = current = 0
    for flag in np.abs(values) >= threshold:
        if flag:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def residual_metrics(residual_sigma: np.ndarray, band_codes: np.ndarray, t: np.ndarray) -> dict[str, Any]:
    abs_r = np.abs(residual_sigma)
    max_run = 0
    for band in np.unique(band_codes):
        mask = band_codes == band
        order = np.argsort(t[mask])
        max_run = max(max_run, max_consecutive_threshold(residual_sigma[mask][order], 4.0))
    return {
        "max_abs_sigma": float(np.max(abs_r)),
        "p99_abs_sigma": float(np.quantile(abs_r, 0.99)),
        "fraction_abs_gt5": float(np.mean(abs_r >= 5.0)),
        "max_run_gt4": int(max_run),
    }


def route_fit(red_chi2: float, metrics: dict[str, Any], config: FitConfig) -> tuple[str, str]:
    reasons: list[str] = []
    if red_chi2 >= config.anomaly_red_chi2:
        reasons.append(f"reduced_chi2={red_chi2:.3f}")
    if metrics["p99_abs_sigma"] >= config.anomaly_p99_abs_sigma:
        reasons.append(f"p99_abs_sigma={metrics['p99_abs_sigma']:.3f}")
    if metrics["fraction_abs_gt5"] >= config.anomaly_fraction_gt5:
        reasons.append(f"fraction_abs_gt5={metrics['fraction_abs_gt5']:.5f}")
    if metrics["max_run_gt4"] >= config.anomaly_max_run_gt4:
        reasons.append(f"max_run_gt4={metrics['max_run_gt4']}")
    if reasons:
        return "anomalous_route", "; ".join(reasons)
    return "1S1L_candidate", "passes Stage 1 photometric residual thresholds"


def prepare_event(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    frame = frame.copy()
    frame = frame[
        (~frame["saturation_flag"].astype(bool))
        & np.isfinite(frame["bjd"])
        & np.isfinite(frame["flux_uJy"])
        & np.isfinite(frame["flux_err_uJy"])
        & (frame["flux_err_uJy"] > 0)
    ]
    if frame.empty:
        raise ValueError("no valid unsaturated photometric rows")

    frame = frame.sort_values("bjd", kind="stable")
    labels = sorted(frame["filt"].astype(str).unique().tolist())
    mapping = {label: index for index, label in enumerate(labels)}
    band_codes = frame["filt"].astype(str).map(mapping).to_numpy(dtype=int)
    return (
        frame["bjd"].to_numpy(dtype=float),
        frame["flux_uJy"].to_numpy(dtype=float),
        frame["flux_err_uJy"].to_numpy(dtype=float),
        band_codes,
        labels,
    )


def build_data_quality_row(event_id: str, frame: pd.DataFrame, reason: str) -> dict[str, Any]:
    """Create a coverage-preserving row when Stage 1 photometry cannot be fit."""
    started = time.perf_counter()
    total_rows = int(len(frame))
    saturated = (
        frame["saturation_flag"].fillna(False).astype(bool)
        if "saturation_flag" in frame
        else pd.Series(False, index=frame.index)
    )
    finite_photometry = (
        np.isfinite(frame["bjd"])
        & np.isfinite(frame["flux_uJy"])
        & np.isfinite(frame["flux_err_uJy"])
    ) if total_rows else np.zeros(0, dtype=bool)
    positive_error = (frame["flux_err_uJy"] > 0) if total_rows else np.zeros(0, dtype=bool)
    valid_unsaturated = (
        (~saturated.to_numpy(dtype=bool))
        & np.asarray(finite_photometry, dtype=bool)
        & np.asarray(positive_error, dtype=bool)
    ) if total_rows else np.zeros(0, dtype=bool)

    saturated_count = int(saturated.sum())
    finite_count = int(np.sum(finite_photometry))
    positive_error_count = int(np.sum(positive_error))
    valid_count = int(np.sum(valid_unsaturated))
    labels = (
        sorted(frame["filt"].dropna().astype(str).unique().tolist())
        if "filt" in frame
        else []
    )

    quality_flags = [reason]
    if total_rows == 0:
        quality_flags.append("event_has_no_rows")
    if total_rows > 0 and saturated_count == total_rows:
        quality_flags.append("all_rows_saturated")
    elif total_rows > 0 and saturated_count > 0:
        quality_flags.append("contains_saturated_rows")
    if finite_count == 0:
        quality_flags.append("no_finite_photometry")
    if positive_error_count == 0:
        quality_flags.append("no_positive_flux_errors")

    nan = float("nan")
    return {
        "event_id": event_id,
        "solution_alias": "astrid_stage1_unfit_photometry",
        "model_tags": json.dumps([]),
        "model_type": "UNFIT_DATA_QUALITY",
        "route": "data_quality_route",
        "route_reason": "; ".join(quality_flags),
        "fit_status": "not_fit",
        "t0": nan,
        "t0_time_system": "input_bjd",
        "u0": nan,
        "tE": nan,
        "chi2": nan,
        "reduced_chi2": nan,
        "log_likelihood": nan,
        "constant_chi2": nan,
        "delta_chi2_vs_constant": nan,
        "n_data_points": total_rows,
        "n_fit_points": 0,
        "n_bands": len(labels),
        "band_map_json": json.dumps({str(i): label for i, label in enumerate(labels)}, sort_keys=True),
        "band_fluxes_json": json.dumps({}, sort_keys=True),
        "total_observation_count": total_rows,
        "saturated_observation_count": saturated_count,
        "finite_photometry_observation_count": finite_count,
        "positive_error_observation_count": positive_error_count,
        "valid_unsaturated_observation_count": valid_count,
        "negative_source_flux_bands": 0,
        "negative_source_flux_labels": json.dumps([]),
        "flux_quality_flag": False,
        "fit_quality_flag": True,
        "quality_review_route": "data_quality_review",
        "quality_flags_json": json.dumps(quality_flags),
        "parameter_boundary_flag": False,
        "optimizer_seed_stuck": False,
        "used_astrometry": False,
        "used_postage_stamps": False,
        "optimizer": "not_run",
        "optimizer_success": False,
        "optimizer_message": reason,
        "optimizer_starts": 0,
        "coarse_starts_evaluated": 0,
        "objective_fit_subset": nan,
        "max_abs_sigma": nan,
        "p99_abs_sigma": nan,
        "fraction_abs_gt5": nan,
        "max_run_gt4": 0,
        "runtime_seconds": time.perf_counter() - started,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "pipeline_stage": "ASTRID_OBSERVATION_QUALITY_GATE",
        "pipeline_version": SCRIPT_VERSION,
        "notes": (
            "No Stage 1 PSPL fit was attempted because no valid unsaturated "
            "photometric observations remained after the documented quality filter."
        ),
    }


def fit_event(event_id: str, frame: pd.DataFrame, config: FitConfig) -> dict[str, Any]:
    started = time.perf_counter()
    t, flux, err, band_codes, band_labels = prepare_event(frame)
    z = standardized_excess(flux, err, band_codes)
    subset = choose_fit_subset(t, z, config.max_fit_points)
    ts, ys, es, bs = t[subset], flux[subset], err[subset], band_codes[subset]

    t_min, t_max = float(np.min(t)), float(np.max(t))
    t_ref = float(np.median(t))
    span = max(t_max - t_min, 0.1)
    t_e_guesses = [
        value
        for value in (0.05, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0)
        if value < span
    ]
    if not t_e_guesses:
        t_e_guesses = [max(span / 10.0, 0.02)]
    u0_guesses = (0.02, 0.05, 0.1, 0.3, 1.0, 2.0)

    bounds = [
        (t_min - t_ref, t_max - t_ref),
        (math.log(1.0e-4), math.log(3.0)),
        (math.log(0.02), math.log(max(span, 0.03))),
    ]

    coarse: list[tuple[float, np.ndarray]] = []
    for t0_guess in candidate_t0s(t, z, config.t0_candidates):
        for u0_guess in u0_guesses:
            for t_e_guess in t_e_guesses:
                seed = np.array(
                    [t0_guess - t_ref, math.log(u0_guess), math.log(t_e_guess)],
                    dtype=float,
                )
                value = centered_objective(seed, t_ref, ts, ys, es, bs)
                if np.isfinite(value) and value < 1.0e95:
                    coarse.append((float(value), seed))

    if not coarse:
        raise RuntimeError("no finite coarse-grid PSPL starts")

    coarse.sort(key=lambda item: item[0])
    seeds = coarse[: max(1, config.coarse_starts)]
    best = None
    best_seed = None
    best_method = None
    starts_tested = 0

    for seed_value, seed in seeds:
        starts_tested += 1
        result = minimize(
            centered_objective,
            seed,
            args=(t_ref, ts, ys, es, bs),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": config.maxiter, "ftol": 1.0e-9, "maxls": 40},
        )
        method = "L-BFGS-B"

        moved = not np.allclose(result.x, seed, rtol=0.0, atol=1.0e-7)
        improved = np.isfinite(result.fun) and float(result.fun) < seed_value * (1.0 - 1.0e-8)
        if (not result.success) or (not moved) or (not improved):
            fallback = minimize(
                centered_objective,
                seed,
                args=(t_ref, ts, ys, es, bs),
                method="Powell",
                bounds=bounds,
                options={
                    "maxiter": max(80, config.maxiter // 2),
                    "xtol": 1.0e-5,
                    "ftol": 1.0e-7,
                },
            )
            if np.isfinite(fallback.fun) and float(fallback.fun) < float(result.fun):
                result = fallback
                method = "Powell-fallback"

        if best is None or float(result.fun) < float(best.fun):
            best = result
            best_seed = seed.copy()
            best_method = method

    if best is None or not np.isfinite(best.fun) or float(best.fun) >= 1.0e95:
        raise RuntimeError("all optimization starts failed")

    dt0, log_u0, log_t_e = map(float, best.x)
    t0 = t_ref + dt0
    u0, t_e = math.exp(log_u0), math.exp(log_t_e)
    magnification = pspl_magnification(t, t0, u0, t_e)
    model, band_fluxes = solve_band_fluxes(magnification, flux, err, band_codes)
    residual_sigma = (flux - model) / err
    chi2 = float(np.dot(residual_sigma, residual_sigma))
    n_bands = len(band_labels)
    dof = max(int(t.size - 3 - 2 * n_bands), 1)
    red_chi2 = chi2 / dof
    c_chi2 = constant_chi2(flux, err, band_codes)
    metrics = residual_metrics(residual_sigma, band_codes, t)
    route, route_reason = route_fit(red_chi2, metrics, config)

    negative_source_bands = [
        band_labels[index]
        for index, (fs, _fb) in sorted(band_fluxes.items())
        if fs <= 0.0
    ]
    # Single-band negative source flux is a fit-quality flag, not by itself
    # evidence for higher-order microlensing structure.
    flux_quality_flag = bool(negative_source_bands)
    quality_flags: list[str] = []
    if negative_source_bands:
        quality_flags.append(
            "negative_source_flux=" + ",".join(negative_source_bands)
        )

    near_t_e_lower = math.isclose(t_e, 0.02, rel_tol=0.0, abs_tol=1.0e-4)
    near_t_e_upper = math.isclose(t_e, max(span, 0.03), rel_tol=0.0, abs_tol=max(1.0e-3, span * 1.0e-6))
    near_u0_lower = math.isclose(u0, 1.0e-4, rel_tol=0.0, abs_tol=1.0e-6)
    near_u0_upper = math.isclose(u0, 3.0, rel_tol=0.0, abs_tol=1.0e-4)
    parameter_boundary_flag = near_t_e_lower or near_t_e_upper or near_u0_lower or near_u0_upper
    seed_stuck = bool(best_seed is not None and np.allclose(best.x, best_seed, rtol=0.0, atol=1.0e-7))

    # Parameter-boundary convergence is retained as model-quality metadata.
    # It does not automatically imply a higher-order light-curve anomaly.
    if parameter_boundary_flag:
        quality_flags.append("parameter_boundary")
    if seed_stuck:
        quality_flags.append("optimizer_seed_stuck")
        route = "quality_review"
        extra = "optimizer_seed_stuck"
        route_reason = extra if route_reason.startswith("passes Stage 1") else f"{route_reason}; {extra}"

    fit_quality_flag = bool(quality_flags)
    quality_review_route = "quality_review" if fit_quality_flag else "none"

    band_map = {str(index): label for index, label in enumerate(band_labels)}
    flux_payload = {
        str(index): {"band": band_labels[index], "source_flux_uJy": fs, "blend_flux_uJy": fb}
        for index, (fs, fb) in sorted(band_fluxes.items())
    }

    row: dict[str, Any] = {
        "event_id": event_id,
        "solution_alias": "astrid_stage1_pspl",
        "model_tags": json.dumps(["1S1L"]),
        "model_type": "1S1L",
        "route": route,
        "route_reason": route_reason,
        "fit_status": "fit_success",
        "t0": t0,
        "t0_time_system": "input_bjd",
        "u0": u0,
        "tE": t_e,
        "chi2": chi2,
        "reduced_chi2": red_chi2,
        "log_likelihood": -0.5 * chi2,
        "constant_chi2": c_chi2,
        "delta_chi2_vs_constant": c_chi2 - chi2,
        "n_data_points": int(t.size),
        "n_fit_points": int(subset.size),
        "n_bands": n_bands,
        "band_map_json": json.dumps(band_map, sort_keys=True),
        "band_fluxes_json": json.dumps(flux_payload, sort_keys=True),
        "total_observation_count": int(len(frame)),
        "saturated_observation_count": int(frame["saturation_flag"].fillna(False).astype(bool).sum()),
        "finite_photometry_observation_count": int(
            np.sum(
                np.isfinite(frame["bjd"])
                & np.isfinite(frame["flux_uJy"])
                & np.isfinite(frame["flux_err_uJy"])
            )
        ),
        "positive_error_observation_count": int(np.sum(frame["flux_err_uJy"] > 0)),
        "valid_unsaturated_observation_count": int(t.size),
        "negative_source_flux_bands": len(negative_source_bands),
        "negative_source_flux_labels": json.dumps(negative_source_bands),
        "flux_quality_flag": flux_quality_flag,
        "fit_quality_flag": fit_quality_flag,
        "quality_review_route": quality_review_route,
        "quality_flags_json": json.dumps(quality_flags),
        "parameter_boundary_flag": parameter_boundary_flag,
        "optimizer_seed_stuck": seed_stuck,
        "used_astrometry": False,
        "used_postage_stamps": False,
        "optimizer": f"scipy.optimize.minimize:{best_method}",
        "optimizer_success": bool(best.success),
        "optimizer_message": str(best.message),
        "optimizer_starts": starts_tested,
        "coarse_starts_evaluated": len(coarse),
        "objective_fit_subset": float(best.fun),
        "max_abs_sigma": metrics["max_abs_sigma"],
        "p99_abs_sigma": metrics["p99_abs_sigma"],
        "fraction_abs_gt5": metrics["fraction_abs_gt5"],
        "max_run_gt4": metrics["max_run_gt4"],
        "runtime_seconds": time.perf_counter() - started,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "pipeline_stage": "ASTRID_INTERPRETATION_STAGE1_PHOTOMETRIC_BASELINE",
        "pipeline_version": SCRIPT_VERSION,
        "notes": (
            "Stage 1 photometric PSPL baseline. Negative single-band source flux and "
            "parameter-boundary convergence are recorded as quality flags rather than "
            "automatic anomaly evidence. Route labels are computational triage, not "
            "final scientific classifications. Astrometry, parallax, finite-source, "
            "binary-lens, binary-source, and other higher-order effects are deferred."
        ),
    }
    for index, (fs, fb) in sorted(band_fluxes.items()):
        row[f"F{index}_S"] = fs
        row[f"F{index}_B"] = fb
    return row


def configure_duckdb(source: Path, output_dir: Path, threads: int, memory_limit: str) -> duckdb.DuckDBPyConnection:
    temp_dir = output_dir / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect()
    connection.execute(f"SET threads = {max(1, threads)}")
    connection.execute(f"SET memory_limit = '{memory_limit}'")
    connection.execute(f"SET temp_directory = '{temp_dir.as_posix()}'")
    connection.execute("SET preserve_insertion_order = false")
    return connection


def list_event_ids(
    connection: duckdb.DuckDBPyConnection,
    source: Path,
    requested: Iterable[str],
) -> list[str]:
    requested = [value.strip() for value in requested if value.strip()]
    if requested:
        return list(dict.fromkeys(requested))
    return (
        connection.execute(
            "SELECT DISTINCT name FROM read_parquet(?) ORDER BY name",
            [str(source)],
        )
        .df()["name"]
        .astype(str)
        .tolist()
    )


def read_event(connection: duckdb.DuckDBPyConnection, source: Path, event_id: str) -> pd.DataFrame:
    return connection.execute(
        """
        SELECT bjd, filt, flux_uJy, flux_err_uJy, saturation_flag
        FROM read_parquet(?)
        WHERE name = ?
        ORDER BY bjd
        """,
        [str(source), event_id],
    ).df()


def write_outputs(rows: list[dict[str, Any]], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / "rmdc26_1s1l_baseline.parquet"
    csv_path = output_dir / "rmdc26_1s1l_baseline.csv"
    frame = pd.DataFrame(rows).sort_values("event_id", kind="stable").reset_index(drop=True)
    frame.to_parquet(parquet_path, index=False)
    frame.to_csv(csv_path, index=False)
    return parquet_path, csv_path


def load_existing(output_dir: Path, overwrite: bool) -> list[dict[str, Any]]:
    path = output_dir / "rmdc26_1s1l_baseline.parquet"
    if overwrite or not path.exists():
        return []
    return pd.read_parquet(path).to_dict(orient="records")


def write_run_manifest(args: argparse.Namespace, config: FitConfig, output_dir: Path, source: Path) -> Path:
    manifest = {
        "manifest_type": "ASTRID_RMDC26_STAGE1_RUN",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "script_version": SCRIPT_VERSION,
        "source": {
            "path": str(source),
            "size_bytes": source.stat().st_size,
            "read_only": not os.access(source, os.W_OK),
        },
        "config": asdict(config),
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "duckdb": duckdb.__version__,
            "scipy": scipy_version,
            "threads": args.threads,
            "memory_limit": args.memory_limit,
        },
    }
    path = output_dir / "rmdc26_1s1l_baseline_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"RMDC26 source not found: {source}")
    output_dir.mkdir(parents=True, exist_ok=True)

    config = FitConfig(max_fit_points=max(500, args.max_fit_points))
    connection = configure_duckdb(source, output_dir, args.threads, args.memory_limit)
    existing = load_existing(output_dir, args.overwrite)
    processed = {str(row["event_id"]) for row in existing if row.get("event_id")}

    event_ids = list_event_ids(connection, source, args.event_id)
    event_ids = [event_id for event_id in event_ids if args.overwrite or event_id not in processed]
    if not args.event_id:
        start = max(args.offset, 0)
        stop = None if args.limit <= 0 else start + args.limit
        event_ids = event_ids[start:stop]
    print(f"ASTRID RMDC26 Stage 1 | selected={len(event_ids)} | already_processed={len(processed)}")

    rows = existing
    failures: list[dict[str, Any]] = []
    for index, event_id in enumerate(event_ids, start=1):
        try:
            frame = read_event(connection, source, event_id)
            try:
                row = fit_event(event_id, frame, config)
            except ValueError as exc:
                if str(exc) != "no valid unsaturated photometric rows":
                    raise
                row = build_data_quality_row(
                    event_id,
                    frame,
                    "no_valid_unsaturated_photometry",
                )
            rows.append(row)
            if row["fit_status"] == "fit_success":
                print(
                    f"[{index}/{len(event_ids)}] {event_id} "
                    f"route={row['route']} red_chi2={row['reduced_chi2']:.3f} "
                    f"tE={row['tE']:.3f}d runtime={row['runtime_seconds']:.2f}s"
                )
            else:
                print(
                    f"[{index}/{len(event_ids)}] {event_id} "
                    f"route={row['route']} reason={row['route_reason']} "
                    f"runtime={row['runtime_seconds']:.2f}s"
                )
        except Exception as exc:  # keep a large batch moving while retaining evidence
            failure = {
                "event_id": event_id,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
            }
            failures.append(failure)
            print(f"[{index}/{len(event_ids)}] {event_id} FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)

        if rows and (index % max(args.checkpoint_every, 1) == 0):
            write_outputs(rows, output_dir)

    parquet_path, csv_path = write_outputs(rows, output_dir) if rows else (None, None)
    manifest_path = write_run_manifest(args, config, output_dir, source)
    if failures:
        (output_dir / "rmdc26_1s1l_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")

    print("\nStage 1 complete")
    print(f"Parquet: {parquet_path}")
    print(f"CSV: {csv_path}")
    print(f"Manifest: {manifest_path}")
    print(f"Failures: {len(failures)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
