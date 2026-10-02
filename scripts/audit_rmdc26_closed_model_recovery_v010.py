#!/usr/bin/env python3
"""Read-only recovery audit for closed RMDC26 higher-order models.

This script inspects an existing Stellar_Intelligence workspace and reports:
1. all evidence records that explicitly close a model;
2. exact files for the validated RMDC26_002050 1S3L mutation UUID;
3. all 2S1L source/flux-related fields for RMDC26_000249, including CSVs;
4. the current model state of selected events in the October final project.

It performs no writes to any submission project.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "0.1.0"

UUID_002050 = "93ceb146-9b90-49c5-ba22-ce6f0f662ff3"
EXPECTED_002050_SHA256 = "c976e9cad9606143684a8f31b66ce263754870876c3d813ce0c8fac19eb5a451"

COMPETITION_000249 = (
    Path("evidence")
    / "rmdc26_000249_2s1l_competition_20260918T053128Z"
    / "2s1l_model_family_competition_report.json"
)

FLUX_REPRO_000249 = (
    Path("evidence")
    / "rmdc26_000249_2s1l_residual_audit_20260918T054235Z"
    / "flux_coefficient_reproduction.csv"
)

CLOSURE_000249 = (
    Path("evidence")
    / "rmdc26_000249_2s1l_closure_20260918T055520Z"
    / "rmdc26_000249_2s1l_model_closure_report.json"
)

MUTATION_002050 = (
    Path("evidence")
    / "rmdc26_002050_submission_mutation_20260809T120023Z"
    / "rmdc26_002050_submission_mutation_report.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.home() / "Stellar_Intelligence",
        help="Original RMDC26 workspace containing evidence and submission projects.",
    )
    parser.add_argument(
        "--final-project",
        default="rmdc26_final_submission_project_20261001",
        help="Final-project directory name inside the workspace.",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def flatten_scalars(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            p = f"{prefix}.{key}" if prefix else str(key)
            out.extend(flatten_scalars(value, p))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            out.extend(flatten_scalars(value, f"{prefix}[{i}]"))
    else:
        out.append((prefix, obj))
    return out


def print_json_fields(path: Path, terms: tuple[str, ...]) -> None:
    print(f"FILE: {path}")
    if not path.is_file():
        print("MISSING")
        return
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return
    for key, value in flatten_scalars(data):
        low = key.lower()
        if any(term in low for term in terms):
            print(f"{key}: {value}")


def print_csv(path: Path) -> None:
    print(f"FILE: {path}")
    if not path.is_file():
        print("MISSING")
        return
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.DictReader(fh))
    print("COLUMNS:", list(rows[0].keys()) if rows else [])
    print("ROW_COUNT:", len(rows))
    for i, row in enumerate(rows[:30]):
        print(f"ROW {i}: {row}")


def main() -> int:
    args = parse_args()
    workspace = args.workspace.expanduser().resolve()
    evidence = workspace / "evidence"
    final_project = workspace / args.final_project

    print("RMDC26 CLOSED MODEL RECOVERY AUDIT")
    print(f"script_version={SCRIPT_VERSION}")
    print(f"workspace={workspace}")
    print("submission_mutation=NO")

    print("\n=== CLOSED MODELS ===")
    closed: list[tuple[str, str, str, str]] = []
    if evidence.is_dir():
        for p in evidence.rglob("*.json"):
            try:
                obj = json.loads(p.read_text())
            except Exception:
                continue
            records = obj if isinstance(obj, list) else [obj]
            for data in records:
                if not isinstance(data, dict):
                    continue
                decision = str(data.get("decision", ""))
                status = str(data.get("status", ""))
                event = str(data.get("event_id", ""))
                if "CLOSED" in decision.upper() or "MODEL_CLOSURE" in status.upper():
                    closed.append((event, decision, status, str(p)))
    for event, decision, status, path in sorted(set(closed)):
        print(f"EVENT: {event}")
        print(f"DECISION: {decision}")
        print(f"STATUS: {status}")
        print(f"FILE: {path}")
        print()
    print(f"CLOSED_RECORD_COUNT={len(set(closed))}")

    print("\n=== 002050 VALIDATED MUTATION RECORD ===")
    mutation = workspace / MUTATION_002050
    print_json_fields(
        mutation,
        (
            "decision",
            "status",
            "new_solution",
            "historical_solution",
            "n_data_points",
            "unit_policy",
            "target_solution_count",
            "target_active_solution_count",
        ),
    )

    print("\n=== 002050 EXACT MUTATED SOLUTION FILE SEARCH ===")
    candidates: list[Path] = []
    # Prefer bounded likely roots first.
    roots = [
        workspace / "rmdc26_full_staging_project",
        workspace / "rmdc26_final_submission_project_20261001",
        workspace / "staging",
        workspace / "evidence",
    ]
    for root in roots:
        if root.exists():
            candidates.extend(root.rglob(f"{UUID_002050}.json"))
    # De-duplicate without changing order.
    seen: set[str] = set()
    unique: list[Path] = []
    for p in candidates:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    for p in unique:
        digest = sha256(p)
        print(f"PATH: {p}")
        print(f"SHA256: {digest}")
        print(f"EXPECTED_SHA256_MATCH: {digest == EXPECTED_002050_SHA256}")
        try:
            data = json.loads(p.read_text())
            print(f"MODEL: {data.get('model_type')}")
            print(f"ACTIVE: {data.get('is_active')}")
            print(f"ALIAS: {data.get('alias')}")
            print(f"PARAMETERS: {data.get('parameters')}")
            print(f"N_DATA_POINTS: {data.get('n_data_points')}")
            print(f"NOTES_PATH: {data.get('notes_path')}")
        except Exception as exc:
            print(f"PARSE_ERROR: {type(exc).__name__}: {exc}")
        print()
    print(f"002050_EXACT_FILE_COUNT={len(unique)}")
    print(
        "002050_EXPECTED_HASH_PRESENT="
        + str(any(sha256(p) == EXPECTED_002050_SHA256 for p in unique))
    )

    print("\n=== 000249 CLOSURE PARAMETERS ===")
    print_json_fields(
        workspace / CLOSURE_000249,
        (
            "decision",
            "status",
            "preferred_model",
            "model_family_evidence",
            "event_season_residuals",
        ),
    )

    print("\n=== 000249 2S1L COMPETITION SOURCE/FLUX FIELDS ===")
    print_json_fields(
        workspace / COMPETITION_000249,
        (
            "flux",
            "source",
            "ratio",
            "t01",
            "t02",
            "u01",
            "u02",
            "te",
            "chi2",
            "bic",
            "decision",
            "status",
            "preferred",
            "winner",
        ),
    )

    print("\n=== 000249 FLUX COEFFICIENT REPRODUCTION CSV ===")
    print_csv(workspace / FLUX_REPRO_000249)

    print("\n=== 000249 OTHER CSVs WITH FLUX-LIKE COLUMNS ===")
    event_dirs = sorted(evidence.glob("rmdc26_000249_*")) if evidence.is_dir() else []
    for event_dir in event_dirs:
        if not event_dir.is_dir():
            continue
        for p in sorted(event_dir.rglob("*.csv")):
            try:
                with p.open(newline="", encoding="utf-8", errors="replace") as fh:
                    reader = csv.reader(fh)
                    header = next(reader, [])
            except Exception:
                continue
            low = [h.lower() for h in header]
            if any(any(term in col for term in ("flux", "fs1", "fs2", "ratio")) for col in low):
                print(f"CSV: {p}")
                print("COLUMNS:", header)

    print("\n=== CURRENT OCTOBER FINAL TARGET STATE ===")
    for event_id in ("RMDC26_002050", "RMDC26_000249", "RMDC26_000435"):
        print(f"EVENT: {event_id}")
        d = final_project / "events" / event_id / "solutions"
        if not d.is_dir():
            print("NO_SOLUTIONS_DIR")
            continue
        files = sorted(d.glob("*.json"))
        print(f"SOLUTION_FILE_COUNT: {len(files)}")
        for p in files:
            try:
                data = json.loads(p.read_text())
            except Exception as exc:
                print(f"PARSE_ERROR {p}: {exc}")
                continue
            print(f"FILE: {p.name}")
            print(f"MODEL: {data.get('model_type')}")
            print(f"ACTIVE: {data.get('is_active')}")
            print(f"ALIAS: {data.get('alias')}")
            print(f"PARAMETERS: {data.get('parameters')}")
        print()

    print("SUBMISSION_MODIFIED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
