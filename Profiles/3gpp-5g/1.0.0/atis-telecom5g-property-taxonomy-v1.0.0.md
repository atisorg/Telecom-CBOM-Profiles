# `atis:telecom5g` Namespace Taxonomy (Version 1.0.0)

This document defines the **ATIS `atis:telecom5g` property taxonomy** used by the **3GPP 5G Architecture CBOM Profile for CycloneDX 1.7**.

## Purpose

This taxonomy defines ATIS telecom-specific **property names, controlled vocabularies, and allowed placement** for 5G cryptographic inventory reporting. **It is a taxonomy, not an implementation-independent information model.** The companion profile defines how these terms are combined with native CycloneDX objects and relationships.

The cryptographic inventory baseline for v1.0.0 is **3GPP TR 33.938 V19.2.0 (Release 19)**. This baseline governs the cryptographic inventory; it is not the source vocabulary for every 5G architectural entity or binding. Protocols/security constructs admitted outside the cryptographic-inventory baseline require the object-scoped provenance defined below.

## Normative terminology

The conformance keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** have the meanings defined by the companion v1.0.0 profile under RFC 2119 / RFC 8174. Lower-case modal verbs are descriptive and are not conformance keywords. Property cardinalities and placement constraints in this taxonomy are normative when expressed using those capitalized keywords.

## Normative status and artifact precedence

This human-readable taxonomy is a normative companion artifact to the v1.0.0 profile. It is authoritative for ATIS property names, controlled vocabularies, placement, and cardinality; the profile is authoritative for profile-level modeling, graph, scope, and interpretation rules. The machine-readable taxonomy JSON and strict overlay schema are conformance artifacts derived from these normative texts and MUST remain consistent with them. If a publication defect creates a conflict, the normative profile/human-readable taxonomy control and the conflict MUST be corrected in a subsequent version.

The supplied Python validators, audits, generators, tests, examples, and negative fixtures are reference tooling and informative test material. They do not define conformance, and independent implementations MAY validate the same normative requirements.

## Taxonomy vs profile boundary

The **taxonomy** defines reusable ATIS vocabulary. The **profile** selects and constrains that vocabulary, adds conformance and modeling rules, and uses native CycloneDX 1.7 constructs where CycloneDX already provides the appropriate representation.

In particular, the profile defines how to represent 5G NFs and architectural bindings, how to use native CycloneDX cryptographic assets, how to use generic dependency edges, and how to map the heterogeneous TR 33.938 Protocol/Function inventory without pretending that every entry is the same semantic kind.

## Version 1.0.0 publication status and retained semantic changes

v1.0.0 is the first stable release under Semantic Versioning 2.0.0. It promotes the final pre-release without changing the established CBOM semantic model or strict-conformance rules. The semantic changes summarized below were developed and reviewed during the pre-release series and are retained in this release.

- v0.7 `atis:telecom5g:cryptoFunction` is replaced by **`securityObjective`**, **`protectionContext`**, and **`cryptoUsageType`**. These respectively capture *why* protection exists, *where/in what operational context* it applies, and *what cryptographic function* is performed.
- `cryptoUsageType` SHOULD be attached to the cryptographic-asset instance to which the usage applies. If the same algorithm has different usage semantics in different contexts and those differences need to be preserved, separate contextual asset instances SHOULD be used.
- v0.7 `atis:telecom5g:pqcRiskLevel` is removed because no ATIS methodology defined `High`/`Medium`/`Low`.
- Heterogeneous non-protocol items are modeled as **`securityConstruct` + `securityConstructType`**. `securityConstructType` is component-only and MUST match the canonical classification for the construct.
- `bindingType` and `binding` model architectural bindings/interfaces; protocols such as `5G-AKA` or `GTP-C` are not themselves binding identifiers.
- `capabilityStatus`, introduced during early v1.0.0 drafting, is removed because a single flat property cannot unambiguously qualify individual capabilities.
- `inventoryCompleteness` is scope-relative: vendor and deployed CBOMs interpret completeness against the entities, bindings, scenario, release, and declaration types actually represented; `complete` never turns absence into a negative assertion.
- BOM-level `kdfAlgorithm` is removed. KDFs are represented as native cryptographic algorithm assets.
- `pki.role` and `pki.authenticationMode` are separate; `mutual` is an authentication mode, not a role.
- Protocols/security constructs admitted outside the TR 33.938 cryptographic-inventory baseline require authoritative provenance on the corresponding referencable component. The baseline does not define every architectural entity/binding vocabulary.
- `effective*` means active/enforced/negotiated/observed deployment state; mere configuration is insufficient, and effective assertions require `metadata.timestamp` as the as-of time of the effective-state snapshot.
- v0.95 `cryptoType` is removed because it mixed cryptography class with primitive/function; v1.0.0 uses algorithm-component-only `cryptographyClass` plus native CycloneDX `algorithmProperties.primitive`. `hybrid` describes one hybrid construction, not a mixed binding.
- Taxonomy version, profile version, and CycloneDX implementation-binding version are explicitly distinguished and can evolve independently.
- v0.7 `assertion` and free-form `usageContext` are retained only as deprecated compatibility properties.

