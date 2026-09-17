#!/usr/bin/env python3
"""Run the QSCII reference QA gates for the ATIS Telecom5G CBOM 1.0.0 release package.

This script is non-normative reference tooling. It runs the ATIS/QSCII QA gates and,
when the CycloneDX CLI is available, independently runs the native CycloneDX 1.7
validation layer over the three positive reference CBOMs.

Strict two-layer validation is reported only when both layers pass.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

VERSION = "1.0.0"
TESTS_DIR = Path(__file__).resolve().parent
PROFILE_ROOT = TESTS_DIR.parent
VALID_DIR = PROFILE_ROOT / "Examples" / "Valid"
POSITIVE_CBOMS = [
    VALID_DIR / f"CBOM_AMF_N2_vendor_services_v{VERSION}_VALID.json",
    VALID_DIR / f"CBOM_SEPP_N32_deployed_services_v{VERSION}_VALID.json",
    VALID_DIR / f"CBOM_UDM_5G_AKA_vendor_v{VERSION}_VALID.json",
]
LOCAL_QA_COMMANDS = [
    [sys.executable, str(TESTS_DIR / "normative_audit.py")],
    [sys.executable, str(TESTS_DIR / "sdo_reviewer_audit.py"), "--fail-on", "info"],
    [sys.executable, str(TESTS_DIR / f"test_v{VERSION}.py")],
]


def display_cmd(cmd: list[str]) -> str:
    return " ".join(str(x) for x in cmd)


def resolve_cyclonedx(explicit: str | None = None) -> str | None:
    """Return the CycloneDX CLI executable path/name, or None if unavailable."""
    candidate = explicit or os.environ.get("CYCLONEDX_CLI")
    if candidate:
        p = Path(candidate).expanduser()
        if p.exists():
            return str(p.resolve())
        resolved = shutil.which(candidate)
        return resolved
    return shutil.which("cyclonedx")


def cyclonedx_version(exe: str) -> str:
    try:
        r = subprocess.run([exe, "--version"], cwd=PROFILE_ROOT, capture_output=True, text=True)
    except OSError as e:
        return f"unavailable ({e})"
    text = (r.stdout or r.stderr).strip()
    return text or "version not reported"


def run_native_cyclonedx(exe: str, quiet: bool = False) -> bool:
    print("\n== Native CycloneDX 1.7 validation ==")
    print(f"CycloneDX CLI: {exe}")
    print(f"Version: {cyclonedx_version(exe)}")
    all_pass = True
    for bom in POSITIVE_CBOMS:
        cmd = [
            exe,
            "validate",
            "--input-file", str(bom),
            "--input-format", "json",
            "--input-version", "v1_7",
            "--fail-on-errors",
        ]
        r = subprocess.run(cmd, cwd=PROFILE_ROOT, capture_output=True, text=True)
        status = "PASS" if r.returncode == 0 else "FAIL"
        print(f"  {bom.name}: {status}")
        if not quiet and (r.stdout.strip() or r.stderr.strip()):
            stream = r.stdout.strip() or r.stderr.strip()
            for line in stream.splitlines():
                print(f"    {line}")
        if r.returncode != 0:
            all_pass = False
    return all_pass


def run_local_qscii() -> bool:
    print("\n== ATIS/QSCII reference QA ==")
    for cmd in LOCAL_QA_COMMANDS:
        print("\n==>", display_cmd(cmd))
        r = subprocess.run(cmd, cwd=PROFILE_ROOT)
        if r.returncode:
            return False
    return True


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run ATIS/QSCII QA and optional native CycloneDX 1.7 validation.")
    p.add_argument(
        "--require-cyclonedx",
        action="store_true",
        help="Fail unless the CycloneDX CLI is available and all positive CBOMs pass native CycloneDX 1.7 validation.",
    )
    p.add_argument(
        "--cyclonedx-exe",
        help="Path or command name for the CycloneDX CLI. Overrides CYCLONEDX_CLI and PATH discovery.",
    )
    p.add_argument(
        "--quiet-cyclonedx",
        action="store_true",
        help="Suppress native CycloneDX CLI stdout/stderr unless summarized by PASS/FAIL.",
    )
    p.add_argument("--version", action="version", version=VERSION)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    # Keep parent/child output ordered in PowerShell and CI logs.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, OSError):
        pass

    exe = resolve_cyclonedx(args.cyclonedx_exe)
    native_state = "unavailable"
    native_ok = False
    if exe:
        try:
            native_ok = run_native_cyclonedx(exe, quiet=args.quiet_cyclonedx)
            native_state = "pass" if native_ok else "fail"
        except OSError as e:
            print(f"\nNative CycloneDX validation could not be executed: {e}")
            native_state = "unavailable"
    else:
        print("\n== Native CycloneDX 1.7 validation ==")
        print("CycloneDX CLI: NOT FOUND")
        print("Native validation was not run. Install CycloneDX CLI or use --cyclonedx-exe / CYCLONEDX_CLI.")

    local_ok = run_local_qscii()

    print("\n== Combined validation result ==")
    print(f"ATIS/QSCII VALIDATION: {'PASS' if local_ok else 'FAIL'}")
    if native_state == "pass" and local_ok:
        print("NATIVE CYCLONEDX 1.7 VALIDATION: PASS")
        print("STRICT TWO-LAYER VALIDATION: PASS")
        print("QSCII LOCAL QA GATES PASSED")
        return 0

    if native_state == "fail":
        print("NATIVE CYCLONEDX 1.7 VALIDATION: FAIL")
        print("STRICT TWO-LAYER VALIDATION: FAIL")
        return 1

    print("NATIVE CYCLONEDX 1.7 VALIDATION: NOT ESTABLISHED")
    print("STRICT TWO-LAYER VALIDATION: NOT ESTABLISHED")
    if not local_ok:
        return 1
    print("QSCII LOCAL QA GATES PASSED (ATIS/QSCII layer only)")
    if args.require_cyclonedx:
        print("Release/CI gate failed because --require-cyclonedx was specified.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
