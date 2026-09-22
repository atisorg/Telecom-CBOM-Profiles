# Changelog

## 1.0.0

First stable Semantic Versioning release. Promotes `1.0.0-rc.2` without changing the normative CBOM semantic model or strict-conformance rules.

### Changed

- Advanced all version-bearing normative artifacts, derived schemas, fixtures, scripts, and documentation to stable `1.0.0`.
- Replaced release-candidate publication designations with final `Version 1.0.0` designations.
- Retained the RC2 integrated native CycloneDX + ATIS/QSCII two-layer validation workflow.
- Added `RELEASE_VALIDATION_RECORD.md` documenting successful independent RC2 strict two-layer validation on Windows with the real CycloneDX CLI.
- Distributed the final ZIP with a flat archive root to avoid duplicate nested directories under common Windows extraction workflows.
- Removed a prerelease-only SemVer explanatory typo that referred to `rc.1` while describing Release Candidate 2; machine version markers and conformance behavior were unaffected.

### Validation basis

- Independent RC2 validation used CycloneDX CLI `0.31.0+1ca06b90df6674674233186e2823decb360601e0` and Python 3.12 on Windows.
- All three positive RC2 CBOMs passed native CycloneDX 1.7 validation.
- The normative audit passed.
- The SDO audit reported `0 BLOCKER / 0 MAJOR / 0 MINOR / 0 INFO`.
- All three ATIS positive fixtures passed and all 28 ATIS negative fixtures were correctly rejected.
- The integrated runner reported `STRICT TWO-LAYER VALIDATION: PASS` and `QSCII LOCAL QA GATES PASSED`.

### Release policy

- Version 1.0.0 is the stable baseline. Subsequent incompatible changes require normal SemVer treatment rather than silent modification of the 1.0.0 artifacts.

## 1.0.0-rc.2

Second release candidate; tooling-only integration of the native CycloneDX CLI validation layer. The normative CBOM semantics and strict-conformance rules are unchanged from `1.0.0-rc.1`.

### Added

- Automatic discovery of the installed CycloneDX CLI by `run_qscii_checks.py`.
- Native CycloneDX 1.7 validation of all three positive reference CBOMs using `cyclonedx validate --input-format json --input-version v1_7 --fail-on-errors`.
- Explicit combined result reporting: `STRICT TWO-LAYER VALIDATION: PASS` only when both native CycloneDX and ATIS/QSCII gates pass.
- `--require-cyclonedx` for CI/release use; absence of the native CLI becomes fatal when this flag is supplied.
- `--cyclonedx-exe` and `CYCLONEDX_CLI` override mechanisms for nonstandard installations.

### Changed

- Advanced version-bearing package artifacts, examples, tests, schemas, and documentation to `1.0.0-rc.2`.
- Updated the QSCII tooling guide and conformance traceability to include native CycloneDX CLI integration.
- The one-command QSCII runner now distinguishes `ATIS/QSCII VALIDATION: PASS` from full strict two-layer validation rather than implying that local ATIS checks alone establish strict conformance.

### Retained

- All `1.0.0-rc.1` normative semantics, SDO closure, publication boundary, IPR, migration, and namespace-coordination behavior.
- The Python tooling remains non-normative reference tooling; the native CycloneDX CLI remains an independent implementation of the CycloneDX validation layer.

### Validation basis

- The three positive RC1 reference CBOMs were independently validated successfully with CycloneDX CLI 0.31.0 on Windows before RC2 integration.
- RC2 regression tests exercise both CLI-present and CLI-absent runner behavior using a controlled test double; release/CI environments should additionally execute `python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --require-cyclonedx` with the real CycloneDX CLI.

## 1.0.0-rc.1

First release candidate; closes the final informational SDO publication-readiness finding while preserving the alpha.3 semantic and strict-conformance model.

### Changed

- Replaced the publication-level `Draft` designation on the normative profile with `Release Candidate 1`.
- Replaced the publication-level `Draft` designation on the normative human-readable taxonomy with `Release Candidate 1`.
- Advanced all version-bearing package artifacts, examples, tests, schemas, and documentation to `1.0.0-rc.1`.
- Raised the SDO package gate to `--fail-on info`; RC QA requires `0 BLOCKER`, `0 MAJOR`, `0 MINOR`, and `0 INFO` findings.

### Retained

- All `1.0.0-alpha.3` semantic, conformance, publication-boundary, IPR, migration, CycloneDX-coordination, and reference-tooling behavior.
- The external requirement to validate against the complete official CycloneDX 1.7 schema/bundle before final `1.0.0`.

### Status

- SDO blockers: 0.
- SDO major findings: 0.
- SDO minor findings: 0.
- SDO informational findings: 0.

## 1.0.0-alpha.3

Third SemVer alpha; SDO minor-finding / publication-boundary cleanup.

### Added

- `IPR_AND_LICENSE_NOTICE.md` for working-package QSCII use and rights/licensing boundary.
- `MIGRATION_GUIDE.md` as explicitly informative legacy-conversion guidance.
- `CYCLONEDX_PROPERTY_TAXONOMY_COORDINATION.md`.
- `cyclonedx_property_taxonomy_manifest.json`, synchronized with the machine-readable taxonomy.
- Alpha quality gate requiring `0 BLOCKER`, `0 MAJOR`, and `0 MINOR` SDO findings.

### Changed

- Moved implementation-package example/test recommendations out of normative requirements; the profile now identifies reference examples/tests only in an informative annex.
- Removed normative statements about migration-tool acceptance from the profile and human taxonomy while retaining the strict prohibition on deprecated/legacy syntax.
- Raised `sdo_reviewer_audit.py`, `run_qscii_checks.py`, and the package regression gate from `--fail-on major` to `--fail-on minor`.
- Updated deprecated-property machine cardinalities so they state only their strict-conformance prohibition; non-strict migration behavior is documented informatively.

### Deliberately retained

- The Draft designation remains present as the single informational SDO finding. Alpha.3 does not close it.
- All alpha.2 semantic, conformance, hostile-implementer, interoperability, normative-language, and SDO-major cleanup behavior.
- Python validation/audit/checker tooling as non-normative QSCII reference tooling.

### Status

- SDO blockers: 0.
- SDO major findings: 0.
- SDO minor findings: 0.
- SDO informational findings: 1 (Draft designation, intentionally retained).
- Full strict validation still requires the official CycloneDX 1.7 schema bundle in CI/implementation environments.

## 1.0.0-alpha.2

Second SemVer alpha; closed the five remaining major SDO publication-readiness findings: terms/definitions, abbreviations, architecture-vocabulary source traceability, testable normative conditions, and PQC/QSC methodology wording.

## 1.0.0-alpha.1

First SemVer pre-release; closed the three v0.99 SDO blockers and introduced normative artifact precedence, deterministic inventory scope closure, and the QSCII reference-tooling guide.