## Scope notes

- **5G-EIR:** `5G-EIR` is a valid 3GPP 5GC Network Function and remains in `entityType`. It is not currently represented in the TR 33.938 V19.2.0 cryptographic inventory; its inclusion does not assert TR 33.938-defined cryptographic usage.
- **PRINS:** PRINS is a valid 3GPP 5G security protocol specified in TS 33.501 and has a native CycloneDX 1.7 protocol type. It is not a separate protocol/function entry in TR 33.938 V19.2.0; a referencable PRINS component MUST therefore carry object-scoped authoritative TS 33.501 provenance via native CycloneDX `externalReferences[]`.
- **MILENAGE/TUAK:** detailed MILENAGE and TUAK algorithms SHOULD be represented as native CycloneDX cryptographic assets. In a vendor capability CBOM, alternatives MUST NOT be represented as though all alternatives were simultaneously required dependencies.

## Placement model

- `metadata` properties apply to the BOM as a whole.
- `service` properties apply to CycloneDX `services[]` objects, including NFs, non-NF entities when represented as services, and reified architectural bindings, subject to each property's stricter placement rule.
- `component` properties apply to CycloneDX `components[]` objects, including cryptographic assets and referencable security constructs.
- Cryptographic protocols, algorithms, keys, and certificates SHOULD use native CycloneDX 1.7 CBOM structures when the native schema defines a representation for that object type.
- Reifying a 3GPP binding as a CycloneDX service is an implementation-binding technique that provides a referencable object; it does not redefine the conceptual binding as a network service.

## Controlled vocabularies

| Vocabulary | Values |
| --- | --- |
| cbom.scope | `vendor`, `deployed` |
| assertion *(migration only)* | `supported`, `effective` |
| inventoryCompleteness | `complete`, `partial`, `unknown` |
| securityObjective | `Authentication`, `Authorization`, `Confidentiality`, `Integrity`, `ReplayProtection` |
| protectionContext | `control-plane`, `user-plane`, `api`, `signaling`, `roaming`, `service-based-interface`, `application-layer`, `transport` |
| cryptoUsageType | `Authentication`, `Confidentiality Protection`, `Integrity Protection`, `Hash Function`, `Digital Signature`, `Key Agreement`, `Session Key Derivation` |
| protocol | `TLS 1.2`, `TLS 1.3`, `DTLS 1.2`, `DTLS 1.3`, `EAP-TLS`, `EAP-TTLS`, `QUIC`, `MPQUIC`, `MIKEY-SAKKE`, `IKEv2`, `IPsec ESP`, `EAP-AKA'`, `5G-AKA`, `MOBIKE`, `OCSP`, `PRINS` |
| securityConstruct | `ECIES`, `PKI`, `COSE`, `PDCP security`, `NAS security`, `KDF`, `JWE`, `JWS`, `OAuth 2.0` |
| securityConstructType | `cryptographic-scheme`, `trust-framework`, `security-format`, `layer-security-function`, `cryptographic-function`, `authorization-framework` |
| bindingType | `reference-point`, `nf-service-interface`, `protocol-based-interface`, `application-interface`, `internal-interface`, `other` |
| 3gppRelease | `Rel-15`, `Rel-16`, `Rel-17`, `Rel-18`, `Rel-19` |
| entityType | `AMF`, `SMF`, `UPF`, `AUSF`, `UDM`, `UDR`, `PCF`, `NRF`, `NSSF`, `NEF`, `AF`, `BSF`, `CHF`, `NWDAF`, `SEPP`, `N3IWF`, `gNB-CU`, `gNB-DU`, `gNB`, `ng-eNB`, `UE`, `5G-EIR` |
| nfType *(migration only)* | `AMF`, `SMF`, `UPF`, `AUSF`, `UDM`, `UDR`, `PCF`, `NRF`, `NSSF`, `NEF`, `AF`, `BSF`, `CHF`, `NWDAF`, `SEPP`, `N3IWF`, `gNB-CU`, `gNB-DU`, `gNB`, `ng-eNB`, `UE`, `5G-EIR` |
| nasIntegrityAlgorithm | `NIA0`, `NIA1`, `NIA2`, `NIA3` |
| nasConfidentialityAlgorithm | `NEA0`, `NEA1`, `NEA2`, `NEA3` |
| upIntegrityAlgorithm | `NIA1`, `NIA2`, `NIA3` |
| suciProtectionScheme | `null-scheme`, `profile-a`, `profile-b` |
| oauthTokenType | `JWT` |
| oauthTokenProtection | `JWS` |
| booleanString | `true`, `false` |
| pkiRole | `client`, `server`, `ca`, `trust-anchor`, `other`, `unknown` |
| pkiAuthenticationMode | `one-way`, `mutual`, `other`, `unknown` |
| cryptographyClass | `symmetric`, `asymmetric`, `hybrid`, `unknown` |

### Protection-context facets

`protectionContext` is a **multi-valued faceted classification**, not a set of mutually exclusive peer classes. A binding MAY carry multiple values from different facets. The v1.0.0 facets are:

