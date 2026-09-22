# ATIS 3GPP-5G CBOM Profile — Version 1.0.0

This directory contains the ATIS 3GPP 5G Architecture CBOM Profile Version 1.0.0 for CycloneDX 1.7.

- **Profile marker:** `3gpp-5g-arch-cbom/1.0.0`
- **Taxonomy namespace:** `atis:telecom5g`
- **Implementation binding:** CycloneDX 1.7

## Artifact status

**Normative**

- `3GPP_5G_CBOM_Profile_CycloneDX1.7_v1.0.0.md`
- `atis-telecom5g-property-taxonomy-v1.0.0.md`

**Derived conformance artifacts**

- `atis-telecom5g-taxonomy-1.0.0.json`
- `atis-telecom5g-profile-1.0.0.schema.json`

**Informative/reference material**

- `Documents/` — profile-specific implementation, assurance, coordination, and release documentation
- `Validation/` — profile-specific reference validation support
- `Tests/` — profile/package self-tests, regression tests, and QA audits
- `Examples/Valid/` and `Examples/Invalid/` — profile-specific positive and negative examples

The Python tooling is non-normative reference tooling and does not define conformance.

## End-user validation

From the repository root:

```text
python Tools/validate_cbom.py <your-cbom.json>
```

The global validator discovers this profile from the CBOM's profile marker and performs both the native CycloneDX layer and the ATIS profile layer.

## Profile/package self-test

From the repository root:

```text
python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --require-cyclonedx
```

See `Documents/TOOLING_GUIDE.md` for installation and detailed usage.
