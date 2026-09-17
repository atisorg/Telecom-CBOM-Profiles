#!/usr/bin/env python3
"""Profile-independent ATIS CBOM end-user validator.

This is non-normative reference tooling. It discovers the ATIS profile declared by
an input CBOM, locates that profile's machine taxonomy and profile-specific
reference validator, runs the native CycloneDX validation layer, runs the ATIS
profile layer, and reports one combined result.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILES_ROOT = REPO_ROOT / "profiles"
VERSION = "0.1"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_cyclonedx(explicit: str | None = None) -> str | None:
    candidate = explicit or os.environ.get("CYCLONEDX_CLI")
    if candidate:
        p = Path(candidate).expanduser()
        if p.exists():
            return str(p.resolve())
        return shutil.which(candidate)
    return shutil.which("cyclonedx")


def discover_profiles() -> dict[str, dict]:
    registry: dict[str, dict] = {}
    for tax_path in PROFILES_ROOT.glob("*/*/atis-*-taxonomy-*.json"):
        try:
            tax = load_json(tax_path)
        except Exception:
            continue
        marker = tax.get("profileMarker")
        if not isinstance(marker, str) or not marker:
            continue
        profile_root = tax_path.parent
        validator = profile_root / "Validation" / "validate_atis_cbom.py"
        if not validator.exists():
            continue
        if marker in registry:
            raise RuntimeError(f"duplicate profile marker {marker!r}: {tax_path} and {registry[marker]['taxonomy']}")
        registry[marker] = {
            "root": profile_root,
            "taxonomy": tax_path,
            "validator": validator,
            "namespace": tax.get("namespace"),
            "version": tax.get("version"),
        }
    return registry


def declared_profile(doc: dict) -> str | None:
    props = ((doc.get("metadata") or {}).get("properties") or [])
    values = []
    for p in props:
        if not isinstance(p, dict):
            continue
        name, value = p.get("name"), p.get("value")
        if isinstance(name, str) and name.startswith("atis:") and name.endswith(":profile") and isinstance(value, str):
            values.append(value)
    values = list(dict.fromkeys(values))
    if len(values) == 1:
        return values[0]
    return None


def native_version_token(doc: dict) -> str | None:
    if doc.get("bomFormat") != "CycloneDX":
        return None
    v = doc.get("specVersion")
    if not isinstance(v, str) or not v:
        return None
    return "v" + v.replace(".", "_")


def run_native(exe: str, cbom: Path, version_token: str, quiet: bool) -> bool:
    cmd = [exe, "validate", "--input-file", str(cbom), "--input-format", "json", "--input-version", version_token, "--fail-on-errors"]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(f"NATIVE CYCLONEDX VALIDATION: {'PASS' if r.returncode == 0 else 'FAIL'}")
    if not quiet and (r.stdout.strip() or r.stderr.strip()):
        for line in (r.stdout.strip() or r.stderr.strip()).splitlines():
            print("  " + line)
    return r.returncode == 0


def run_atis(entry: dict, cbom: Path) -> bool:
    cmd = [sys.executable, str(entry["validator"]), str(entry["taxonomy"]), str(cbom)]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if r.stdout.strip():
        for line in r.stdout.strip().splitlines():
            if "official CycloneDX 1.7 schema validation was not run" in line:
                continue
            print("  " + line)
    if r.stderr.strip():
        for line in r.stderr.strip().splitlines():
            print("  " + line)
    print(f"ATIS PROFILE VALIDATION: {'PASS' if r.returncode == 0 else 'FAIL'}")
    return r.returncode == 0


def validate_one(path: Path, registry: dict[str, dict], exe: str, quiet: bool) -> bool:
    print(f"\n== {path} ==")
    try:
        doc = load_json(path)
    except Exception as e:
        print(f"INPUT JSON: FAIL ({e})")
        print("STRICT TWO-LAYER VALIDATION: FAIL")
        return False
    marker = declared_profile(doc)
    if marker is None:
        print("ATIS PROFILE DISCOVERY: FAIL (exactly one ATIS metadata *:profile marker is required)")
        print("STRICT TWO-LAYER VALIDATION: FAIL")
        return False
    entry = registry.get(marker)
    if entry is None:
        print(f"ATIS PROFILE DISCOVERY: FAIL (unsupported profile marker {marker!r})")
        if registry:
            print("Supported profiles:")
            for m in sorted(registry): print(f"  {m}")
        print("STRICT TWO-LAYER VALIDATION: FAIL")
        return False
    print(f"ATIS PROFILE: {marker}")
    token = native_version_token(doc)
    if token is None:
        print("NATIVE CYCLONEDX VALIDATION: FAIL (bomFormat/specVersion unavailable)")
        native_ok = False
    else:
        native_ok = run_native(exe, path, token, quiet)
    atis_ok = run_atis(entry, path)
    ok = native_ok and atis_ok
    print(f"STRICT TWO-LAYER VALIDATION: {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate CBOMs using native CycloneDX plus the ATIS profile they declare.")
    ap.add_argument("cbom", type=Path, nargs="+", help="one or more CBOM JSON files")
    ap.add_argument("--cyclonedx-exe", help="CycloneDX CLI path/command; overrides CYCLONEDX_CLI and PATH")
    ap.add_argument("--quiet-cyclonedx", action="store_true", help="suppress CycloneDX CLI detail")
    ap.add_argument("--version", action="version", version=f"ATIS CBOM global reference validator {VERSION}")
    a = ap.parse_args(argv)
    try:
        registry = discover_profiles()
    except Exception as e:
        print(f"PROFILE REGISTRY: FAIL ({e})")
        return 2
    if not registry:
        print("PROFILE REGISTRY: FAIL (no installed ATIS profiles were discovered)")
        return 2
    exe = resolve_cyclonedx(a.cyclonedx_exe)
    if not exe:
        print("CycloneDX CLI: NOT FOUND")
        print("Install CycloneDX CLI or use --cyclonedx-exe / CYCLONEDX_CLI.")
        return 2
    results = [validate_one(p, registry, exe, a.quiet_cyclonedx) for p in a.cbom]
    print("\n== Overall result ==")
    print(f"FILES PASSED: {sum(results)}/{len(results)}")
    print(f"OVERALL STRICT TWO-LAYER VALIDATION: {'PASS' if all(results) else 'FAIL'}")
    return 0 if all(results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
