#!/usr/bin/env python3
"""Create a documentation-corrected RMDC26 recovery candidate.

Safety rules:
- never modifies the original October project;
- never modifies the first recovered candidate;
- never overwrites either existing ZIP;
- never renames 1S3L geometry fields unless a scientific mapping is proven;
- preserves the exact recovered fit values;
- makes the F146 scalar flux-ratio convention explicit for RMDC26_000249.

The script probes the installed microlens-submit package. If the installed
schema still does not represent the recovered 1S3L native geometry, it records
that limitation in notes rather than inventing parameter replacements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

EVENT_2050 = "RMDC26_002050"
EVENT_0249 = "RMDC26_000249"

ALIAS_2050 = "rmdc26_stage2_exact_1s3l_rmdc26_002050_closed_v010"
ALIAS_0249 = "rmdc26_stage2_2s1l_rmdc26_000249_closed_v010"

EXPECTED_2050 = {
    "t0": 2462937.4494308094,
    "u0": 0.1740851251464745,
    "tE": 24.9891751751578,
    "s_21": 0.12301369727721631,
    "q_21": 0.32016267221703165,
    "s_31": 7.699994419344329,
    "q_31": 1.266453926332858,
    "alpha": 1.204586116633564,
    "psi": -1.9793896970015743,
}

EXPECTED_0249 = {
    "t0": 2461637.5901571997,
    "u0": 0.5644199357921323,
    "tE": 29.33125618198735,
    "t0_source2": 2461648.5071867188,
    "u0_source2": 0.11334561438362734,
    "flux_ratio": 19.854682394742422,
    "F0_S1": 3.2110174860357614,
    "F0_S2": 65.13525785071953,
    "F0_B": -1.8601054076907124,
    "F1_S1": 13.931107703247939,
    "F1_S2": 276.5977188549374,
    "F1_B": -0.9137533470779077,
    "F2_S1": 19.204940993176407,
    "F2_S2": 375.55748812244747,
    "F2_B": 76.68245365078552,
}

BAND_RATIOS = {
    "F087": 20.28492779437767,
    "F146": 19.854682394742422,
    "F213": 19.555253424412214,
}

ORIGINAL_RECOVERED_ZIP_SHA256 = (
    "902d3742bf6f4e8ae20e19c58c5b15f56df668799908471541f18d76acaf301f"
)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, default=Path.home() / "Stellar_Intelligence")
    p.add_argument(
        "--source-project",
        default="rmdc26_experienced_recovered_candidate_20261002",
    )
    p.add_argument(
        "--candidate-project",
        default="rmdc26_experienced_documented_corrected_candidate_20261002",
    )
    p.add_argument(
        "--output-zip",
        default="RMDC26_Sierra_Warren_Experienced_CORRECTED_20261002.zip",
    )
    p.add_argument(
        "--cli",
        type=Path,
        default=Path.home() / ".local" / "bin" / "microlens-submit",
    )
    return p.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    print("\n$", " ".join(cmd))
    p = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    if p.stdout:
        print(p.stdout.rstrip())
    if p.stderr:
        print(p.stderr.rstrip())
    if p.returncode != 0:
        raise RuntimeError(f"command failed with exit code {p.returncode}")
    return p


def load_json(path: Path):
    return json.loads(path.read_text())


def find_alias(project: Path, event_id: str, alias: str) -> Path:
    sol_dir = project / "events" / event_id / "solutions"
    hits = []
    for p in sol_dir.glob("*.json"):
        d = load_json(p)
        if d.get("alias") == alias:
            hits.append(p)
    if len(hits) != 1:
        raise RuntimeError(f"{event_id}: expected one alias {alias!r}, found {len(hits)}")
    return hits[0]


def assert_exact_subset(actual: dict, expected: dict, label: str) -> None:
    for k, v in expected.items():
        if k not in actual:
            raise RuntimeError(f"{label}: missing parameter {k}")
        if actual[k] != v:
            raise RuntimeError(f"{label}: {k} changed: {actual[k]!r} != {v!r}")


def note_path_for_solution(project: Path, sol_path: Path, data: dict) -> Path:
    existing = data.get("notes_path")
    if existing:
        p = project / existing
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    sid = data.get("solution_id") or sol_path.stem
    p = sol_path.parent / sid / f"{sid}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    data["notes_path"] = str(p.relative_to(project))
    sol_path.write_text(json.dumps(data, indent=2))
    return p


def toolkit_probe():
    import microlens_submit
    from microlens_submit.validate_parameters import validate_parameter_types

    version = getattr(microlens_submit, "__version__", "unknown")
    probe = {
        "t0": EXPECTED_2050["t0"],
        "u0": EXPECTED_2050["u0"],
        "tE": EXPECTED_2050["tE"],
        "s01": EXPECTED_2050["s_21"],
        "q01": EXPECTED_2050["q_21"],
        "alpha01": EXPECTED_2050["alpha"],
        "s02": EXPECTED_2050["s_31"],
        "q02": EXPECTED_2050["q_31"],
        "alpha02": EXPECTED_2050["psi"],
    }
    messages = validate_parameter_types(probe, "1S3L")
    return version, messages


def exported_audit(path: Path):
    models = {}
    events = set()
    inactive = 0
    targets = {}
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP integrity failure at {bad}")
        for name in zf.namelist():
            if not (
                name.startswith("events/")
                and "/solutions/" in name
                and name.endswith(".json")
            ):
                continue
            d = json.loads(zf.read(name))
            eid = name.split("/")[1]
            events.add(eid)
            model = d.get("model_type")
            models[model] = models.get(model, 0) + 1
            if not d.get("is_active", True):
                inactive += 1
            if eid in (EVENT_2050, EVENT_0249, "RMDC26_000435"):
                targets[eid] = {
                    "model_type": model,
                    "alias": d.get("alias"),
                    "parameters": d.get("parameters"),
                }
    return {
        "events": len(events),
        "solutions": sum(models.values()),
        "models": models,
        "inactive_solutions_in_export": inactive,
        "targets": targets,
    }


def main() -> int:
    args = parse_args()
    ws = args.workspace.expanduser().resolve()
    src = ws / args.source_project
    dst = ws / args.candidate_project
    out = ws / args.output_zip
    cli = args.cli.expanduser().resolve()

    print("RMDC26 DOCUMENTED CORRECTED CANDIDATE")
    print(f"source={src}")
    print(f"candidate={dst}")
    print(f"output={out}")
    print("ORIGINAL_RECOVERED_ZIP_MODIFIED=NO")

    if not src.is_dir():
        raise FileNotFoundError(src)
    if dst.exists():
        raise FileExistsError(dst)
    if out.exists():
        raise FileExistsError(out)
    if not cli.is_file():
        raise FileNotFoundError(cli)

    original_zip = ws / "RMDC26_Sierra_Warren_Experienced_RECOVERED_20261002.zip"
    if original_zip.is_file():
        got = sha256(original_zip)
        print(f"original_recovered_zip_sha256={got}")
        if got != ORIGINAL_RECOVERED_ZIP_SHA256:
            raise RuntimeError("original recovered ZIP hash changed")

    version, canonical_probe_messages = toolkit_probe()
    print(f"microlens_submit_version={version}")
    print("canonical_1S3L_probe_messages:")
    for m in canonical_probe_messages:
        print("  ", m)

    schema_support = (
        "accepted_without_type_warnings"
        if not canonical_probe_messages
        else "partial_or_unsupported"
    )
    print(f"canonical_1S3L_probe={schema_support}")
    print("geometry_rename_applied=NO")

    shutil.copytree(src, dst)

    p2050 = find_alias(dst, EVENT_2050, ALIAS_2050)
    d2050 = load_json(p2050)
    if d2050.get("model_type") != "1S3L" or not d2050.get("is_active", True):
        raise RuntimeError("002050 recovered 1S3L is not the active recovered solution")
    assert_exact_subset(d2050.get("parameters", {}), EXPECTED_2050, EVENT_2050)

    p0249 = find_alias(dst, EVENT_0249, ALIAS_0249)
    d0249 = load_json(p0249)
    if d0249.get("model_type") != "2S1L" or not d0249.get("is_active", True):
        raise RuntimeError("000249 recovered 2S1L is not the active recovered solution")
    assert_exact_subset(d0249.get("parameters", {}), EXPECTED_0249, EVENT_0249)

    note2050 = note_path_for_solution(dst, p2050, d2050)
    note2050.write_text(
        """# RMDC26_002050 recovered closed 1S3L solution

