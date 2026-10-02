#!/usr/bin/env python3
"""RMDC26 Experienced-tier Stage 2 binary-lens rescue fitter.

This script is intentionally read-only with respect to the locked Stage 1
submission. It fits a small set of real RMDC26 Experienced-tier events with a
1S2L binary-lens model using VBMicrolensing and compares each result directly
against the locked Stage 1 1S1L baseline.

The fitting strategy follows the organizer's RMDC26 binary-lens workshop:
coarse search over (log10(s), log10(q), alpha), with local optimization of the
single-lens geometry at each fixed binary grid point.

No submission files are edited by this script.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd
from scipy.optimize import minimize

try:
    import VBMicrolensing as vbm
except ImportError as exc:
    raise SystemExit(
        "VBMicrolensing is required. On Roman Nexus use the RGES PIT Nexus "
        "kernel/environment, where the organizer notebook dependencies are installed."
    ) from exc

SCRIPT_VERSION = "0.1.0"

SOURCE_CANDIDATES = [
    Path("/data/data-challenge/rges/RMDC26_Experienced_Tier.parquet"),
    Path("/data/data-challenge/rges/RMDC26_Experienced_Data.parquet"),
]

DEFAULT_STAGE1 = (
    Path.home()
    / "Stellar_Intelligence"
    / "outputs"
    / "fits_v022_full"
    / "rmdc26_1s1l_baseline.parquet"
)

DEFAULT_CANARY = (
    Path.home()
    / "Stellar_Intelligence"
    / "outputs"
    / "stage2_canary_v010"
    / "rmdc26_stage2_canary_v010.csv"
)

DEFAULT_OUTPUT = (
    Path.home()
    / "Stellar_Intelligence"
    / "outputs"
    / "stage2_1s2l_rescue_v010"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--stage1", type=Path, default=DEFAULT_STAGE1)
    parser.add_argument("--canary", type=Path, default=DEFAULT_CANARY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--event-id",
        action="append",
        default=[],
        help="Repeat to fit explicit events. If omitted, events are read from --canary.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=4,
        help="Maximum events to fit from the canary. Default: 4.",
    )
    parser.add_argument(
        "--max-fit-points",
        type=int,
        default=600,
        help="Maximum photometric points per event used during the grid search.",
    )
    parser.add_argument(
        "--rho",
        type=float,
        default=1.0e-4,
        help=(
            "Fixed finite-source radius used by VBMicrolensing during the coarse "
            "binary search. This is a numerical fitting assumption and is not "
            "automatically promoted to submission metadata."
        ),
    )
    parser.add_argument(
        "--profile",
        choices=("quick", "coarse"),
        default="quick",
        help="Grid density. Use quick first; coarse is substantially more expensive.",
    )
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def resolve_source(explicit: Path | None) -> Path:
    if explicit is not None:
        source = explicit.expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        return source
    for candidate in SOURCE_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Could not find RMDC26 Experienced parquet. Checked: "
        + ", ".join(str(p) for p in SOURCE_CANDIDATES)
    )


def load_stage1(path: Path) -> pd.DataFrame:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Stage 1 table not found: {path}")
    if path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(path)
    else:
        frame = pd.read_csv(path)
    required = {
        "event_id",
        "route",
        "fit_status",
        "t0",
        "u0",
        "tE",
        "chi2",
        "reduced_chi2",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Stage 1 table missing columns: {missing}")
    frame["event_id"] = frame["event_id"].astype(str)
    return frame


def choose_events(args: argparse.Namespace, stage1: pd.DataFrame) -> list[str]:
    if args.event_id:
        event_ids = list(dict.fromkeys(str(x).strip() for x in args.event_id if str(x).strip()))
    else:
        canary = args.canary.expanduser().resolve()
        if canary.is_file():
            c = pd.read_csv(canary)
            if "event_id" not in c.columns:
                raise ValueError(f"Canary file lacks event_id: {canary}")
            event_ids = c["event_id"].astype(str).tolist()
        else:
            # Safe fallback: strongest successful anomalous Stage 1 fits.
            work = stage1[
                (stage1["route"].astype(str) == "anomalous_route")
                & (stage1["fit_status"].astype(str) == "fit_success")
            ].copy()
            work["reduced_chi2"] = pd.to_numeric(work["reduced_chi2"], errors="coerce")
            work = work.sort_values(
                ["reduced_chi2", "event_id"],
                ascending=[False, True],
                kind="stable",
            )
            event_ids = work["event_id"].astype(str).tolist()
    if args.limit > 0:
        event_ids = event_ids[: args.limit]
    if not event_ids:
        raise ValueError("No events selected")
    return event_ids


def read_event(con: duckdb.DuckDBPyConnection, source: Path, event_id: str) -> pd.DataFrame:
    return con.execute(
        """
        SELECT bjd, filt, flux_uJy, flux_err_uJy, saturation_flag
        FROM read_parquet(?)
        WHERE name = ?
        ORDER BY bjd
        """,
        [str(source), event_id],
    ).df()


def prepare_event(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    if frame.empty:
        raise ValueError("event has no rows")
    saturated = frame["saturation_flag"].fillna(False).astype(bool).to_numpy()
    valid = (
        (~saturated)
        & np.isfinite(frame["bjd"].to_numpy(dtype=float))
        & np.isfinite(frame["flux_uJy"].to_numpy(dtype=float))
        & np.isfinite(frame["flux_err_uJy"].to_numpy(dtype=float))
        & (frame["flux_err_uJy"].to_numpy(dtype=float) > 0.0)
    )
    clean = frame.loc[valid].copy()
    if clean.empty:
        raise ValueError("no valid unsaturated photometry")

    labels = sorted(clean["filt"].astype(str).unique().tolist())
    mapping = {label: idx for idx, label in enumerate(labels)}
    return (
        clean["bjd"].to_numpy(dtype=float),
        clean["flux_uJy"].to_numpy(dtype=float),
        clean["flux_err_uJy"].to_numpy(dtype=float),
        clean["filt"].astype(str).map(mapping).to_numpy(dtype=int),
        labels,
    )


def pspl_magnification(t: np.ndarray, t0: float, u0: float, t_e: float) -> np.ndarray:
    tau = (t - t0) / t_e
    u2 = u0 * u0 + tau * tau
    u = np.sqrt(np.maximum(u2, 1.0e-18))
    return (u2 + 2.0) / (u * np.sqrt(u2 + 4.0))


def solve_band_fluxes(
    magnification: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    band_codes: np.ndarray,
) -> tuple[np.ndarray, dict[int, tuple[float, float]]]:
    model = np.empty_like(flux, dtype=float)
    coeff: dict[int, tuple[float, float]] = {}
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
        ridge = max(float(np.trace(normal)), 1.0) * 1.0e-12
        normal.flat[::3] += ridge
        fs, fb = np.linalg.solve(normal, rhs)
        coeff[int(band)] = (float(fs), float(fb))
        model[mask] = fs * a + fb
    return model, coeff


def stage1_model(
    t: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    bands: np.ndarray,
    row: pd.Series,
) -> tuple[np.ndarray, float]:
    mag = pspl_magnification(t, float(row["t0"]), abs(float(row["u0"])), float(row["tE"]))
    model, _ = solve_band_fluxes(mag, flux, err, bands)
    residual = (flux - model) / err
    return residual, float(np.dot(residual, residual))


def select_fit_subset(
    t: np.ndarray,
    residual_sigma: np.ndarray,
    max_points: int,
) -> np.ndarray:
    n = len(t)
    if n <= max_points:
        return np.arange(n, dtype=int)

    # Preserve the strongest Stage 1 residual structure and fill the rest
    # deterministically across the full time range.
    priority = np.argsort(np.abs(residual_sigma))[::-1][: max_points // 2]
    regular = np.linspace(0, n - 1, max_points - len(priority), dtype=int)
    selected = np.unique(np.concatenate([priority, regular]))
    if len(selected) < max_points:
        missing = np.setdiff1d(np.arange(n), selected)
        selected = np.concatenate([selected, missing[: max_points - len(selected)]])
    return np.sort(selected[:max_points])


VBM = vbm.VBMicrolensing()


def binary_magnification(
    t: np.ndarray,
    t0: float,
    u0: float,
    t_e: float,
    s: float,
    q: float,
    alpha_deg: float,
    rho: float,
) -> np.ndarray:
    tau = (t - t0) / t_e
    alpha = np.radians(alpha_deg)
    sin_a = np.sin(alpha)
    cos_a = np.cos(alpha)
    xs = -u0 * sin_a + tau * cos_a
    ys = u0 * cos_a + tau * sin_a
    try:
        return np.asarray(
            [VBM.BinaryMag2(s, q, float(x), float(y), rho) for x, y in zip(xs, ys)],
            dtype=float,
        )
    except Exception:
        return np.full(len(t), np.nan, dtype=float)


def binary_chi2(
    theta: np.ndarray,
    fixed: tuple[float, float, float, float],
    t: np.ndarray,
    flux: np.ndarray,
    err: np.ndarray,
    bands: np.ndarray,
) -> float:
    t0, u0, log_t_e = map(float, theta)
    log_s, log_q, alpha_deg, rho = fixed
    t_e = math.exp(log_t_e)
    s = 10.0 ** log_s
    q = 10.0 ** log_q

    mag = binary_magnification(t, t0, u0, t_e, s, q, alpha_deg, rho)
    if (not np.isfinite(mag).all()) or np.any(mag <= 0):
        return 1.0e100
    try:
        model, coeff = solve_band_fluxes(mag, flux, err, bands)
    except (ValueError, np.linalg.LinAlgError, FloatingPointError):
        return 1.0e100
    if any(not np.isfinite(v) for pair in coeff.values() for v in pair):
        return 1.0e100
    residual = (flux - model) / err
    value = float(np.dot(residual, residual))
    return value if np.isfinite(value) else 1.0e100


def grids(profile: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if profile == "quick":
        return (
            np.linspace(-0.7, 0.7, 5),
            np.array([-4.0, -3.0, -2.0, -1.0, -0.3]),
            np.arange(0.0, 360.0, 45.0),
        )
    return (
        np.linspace(-1.0, 1.0, 9),
        np.linspace(-4.5, 0.0, 10),
        np.arange(0.0, 360.0, 30.0),
    )


def fit_event_1s2l(
    event_id: str,
    stage1_row: pd.Series,
    frame: pd.DataFrame,
    max_fit_points: int,
    rho: float,
    profile: str,
    verbose: bool,
) -> dict[str, Any]:
    started = time.perf_counter()
    t, flux, err, bands, band_labels = prepare_event(frame)
    stage1_residual, stage1_chi2_full = stage1_model(t, flux, err, bands, stage1_row)
    subset = select_fit_subset(t, stage1_residual, max_fit_points)
    ts, fs, es, bs = t[subset], flux[subset], err[subset], bands[subset]

    t0_init = float(stage1_row["t0"])
    u0_init = float(stage1_row["u0"])
    t_e_init = max(float(stage1_row["tE"]), 0.02)

    span = max(float(np.ptp(ts)), 0.1)
    t0_margin = max(min(t_e_init, span / 2.0), 0.2)
    t0_bounds = (max(float(ts.min()), t0_init - t0_margin), min(float(ts.max()), t0_init + t0_margin))
    if t0_bounds[0] >= t0_bounds[1]:
        t0_bounds = (float(ts.min()), float(ts.max()))

    u0_scale = max(abs(u0_init), 0.05)
    u0_bounds = (-max(3.0, 3.0 * u0_scale), max(3.0, 3.0 * u0_scale))
    te_bounds = (math.log(0.02), math.log(max(span, t_e_init * 3.0, 0.03)))

    logs_vals, logq_vals, alpha_vals = grids(profile)
    best: dict[str, Any] | None = None
    tested = 0

    for log_s in logs_vals:
        for log_q in logq_vals:
            for alpha_deg in alpha_vals:
                tested += 1
                x0 = np.array([t0_init, u0_init, math.log(t_e_init)], dtype=float)
                fixed = (float(log_s), float(log_q), float(alpha_deg), float(rho))
                result = minimize(
                    binary_chi2,
                    x0,
                    args=(fixed, ts, fs, es, bs),
                    method="Nelder-Mead",
                    bounds=[t0_bounds, u0_bounds, te_bounds],
                    options={"maxfev": 240, "xatol": 1.0e-5, "fatol": 1.0e-4, "adaptive": False},
                )
                value = float(result.fun) if np.isfinite(result.fun) else 1.0e100
                if best is None or value < best["chi2_subset"]:
                    best = {
                        "chi2_subset": value,
                        "x": np.asarray(result.x, dtype=float),
                        "log_s": float(log_s),
                        "log_q": float(log_q),
                        "alpha_deg": float(alpha_deg),
                        "optimizer_success": bool(result.success),
                        "optimizer_message": str(result.message),
                    }
                if verbose and tested % 50 == 0:
                    print(f"  {event_id}: tested={tested} best_subset_chi2={best['chi2_subset']:.2f}")

    if best is None or best["chi2_subset"] >= 1.0e95:
        raise RuntimeError("no finite 1S2L grid solution")

    t0, u0, log_t_e = map(float, best["x"])
    t_e = math.exp(log_t_e)
    s = 10.0 ** float(best["log_s"])
    q = 10.0 ** float(best["log_q"])
    alpha_deg = float(best["alpha_deg"])

    mag_full = binary_magnification(t, t0, u0, t_e, s, q, alpha_deg, rho)
    if not np.isfinite(mag_full).all():
        raise RuntimeError("best 1S2L solution failed full-data magnification")
    model_full, flux_coeff = solve_band_fluxes(mag_full, flux, err, bands)
    residual_full = (flux - model_full) / err
    chi2_full = float(np.dot(residual_full, residual_full))

    n_bands = len(band_labels)
    dof_1s1l = max(len(t) - 3 - 2 * n_bands, 1)
    dof_1s2l = max(len(t) - 6 - 2 * n_bands, 1)

    flux_payload = {
        band_labels[index]: {
            "source_flux_uJy": float(pair[0]),
            "blend_flux_uJy": float(pair[1]),
        }
        for index, pair in sorted(flux_coeff.items())
    }

    return {
        "event_id": event_id,
        "stage1_t0": float(stage1_row["t0"]),
        "stage1_u0": float(stage1_row["u0"]),
        "stage1_tE": float(stage1_row["tE"]),
        "stage1_chi2_recomputed": stage1_chi2_full,
        "stage1_reduced_chi2_recomputed": stage1_chi2_full / dof_1s1l,
        "fit_model": "1S2L",
        "t0": t0,
        "u0": u0,
        "tE": t_e,
        "s": s,
        "q": q,
        "alpha_deg": alpha_deg,
        "alpha_rad": float(np.radians(alpha_deg)),
        "rho_fixed_for_search": float(rho),
        "chi2": chi2_full,
        "reduced_chi2": chi2_full / dof_1s2l,
        "delta_chi2_vs_stage1": stage1_chi2_full - chi2_full,
        "n_data_points": int(len(t)),
        "n_fit_points_grid": int(len(ts)),
        "n_bands": int(n_bands),
        "bands": band_labels,
        "band_fluxes": flux_payload,
        "grid_profile": profile,
        "grid_points_tested": int(tested),
        "optimizer_success": bool(best["optimizer_success"]),
        "optimizer_message": str(best["optimizer_message"]),
        "runtime_seconds": time.perf_counter() - started,
        "scope_note": (
            "Coarse 1S2L rescue fit using the organizer binary-lens strategy. "
            "rho was fixed during this search and is not automatically claimed as a "
            "finite-source measurement. Submission mapping requires separate review."
        ),
    }


def main() -> int:
    args = parse_args()
    source = resolve_source(args.source)
    stage1_path = args.stage1.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.rho <= 0:
        raise ValueError("--rho must be positive")

    stage1 = load_stage1(stage1_path)
    event_ids = choose_events(args, stage1)
    index = stage1.set_index("event_id", drop=False)

    missing = [event_id for event_id in event_ids if event_id not in index.index]
    if missing:
        raise ValueError(f"Selected events missing from Stage 1 table: {missing}")

    con = duckdb.connect()
    con.execute(f"SET threads = {max(1, int(args.threads))}")
    con.execute("SET preserve_insertion_order = false")

    print("RMDC26 Stage 2 1S2L rescue")
    print(f"script_version={SCRIPT_VERSION}")
    print(f"source={source}")
    print(f"stage1={stage1_path}")
    print(f"profile={args.profile}")
    print(f"events={len(event_ids)}")
    print("submission_mutation=NO")

    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for i, event_id in enumerate(event_ids, start=1):
        print(f"[{i}/{len(event_ids)}] {event_id}")
        try:
            row = index.loc[event_id]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]
            frame = read_event(con, source, event_id)
            result = fit_event_1s2l(
                event_id=event_id,
                stage1_row=row,
                frame=frame,
                max_fit_points=max(100, int(args.max_fit_points)),
                rho=float(args.rho),
                profile=args.profile,
                verbose=bool(args.verbose),
            )
            results.append(result)
            print(
                f"  delta_chi2={result['delta_chi2_vs_stage1']:.2f} "
                f"s={result['s']:.5g} q={result['q']:.5g} "
                f"alpha_deg={result['alpha_deg']:.1f} "
                f"runtime={result['runtime_seconds']:.1f}s"
            )
        except Exception as exc:
            failures.append(
                {
                    "event_id": event_id,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            print(f"  FAILED {type(exc).__name__}: {exc}")

        # Checkpoint after every event.
        if results:
            pd.DataFrame(results).drop(columns=["bands", "band_fluxes"], errors="ignore").to_csv(
                output_dir / "rmdc26_1s2l_rescue_results.csv",
                index=False,
            )
            (output_dir / "rmdc26_1s2l_rescue_results.json").write_text(
                json.dumps(results, indent=2),
                encoding="utf-8",
            )
        (output_dir / "rmdc26_1s2l_rescue_failures.json").write_text(
            json.dumps(failures, indent=2),
            encoding="utf-8",
        )

    if results:
        ranked = sorted(results, key=lambda x: x["delta_chi2_vs_stage1"], reverse=True)
        (output_dir / "rmdc26_1s2l_rescue_ranked.json").write_text(
            json.dumps(ranked, indent=2),
            encoding="utf-8",
        )
        print("\nRanked improvements:")
        for row in ranked:
            print(
                f"  {row['event_id']} "
                f"delta_chi2={row['delta_chi2_vs_stage1']:.2f} "
                f"redchi2={row['reduced_chi2']:.3f}"
            )

    manifest = {
        "manifest_type": "RMDC26_STAGE2_1S2L_RESCUE",
        "script_version": SCRIPT_VERSION,
        "source": str(source),
        "stage1": str(stage1_path),
        "event_ids": event_ids,
        "grid_profile": args.profile,
        "rho_fixed_for_search": float(args.rho),
        "result_count": len(results),
        "failure_count": len(failures),
        "submission_mutated": False,
        "stage1_mutated": False,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\noutput_dir={output_dir}")
    print(f"results={len(results)} failures={len(failures)}")
    print("STAGE1_MODIFIED=NO")
    print("SUBMISSION_MODIFIED=NO")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
