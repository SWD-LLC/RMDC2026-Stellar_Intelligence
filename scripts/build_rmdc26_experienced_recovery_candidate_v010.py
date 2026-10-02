#!/usr/bin/env python3
"""Build a recovered RMDC26 Experienced-tier candidate without touching the frozen ZIP.

The candidate is copied from the validated October project, then:
- RMDC26_002050: adds the previously closed static exact 1S3L solution and
  deactivates the Stage-1 1S1L fallback in the candidate only.
- RMDC26_000249: adds the closed 2S1L solution with exact geometry and
  per-band source/blend fluxes, then deactivates its Stage-1 1S1L fallback
  in the candidate only.
- RMDC26_000435 is intentionally untouched because its higher-order family
  was not scientifically closed.

For 000249 the microlens-submit schema requires one scalar flux_ratio even
when band-specific binary-source fluxes are also supplied. The recovered fit
is chromatic, so this script uses the F146 (band code 1) ratio as the explicit
reference-band scalar while preserving all fitted F087/F146/F213 fluxes.

No existing submission project or ZIP is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "0.1.0"

EVENT_002050 = "RMDC26_002050"
EVENT_000249 = "RMDC26_000249"
EVENT_000435 = "RMDC26_000435"

SOURCE_002050 = Path(
    "staging/rmdc26_full_staging_execution_valid_20260808T205433Z/"
    "events/RMDC26_002050/solutions/"
    "93ceb146-9b90-49c5-ba22-ce6f0f662ff3.json"
)
SOURCE_002050_SHA256 = "c976e9cad9606143684a8f31b66ce263754870876c3d813ce0c8fac19eb5a451"

COMPETITION_000249 = Path(
    "evidence/rmdc26_000249_2s1l_competition_20260918T053128Z/"
    "2s1l_model_family_competition_report.json"
)

DEFAULT_SOURCE_PROJECT = "rmdc26_final_submission_project_20261001"
DEFAULT_DEST_PROJECT = "rmdc26_experienced_recovered_candidate_20261002"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--workspace",
        type=Path,
        default=Path.home() / "Stellar_Intelligence",
    )
    p.add_argument("--source-project", default=DEFAULT_SOURCE_PROJECT)
    p.add_argument("--candidate-project", default=DEFAULT_DEST_PROJECT)
    p.add_argument(
        "--microlens-submit",
        type=Path,
        default=Path.home() / ".local" / "bin" / "microlens-submit",
    )
    return p.parse_args()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    print("\n$", " ".join(cmd))
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip())
    if proc.returncode != 0:
        raise RuntimeError(f"command failed with exit code {proc.returncode}")
    return proc


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def active_solution_ids(project: Path, event_id: str) -> list[str]:
    d = project / "events" / event_id / "solutions"
    out: list[str] = []
    for p in sorted(d.glob("*.json")):
        data = load_json(p)
        if bool(data.get("is_active", True)):
            out.append(str(data.get("solution_id") or p.stem))
    return out


def find_solution_by_alias(project: Path, event_id: str, alias: str) -> Path:
    d = project / "events" / event_id / "solutions"
    hits = []
    for p in sorted(d.glob("*.json")):
        data = load_json(p)
        if data.get("alias") == alias:
            hits.append(p)
    if len(hits) != 1:
        raise RuntimeError(
            f"Expected exactly one {event_id} solution with alias {alias!r}; found {len(hits)}"
        )
    return hits[0]


def add_solution(
    cli: Path,
    project: Path,
    event_id: str,
    model_type: str,
    parameters: dict[str, float],
    alias: str,
    notes: str,
    n_data_points: int,
    bands: list[str] | None = None,
) -> Path:
    cmd = [
        str(cli),
        "--no-color",
        "add-solution",
        event_id,
        model_type,
        str(project),
    ]
    for key, value in parameters.items():
        cmd += ["--param", f"{key}={value}"]
    if bands:
        for band in bands:
            cmd += ["--bands", band]
    cmd += [
        "--alias",
        alias,
        "--n-data-points",
        str(n_data_points),
        "--relative-probability",
        "1.0",
        "--notes",
        notes,
    ]
    run(cmd, project.parent)
    return find_solution_by_alias(project, event_id, alias)


def deactivate_existing(
    cli: Path,
    project: Path,
    event_id: str,
    keep_solution_id: str,
) -> None:
    for sid in active_solution_ids(project, event_id):
        if sid == keep_solution_id:
            continue
        run(
            [str(cli), "--no-color", "deactivate", sid, str(project)],
            project.parent,
        )


def main() -> int:
    args = parse_args()
    workspace = args.workspace.expanduser().resolve()
    source_project = workspace / args.source_project
    candidate = workspace / args.candidate_project
    cli = args.microlens_submit.expanduser().resolve()

    print("RMDC26 EXPERIENCED RECOVERY CANDIDATE")
    print(f"script_version={SCRIPT_VERSION}")
    print(f"workspace={workspace}")
    print(f"source_project={source_project}")
    print(f"candidate_project={candidate}")
    print("frozen_zip_mutation=NO")

    if not source_project.is_dir():
        raise FileNotFoundError(source_project)
    if candidate.exists():
        raise FileExistsError(
            f"Candidate already exists: {candidate}. "
            "Remove/rename it deliberately before rerunning."
        )
    if not cli.is_file():
        raise FileNotFoundError(cli)

    source_002050 = workspace / SOURCE_002050
    if not source_002050.is_file():
        raise FileNotFoundError(source_002050)
    actual = digest(source_002050)
    if actual != SOURCE_002050_SHA256:
        raise RuntimeError(
            f"002050 source hash mismatch: {actual} != {SOURCE_002050_SHA256}"
        )

    comp_path = workspace / COMPETITION_000249
    comp = load_json(comp_path)
    best = comp["models"]["2S1L"]["best"]

    # Exact recovered 2S1L geometry and per-band fluxes.
    params_000249: dict[str, float] = {
        "t0": float(best["t01"]),
        "u0": float(best["u01"]),
        "tE": float(best["tE"]),
        "t0_source2": float(best["t02"]),
        "u0_source2": float(best["u02"]),
        # Explicit packaging convention: reference scalar = F146 ratio.
        "flux_ratio": float(best["fluxes"]["F146"]["fs2_over_fs1"]),
        "F0_S1": float(best["fluxes"]["F087"]["fs1"]),
        "F0_S2": float(best["fluxes"]["F087"]["fs2"]),
        "F0_B": float(best["fluxes"]["F087"]["fb"]),
        "F1_S1": float(best["fluxes"]["F146"]["fs1"]),
        "F1_S2": float(best["fluxes"]["F146"]["fs2"]),
        "F1_B": float(best["fluxes"]["F146"]["fb"]),
        "F2_S1": float(best["fluxes"]["F213"]["fs1"]),
        "F2_S2": float(best["fluxes"]["F213"]["fs2"]),
        "F2_B": float(best["fluxes"]["F213"]["fb"]),
    }

    recovered_002050 = load_json(source_002050)
    p2050 = recovered_002050["parameters"]
    params_002050 = {k: float(v) for k, v in p2050.items()}

    print("\nRecovered checks:")
    print(f"002050_source_sha256={actual}")
    print(f"000249_delta_chi2_2S1L_minus_1S2L={comp['competition']['chi2_2S1L_minus_1S2L']}")
    print(f"000249_flux_ratio_reference_band=F146")
    print(f"000249_flux_ratio={params_000249['flux_ratio']}")
    print(
        "000249_band_ratios="
        + json.dumps(
            {
                b: best["fluxes"][b]["fs2_over_fs1"]
                for b in ("F087", "F146", "F213")
            },
            sort_keys=True,
        )
    )

    shutil.copytree(source_project, candidate)

    # Add recovered 002050 1S3L.
    alias_2050 = "rmdc26_stage2_exact_1s3l_rmdc26_002050_closed_v010"
    notes_2050 = (
        "# RMDC26_002050 recovered closed 1S3L solution\n\n"
        "Recovered from the previously validated Stage 2 mutation record. "
        "The static exact point-source 1S3L model was scientifically closed before "
        "the October packaging pass. Finite-source, parallax, and tested linear "
        "lens-orbital-motion extensions were not required by the closure screens.\n\n"
        "The fit-native geometry is retained exactly. microlens-submit 0.17.9 "
        "classifies 1S3L as planned and may emit non-critical warnings for these "
        "fit-native triple-lens geometry names. No alternate geometry mapping was "
        "invented during recovery."
    )
    sol2050 = add_solution(
        cli,
        candidate,
        EVENT_002050,
        "1S3L",
        params_002050,
        alias_2050,
        notes_2050,
        49488,
    )
    sid2050 = load_json(sol2050).get("solution_id", sol2050.stem)
    deactivate_existing(cli, candidate, EVENT_002050, str(sid2050))

    # Add closed 000249 2S1L with full band flux coefficients.
    alias_0249 = "rmdc26_stage2_2s1l_rmdc26_000249_closed_v010"
    notes_0249 = (
        "# RMDC26_000249 closed 2S1L solution\n\n"
        "Recovered from the Stage 2 model-family competition and closure evidence. "
        "The 2S1L family was preferred over the competing 1S2L family by "
        "Delta chi-square = 3923.2182862332793 and passed the event-season residual "
        "closure gates.\n\n"
        "Band mapping used by the recovered fit: 0=F087, 1=F146, 2=F213. "
        "The exact fitted source and blend fluxes for all three bands are included. "
        "microlens-submit 0.17.9 also requires a single scalar flux_ratio for 2S1L. "
        "Because the recovered fit is chromatic, that scalar is explicitly defined "
        "here as the F146 reference-band ratio F_S2/F_S1 = "
        f"{params_000249['flux_ratio']:.15g}. "
        "The F087 and F213 ratios remain represented by their exact band-specific "
        "source flux parameters rather than being overwritten by the reference scalar."
    )
    sol0249 = add_solution(
        cli,
        candidate,
        EVENT_000249,
        "2S1L",
        params_000249,
        alias_0249,
        notes_0249,
        7190,
        bands=["0", "1", "2"],
    )
    sid0249 = load_json(sol0249).get("solution_id", sol0249.stem)
    deactivate_existing(cli, candidate, EVENT_000249, str(sid0249))

    # Confirm untouched 000435 remains its existing active solution.
    active_0435 = active_solution_ids(candidate, EVENT_000435)

    print("\n=== POST-RECOVERY ACTIVE SOLUTIONS ===")
    for event_id in (EVENT_002050, EVENT_000249, EVENT_000435):
        print(event_id, active_solution_ids(candidate, event_id))

    validation = run(
        [str(cli), "--no-color", "validate-submission", str(candidate)],
        candidate.parent,
    )

    report = {
        "manifest_type": "RMDC26_EXPERIENCED_RECOVERY_CANDIDATE_V010",
        "script_version": SCRIPT_VERSION,
        "source_project": str(source_project),
        "candidate_project": str(candidate),
        "source_project_modified": False,
        "frozen_zip_modified": False,
        "events_recovered": {
            EVENT_002050: {
                "model": "1S3L",
                "alias": alias_2050,
                "source_sha256": actual,
                "solution_id": sid2050,
            },
            EVENT_000249: {
                "model": "2S1L",
                "alias": alias_0249,
                "solution_id": sid0249,
                "flux_ratio_reference_band": "F146",
                "flux_ratio": params_000249["flux_ratio"],
                "band_ratios": {
                    b: best["fluxes"][b]["fs2_over_fs1"]
                    for b in ("F087", "F146", "F213")
                },
            },
        },
        EVENT_000435: {
            "modified": False,
            "active_solution_ids": active_0435,
        },
        "validation_stdout": validation.stdout,
        "validation_stderr": validation.stderr,
    }
    manifest_path = candidate / "RECOVERY_MANIFEST.json"
    manifest_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\nCANDIDATE_BUILD_COMPLETE")
    print(f"candidate={candidate}")
    print(f"manifest={manifest_path}")
    print("SOURCE_PROJECT_MODIFIED=NO")
    print("FROZEN_ZIP_MODIFIED=NO")
    print("EXPORT_CREATED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