| Facet | Values |
| --- | --- |
| plane | `control-plane`, `user-plane` |
| interface/application context | `api`, `service-based-interface` |
| layer | `application-layer`, `transport` |
| operational context | `signaling`, `roaming` |

The presence of one facet value does not imply or exclude a value from another facet. For example, a binding can legitimately be both `control-plane` and `roaming`. v1.0.0 intentionally defines no unqualified `other` value because it would not identify which facet is being extended; new values require an explicitly classified taxonomy extension.

## Artifact versioning

v1.0.0 distinguishes the ATIS taxonomy version, the ATIS profile version, and the implementation-binding version. These versions can evolve independently.

| Artifact/layer | v1.0.0 identifier | Declaration |
| --- | --- | --- |
| ATIS `atis:telecom5g` taxonomy | `1.0.0` | `atis:telecom5g:taxonomyVersion = 1.0.0` |
| 3GPP 5G Architecture CBOM Profile | `1.0.0` | `atis:telecom5g:profile = 3gpp-5g-arch-cbom/1.0.0` |
| Implementation binding | CycloneDX `1.7` | native `bomFormat` / `specVersion` |

Profile v1.0.0 is compatible with taxonomy v1.0.0 and CycloneDX 1.7. The profile, rather than version-number equality, defines compatibility.

Taxonomy/profile versions use Semantic Versioning 2.0.0. The semantic version of this release is `1.0.0`; a leading `v` in a filename or source-control tag is not part of the version. Version `1.0.0` is the first stable release in this version line.

## Metadata properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:profile` | Identifies the ATIS 5G CBOM profile and version claimed by this BOM. | enum: `3gpp-5g-arch-cbom/1.0.0` | MUST appear once | `metadata` |
| `atis:telecom5g:taxonomyVersion` | Identifies the ATIS telecom5g taxonomy version used by this BOM, independently of profile and CycloneDX binding versions. | enum: `1.0.0` | MUST appear once | `metadata` |
| `atis:telecom5g:cbom.scope` | Declares whether the CBOM represents vendor capability or deployment-specific posture. Strict v1.0.0 requires exactly one value. | enum: `vendor`, `deployed` | MUST appear once | `metadata` |
| `atis:telecom5g:baselineRelease` | BOM-level default 3GPP architecture/specification release for represented entities and bindings unless an object supplies `3gppSpecRelease`. | enum: `Rel-15`, `Rel-16`, `Rel-17`, `Rel-18`, `Rel-19` | MAY appear once | `metadata` |
| `atis:telecom5g:inventoryBaseline` | Specific cryptographic inventory baseline used by the profile or producer. | enum: `3GPP TR 33.938 V19.2.0` | SHOULD appear once | `metadata` |
| `atis:telecom5g:inventoryCompleteness` | Scope-relative producer assertion about completeness of the explicitly rooted telecom cryptographic inventory scope. `complete` does not imply a negative assertion for absent values. | enum: `complete`, `partial`, `unknown` | SHOULD appear once | `metadata` |
| `atis:telecom5g:inventoryScopeRef` | `bom-ref` of a represented entity or reified binding that forms an explicit inventory-scope root. At least one is required when `inventoryCompleteness=complete`. | string | MAY appear multiple times; MUST appear at least once when complete | `metadata` |
| `atis:telecom5g:scenario` | Architecture scenario target, e.g., TS23.501-roaming. | string | MAY appear once | `metadata` |

