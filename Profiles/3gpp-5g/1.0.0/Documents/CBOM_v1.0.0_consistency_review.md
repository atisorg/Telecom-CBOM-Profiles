# ATIS Telecom5G CBOM 1.0.0 — Final Release Review

## Overall assessment

`1.0.0` is a release promotion of `1.0.0-rc.2`. No taxonomy semantics, graph predicates, assertion/evidence model, cryptographic modeling feature, or strict-conformance rule was added or changed during finalization.

The finalization work is limited to stable-version identifiers, final publication designation, release documentation, a release-validation record, and flat ZIP packaging.

The executable SDO audit is:

- **BLOCKER: 0**
- **MAJOR: 0**
- **MINOR: 0**
- **INFO: 0**

## Strict two-layer validation architecture

`run_qscii_checks.py` retains the RC2 integration of the independent native CycloneDX validation layer with the ATIS/QSCII reference QA gates. When the `cyclonedx` CLI is available, the three positive reference CBOMs are validated using:

```text
cyclonedx validate --input-file <file> --input-format json --input-version v1_7 --fail-on-errors
```

Strict two-layer validation is reported only when both native CycloneDX validation and the ATIS/QSCII gates pass.

The runner supports:

- PATH auto-discovery;
- `--cyclonedx-exe` explicit override;
- `CYCLONEDX_CLI` environment override;
- `--require-cyclonedx` for release/CI enforcement; and
- `--quiet-cyclonedx` for compact CI logs.

If the CLI is absent in ordinary developer mode, local ATIS/QSCII QA can still pass, but the runner explicitly reports `STRICT TWO-LAYER VALIDATION: NOT ESTABLISHED`.

## Independent RC2 validation evidence

The final RC2 package was executed on an independent Windows/PowerShell environment using CycloneDX CLI `0.31.0+1ca06b90df6674674233186e2823decb360601e0` and Python 3.12. All three positive RC2 CBOMs passed native CycloneDX 1.7 validation. The normative audit passed, the SDO audit reported `0/0/0/0`, all three ATIS positive fixtures passed, all 28 ATIS negative fixtures were correctly rejected, and the integrated runner ended with:

```text
ATIS/QSCII VALIDATION: PASS
NATIVE CYCLONEDX 1.7 VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
QSCII LOCAL QA GATES PASSED
```

The Version 1.0.0 examples retain the same native CycloneDX structures and ATIS semantics; only the profile/taxonomy/version marker values advance from RC2 to `1.0.0`.

## Final release quality gate

For QSCII release/CI use:

```bash
python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --require-cyclonedx
```

A successful run must end with:

```text
ATIS/QSCII VALIDATION: PASS
NATIVE CYCLONEDX 1.7 VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
QSCII LOCAL QA GATES PASSED
```

## Retained closures

Version 1.0.0 retains without semantic change:

- normative references and artifact precedence;
- deterministic inventory-scope closure;
- terms/definitions and abbreviations;
- architecture/service source traceability;
- testable normative wording and PQC/QSC methodology boundary;
- IPR/license working-package notice;
- CycloneDX Property Taxonomy coordination material;
- informative-only migration and example/test guidance;
- clean `0/0/0/0` SDO audit;
- non-normative QSCII Python reference tooling; and
- integrated native CycloneDX validation with strict-vs-ATIS-only status separation.

## Editorial correction during promotion

RC2 contained a prerelease-only SemVer explanatory sentence that referred to `rc.1` while describing Release Candidate 2. The actual profile/taxonomy markers, filenames, fixtures, schemas, and tool versions all correctly used `1.0.0-rc.2`; therefore the wording defect had no conformance effect. The final `1.0.0` artifacts remove prerelease-specific explanatory language.

## Final assessment

The Version 1.0.0 package is suitable as the stable release baseline. Further changes should use normal SemVer evolution and should not be folded silently into the 1.0.0 artifacts.
