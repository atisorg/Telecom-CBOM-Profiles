# ATIS Telecom5G CBOM 1.0.0 — Conformance Traceability

This table maps major machine-testable normative requirements and publication-quality gates to the supplied **reference** conformance artifacts. It is informative and does not replace the normative profile/taxonomy.

| Requirement area | Normative source | Derived overlay | Reference semantic/checker support | Positive / negative evidence |
|---|---|---:|---:|---|
| CycloneDX 1.7 + ATIS two-layer validation | Profile §§1, 17 | partial | `run_qscii_checks.py --require-cyclonedx`; `validate_atis_cbom.py --cyclonedx-schema` | all positive fixtures; native CLI invocation-contract tests; validator status tests; independent RC2 validation record |
| Profile marker / taxonomy version / mandatory scope | Profile §7; taxonomy Metadata | yes | yes | all valid fixtures; `CBOM_INVALID_missing_scope_*` |
| Deprecated syntax prohibited in strict mode | Profile §7.2; taxonomy strict-conformance clauses | yes | yes | deprecated + dotted negative fixtures |
| `inventoryCompleteness=complete` requires explicit roots | Profile §9.1.1 | property layer | yes | `CBOM_INVALID_complete_without_scope_ref_*` |
| `inventoryScopeRef` fixed-point closure | Profile §9.1.1 | no | `--show-scope-closure` | UDM closure regression includes edge-less MILENAGE/TUAK |
| Vendor vs deployed / effective timestamp | Profile §9.2 | property layer | yes | vendor-effective + missing-timestamp negatives; SEPP positive |
| Summary/detail backing and graph authority | Profile §9.3 | property layer | yes | summary-graph mismatch negative; all positives |
| Duplicate-fact consistency | Profile §9.4 | no | yes | PKI mutual, key-length, curve negatives |
| Reified binding form + entity association | Profile §§10.1, 10.3 | placement | yes | orphan-binding negative; all positives |
| Canonical binding spelling/type | Profile §10.3.1 | vocab/placement | yes | noncanonical/alias negatives |
| Architecture/entity/binding source traceability | Profile §10.3.2; taxonomy source-traceability clauses | n/a | `normative_audit.py`, `sdo_reviewer_audit.py` | source-token audit |
| `cryptographyClass` algorithm-component-only | Profile §11.1.1 | placement | yes | cryptographyClass-on-binding negative |
| Security construct/type canonical pairing | Profile §11.3 | placement/vocab | yes | construct-type service/mismatch/other negatives |
| Canonical protocol ↔ native CycloneDX normalization | Profile §12.1 | vocab | yes | protocol-native mismatch negative |
| Out-of-baseline object-scoped provenance | Profile §§12.3, 15 | property layer | yes | missing-object-provenance negative |
| Alternative dependency open-world semantics | Profile §13 | no | regression assertions | UDM MILENAGE/TUAK positive regression |
| PKI/SBI mutual-auth consistency | Profile §15 | property layer | yes | PKI mutual conflict negative |
| Human/machine normative alignment | Profile §6; taxonomy status clause | n/a | `normative_audit.py` | full audit |
| Terms/definitions + abbreviations | Profile §§4–5 | n/a | `normative_audit.py`, `sdo_reviewer_audit.py` | publication-structure audit |
| PQC/QSC does not impose undefined assessment methodology | Profile §16 | n/a | `normative_audit.py`, `sdo_reviewer_audit.py` | wording audit |
| SDO final-release quality gate | Profile publication package | n/a | `sdo_reviewer_audit.py --fail-on info` | expected `BLOCKER: 0`, `MAJOR: 0`, `MINOR: 0`, `INFO: 0` |
| Migration behavior separated from strict conformance | Profile §7.2 + taxonomy strict-conformance clause | n/a | `normative_audit.py`, `sdo_reviewer_audit.py` | `MIGRATION_GUIDE.md`; legacy strict negative fixtures |
| Reference example/test material is informative | Profile Annex A (informative) | n/a | `sdo_reviewer_audit.py` | tooling guide + positive/negative fixture suite |
| Package IPR/licensing governance notice | non-normative package metadata | n/a | `sdo_reviewer_audit.py` | `IPR_AND_LICENSE_NOTICE.md` |
| CycloneDX Property Taxonomy coordination package | non-normative coordination metadata | n/a | `sdo_reviewer_audit.py`, regression sync check | coordination note + registration manifest |
| Independent strict two-layer release evidence | informative release record | n/a | `run_qscii_checks.py --require-cyclonedx` | `RELEASE_VALIDATION_RECORD.md` |

## Version 1.0.0 release-runner traceability

`run_qscii_checks.py` is non-normative orchestration. It locates an independently installed CycloneDX CLI, validates the three positive fixtures as CycloneDX 1.7, then runs the ATIS/QSCII audits and regression suite. `STRICT TWO-LAYER VALIDATION: PASS` is emitted only when both layers pass. The `--require-cyclonedx` option makes native CLI availability mandatory for release/CI use.
