# ATIS Telecom5G CBOM 1.0.0 — Release Validation Record

**Status: informative release evidence.** This record does not replace the normative conformance requirements or an implementation's own validation obligations.

## Final-release independent validation

On **2026-08-25**, the final **Version 1.0.0** package was exercised in an independent Windows PowerShell environment using the packaged QSCII tooling and an independently installed native CycloneDX validator.

Validation environment:

- Windows PowerShell;
- Python 3.12;
- CycloneDX CLI `0.31.0+1ca06b90df6674674233186e2823decb360601e0`; and
- the dependencies declared by the packaged `requirements.txt`.

The validation command was:

```powershell
python .\run_qscii_checks.py --require-cyclonedx
```

## Native CycloneDX 1.7 validation

The integrated runner detected the independently installed CycloneDX CLI and validated all three positive Version 1.0.0 reference CBOMs using native CycloneDX 1.7 validation.

| Version 1.0.0 positive fixture | Native CycloneDX 1.7 result |
|---|---|
| `CBOM_AMF_N2_vendor_services_v1.0.0_VALID.json` | **PASS** |
| `CBOM_SEPP_N32_deployed_services_v1.0.0_VALID.json` | **PASS** |
| `CBOM_UDM_5G_AKA_vendor_v1.0.0_VALID.json` | **PASS** |

For each positive fixture, the native validator reported `BOM validated successfully.`

## ATIS/QSCII reference QA

The same integrated run reported:

```text
NORMATIVE AUDIT PASSED

SDO REVIEW AUDIT SUMMARY
  BLOCKER: 0
  MAJOR: 0
  MINOR: 0
  INFO: 0
  Gate: fail-on=info -> PASS

ALL 1.0.0 FINAL-RELEASE TESTS PASSED
  JSON parse: 33 files
  Draft-07 strict ATIS overlay schema: valid
  Positive CBOM examples: 3 passed
  Negative examples: 28 correctly rejected
```

The final combined result was:

```text
ATIS/QSCII VALIDATION: PASS
NATIVE CYCLONEDX 1.7 VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
QSCII LOCAL QA GATES PASSED
```

## Interpretation

This run demonstrates the two validation layers required by the Version 1.0.0 profile for the packaged positive reference CBOMs:

1. **native CycloneDX 1.7 validity**, established using the independently installed CycloneDX CLI; and
2. **ATIS profile/taxonomy conformance**, established using the packaged QSCII reference QA tooling.

The packaged regression suite also verified that all 28 ATIS negative fixtures were correctly rejected and that the integrated runner does not claim strict two-layer validation when the native CycloneDX layer fails or is unavailable.

## Release conclusion

**Version 1.0.0 achieved `STRICT TWO-LAYER VALIDATION: PASS` in the independent Windows release-validation environment.**

This record captures release evidence for the shipped Version 1.0.0 package. Conforming producers, consumers, validators, and CI environments remain responsible for applying the normative requirements of the profile to the CBOMs they process.


## Independent Validation of Reorganized Repository (2026-09-08)
On 2026-09-08, the reorganized GitHub repository was independently exercised on Windows 11 from a different repository root using Python 3.12 and the independently installed CycloneDX CLI 0.31.0.

```powershell
python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --require-cyclonedx
```

