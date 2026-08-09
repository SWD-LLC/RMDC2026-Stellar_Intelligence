#!/usr/bin/env python3
"""Synthetic regression tests for the RMDC26 Stage 2 canary selector."""
from __future__ import annotations

import numpy as np
import pandas as pd

import select_rmdc26_stage2_canary_v010 as selector


def synthetic_stage1() -> pd.DataFrame:
    rows = []

    # 40 successful anomalous events spanning several residual/quality regimes.
    for i in range(40):
        rows.append(
            {
                "event_id": f"RMDC26_SYN_{i:04d}",
                "route": "anomalous_route",
                "fit_status": "fit_success",
                "reduced_chi2": 2.05 + i * 0.35,
                "p99_abs_sigma": 5.1 + (39 - i) * 0.18,
                "fraction_abs_gt5": 0.0025 + (i % 9) * 0.001,
                "max_run_gt4": 8 + (i % 13),
                "parameter_boundary_flag": i in {3, 17, 29},
                "flux_quality_flag": i in {5, 17, 31},
                "t0": 2_460_000.0 + i,
                "u0": 0.05 + i * 0.003,
                "tE": 10.0 + i,
                "log_likelihood": -1000.0 - i,
                "delta_chi2_vs_constant": 500.0 + i * 10.0,
                "n_data_points": 1000 + i,
                "n_fit_points": 800 + i,
            }
        )

    # These rows must never enter the canary.
    rows.extend(
        [
            {
                "event_id": "RMDC26_CLEAN_0001",
                "route": "1S1L_candidate",
                "fit_status": "fit_success",
                "reduced_chi2": 1.0,
                "p99_abs_sigma": 2.0,
                "fraction_abs_gt5": 0.0,
                "max_run_gt4": 0,
                "parameter_boundary_flag": False,
                "flux_quality_flag": False,
                "t0": 2_460_100.0,
                "u0": 0.2,
                "tE": 20.0,
                "log_likelihood": -100.0,
                "delta_chi2_vs_constant": 100.0,
                "n_data_points": 1000,
                "n_fit_points": 800,
            },
            {
                "event_id": "RMDC26_DQ_0001",
                "route": "data_quality_route",
                "fit_status": "not_fit",
                "reduced_chi2": np.nan,
                "p99_abs_sigma": np.nan,
                "fraction_abs_gt5": np.nan,
                "max_run_gt4": 0,
                "parameter_boundary_flag": False,
                "flux_quality_flag": False,
                "t0": np.nan,
                "u0": np.nan,
                "tE": np.nan,
                "log_likelihood": np.nan,
                "delta_chi2_vs_constant": np.nan,
                "n_data_points": 2,
                "n_fit_points": 0,
            },
        ]
    )

    return pd.DataFrame(rows)


def main() -> None:
    frame = synthetic_stage1()

    first = selector.select_canary(frame, count=16)
    second = selector.select_canary(frame.sample(frac=1.0, random_state=99), count=16)

    assert len(first) == 16
    assert first["event_id"].nunique() == 16
    assert (first["route"] == "anomalous_route").all()
    assert (first["fit_status"] == "fit_success").all()
    assert "RMDC26_CLEAN_0001" not in set(first["event_id"])
    assert "RMDC26_DQ_0001" not in set(first["event_id"])

    # Selection must be deterministic even when source-row order changes.
    assert first["event_id"].tolist() == second["event_id"].tolist()
    assert first["canary_category"].tolist() == second["canary_category"].tolist()

    categories = set(first["canary_category"])
    assert "strongest_chi2" in categories
    assert "coherent_run" in categories
    assert "high_p99" in categories
    assert "quality_boundary" in categories
    assert "moderate_ambiguous" in categories

    print("PASS: Stage 2 canary selector produced 16 unique anomalous events")
    print("PASS: clean and data-quality routes excluded")
    print("PASS: deterministic under shuffled input order")
    print("PASS: all target evidence strata represented")


if __name__ == "__main__":
    main()