## Entity / NF and binding properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:entityType` | 3GPP 5GS entity or Network Function type represented by the CBOM. The name intentionally includes non-NF entities such as UE, gNB, and ng-eNB. Where applicable, cryptographic usage for that entity is aligned with TR 33.938. | enum: `AMF`, `SMF`, `UPF`, `AUSF`, `UDM`, `UDR`, `PCF`, `NRF`, `NSSF`, `NEF`, `AF`, `BSF`, `CHF`, `NWDAF`, `SEPP`, `N3IWF`, `gNB-CU`, `gNB-DU`, `gNB`, `ng-eNB`, `UE`, `5G-EIR` | MAY appear once | `service`, `component` |
| `atis:telecom5g:nfType` | Deprecated compatibility alias for `atis:telecom5g:entityType`. **MUST NOT appear in a strict v1.0.0 CBOM.** | enum: `AMF`, `SMF`, `UPF`, `AUSF`, `UDM`, `UDR`, `PCF`, `NRF`, `NSSF`, `NEF`, `AF`, `BSF`, `CHF`, `NWDAF`, `SEPP`, `N3IWF`, `gNB-CU`, `gNB-DU`, `gNB`, `ng-eNB`, `UE`, `5G-EIR` | MUST NOT appear in strict v1.0.0 | `service`, `component` |
| `atis:telecom5g:3gppSpecRelease` | Object-level 3GPP release for the entity or binding; when present it explicitly overrides metadata `baselineRelease` for that object. | enum: `Rel-15`, `Rel-16`, `Rel-17`, `Rel-18`, `Rel-19` | MAY appear once | `service`, `component` |
| `atis:telecom5g:nf.name` | Canonical NF identifier when native service/component name is not canonical. NF-scoped only; subject MUST be classified as an NF. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:nf.type` | Optional NF category, e.g., SBA, Access, UserPlane, RoamingSecurity. NF-scoped only; subject MUST be classified as an NF. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:nf.role` | Optional NF architecture role hint, e.g., control-plane, user-plane, security-edge. NF-scoped only; subject MUST be classified as an NF. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:bindingType` | Semantic kind of the modeled 5G architectural binding/interface. | enum: `reference-point`, `nf-service-interface`, `protocol-based-interface`, `application-interface`, `internal-interface`, `other` | MUST appear once per reified binding | `service` |
| `atis:telecom5g:binding` | Canonical 3GPP architectural binding/interface label, e.g., N2, N32-f, Ua, NEF-AF, or Nausf_UEAuthentication. A protocol name such as GTP-C or 5G-AKA is not itself a binding identifier. | string | MUST appear once per reified binding | `service` |
| `atis:telecom5g:interfaces` | Migration-only compatibility summary listing 3GPP reference points supported/exposed by an NF or entity. **MUST NOT appear in a strict v1.0.0 CBOM.** | string pattern: `^[A-Za-z][A-Za-z0-9_.-]*(,[A-Za-z][A-Za-z0-9_.-]*)*$` | MUST NOT appear in strict v1.0.0 | `service`, `component` |
| `atis:telecom5g:interface` | Migration-only compatibility property for a single 3GPP reference point. **MUST NOT appear in a strict v1.0.0 CBOM.** | string pattern: `^[A-Za-z][A-Za-z0-9_.-]*$` | MUST NOT appear in strict v1.0.0 | `service`, `component` |
| `atis:telecom5g:assertion` | Migration-only compatibility qualifier for a crypto statement as supported or effective. **MUST NOT appear in a strict v1.0.0 CBOM.** | enum: `supported`, `effective` | MUST NOT appear in strict v1.0.0 | `service`, `component` |

### Entity-vocabulary source traceability

The `entityType` vocabulary is source-aligned to 3GPP architecture specifications: 5GS core NF/entity labels and UE are derived from 3GPP TS 23.501, while `gNB`, `gNB-CU`, `gNB-DU`, and `ng-eNB` are derived from 3GPP TS 38.401. `5G-EIR` is retained as a valid 5GC NF label even though it is not represented in the TR 33.938 V19.2.0 cryptographic inventory.

### NF-scoped compatibility properties

The legacy `atis:telecom5g:nf.name`, `atis:telecom5g:nf.type`, and `atis:telecom5g:nf.role` properties are valid only for subjects classified as Network Functions. For v1.0.0, the NF-classified `entityType` values are: `AMF`, `SMF`, `UPF`, `AUSF`, `UDM`, `UDR`, `PCF`, `NRF`, `NSSF`, `NEF`, `AF`, `BSF`, `CHF`, `NWDAF`, `SEPP`, `N3IWF`, and `5G-EIR`. They MUST NOT be used as generic properties of `UE`, `gNB`, `gNB-CU`, `gNB-DU`, or `ng-eNB`. The deprecated `nfType` alias is documented for migration only and is prohibited in strict v1.0.0 conformance.

### Strict conformance and semantic subject placement

Strict v1.0.0 rejects deprecated `nfType`, `interface`, `interfaces`, `assertion`, `usageContext`, and legacy dotted `iface.*` syntax. Conversion and diagnostic handling for earlier drafts is non-normative and is documented separately in `MIGRATION_GUIDE.md`.

Semantic roles are determined from ATIS/native properties, not from `bom-ref` prefixes. In strict v1.0.0:

- binding-semantic properties apply only to a reified binding service carrying exactly one `bindingType` and one `binding`;
- service-level `securityConstruct` is a binding summary; component-level `securityConstruct` identifies a referencable construct and MUST be paired with `securityConstructType`;
- component-level `cryptoUsageType` requires a native cryptographic algorithm asset, while service-level use is binding-summary only; and
- `crypto.supported*` properties require an `entityType`-classified subject; and
- `cryptographyClass` requires a native cryptographic algorithm/construction component.

When an architectural binding/interface is represented using this profile, it MUST be represented as a reified CycloneDX service carrying exactly one `bindingType` and one `binding`. Every such reified binding service MUST have a `bom-ref` and MUST be a direct `dependsOn` target of at least one represented `entityType`-classified subject in the same CBOM. v1.0.0 requires at least one represented entity association but does not require both architectural endpoints.

### 3GPP release precedence

`baselineRelease` is the BOM-level default. `3gppSpecRelease`, when present on an entity or binding, overrides that default for that object. Different values are therefore permitted and are not inherently contradictory; consumers use the object-level value first and otherwise inherit the BOM default when needed.

### Canonical binding registry (v1.0.0 initial set)

`binding` remains extensible, but known ATIS binding identifiers MUST use the canonical spelling below. A producer MUST NOT use a spelling variant that is semantically equivalent to a registered identifier. Values not covered by this initial registry remain permitted.

| Canonical binding | `bindingType` | Source traceability |
| --- | --- | --- |
| `N1` | `reference-point` | 3GPP TS 23.501 |
| `N2` | `reference-point` | 3GPP TS 23.501 |
| `N3` | `reference-point` | 3GPP TS 23.501 |
| `N4` | `reference-point` | 3GPP TS 23.501 |
| `N6` | `reference-point` | 3GPP TS 23.501 |
| `N9` | `reference-point` | 3GPP TS 23.501 |
| `N11` | `reference-point` | 3GPP TS 23.501 |
| `N12` | `reference-point` | 3GPP TS 23.501 |
| `N15` | `reference-point` | 3GPP TS 23.501 |
| `N22` | `reference-point` | 3GPP TS 23.501 |
| `N32` | `reference-point` | 3GPP TS 23.501 |
| `N32-c` | `reference-point` | 3GPP TS 33.501 |
| `N32-f` | `reference-point` | 3GPP TS 33.501 |
| `Xn` | `reference-point` | 3GPP TS 38.423 |
| `F1` | `reference-point` | 3GPP TS 38.470 |
| `E1` | `reference-point` | 3GPP TS 38.460 |
| `Ua` | `application-interface` | 3GPP TS 33.220 |
| `NEF-AF` | `application-interface` | TR 33.938 inventory context; TS 29.522 NEF northbound API context |
| `Nausf_UEAuthentication` | `nf-service-interface` | 3GPP TS 29.509 |
| `Nudm_UEAuthentication` | `nf-service-interface` | 3GPP TS 29.503 |

### Canonical security-construct classification

`securityConstructType` is defined only on referencable **components** and MUST match the corresponding `securityConstruct` value.

| `securityConstruct` | Required `securityConstructType` |
| --- | --- |
| `ECIES` | `cryptographic-scheme` |
| `PKI` | `trust-framework` |
| `COSE` | `security-format` |
| `PDCP security` | `layer-security-function` |
| `NAS security` | `layer-security-function` |
| `KDF` | `cryptographic-function` |
| `JWE` | `security-format` |
| `JWS` | `security-format` |
| `OAuth 2.0` | `authorization-framework` |

A service/binding summary MAY carry `securityConstruct`, but it MUST NOT carry `securityConstructType`; type association belongs to the referencable construct component.

## Entity / product capability summary properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:crypto.supportedProtocols` | Vendor capability summary of canonical cryptographic protocols supported by the represented entity/product. | enum: `TLS 1.2`, `TLS 1.3`, `DTLS 1.2`, `DTLS 1.3`, `EAP-TLS`, `EAP-TTLS`, `QUIC`, `MPQUIC`, `MIKEY-SAKKE`, `IKEv2`, `IPsec ESP`, `EAP-AKA'`, `5G-AKA`, `MOBIKE`, `OCSP`, `PRINS` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:crypto.supportedConstructs` | Vendor capability summary of canonical non-protocol security constructs supported by the represented entity/product. | enum: `ECIES`, `PKI`, `COSE`, `PDCP security`, `NAS security`, `KDF`, `JWE`, `JWS`, `OAuth 2.0` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:crypto.supportedCryptography` | Vendor capability summary using noncanonical display/index labels for cryptographic algorithms, suites, or primitives. Each value MUST correspond to a detailed asset; native CycloneDX cryptographic fields are authoritative for normalized interpretation. | string | MAY appear multiple times | `service`, `component` |