```text
== Native CycloneDX 1.7 validation ==
CycloneDX CLI: <user-profile>\CycloneDX.CLI_Microsoft.Winget.Source_8wekyb3d8bbwe\cyclonedx.EXE
Version: 0.31.0+1ca06b90df6674674233186e2823decb360601e0
  CBOM_AMF_N2_vendor_services_v1.0.0_VALID.json: PASS
    Validating JSON BOM...
    BOM validated successfully.
  CBOM_SEPP_N32_deployed_services_v1.0.0_VALID.json: PASS
    Validating JSON BOM...
    BOM validated successfully.
  CBOM_UDM_5G_AKA_vendor_v1.0.0_VALID.json: PASS
    Validating JSON BOM...
    BOM validated successfully.

== ATIS/QSCII reference QA ==

==> <python-executable> <repository-root>\profiles\3gpp-5g\1.0.0\Tests\normative_audit.py
NORMATIVE AUDIT PASSED
  RFC 2119/RFC 8174 keyword declaration: complete
  Lower-case modal ambiguity: none
  Mandatory two-layer validation wording: aligned
  Normative references + artifact authority/precedence: aligned
  inventoryScopeRef fixed-point closure: aligned
  SemVer 1.0.0 stable-release declaration: aligned
  Publication/tooling separation: aligned
  Terms/definitions + abbreviations: aligned
  Architecture/service source traceability: aligned
  PQC/QSC methodology wording: informative/non-normative
  Binding representation conditionality: aligned
  Markdown/machine cardinality alignment: passed
  Migration-only strict prohibitions: aligned
  Native backing representation requirement: aligned

==> <python-executable> <repository-root>\profiles\3gpp-5g\1.0.0\Tests\sdo_reviewer_audit.py --fail-on info

SDO REVIEW AUDIT SUMMARY
  BLOCKER: 0
  MAJOR: 0
  MINOR: 0
  INFO: 0
  Gate: fail-on=info -> PASS

==> <python-executable> <repository-root>\profiles\3gpp-5g\1.0.0\Tests\test_v1.0.0.py

== Native CycloneDX 1.7 validation ==
CycloneDX CLI: cyclonedx-test
Version: CycloneDX CLI 0.31.0
  CBOM_AMF_N2_vendor_services_v1.0.0_VALID.json: PASS
  CBOM_SEPP_N32_deployed_services_v1.0.0_VALID.json: PASS
  CBOM_UDM_5G_AKA_vendor_v1.0.0_VALID.json: PASS

== Native CycloneDX 1.7 validation ==
CycloneDX CLI: cyclonedx-test
Version: CycloneDX CLI test
  CBOM_AMF_N2_vendor_services_v1.0.0_VALID.json: PASS
  CBOM_SEPP_N32_deployed_services_v1.0.0_VALID.json: FAIL
  CBOM_UDM_5G_AKA_vendor_v1.0.0_VALID.json: PASS
ALL 1.0.0 FINAL-RELEASE TESTS PASSED
  JSON parse: 33 files
  Draft-07 strict ATIS overlay schema: valid
  Positive CBOM examples: 3 passed
  Negative examples: 28 correctly rejected
  Retained v0.97 conformance closure (#1-#6): passed
  #7 algorithm-only cryptographyClass + hybrid semantics: passed
  #8 noncanonical crypto summary labels/native normalization authority: passed
  #9 duplicate-fact consistency rules: passed
  #10 baselineRelease/object-release override semantics: passed
  #11 effective-state snapshot timestamp semantics: passed
  #12 mandatory entity association for reified bindings: passed
  RFC 2119/RFC 8174 normative-language audit: passed
  SDO publication audit: 0 blockers / 0 major / 0 minor / 0 informational
  Normative references + artifact authority/precedence: passed
  inventoryScopeRef fixed-point closure + reference output: passed
  SemVer 1.0.0 transition: passed
  Terms/definitions + abbreviations: passed
  Architecture/service source traceability: passed
  Vague normative-condition cleanup: passed
  PQC/QSC methodology wording: passed
  IPR/license packaging notice: passed
  CycloneDX property-taxonomy coordination package: passed
  Informative example/test + migration guidance separation: passed
  Final Version 1.0.0 designation: passed
  Markdown/machine cardinality alignment: passed
  Validator PASS/full-conformance messaging distinction: passed
  Integrated native CycloneDX CLI runner invocation: passed
  Strict two-layer vs ATIS-only result distinction: passed

== Combined validation result ==
ATIS/QSCII VALIDATION: PASS
NATIVE CYCLONEDX 1.7 VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
QSCII LOCAL QA GATES PASSED
```

Note: The SEPP ... FAIL shown within test_v1.0.0.py is an intentional simulated CycloneDX failure used by the regression suite to verify correct failure propagation. It is not a failure of the SEPP reference CBOM. The actual SEPP reference CBOM passed the independently installed native CycloneDX CLI earlier in the same run.

## Reorganized repository validation conclusion

**The reorganized Version 1.0.0 repository achieved `STRICT TWO-LAYER VALIDATION: PASS` in the independent Windows validation environment.**

This validation provides evidence that the repository reorganization and associated path-only tooling changes preserved the conformance behavior of the previously validated Version 1.0.0 release.

## Repository reorganization validation (2026-09-08)

The Version 1.0.0 GitHub repository was reorganized by architectural responsibility after the original release validation. The reorganization did not change the normative profile, human-readable taxonomy, machine-readable taxonomy, overlay schema constraints, or CBOM examples. Profile-specific scripts and examples were relocated, with corresponding relative-path updates to the reference tooling.

The reorganized repository was then independently revalidated on Windows using:

```powershell
python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --require-cyclonedx
```

The reorganized repository achieved:

```text
ATIS/QSCII VALIDATION: PASS
NATIVE CYCLONEDX 1.7 VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
QSCII LOCAL QA GATES PASSED
```

This confirms that the repository restructuring and associated path-only tooling changes did not alter Version 1.0.0 conformance behavior.

