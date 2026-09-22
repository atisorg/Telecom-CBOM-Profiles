# Contributing

Thank you for helping improve ATIS Telecom CBOM Profiles and taxonomies.

This repository is intended to host **stable, implementer-focused** profiles, taxonomies, validation resources, tests, examples, and supporting documentation that enable consistent interchange and validation of CBOM data.

> Note: Even if you are not a code or documentation contributor, you can still participate by submitting requests and feedback through GitHub Issues (see **Submitting requests** below).

## Ways to contribute

- Suggest new properties, enums, or patterns for an existing profile or taxonomy
- Report ambiguities or gaps, especially where standards alignment is unclear
- Add or improve example CBOMs
- Improve ATIS validation rules, tests, and helper scripts
- Improve supporting documentation
- Propose a new ATIS profile or taxonomy package for an additional telecom domain

## Repository structure

Contributions should follow the repository structure below:

```text
profiles/<profile>/<version>/
Documents/
Validation/
Tests/
Examples/
```

In general:

- `profiles/<profile>/<version>/` contains versioned ATIS profile and taxonomy artifacts.
- `Documents/` contains supporting human-readable documentation and implementation guidance.
- `Validation/` contains ATIS profile/taxonomy validation artifacts and related tooling.
- `Tests/` contains test cases used to exercise and verify validation behavior.
- `Examples/` contains informative example CBOMs and related sample artifacts.

Do not create alternate top-level structures for taxonomy, validator, test, or example content unless the repository maintainers have agreed to an architectural change.

## Submitting requests (no code required)

If you would like ATIS to add or adjust properties, examples, validation rules, tests, or guidance, the preferred path is to open a **GitHub Issue**.

### 1) Open a GitHub Issue

Use the repository **Issues** tab and create a new issue. Please include as much of the following as possible:

- **Profile/taxonomy name** (for example, `telecom5g-cbom`)
- **Version** you are referencing (for example, `1.0.0`)
- **Request type**: property / enum / example / validation / test / documentation
- **What you want to change** (clear description)
- **Why** (the problem it solves and consumer impact)
- **Standards alignment** (for example, 3GPP specification and section if available)
- **Example** (a small CBOM fragment or snippet showing desired usage)

### 2) What happens next (maintainer workflow)

Issues are triaged by the maintainer and typically labeled as one of:

- `accepted` – planned for inclusion
- `needs-info` – more detail needed (for example, specification section or example)
- `deferred` – acknowledged but not scheduled yet
- `rejected` – not aligned with scope or duplicates another mechanism

For accepted items, the maintainer will map the change to the next appropriate release and update CHANGELOG notes.

### 3) Submitting a Pull Request (optional)

If you are able to implement changes yourself:

1. Fork the repository.
2. Create a branch.
3. Submit a Pull Request referencing the Issue (for example, “Fixes #123”).

PRs are reviewed and merged by the maintainer.

## Ground rules

- **Do not** duplicate the same normative profile or taxonomy content in multiple places.
- Treat the applicable versioned content under `profiles/<profile>/<version>/` as the authoritative ATIS profile/taxonomy content for that release.
- Keep supporting documentation in `Documents/`.
- Keep ATIS-specific validation artifacts in `Validation/`.
- Keep validation test cases in `Tests/`.
- Keep examples in `Examples/` and treat them as **informative**, not normative.
- Preserve the separation between official CycloneDX schema validation and ATIS profile/taxonomy validation.

## Contribution workflow

1. **Open an issue first** for substantial changes, such as new property sets, significant validation changes, or new profile/taxonomy packages.
2. Create a branch and submit a PR referencing the issue.
3. Keep changes small and reviewable when possible.
4. Update all affected profile, documentation, validation, test, and example artifacts together where practical.

### PR checklist

For changes affecting a profile or taxonomy:

- [ ] Updated the applicable versioned artifact(s) under `profiles/<profile>/<version>/`
- [ ] Updated supporting content in `Documents/` if implementation guidance is affected
- [ ] Updated ATIS-specific validation rules or tooling in `Validation/` if conformance rules are affected
- [ ] Added or updated test cases in `Tests/`
- [ ] Added or updated informative examples in `Examples/`
- [ ] Confirmed examples pass official CycloneDX 1.7 schema validation where applicable
- [ ] Confirmed examples pass the applicable ATIS profile/taxonomy validation
- [ ] Updated release notes or CHANGELOG information as required

## Validation expectations

Strict ATIS 1.0.0 conformance uses a **two-layer validation architecture**:

```text
Layer 1: Official CycloneDX 1.7 validation
                       +
Layer 2: ATIS profile/taxonomy validation
                       =
Strict ATIS 1.0.0 conformance
```

These layers are intentionally separate:

1. **Layer 1 — Official CycloneDX 1.7 validation**  
   Validate the CBOM against the official CycloneDX 1.7 schema using appropriate CycloneDX-compatible tooling.

2. **Layer 2 — ATIS profile/taxonomy validation**  
   Apply the ATIS validation rules for the relevant profile/taxonomy version. These rules may verify, for example:
   - recognized ATIS property names
   - allowed values, enums, and patterns
   - required ATIS profile or taxonomy markers
   - profile-specific structural or semantic requirements

The ATIS profile/taxonomy validation layer is **not a replacement for the official CycloneDX schema** and should not absorb or duplicate CycloneDX schema validation. A CBOM claiming strict ATIS 1.0.0 conformance must satisfy both validation layers.

Where additional scenario-specific validation is provided, it should be placed within the agreed `Validation/` and `Tests/` structure and clearly identified as required or optional for the relevant profile/version.

## Versioning and releases

Use Semantic Versioning in the form:

```text
<majorVersion>.<minorVersion>.<patchVersion>
```

For example:

```text
1.0.0 → 1.1.0
```

General guidance:

- Increment the **patch** version for backward-compatible corrections or clarifications that do not change the defined behavior.
- Increment the **minor** version for backward-compatible additions or enhancements.
- Increment the **major** version for breaking changes.
- Provide migration notes when a release introduces breaking changes.

If you create a release:

- Use the repository's agreed release/tag naming convention for the version.
- Ensure the corresponding versioned profile artifacts are present under `profiles/<profile>/<version>/`.
- Update the relevant documentation, validation artifacts, tests, examples, and CHANGELOG/release notes.
- Confirm that published examples pass both the official CycloneDX 1.7 validation layer and the applicable ATIS profile/taxonomy validation layer.

## Code of conduct

Be respectful, assume good intent, and focus discussions on technical clarity and implementer usability.