### Summary-property authority

The `crypto.supported*`, `protocol`, `securityConstruct`, `cryptography`, `effective*` properties are **summary/index properties**. Where the same information is also represented by native CycloneDX assets and dependency edges, the detailed asset/dependency graph is authoritative for relationships. Summary properties MUST be consistent with the detailed graph but MUST NOT be used to infer associations among independently listed values. `cryptography`, `crypto.supportedCryptography`, and `effectiveCryptography` are intentionally **noncanonical display/index labels**; normalized cross-vendor algorithm comparison MUST use the detailed native CycloneDX cryptographic asset fields rather than the summary strings.

For vendor capability summaries, a declared summary value MUST correspond to a detailed asset/construct represented in the CBOM. Binding-level and effective summary values MUST correspond to a detailed asset/construct reachable from the reified binding. A protocol or algorithm asset that backs these summaries MUST use the applicable native CycloneDX cryptographic-asset representation. A generic dependency edge is not required where it would falsely imply that alternative capabilities are simultaneously required. The absence of such an edge MUST NOT, by itself, be interpreted as an assertion that no dependency or conditional relationship exists.

### Duplicate-fact consistency

Where an ATIS summary/fallback property and a native CycloneDX field represent the same semantic fact, the native detailed representation is authoritative and the ATIS value MUST be consistent with it. Where two ATIS properties directly assert the same fact from different views, they MUST NOT contradict one another. Machine-comparable examples enforced by the v1.0.0 validator include `pki.authenticationMode = mutual` versus `sbi.mutualAuthentication = false`, and selected `keyLength`/`curve` fallback values versus native algorithm parameters.

