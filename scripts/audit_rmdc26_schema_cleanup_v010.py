#!/usr/bin/env python3
"""Read-only RMDC26 schema-cleanup audit.

Checks the installed microlens-submit contract for:
1. official-style 1S3L geometry names;
2. the recovered 2S1L payload with band-specific fluxes;
3. local RMDC26_002050 source lines that define q_21/q_31/s_21/s_31/alpha/psi
   so any renaming can be scientifically mapped rather than guessed.

This script does not modify any submission project or ZIP.
"""
from __future__ import annotations

import importlib
import inspect
from pathlib import Path

WORKSPACE = Path.home() / "Stellar_Intelligence"

P2050 = {
    "t0": 2462937.4494308094,
    "u0": 0.1740851251464745,
    "tE": 24.9891751751578,
    "s01": 0.12301369727721631,
    "q01": 0.32016267221703165,
    "alpha01": 1.204586116633564,
    "s02": 7.699994419344329,
    "q02": 1.266453926332858,
    "alpha02": -1.9793896970015743,
}

P0249 = {
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

TARGET_SCRIPTS = [
    "search_rmdc26_002050_exact_1s3l_stageA_v010.py",
    "refine_rmdc26_002050_exact_1s3l_stageB_v010.py",
    "refine_rmdc26_002050_exact_1s3l_full9_v010.py",
    "polish_rmdc26_002050_exact_1s3l_full_static_v010.py",
    "evaluate_rmdc26_002050_exact_1s3l_full_photometry_v010.py",
    "close_rmdc26_002050_model_v010.py",
]
TERMS = ("q_21", "q_31", "s_21", "s_31", "psi", "alpha", "lens_pos", "lens_position", "z1", "z2", "z3")


def show_messages(label, messages):
    print(f"\n=== {label} ===")
    print("MESSAGE_COUNT:", len(messages))
    for m in messages:
        print(m)
    print("CLEAN:", len(messages) == 0)


def main() -> int:
    import microlens_submit
    from microlens_submit.validate_parameters import (
        check_solution_completeness,
        validate_parameter_types,
    )

    print("RMDC26 SCHEMA CLEANUP AUDIT")
    print("submission_mutation=NO")
    print("microlens_submit_version=", getattr(microlens_submit, "__version__", "unknown"))
    print("microlens_submit_path=", inspect.getfile(microlens_submit))

    msgs_2050 = []
    msgs_2050.extend(check_solution_completeness("1S3L", P2050, bands=[]))
    msgs_2050.extend(validate_parameter_types(P2050, "1S3L"))
    show_messages("1S3L OFFICIAL-STYLE NAME PROBE", list(dict.fromkeys(msgs_2050)))

    msgs_0249 = []
    msgs_0249.extend(check_solution_completeness("2S1L", P0249, bands=["0", "1", "2"]))
    msgs_0249.extend(validate_parameter_types(P0249, "2S1L"))
    show_messages("2S1L RECOVERED PAYLOAD PROBE", list(dict.fromkeys(msgs_0249)))

    print("\n=== LOCAL 002050 GEOMETRY SOURCE LINES ===")
    scripts_dir = WORKSPACE / "scripts"
    for name in TARGET_SCRIPTS:
        p = scripts_dir / name
        if not p.is_file():
            continue
        lines = p.read_text(errors="replace").splitlines()
        hits = [i for i, line in enumerate(lines) if any(t in line for t in TERMS)]
        if not hits:
            continue
        print(f"\n--- {p} ---")
        emitted = set()
        for i in hits:
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j in emitted:
                    continue
                emitted.add(j)
                print(f"{j+1:5d}: {lines[j]}")

    print("\nSUBMISSION_MODIFIED=NO")
    print("ZIP_MODIFIED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
