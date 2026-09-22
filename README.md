# ATIS Telecom CBOM

This repository is the extensible home for ATIS Telecom CBOM profiles and reusable reference tooling. Repository placement follows **architectural scope and responsibility**, not file type or implementation language.

The current published profile is the ATIS **3GPP-5G CBOM Profile Version 1.0.0**. Future profiles may address other telecom domains or baselines without forcing their normative content, examples, or tests into the 3GPP-5G profile.

## Repository organization

```text
telecom-cbom-profiles/
├── README.md
├── ROADMAP.md
├── requirements.txt
├── Tools/
│   └── validate_cbom.py
└── profiles/
    └── 3gpp-5g/
        └── 1.0.0/
            ├── README.md
            ├── 3GPP_5G_CBOM_Profile_CycloneDX1.7_v1.0.0.md
            ├── atis-telecom5g-property-taxonomy-v1.0.0.md
            ├── atis-telecom5g-taxonomy-1.0.0.json
            ├── atis-telecom5g-profile-1.0.0.schema.json
            ├── Documents/
            ├── Validation/
            ├── Tests/
            └── Examples/
                ├── Valid/
                └── Invalid/
```

## Organizing principles

- **Documents and examples follow the profile** because they describe or instantiate profile-specific scope, vocabularies, semantics, baselines, and conformance expectations.
- **Reusable operational tools are repository-wide** when they are independent of any one profile.
- **Profile-specific validation support remains with the profile.**
- **Tests and QA remain with the profile** because they verify that profile/package, even when the tests happen to be implemented in Python.

## Validate a CBOM

Install the Python dependencies and CycloneDX CLI, then from the repository root run:

```text
python -m pip install -r requirements.txt
python Tools/validate_cbom.py <your-cbom.json>
```

`Tools/validate_cbom.py` is non-normative reference tooling. It discovers the ATIS profile declared by the CBOM, runs native CycloneDX validation, invokes the corresponding profile-specific ATIS validation layer, and returns one combined result.

## Roadmap

See `ROADMAP.md` for the current contribution-driven roadmap for extending ATIS Telecom CBOM beyond the initial 3GPP-5G profile. The roadmap is forward-looking; it does not make future information-model, ontology, knowledge-graph, domain, or platform work part of the current 3GPP-5G 1.0.0 normative profile.