## Binding and cryptographic semantic properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:securityObjective` | Security objective provided on the binding, kept distinct from operational context and cryptographic usage type. | enum: `Authentication`, `Authorization`, `Confidentiality`, `Integrity`, `ReplayProtection` | MAY appear multiple times | `service` |
| `atis:telecom5g:protectionContext` | Multi-valued faceted operational-context classification. Values from different facets (plane, layer, interface/application context, operational context) MAY coexist and are not mutually exclusive. | enum: `control-plane`, `user-plane`, `api`, `signaling`, `roaming`, `service-based-interface`, `application-layer`, `transport` | MAY appear multiple times | `service` |
| `atis:telecom5g:cryptoUsageType` | TR 33.938-aligned usage type for the represented cryptographic-asset instance. If the same algorithm has materially different usages in different contexts, separate contextual asset instances with distinct `bom-ref` values SHOULD be used. Binding-level use is summary-only. | enum: `Authentication`, `Confidentiality Protection`, `Integrity Protection`, `Hash Function`, `Digital Signature`, `Key Agreement`, `Session Key Derivation` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:protocol` | Canonical telecom-facing protocol label used by the binding. | enum: `TLS 1.2`, `TLS 1.3`, `DTLS 1.2`, `DTLS 1.3`, `EAP-TLS`, `EAP-TTLS`, `QUIC`, `MPQUIC`, `MIKEY-SAKKE`, `IKEv2`, `IPsec ESP`, `EAP-AKA'`, `5G-AKA`, `MOBIKE`, `OCSP`, `PRINS` | MAY appear multiple times | `service` |
| `atis:telecom5g:securityConstruct` | Canonical telecom-facing non-protocol security construct identifier. Prefer a distinct referencable construct asset when graph identity is needed. | enum: `ECIES`, `PKI`, `COSE`, `PDCP security`, `NAS security`, `KDF`, `JWE`, `JWS`, `OAuth 2.0` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:securityConstructType` | Canonical semantic classification of a `securityConstruct` on a referencable construct component. It MUST match the v1.0.0 construct/type table. Binding/service summaries use `securityConstruct` without this property. | enum: `cryptographic-scheme`, `trust-framework`, `security-format`, `layer-security-function`, `cryptographic-function`, `authorization-framework` | MUST appear once per referencable security-construct component | `component` |
| `atis:telecom5g:cryptography` | Noncanonical display/index label for a cryptographic algorithm, suite, or primitive used by the binding. It MUST correspond to a reachable detailed asset; native CycloneDX cryptographic fields are authoritative for normalized interpretation. | string | MAY appear multiple times | `service` |
| `atis:telecom5g:effectiveProtocol` | Protocol known to be active, enforced, negotiated, or directly observed in the deployed binding; mere configuration is insufficient. | enum: `TLS 1.2`, `TLS 1.3`, `DTLS 1.2`, `DTLS 1.3`, `EAP-TLS`, `EAP-TTLS`, `QUIC`, `MPQUIC`, `MIKEY-SAKKE`, `IKEv2`, `IPsec ESP`, `EAP-AKA'`, `5G-AKA`, `MOBIKE`, `OCSP`, `PRINS` | MAY appear multiple times | `service` |
| `atis:telecom5g:effectiveConstruct` | Non-protocol security construct known to be active, enforced, negotiated, or directly observed in the deployed binding; mere configuration is insufficient. | enum: `ECIES`, `PKI`, `COSE`, `PDCP security`, `NAS security`, `KDF`, `JWE`, `JWS`, `OAuth 2.0` | MAY appear multiple times | `service` |
| `atis:telecom5g:effectiveCryptography` | Noncanonical display/index label for an algorithm or suite known to be active, enforced, negotiated, or directly observed in the deployed binding. It MUST correspond to a reachable detailed asset; native CycloneDX cryptographic fields are authoritative for normalized interpretation. | string | MAY appear multiple times | `service` |
| `atis:telecom5g:usageContext` | Migration-only free-form compatibility context. **MUST NOT appear in a strict v1.0.0 CBOM.** | string | MUST NOT appear in strict v1.0.0 | `service`, `component` |

### Contextual cryptographic usage semantics

`cryptoUsageType` describes the usage of the **represented cryptographic-asset instance**. It does not assert that an algorithm family always serves that usage. If one algorithm performs materially different usages in different protocol/binding contexts and the distinction matters, producers SHOULD instantiate separate contextual components with distinct `bom-ref` values. A shared component is appropriate only when the asserted usage set is intended to apply identically in every referencing context.

## Optional summary/fallback crypto and certificate properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:cryptographyClass` | High-level class of the represented native cryptographic algorithm/construction component. `hybrid` denotes one construction deliberately combining cryptographic schemes/classes; mixed algorithms on a binding do not make the binding hybrid. Primitive/function uses native CycloneDX `algorithmProperties.primitive`. | enum: `symmetric`, `asymmetric`, `hybrid`, `unknown` | MAY appear once | `component` |
| `atis:telecom5g:keyLength` | Key size in bits when useful as a summary/fallback field. Prefer native CycloneDX fields for cryptographic assets. | string pattern: `^[0-9]+$` | MAY appear once | `service`, `component` |
| `atis:telecom5g:curve` | Elliptic curve identifier when useful as a summary/fallback field. Prefer native CycloneDX fields for cryptographic assets. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:cert.profile` | Certificate profile identifier/reference when native CycloneDX certificate modeling is not available. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:cert.validation` | Certificate validation mechanism summary, e.g., OCSP, CRL. Prefer native CycloneDX certificate objects where detailed data is needed. | string | MAY appear once | `service`, `component` |