This active solution preserves the exact fit-native parameters from the
scientifically closed static point-source 1S3L model.

microlens-submit records the model type as 1S3L and the full submission
validator passes. The installed toolkit emits event/solution-level warnings
for the fit-native geometry names s_21, q_21, s_31, q_31, alpha, and psi.

Those native geometry fields are intentionally retained rather than renamed
to unsupported or semantically unverified alternatives. Prior isolated-save
and isolated-export canaries demonstrated that the toolkit serializes and
exports the native geometry without dropping the values. No 1S1L fallback
replacement and no invented geometry mapping was used.

Fit-native submission values are preserved exactly:
- t0 = 2462937.4494308094
- u0 = 0.1740851251464745
- tE = 24.9891751751578
- s_21 = 0.12301369727721631
- q_21 = 0.32016267221703165
- s_31 = 7.699994419344329
- q_31 = 1.266453926332858
- alpha = 1.204586116633564 rad
- psi = -1.9793896970015743 rad

The recovered model closure used 49,488 data points. Finite-source, parallax,
and tested linear lens-orbital-motion extensions were screened and were not
required by the closure evidence.
""",
        encoding="utf-8",
    )

    note0249 = note_path_for_solution(dst, p0249, d0249)
    note0249.write_text(
        """# RMDC26_000249 recovered closed 2S1L solution

