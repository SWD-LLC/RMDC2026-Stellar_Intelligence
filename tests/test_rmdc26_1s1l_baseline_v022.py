#!/usr/bin/env python3
"""Synthetic validation for ASTRID RMDC26 Stage 1 fitter v0.2.2."""
from __future__ import annotations

import numpy as np
import pandas as pd

import fit_rmdc26_1s1l_baseline_v022 as module


def synthetic_event(*, anomaly: bool, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t0, u0, t_e = 2_460_500.0, 0.18, 24.0
    rows: list[tuple[float, str, float, float, bool]] = []
    bands = [
        ("F087", 120.0, 30.0, 0.7),
        ("F146", 180.0, 55.0, 0.9),
        ("F213", 90.0, 20.0, 1.1),
    ]
    for band, source_flux, blend_flux, cadence in bands:
        time = np.arange(t0 - 120.0, t0 + 120.0, cadence)
        amplification = module.pspl_magnification(time, t0, u0, t_e)
        error = np.full_like(time, 2.0)
        flux = source_flux * amplification + blend_flux + rng.normal(0.0, error)
        if anomaly:
            flux += 40.0 * np.exp(-0.5 * ((time - (t0 + 12.0)) / 0.8) ** 2)
        rows.extend(zip(time, [band] * len(time), flux, error, [False] * len(time)))
    return pd.DataFrame(
        rows,
        columns=["bjd", "filt", "flux_uJy", "flux_err_uJy", "saturation_flag"],
    )


def saturated_event() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "bjd": [2_460_000.0, 2_460_001.0],
            "filt": ["F087", "F146"],
            "flux_uJy": [100.0, 200.0],
            "flux_err_uJy": [1.0, 1.0],
            "saturation_flag": [True, True],
        }
    )


def main() -> None:
    config = module.FitConfig(
        max_fit_points=1_200,
        t0_candidates=3,
        coarse_starts=8,
        maxiter=120,
    )

    clean = module.fit_event("SYNTHETIC_CLEAN", synthetic_event(anomaly=False, seed=42), config)
    assert clean["route"] == "1S1L_candidate", clean["route_reason"]
    assert clean["fit_status"] == "fit_success"
    assert abs(clean["t0"] - 2_460_500.0) < 0.5, clean["t0"]
    assert abs(clean["u0"] - 0.18) < 0.05, clean["u0"]
    assert abs(clean["tE"] - 24.0) < 3.0, clean["tE"]
    assert not clean["optimizer_seed_stuck"]

    anomalous = module.fit_event(
        "SYNTHETIC_ANOMALOUS",
        synthetic_event(anomaly=True, seed=7),
        config,
    )
    assert anomalous["route"] == "anomalous_route", anomalous["route_reason"]

    quality = module.build_data_quality_row(
        "SYNTHETIC_SATURATED",
        saturated_event(),
        "no_valid_unsaturated_photometry",
    )
    assert quality["route"] == "data_quality_route"
    assert quality["fit_status"] == "not_fit"
    assert quality["valid_unsaturated_observation_count"] == 0
    assert "all_rows_saturated" in quality["route_reason"]

    print("PASS: v0.2.2 clean PSPL recovery")
    print(
        f"  t0={clean['t0']:.6f}, u0={clean['u0']:.6f}, "
        f"tE={clean['tE']:.6f}, reduced_chi2={clean['reduced_chi2']:.3f}"
    )
    print("PASS: v0.2.2 injected anomaly routing")
    print(f"  {anomalous['route_reason']}")
    print("PASS: v0.2.2 no-valid-photometry coverage row")
    print(f"  {quality['route_reason']}")


if __name__ == "__main__":
    main()