### Cryptography summary-label semantics

`cryptography`, `crypto.supportedCryptography`, and `effectiveCryptography` are human-readable display/index labels, not a canonical ATIS algorithm namespace. Producers SHOULD use stable labels, but normalized comparison MUST use native CycloneDX algorithm/protocol fields such as algorithm family, primitive, parameter set, mode, and cipher-suite structure.

## Canonical protocol/native normalization

For canonical protocol labels, the native CycloneDX protocol representation is normative and MUST agree with the ATIS label. Exact mappings include TLS/DTLS versions, IKEv2 (`ike`, version `2`), IPsec ESP (`ipsec`, version `ESP`), EAP-AKA' (`eap-aka-prime`), 5G-AKA (`5g-aka`), PRINS (`prins`), and the `other` representation used for EAP-TLS, EAP-TTLS, MIKEY-SAKKE, MOBIKE, and OCSP. The machine-readable taxonomy contains the complete v1.0.0 mapping.

Selected algorithm display labels used by the conformance examples also have registered native identity constraints. Algorithm labels outside that selected registry remain permitted as noncanonical display/index labels by design; native CycloneDX cryptographic fields, not the strings, are authoritative for normalized comparison.

## Object-scoped provenance for out-of-baseline constructs

A protocol or security construct admitted by this taxonomy/profile outside the declared TR 33.938 inventory baseline MUST identify its authoritative source on the corresponding referencable component using native CycloneDX `externalReferences[]`. For v1.0.0, `PRINS` is the current such protocol and its authoritative source is **3GPP TS 33.501**. If the producer knows the applicable release or version, the reference or associated comment/metadata SHOULD identify it. A BOM-level reference or a reference attached to a different object does not satisfy object-scoped provenance.

## PKI, trust, and standards traceability properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:pki.usage` | High-level indicator that PKI/X.509 is used for the service/binding. Detailed certificate/key material SHOULD use native CycloneDX CBOM structures. | enum: `true`, `false` | MAY appear once | `service`, `component` |
| `atis:telecom5g:pki.role` | High-level PKI role of the subject in scope. Authentication mode is modeled separately. | enum: `client`, `server`, `ca`, `trust-anchor`, `other`, `unknown` | MAY appear once | `service`, `component` |
| `atis:telecom5g:pki.authenticationMode` | Authentication mode for PKI/X.509 use, kept distinct from PKI role. Where it describes the same subject as `sbi.mutualAuthentication`, the two properties MUST be consistent. | enum: `one-way`, `mutual`, `other`, `unknown` | MAY appear once | `service`, `component` |
| `atis:telecom5g:pki.trustAnchor` | Trust anchor identifier or label when needed for operational context. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:trust.domain` | Trust domain/zone classification, e.g., access, core, inter-PLMN. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:trust.boundary` | Boolean-like indicator that the service/binding sits at a trust boundary. | enum: `true`, `false` | MAY appear once | `service`, `component` |
| `atis:telecom5g:spec.primary` | Primary 3GPP specification reference when native CycloneDX externalReferences cannot be used. | string | MAY appear once | `service`, `component` |
| `atis:telecom5g:spec.crypto` | Crypto-specific specification reference when native CycloneDX externalReferences cannot be used. | string | MAY appear multiple times | `service`, `component` |

## 5G-specific supporting properties

| Property | Description | Value type | Cardinality | Property of |
| --- | --- | --- | --- | --- |
| `atis:telecom5g:nasIntegrityAlgorithm` | NAS integrity algorithm identifier. | enum: `NIA0`, `NIA1`, `NIA2`, `NIA3` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:nasConfidentialityAlgorithm` | NAS confidentiality algorithm identifier. | enum: `NEA0`, `NEA1`, `NEA2`, `NEA3` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:upIntegrityAlgorithm` | User-plane integrity algorithm identifier where UP integrity is used/activated. | enum: `NIA1`, `NIA2`, `NIA3` | MAY appear multiple times | `service`, `component` |
| `atis:telecom5g:suciProtectionScheme` | SUCI protection scheme used for SUPI concealment when applicable. | enum: `null-scheme`, `profile-a`, `profile-b` | MAY appear once | `service`, `component` |
| `atis:telecom5g:sbi.mutualAuthentication` | Indicates whether mutual authentication is required/implemented for SBI. | enum: `true`, `false` | MAY appear once | `service`, `component` |
| `atis:telecom5g:oauthTokenType` | NF access token type used for SBI authorization. | enum: `JWT` | MAY appear once | `service`, `component` |
| `atis:telecom5g:oauthTokenProtection` | Protection mechanism used for an OAuth/JWT access token in the 3GPP profile. | enum: `JWS` | MAY appear once | `service`, `component` |