The recovered model-family competition and closure evidence support a 2S1L
point-lens/binary-source solution.

The required scalar flux_ratio is reported using F146 as the reference band:

flux_ratio = F_S2 / F_S1 = 19.854682394742422 in F146.

The recovered fit is chromatic and the toolkit does not define a
reference-band convention for the single scalar flux_ratio. Therefore the
scalar is not an average across filters. The exact band-specific source and
blend flux parameters are retained alongside it.

Recovered source-flux ratios:
- F087: 20.28492779437767
- F146: 19.854682394742422
- F213: 19.555253424412214

Band mapping in the serialized solution:
- band 0 = F087
- band 1 = F146
- band 2 = F213

No conversion from another band and no cross-band averaging was applied.
""",
        encoding="utf-8",
    )

    print(f"002050_notes={note2050}")
    print(f"000249_notes={note0249}")

    run([str(cli), "--no-color", "validate-submission", str(dst)], ws)
    run([str(cli), "--no-color", "validate-event", EVENT_2050, str(dst)], ws)
    run([str(cli), "--no-color", "validate-solution", d0249["solution_id"], str(dst)], ws)
    run([str(cli), "--no-color", "generate-dossier", str(dst)], ws)
    run([str(cli), "--no-color", "export", str(out), str(dst)], ws)

    audit = exported_audit(out)
    print("\n=== EXPORTED ARCHIVE AUDIT ===")
    print(json.dumps(audit, indent=2))

    expected_models = {"1S1L": 2076, "1S3L": 1, "2S1L": 1}
    if audit["events"] != 2078:
        raise RuntimeError(f"event count mismatch: {audit['events']}")
    if audit["solutions"] != 2078:
        raise RuntimeError(f"solution count mismatch: {audit['solutions']}")
    if audit["models"] != expected_models:
        raise RuntimeError(f"model counts mismatch: {audit['models']}")
    if audit["inactive_solutions_in_export"] != 0:
        raise RuntimeError("inactive solution present in exported archive")
    if audit["targets"][EVENT_2050]["model_type"] != "1S3L":
        raise RuntimeError("002050 model changed")
    if audit["targets"][EVENT_0249]["model_type"] != "2S1L":
        raise RuntimeError("000249 model changed")

    zip_hash = sha256(out)
    report = {
        "report_type": "RMDC26_DOCUMENTED_CORRECTED_EXPORT_V010",
        "microlens_submit_version": version,
        "canonical_1S3L_probe": schema_support,
        "canonical_1S3L_probe_messages": canonical_probe_messages,
        "geometry_rename_applied": False,
        "f146_flux_ratio_convention": EXPECTED_0249["flux_ratio"],
        "original_recovered_zip_sha256": ORIGINAL_RECOVERED_ZIP_SHA256,
        "corrected_zip": str(out),
        "corrected_zip_sha256": zip_hash,
        "archive_audit": audit,
    }
    report_path = ws / "RMDC26_Sierra_Warren_Experienced_CORRECTED_20261002.audit.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\nFINAL_CORRECTED_EXPORT=PASS")
    print(f"CORRECTED_ZIP={out}")
    print(f"CORRECTED_ZIP_SHA256={zip_hash}")
    print(f"AUDIT_REPORT={report_path}")
    print("ORIGINAL_RECOVERED_ZIP_MODIFIED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
