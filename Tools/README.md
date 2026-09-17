# Repository-wide Tools

These tools are **non-normative reference tooling** and are intended to operate across ATIS CBOM profiles.

- `validate_cbom.py` — end-user validator. It discovers the profile declared by each CBOM, runs native CycloneDX validation, invokes the corresponding profile-specific ATIS validation layer, and returns one combined result.

Profile-specific validation implementations and package QA tests live with their profiles under `profiles/<profile>/<version>/Validation/` and `Tests/`.
