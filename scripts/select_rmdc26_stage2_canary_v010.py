#!/usr/bin/env python3
"""Select a deterministic, evidence-stratified RMDC26 Stage 2 canary set.

This script does not fit higher-order models and does not modify Stage 1 outputs.
It reads the locked Stage 1 result table, restricts to successful
``anomalous_route`` rows, and selects a compact canary spanning several residual
and quality regimes before any bulk Stage 2 execution.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

SCRIPT_VERSION = "0.1.0"
DEFAULT_INPUT = (
    Path.home()
    / "Stellar_Intelligence"
    / "outputs"
    / "fits_v022_full"
    / "rmdc26_1s1l_baseline.parquet"
)
DEFAULT_OUTPUT_DIR = (
    Path.home()
    / "Stellar_Intelligence"
    / "outputs"
    / "stage2_canary_v010"
)

REQUIRED_COLUMNS = {
    "event_id",
    "route",
    "fit_status",
    "reduced_chi2",
    "p99_abs_sigma",
    "fraction_abs_gt5",
    "max_run_gt4",
    "parameter_boundary_flag",
    "flux_quality_flag",
}


@dataclass(frozen=True)
class Quotas:
    strongest_chi2: int = 4
    coherent_run: int = 3
    high_p99: int = 3
    quality_boundary: int = 2
    moderate_ambiguous: int = 4

    @property
    def total(self) -> int:
        return (
            self.strongest_chi2
            + self.coherent_run
            + self.high_p99
            + self.quality_boundary
            + self.moderate_ambiguous
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--count", type=int, default=16)
    return parser.parse_args()


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"unsupported Stage 1 table format: {path.suffix}")


def require_columns(frame: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"missing required Stage 1 columns: {missing}")


def _finite_numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan)


def _append_unique(
    selected: list[dict[str, object]],
    seen: set[str],
    rows: Iterable[pd.Series],
    category: str,
    quota: int,
) -> None:
    added = 0
    for row in rows:
        event_id = str(row["event_id"])
        if event_id in seen:
            continue
        payload = row.to_dict()
        payload["canary_category"] = category
        selected.append(payload)
        seen.add(event_id)
        added += 1
        if added >= quota:
            break


def select_canary(frame: pd.DataFrame, count: int = 16) -> pd.DataFrame:
    require_columns(frame)
    if count <= 0:
        raise ValueError("count must be positive")

    work = frame.copy()
    work = work[
        (work["route"].astype(str) == "anomalous_route")
        & (work["fit_status"].astype(str) == "fit_success")
    ].copy()

    if len(work) < count:
        raise ValueError(
            f"not enough successful anomalous rows for count={count}: {len(work)}"
        )

    for column in (
        "reduced_chi2",
        "p99_abs_sigma",
        "fraction_abs_gt5",
        "max_run_gt4",
    ):
        work[column] = _finite_numeric(work, column)

    work["parameter_boundary_flag"] = work["parameter_boundary_flag"].fillna(False).astype(bool)
    work["flux_quality_flag"] = work["flux_quality_flag"].fillna(False).astype(bool)
    work["event_id"] = work["event_id"].astype(str)
    work = work.sort_values("event_id", kind="stable").reset_index(drop=True)

    quotas = Quotas()
    scale = count / quotas.total
    requested = {
        "strongest_chi2": max(1, round(quotas.strongest_chi2 * scale)),
        "coherent_run": max(1, round(quotas.coherent_run * scale)),
        "high_p99": max(1, round(quotas.high_p99 * scale)),
        "quality_boundary": max(1, round(quotas.quality_boundary * scale)),
        "moderate_ambiguous": max(1, round(quotas.moderate_ambiguous * scale)),
    }

    # Make the requested total exact while retaining at least one per category.
    while sum(requested.values()) > count:
        key = max(requested, key=requested.get)
        if requested[key] > 1:
            requested[key] -= 1
        else:
            break
    while sum(requested.values()) < count:
        requested["moderate_ambiguous"] += 1

    selected: list[dict[str, object]] = []
    seen: set[str] = set()

    strongest = work.sort_values(
        ["reduced_chi2", "p99_abs_sigma", "event_id"],
        ascending=[False, False, True],
        kind="stable",
    )
    _append_unique(
        selected,
        seen,
        (row for _, row in strongest.iterrows()),
        "strongest_chi2",
        requested["strongest_chi2"],
    )

    coherent = work.sort_values(
        ["max_run_gt4", "fraction_abs_gt5", "event_id"],
        ascending=[False, False, True],
        kind="stable",
    )
    _append_unique(
        selected,
        seen,
        (row for _, row in coherent.iterrows()),
        "coherent_run",
        requested["coherent_run"],
    )

    p99 = work.sort_values(
        ["p99_abs_sigma", "reduced_chi2", "event_id"],
        ascending=[False, False, True],
        kind="stable",
    )
    _append_unique(
        selected,
        seen,
        (row for _, row in p99.iterrows()),
        "high_p99",
        requested["high_p99"],
    )

    quality = work[
        work["parameter_boundary_flag"] | work["flux_quality_flag"]
    ].sort_values(
        ["parameter_boundary_flag", "flux_quality_flag", "reduced_chi2", "event_id"],
        ascending=[False, False, False, True],
        kind="stable",
    )
    _append_unique(
        selected,
        seen,
        (row for _, row in quality.iterrows()),
        "quality_boundary",
        requested["quality_boundary"],
    )

    # Moderate anomalies sample the middle of the anomaly distribution rather
    # than merely taking the next-highest extremes.
    rank_columns = ["reduced_chi2", "p99_abs_sigma", "fraction_abs_gt5", "max_run_gt4"]
    percentile_components = []
    for column in rank_columns:
        percentile_components.append(work[column].rank(pct=True, method="average"))
    work["anomaly_percentile_mean"] = pd.concat(percentile_components, axis=1).mean(axis=1)
    moderate = work.assign(
        distance_from_mid=(work["anomaly_percentile_mean"] - 0.5).abs()
    ).sort_values(
        ["distance_from_mid", "event_id"],
        ascending=[True, True],
        kind="stable",
    )
    _append_unique(
        selected,
        seen,
        (row for _, row in moderate.iterrows()),
        "moderate_ambiguous",
        requested["moderate_ambiguous"],
    )

    if len(selected) < count:
        # Deterministic fallback fills any category shortfall without changing
        # the already-assigned category labels.
        fallback = work.sort_values(
            ["reduced_chi2", "event_id"],
            ascending=[False, True],
            kind="stable",
        )
        _append_unique(
            selected,
            seen,
            (row for _, row in fallback.iterrows()),
            "fallback_unfilled_quota",
            count - len(selected),
        )

    result = pd.DataFrame(selected).head(count).copy()
    if len(result) != count:
        raise RuntimeError(f"selector produced {len(result)} rows, expected {count}")
    if result["event_id"].nunique() != count:
        raise RuntimeError("selector produced duplicate event IDs")
    if not (result["route"] == "anomalous_route").all():
        raise RuntimeError("selector emitted a non-anomalous route")
    if not (result["fit_status"] == "fit_success").all():
        raise RuntimeError("selector emitted a non-successful Stage 1 fit")

    preferred = [
        "event_id",
        "canary_category",
        "route",
        "fit_status",
        "reduced_chi2",
        "p99_abs_sigma",
        "fraction_abs_gt5",
        "max_run_gt4",
        "parameter_boundary_flag",
        "flux_quality_flag",
        "t0",
        "u0",
        "tE",
        "log_likelihood",
        "delta_chi2_vs_constant",
        "n_data_points",
        "n_fit_points",
    ]
    columns = [column for column in preferred if column in result.columns]
    return result[columns].reset_index(drop=True)


def write_outputs(result: pd.DataFrame, output_dir: Path, source: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "rmdc26_stage2_canary_v010.csv"
    json_path = output_dir / "rmdc26_stage2_canary_v010.json"

    result.to_csv(csv_path, index=False)
    payload = {
        "manifest_type": "RMDC26_STAGE2_CANARY_SELECTION",
        "selector_version": SCRIPT_VERSION,
        "source_stage1_table": str(source),
        "count": int(len(result)),
        "event_ids": result["event_id"].tolist(),
        "category_counts": result["canary_category"].value_counts().sort_index().to_dict(),
        "rows": result.to_dict(orient="records"),
        "scope": {
            "higher_order_models_executed": False,
            "stage1_modified": False,
            "submission_modified": False,
        },
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return csv_path, json_path


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not source.is_file():
        raise FileNotFoundError(f"Stage 1 result table not found: {source}")

    frame = read_table(source)
    result = select_canary(frame, count=args.count)
    csv_path, json_path = write_outputs(result, output_dir, source)

    print("RMDC26 Stage 2 canary selection complete")
    print(f"Selector version: {SCRIPT_VERSION}")
    print(f"Selected: {len(result)}")
    print(f"Unique event IDs: {result['event_id'].nunique()}")
    print("Category counts:")
    for category, value in result["canary_category"].value_counts().sort_index().items():
        print(f"  {category}: {value}")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    print("HIGHER_ORDER_MODELS_EXECUTED=NO")
    print("STAGE1_MODIFIED=NO")
    print("SUBMISSION_MODIFIED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