## Deployment/effective semantics

`cbom.scope = deployed` identifies a deployment-specific CBOM; it does not by itself claim that every listed item is active. `effectiveProtocol`, `effectiveConstruct`, and `effectiveCryptography` are reserved for values known to be active, enforced, negotiated, or directly observed. Mere configuration/provisioning is insufficient. A deployed CBOM carrying any `effective*` assertion MUST include native CycloneDX `metadata.timestamp`, and for this profile that timestamp is the **as-of time of the effective-state snapshot**, not merely document-generation time. If effective assertions do not share the same as-of time, they SHOULD be represented in separate snapshots until a structured evidence/time model exists. A vendor-scope CBOM MUST NOT carry `effective*`.

## Cryptography class vs primitive

v1.0.0 removes the overloaded v0.95 `atis:telecom5g:cryptoType`. `atis:telecom5g:cryptographyClass` applies only to a native cryptographic algorithm/construction component and captures the high-level class `symmetric`, `asymmetric`, `hybrid`, or `unknown`. `hybrid` means that the represented construction itself combines cryptographic schemes/classes; simply having both symmetric and asymmetric algorithms in a protocol or binding does not make it hybrid. Algorithm primitive/function (for example `hash`, `mac`, `signature`, `kdf`, `key-agree`, or `ae`) SHOULD use native CycloneDX `cryptoProperties.algorithmProperties.primitive`.

## Entity-model scope

`entityType` classifies the represented 3GPP entity; it does not determine the native CycloneDX object kind. NFs are preferably modeled as `services[]`; non-NF entities such as UE or gNB MAY be represented as services or components according to the native CycloneDX semantics of the object being described.

## Reified-binding entity association

Every reified binding service MUST have a `bom-ref` and MUST be directly associated from at least one represented entity through CycloneDX `dependencies[]`: an entity subject's `dependsOn` set includes the binding `bom-ref`. v1.0.0 requires at least one such entity association and does not require both architectural endpoints to be represented.

## Legacy dotted per-interface migration syntax

Dotted `atis:telecom5g:iface.*` syntax is retained only to identify legacy input and is **prohibited in strict v1.0.0 conformance**. Informative conversion guidance is provided in `MIGRATION_GUIDE.md`.

| Pattern | Description | Value type | Property of |
| --- | --- | --- | --- |
| `^atis:telecom5g:iface\.[A-Za-z][A-Za-z0-9_.-]*\.(securityObjective\|protectionContext\|cryptoUsageType\|protocol\|securityConstruct\|cryptography\|effectiveProtocol\|effectiveConstruct\|effectiveCryptography\|usageContext\|standardRefs)$` | Migration-only compact per-interface syntax; MUST NOT appear in a strict v1.0.0 CBOM. | `string` | `service`, `component` |
| `^atis:telecom5g:iface\.[A-Za-z][A-Za-z0-9_.-]*\.cert\.(keyType\|keyLength\|curve\|validation)$` | Migration-only compact per-interface certificate summary properties; MUST NOT appear in a strict v1.0.0 CBOM. | `string` | `service`, `component` |


## Absence and completeness semantics

For a vendor CBOM, the absence of a protocol, security construct, algorithm, or other capability **MUST NOT** be interpreted as an assertion that the capability is unsupported. Absence means **not declared**.

`inventoryCompleteness` is interpreted relative to mandatory `cbom.scope` and explicit `inventoryScopeRef` roots, together with declared scenario/release qualifiers; it does **not** assert coverage of the entire 5G System. When `complete`, at least one scope root MUST reference a represented entity or reified binding.

The **inventory scope closure** is the least fixed-point set formed by: (1) the declared roots; (2) all objects transitively reachable from included objects through CycloneDX `dependsOn`; and (3) every detailed protocol, security-construct, or cryptographic asset required to back an ATIS supported, binding-level, or effective summary on an included entity/binding, even when an edge was intentionally omitted to avoid false conjunctive semantics. If multiple detailed objects match the same in-scope summary value and no narrower graph association identifies one backing instance, all matching objects are included. Dependency traversal and summary-backed inclusion are repeated until no new object is added. Objects elsewhere in the BOM are not in scope merely because they are present.

- For `vendor`, `complete` means all known in-scope positive supported-capability declarations are included.
- For `deployed`, `complete` means all known in-scope positive deployment-specific cryptographic declarations represented by the BOM are included.
- `partial` means known in-scope declarations can be omitted; `unknown` means completeness has not been determined.

Even when the value is `complete`, absence does not become an explicit `unsupported`, `not configured`, or `not used` assertion. CycloneDX native `compositions.aggregate` SHOULD be used for completeness of referenced assemblies/dependency relationships.

### Dependency-edge absence semantics

A present CycloneDX `dependsOn` edge asserts a generic dependency. The absence of an edge MUST NOT, by itself, be interpreted as an assertion of non-dependency. An edge can be intentionally omitted when the generic relation cannot represent alternative, conditional, or choice semantics without falsely asserting simultaneous/conjunctive dependency.
