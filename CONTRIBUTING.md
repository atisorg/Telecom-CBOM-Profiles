# Contributing to ATIS Telecom CBOM Profiles

Thank you for helping improve ATIS Telecom CBOM Profiles and taxonomies.

This repository hosts **stable, implementer-focused** profiles, taxonomies, validation resources, tests, examples, and supporting documentation for consistent interchange and validation of cryptographic bill of materials (CBOM) data.

**You do not need to write code to contribute.** Telecom operators, vendors, standards participants, and other interested parties can submit requirements, report gaps, or suggest improvements through GitHub Issues.

## How to submit a request

**Preferred method: [Telecom CBOM change request template](https://github.com/atisorg/Telecom-CBOM-Profiles/blob/main/.github/ISSUE_TEMPLATE/change-request.yml).** To submit a request, [open the template as a new GitHub Issue](https://github.com/atisorg/Telecom-CBOM-Profiles/issues/new?template=change-request.yml). You will need a GitHub account to submit a request.

1. Open the [Telecom CBOM change request form](https://github.com/atisorg/Telecom-CBOM-Profiles/issues/new?template=change-request.yml), or select **Issues → New issue** in this repository.
2. Complete the **Telecom CBOM change request** form. You can [view the template file here](https://github.com/atisorg/Telecom-CBOM-Profiles/blob/main/.github/ISSUE_TEMPLATE/change-request.yml).
3. Describe the change, its purpose, and the affected profile or taxonomy. Include standards references and a short example if available.
4. Submit the issue. ATIS maintainers will review it and may request further details.

If the template is unavailable, [open a blank Issue](https://github.com/atisorg/Telecom-CBOM-Profiles/issues/new) and include these details:

- **Profile/taxonomy** and **version** (for example, `telecom5g-cbom`, `1.0.0`)
- **Request type**: property / enum / algorithm or protocol / 3GPP interface mapping / example / validation / test / documentation / new domain profile
- **Proposed change** and **reason for the change**, including implementer or carrier impact
- **Standards alignment**, such as a relevant 3GPP specification and clause
- **Illustrative CBOM fragment**, when useful (do not include secrets or proprietary deployment details)

Requests may cover new cryptographic properties, 5G network-function and interface mappings, PQC or crypto-agility metadata, example CBOMs, validator behavior, or future domain-specific taxonomies.

**Questions or difficulty using GitHub:** You may contact ATIS through the contact channel available on the [ATIS Quantum-Safe Communications and Information Initiative page](https://atis.org/initiatives/quantum/). GitHub Issues remain the preferred route for technical change requests so that proposals and feedback can be tracked. Do not post sensitive network, key, certificate-private-key, or customer information in this public repository.

## Review of submitted requests

ATIS will review submitted Issues, consider their relevance to the profile or taxonomy, and may seek clarification or additional technical input. Issues may be labeled:

- `accepted` — accepted for further development or inclusion in a planned release
- `needs-info` — additional details or examples are required
- `deferred` — acknowledged but not currently scheduled
- `rejected` — outside scope, unsuitable, or addressed by an existing mechanism

ATIS will consider accepted requests for an appropriate future release, taking account of technical review, compatibility, and implementation impact. An accepted Issue does not mean the change has already been incorporated into a published profile. Changes included in a release will be documented in the relevant release notes or CHANGELOG.

## Ways to contribute

- Suggest properties, enumerations, or modeling patterns for an existing profile or taxonomy
- Report ambiguities or gaps, especially in standards alignment
- Propose network-function, interface, and cryptographic-dependency mappings
- Add or improve informative example CBOMs
- Improve ATIS validation rules, tests, and helper scripts
- Improve documentation and implementation guidance
- Propose a new ATIS profile or taxonomy package for another telecom domain

## Submitting a Pull Request

If you can implement a change, you may submit a Pull Request (PR):

1. **Open an Issue first** for substantial changes, such as new property sets, validation behavior, or profile packages.
2. Fork the repository and create a working branch.
3. Make focused changes, including affected tests, examples, and documentation where practical.
4. Open a PR against `main`, explain the change, and reference the Issue (for example, `Fixes #123`).
5. Respond to review comments. ATIS will review the proposed changes and provide feedback before they are considered for merging.

For small editorial fixes, maintainers may accept a PR without a prior Issue.

### Pull Request checklist

For changes affecting a profile or taxonomy:

- [ ] Updated the applicable versioned artifact(s) under `profiles/<profile>/<version>/`
- [ ] Updated supporting content in `Documents/` if implementation guidance is affected
- [ ] Updated ATIS-specific validation rules or tooling in `Validation/` if conformance rules are affected
- [ ] Added or updated test cases in `Tests/`
- [ ] Added or updated informative examples in `Examples/`
- [ ] Confirmed examples pass official CycloneDX 1.7 schema validation where applicable
- [ ] Confirmed examples pass the applicable ATIS profile/taxonomy validation
- [ ] Updated release notes or CHANGELOG information as required

## Repository structure

Contributions should follow the agreed repository structure:

```text
profiles/<profile>/<version>/
Documents/
Validation/
Tests/
Examples/
```

- `profiles/<profile>/<version>/` contains versioned authoritative ATIS profile and taxonomy artifacts.
- `Documents/` contains supporting documentation and implementation guidance.
- `Validation/` contains ATIS-specific validation artifacts and tooling.
- `Tests/` contains validation test cases.
- `Examples/` contains **informative**, not normative, example CBOMs.

Please discuss proposed changes to the top-level directory structure through a GitHub Issue before implementing them. Some directories may be introduced as the repository evolves.

## Ground rules

- Do not duplicate normative profile or taxonomy content in multiple locations.
- Treat the applicable versioned content under `profiles/<profile>/<version>/` as authoritative for that ATIS release.
- Keep documentation, ATIS validation, tests, and examples in their respective agreed locations.
- Preserve the distinction between the official CycloneDX specification and ATIS-specific profile and taxonomy requirements.
- Proposals to change the upstream CycloneDX schema should be distinguished from changes to ATIS profiles and, where appropriate, coordinated with the CycloneDX project.
- Do not submit private keys, secrets, confidential network configurations, or other sensitive information.

## Validation expectations

Strict ATIS 1.0.0 conformance uses **two separate validation layers**:

```text
Layer 1: Official CycloneDX 1.7 schema validation
                       +
Layer 2: ATIS profile/taxonomy validation
                       =
Strict ATIS 1.0.0 conformance
```

1. **Official CycloneDX 1.7 validation:** Validate CBOM documents against the official CycloneDX schema using suitable CycloneDX-compatible tooling.
2. **ATIS profile/taxonomy validation:** Apply the rules for the applicable ATIS version, which may check recognized property names, allowed values and patterns, profile markers, and structural or semantic requirements.

ATIS validation does not replace or duplicate official CycloneDX schema validation. Where additional scenario-specific validation is provided, place it in the agreed `Validation/` and `Tests/` structure and identify whether it is required or optional.

## Versioning and releases

Use Semantic Versioning: `<majorVersion>.<minorVersion>.<patchVersion>` (for example, `1.0.0` → `1.1.0`).

- **Patch**: backward-compatible corrections or clarifications without behavioral changes.
- **Minor**: backward-compatible additions or enhancements.
- **Major**: breaking changes, with migration notes.

For releases, use the agreed release/tag convention, ensure the versioned profile artifacts are present, update relevant documentation, validation, tests, examples, and release notes, and confirm published examples pass both validation layers.

## Code of conduct

Be respectful, assume good intent, and focus discussions on technical clarity and implementer usability.
