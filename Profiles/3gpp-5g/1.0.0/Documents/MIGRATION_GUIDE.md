# ATIS Telecom5G CBOM 1.0.0 — Migration Guide

**Informative. This document does not define strict conformance.**

Strict `1.0.0` conformance prohibits deprecated ATIS properties and legacy dotted `atis:telecom5g:iface.*` syntax. This guide exists only to help QSCII reviewers and implementers diagnose or convert artifacts produced from earlier drafts.

## Reference migration checker

The supplied reference validator can inspect legacy input with:

```bash
python profiles/3gpp-5g/1.0.0/Validation/validate_atis_cbom.py \
  --legacy-compat \
  profiles/3gpp-5g/1.0.0/atis-telecom5g-taxonomy-1.0.0.json \
  <legacy-cbom.json>
```

Acceptance in `--legacy-compat` mode does **not** establish strict `1.0.0` conformance. A migrated artifact must be emitted without deprecated/legacy properties and then pass the normal strict-conformance checks.

## Legacy-to-current guidance

| Earlier-draft construct | Alpha.3 direction |
|---|---|
| `atis:telecom5g:nfType` | Replace with `atis:telecom5g:entityType`. |
| `atis:telecom5g:interface` / `interfaces` | Reify each represented architectural binding as a CycloneDX service and use `bindingType` + `binding`. |
| `atis:telecom5g:assertion` | Use mandatory `cbom.scope` plus `crypto.supported*` for vendor capability or `effective*` for deployed effective state. |
| free-form `usageContext` | Use controlled/faceted `protectionContext` when its vocabulary applies. |
| `atis:telecom5g:iface.*` dotted properties | Move binding-specific data onto the corresponding reified binding service. |
| `cryptoFunction` | Use the orthogonal `securityObjective`, `protectionContext`, and `cryptoUsageType` concepts. |
| `cryptoType` | Use algorithm-component `cryptographyClass`; use native CycloneDX `algorithmProperties.primitive` for primitive/function. |
| `capabilityStatus` | Do not migrate to a flat replacement; the profile deliberately has no flat per-object capability-status property. |
| `pqcRiskLevel` | Remove; the profile does not define a PQC/CRQC risk methodology. |

## Migration principle

Migration must preserve the distinction between vendor-supported capability and deployment-effective state. It must also preserve open-world semantics: the absence of a declaration or dependency edge is not automatically a negative assertion.

When a legacy representation cannot be transformed without inventing relationships, status, or evidence that the source artifact did not contain, the migration output should remain conservative rather than manufacturing semantics.
