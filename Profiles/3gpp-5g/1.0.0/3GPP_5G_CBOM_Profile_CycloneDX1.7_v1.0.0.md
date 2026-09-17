# 3GPP 5G Architecture CBOM Profile for CycloneDX 1.7 (Version 1.0.0)

## 1. Scope and inventory baseline

This profile defines interoperable modeling expectations for a **3GPP 5G Architecture CBOM** using **CycloneDX 1.7** and the ATIS `atis:telecom5g` property taxonomy v1.0.0.

This is a **profile of CycloneDX 1.7**, not a replacement schema. CBOMs claiming this profile MUST validate against the official CycloneDX 1.7 BOM schema and against the ATIS v1.0.0 overlay/validation rules.

The cryptographic inventory baseline for this profile is **3GPP TR 33.938 V19.2.0 (Release 19)**. This baseline governs the cryptographic inventory represented by the profile; it is **not** the source vocabulary for every 5G architectural entity or binding. Protocols or security constructs admitted outside that cryptographic-inventory baseline MAY be represented only with the object-scoped provenance required by this profile.

## 2. Conformance keywords

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119 / RFC 8174 when, and only when, they appear in all capitals. Lower-case modal verbs are descriptive and are not conformance keywords.

## 3. References

### 3.1 Normative references

The following documents are indispensable for application of this profile. For dated references, the cited edition applies.

- **[CDX-1.7]** CycloneDX Specification 1.7, JSON serialization and official JSON schema bundle, including `bom-1.7.schema.json`: https://cyclonedx.org/docs/1.7/json/
- **[RFC2119]** S. Bradner, *Key words for use in RFCs to Indicate Requirement Levels*, BCP 14, RFC 2119, March 1997: https://www.rfc-editor.org/info/rfc2119
- **[RFC8174]** B. Leiba, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*, BCP 14, RFC 8174, May 2017: https://www.rfc-editor.org/info/rfc8174
- **[3GPP-TR33938]** 3GPP TR 33.938 V19.2.0, *3GPP Cryptographic Inventory*, Release 19.
- **[3GPP-TS33501]** 3GPP TS 33.501, *Security architecture and procedures for 5G System*.
- **[SEMVER]** *Semantic Versioning 2.0.0*: https://semver.org/

### 3.2 Architecture-vocabulary source references (informative)

The following specifications provide source traceability for architecture/entity/binding labels used by this profile. The canonical spelling and ATIS classification defined by the profile/taxonomy remain normative; this subsection does not import unrelated requirements from the cited specifications.

- **[3GPP-TS23501]** 3GPP TS 23.501, *System architecture for the 5G System (5GS)*.
- **[3GPP-TS38401]** 3GPP TS 38.401, *NG-RAN; Architecture description*.
- **[3GPP-TS38423]** 3GPP TS 38.423, *NG-RAN; Xn Application Protocol (XnAP)*.
- **[3GPP-TS38470]** 3GPP TS 38.470, *NG-RAN; F1 general aspects and principles*.
- **[3GPP-TS38460]** 3GPP TS 38.460, *NG-RAN; E1 general aspects and principles*.
- **[3GPP-TS33220]** 3GPP TS 33.220, *Generic Authentication Architecture (GAA); Generic Bootstrapping Architecture (GBA)*.
- **[3GPP-TS29522]** 3GPP TS 29.522, *5G System; Network Exposure Function Northbound APIs; Stage 3*.
- **[3GPP-TS29509]** 3GPP TS 29.509, *5G System; Authentication Server Services; Stage 3*.
- **[3GPP-TS29503]** 3GPP TS 29.503, *5G System; Unified Data Management Services; Stage 3*.

## 4. Terms and definitions

For this profile, the following terms apply. Terms defined by CycloneDX retain their CycloneDX meanings unless this profile explicitly specializes them.

**architectural binding/interface**: named architectural connection, reference point, NF service interface, protocol-based interface, application interface, or internal interface represented by the paired `binding` and `bindingType` properties.

**effective state**: deployment-specific cryptographic state known to be active, enforced, negotiated, or directly observed at the `metadata.timestamp` as-of time. Configuration or permission alone is not effective state.

**inventory scope root**: represented entity or reified binding whose `bom-ref` is named by `atis:telecom5g:inventoryScopeRef`.

**inventory scope closure**: least fixed-point set derived from one or more inventory scope roots according to Clause 9.1.1.

**reified binding**: CycloneDX `service` object used by this profile to give an architectural binding/interface a `bom-ref`, ATIS binding properties, and graph identity. Reification is a serialization technique and does not redefine the architectural binding as a network service.

**strict conformance**: conformance established by satisfying both the official CycloneDX 1.7 schema and all normative requirements of this profile and its same-version human-readable ATIS taxonomy, without migration-only properties.

**summary/index property**: ATIS property that provides a searchable or human-readable summary of detailed native CycloneDX content. A summary/index property does not, by itself, preserve pairwise relationships among independently listed values.

**vendor CBOM**: CBOM with `cbom.scope = vendor` describing supported cryptographic capability rather than deployment-effective state.

**deployed CBOM**: CBOM with `cbom.scope = deployed` describing cryptographic state for a specific deployment; only values satisfying the effective-state definition are represented using `effective*` properties.

## 5. Abbreviations

| Abbreviation | Meaning |
|---|---|
| 5GC | 5G Core |
| 5GS | 5G System |
| AF | Application Function |
| AMF | Access and Mobility Management Function |
| AUSF | Authentication Server Function |
| BOM | Bill of Materials |
| CBOM | Cryptography Bill of Materials |
| CRQC | Cryptographically Relevant Quantum Computer |
| GAA | Generic Authentication Architecture |
| GBA | Generic Bootstrapping Architecture |
| HBOM | Hardware Bill of Materials |
| KDF | Key Derivation Function |
| NAF | Network Application Function |
| NEF | Network Exposure Function |
| NF | Network Function |
| NG-RAN | Next Generation Radio Access Network |
| PKI | Public Key Infrastructure |
| PQC | Post-Quantum Cryptography |
| PRINS | Protocol for N32 Interconnect Security |
| QSC | Quantum-Safe Cryptography |
| QSCII | Quantum-Safe Communications and Infrastructure Initiative |
| SBOM | Software Bill of Materials |
| SBI | Service-Based Interface |
| SEPP | Security Edge Protection Proxy |
| TLS | Transport Layer Security |
| TR | Technical Report |
| TS | Technical Specification |
| UDM | Unified Data Management |
| UE | User Equipment |

## 6. Normative artifacts, reference tooling, and precedence

The normative specification consists of this profile together with the human-readable `atis:telecom5g` property taxonomy for the same profile version. This profile is authoritative for profile-level modeling, conformance, graph, scope, and interpretation rules. The human-readable taxonomy is authoritative for ATIS property names, controlled vocabularies, placement, and cardinality.

The machine-readable taxonomy JSON and the strict ATIS overlay schema are conformance artifacts generated from, and required to remain consistent with, those normative texts. If a publication defect causes a machine-readable artifact to conflict with the normative profile or human-readable taxonomy, the normative text controls and the conflict MUST be reported and corrected in a subsequent version; an implementation MUST NOT use the conflicting machine artifact to weaken a normative requirement.

`validate_atis_cbom.py`, `generate_overlay.py`, `normative_audit.py`, `sdo_reviewer_audit.py`, the regression test script, and all example/negative-fixture CBOMs are **reference tooling and informative test material**. They are supplied to support repeatable implementation and QSCII review, but they do not define conformance. An implementation MAY use any validator that establishes the same normative requirements.

## 7. Profile identification

A BOM claiming this profile MUST include `bomFormat = "CycloneDX"`, `specVersion = "1.7"`, exactly one metadata property `atis:telecom5g:profile = "3gpp-5g-arch-cbom/1.0.0"`, exactly one metadata property `atis:telecom5g:taxonomyVersion = "1.0.0"`, and exactly one `atis:telecom5g:cbom.scope = vendor | deployed`.

A BOM SHOULD also include:

- `atis:telecom5g:inventoryBaseline = "3GPP TR 33.938 V19.2.0"`; and
- `atis:telecom5g:inventoryCompleteness = complete | partial | unknown`.

When the 3GPP release assumed for the represented architecture or product is known, the BOM SHOULD include `atis:telecom5g:baselineRelease`.

When `inventoryCompleteness = complete`, the BOM MUST include at least one metadata `atis:telecom5g:inventoryScopeRef` identifying a represented entity or reified binding that forms an explicit scope root.

The TR version and the represented 3GPP architecture release are distinct. A Rel-17 product, for example, can be described using the v1.0.0 profile whose inventory baseline is TR 33.938 V19.2.0.

### 7.1 Independent artifact versioning

v1.0.0 explicitly distinguishes three independently versioned artifacts/layers:

| Artifact/layer | v1.0.0 identifier | How a CBOM declares it |
|---|---|---|
| ATIS property taxonomy | `1.0.0` | `atis:telecom5g:taxonomyVersion = "1.0.0"` |
| ATIS 5G CBOM profile | `1.0.0` | `atis:telecom5g:profile = "3gpp-5g-arch-cbom/1.0.0"` |
| Implementation binding | CycloneDX `1.7` | native `bomFormat = "CycloneDX"`, `specVersion = "1.7"` |

These versions are **not semantically required to advance in lockstep**. Profile v1.0.0 is compatible with taxonomy v1.0.0 and the CycloneDX 1.7 implementation binding. A future taxonomy revision can be compatible with an unchanged profile, and a future profile can declare compatibility with more than one taxonomy version. The native CycloneDX `specVersion` remains authoritative for the implementation-binding version; ATIS does not duplicate that value in another property.

ATIS profile and taxonomy versions use **Semantic Versioning 2.0.0** [SEMVER]. The version value of this release is `1.0.0`; a leading `v` used in filenames or source-control tags is presentation syntax and is not part of the Semantic Version. Version `1.0.0` is the first stable release in this version line.


### 7.2 Strict conformance

A CBOM claiming strict v1.0.0 conformance **MUST NOT contain deprecated ATIS properties or legacy dotted `iface.*` syntax**. Handling and conversion of artifacts from earlier drafts is outside strict conformance and is described only in the informative `MIGRATION_GUIDE.md` supplied with the reference package.

Semantic object roles are determined by ATIS/native properties, not by `bom-ref` naming conventions. Recommended `bom-ref` patterns remain identifiers only and MUST NOT be used as hidden semantic type discriminators.

## 8. Taxonomy vs profile

The **taxonomy** defines reusable ATIS property names, controlled vocabularies, and placement. This **profile** selects and constrains those terms, defines modeling and conformance rules, uses native CycloneDX structures for cryptographic assets and dependency graphs, and defines how the heterogeneous TR 33.938 Protocol/Function inventory is represented.

The taxonomy is not, by itself, an implementation-independent information model.

## 9. Vendor vs deployed CBOM semantics

### 9.1 Vendor CBOM

A vendor CBOM (`atis:telecom5g:cbom.scope = vendor`) describes what a represented entity or product **supports**. Supported capability MUST NOT be interpreted as evidence that the cryptography is enabled, negotiated, or active in a deployment.

Vendor CBOMs SHOULD use:

- `atis:telecom5g:crypto.supportedProtocols`;
- `atis:telecom5g:crypto.supportedConstructs`; and
- `atis:telecom5g:crypto.supportedCryptography`.

#### 9.1.1 Meaning of absence and completeness

The absence of a protocol, security construct, algorithm, or capability from a vendor CBOM **MUST NOT** be interpreted as `unsupported`. Absence means only **not declared**.

v1.0.0 intentionally does not define a flat `capabilityStatus` property. A single status attached to a service/component cannot unambiguously qualify multiple individual capabilities. Explicit negative capability assertions are therefore deferred until a structured assertion model is defined.

`atis:telecom5g:inventoryCompleteness` is **scope-relative**. Explicit scope roots are declared with metadata `atis:telecom5g:inventoryScopeRef`, whose value is the `bom-ref` of a represented entity or reified binding. If `inventoryCompleteness = complete`, at least one such scope root is mandatory.

For this profile, the **inventory scope closure** of the declared roots is the least fixed-point set obtained as follows:

1. include every object named by an `inventoryScopeRef`;
2. include every object transitively reachable from an included object through CycloneDX `dependencies[].dependsOn`;
3. for every included entity or reified binding that carries an ATIS supported, binding-level, or effective summary, include every detailed protocol, security-construct, or cryptographic asset required by Clause 9.3 to back that summary, even when a generic dependency edge was intentionally omitted to avoid falsely representing alternative or conditional capability as conjunctive. If more than one detailed object in the BOM matches the same in-scope summary value and no narrower graph association distinguishes the backing instance, all matching detailed objects are included;
4. recursively apply steps 2 and 3 to newly included objects until no additional object is added.

An object is not part of the inventory scope closure merely because it is present elsewhere in the same BOM. Completeness is evaluated against this closure together with any declared scenario/release qualifiers; it does not assert coverage of the entire 5G System. This definition preserves the profile's open-world dependency semantics while preventing deliberately edge-less alternative capabilities from falling outside a declared completeness boundary.

For a vendor CBOM:

- `complete`: all known in-scope **positive supported-capability declarations** are included;
- `partial`: known in-scope declarations can be omitted; and
- `unknown`: completeness has not been determined.

For a deployed CBOM, `complete` means that all known in-scope **positive deployment-specific cryptographic declarations represented by that BOM** are included.

In either scope, `complete` does **not** convert an absent declaration into an `unsupported`, `not configured`, or `not used` assertion.

CycloneDX native `compositions.aggregate` SHOULD be used for completeness of referenced assemblies and dependency relationships. ATIS `inventoryCompleteness` is narrower and describes completeness of the telecom cryptographic inventory declarations made under this profile.

#### 9.1.2 Linking companion SBOM/HBOM artifacts

When a companion SBOM, HBOM, or other BOM artifact exists and is intended to be associated with the vendor CBOM, the vendor CBOM SHOULD link to it using native CycloneDX **top-level** `externalReferences[]` with `type = "bom"`. Where the referenced artifact is a CycloneDX BOM with a BOM identifier, the `url` SHOULD use the corresponding CycloneDX **BOM-Link** URN.

An ATIS-specific property SHOULD NOT be defined for this purpose when the native CycloneDX mechanism is sufficient.

### 9.2 Deployed CBOM

A deployed CBOM (`atis:telecom5g:cbom.scope = deployed`) describes **deployment-specific cryptographic state**. It MAY contain configuration information. It MAY contain effective-state assertions only when the asserted values satisfy the effective-state criteria in the following paragraph.

The `effective*` properties are reserved for a protocol, construct, algorithm, or suite known to be **active, enforced, negotiated, or directly observed** in the represented deployment. A value that is merely configured, provisioned, or permitted **MUST NOT** be labeled `effective` without evidence that it is active/effective in that deployment.

When a deployed CBOM declares effective protocol, security-construct, or cryptographic-algorithm state using ATIS summary properties, it SHOULD use the corresponding property:

- `atis:telecom5g:effectiveProtocol`;
- `atis:telecom5g:effectiveConstruct`; or
- `atis:telecom5g:effectiveCryptography`.

A deployed CBOM containing any `effective*` assertion **MUST** include native CycloneDX `metadata.timestamp`. For this profile, that timestamp is the **as-of time of the effective-state snapshot**, not merely the time at which the CBOM document was serialized or emitted. If two effective assertions do not share the same as-of time, producers SHOULD emit them in separate CBOM snapshots until a structured assertion/evidence-time model is defined.

A vendor-scope CBOM **MUST NOT** contain `effective*` properties. A deployed CBOM MAY include `crypto.supported*` summaries as supplemental product-capability context, but supported capability MUST NOT be interpreted as effective deployment state.

### 9.3 Summary properties and graph authority

ATIS `crypto.supported*`, `protocol`, `securityConstruct`, `cryptography`, and `effective*` properties are summary/index properties. They improve inventory search and canonical lookup for controlled ATIS vocabularies, but they do not preserve all associations among listed values. In particular, `cryptography`, `crypto.supportedCryptography`, and `effectiveCryptography` are **noncanonical display/index labels**: their strings MUST NOT be treated as canonical cross-vendor algorithm identifiers. Native CycloneDX cryptographic-asset fields are authoritative for normalized algorithm/suite interpretation.

Where corresponding native CycloneDX assets and dependency edges are present, the **detailed asset/dependency graph is authoritative for relationships**. Summary properties MUST be consistent with that graph and MUST NOT be used to infer that independently listed values are related to one another.

For vendor capability summaries, each declared protocol, security construct, or cryptographic algorithm MUST have a corresponding detailed asset/construct in the CBOM. A dependency edge MAY be omitted when the candidate edge would represent mutually exclusive or conditional alternatives as simultaneously required dependencies.

For binding-level `protocol`, `securityConstruct`, `cryptography`, and `effective*` summaries, each declared value MUST correspond to a detailed asset/construct reachable from that reified binding through the dependency graph.

### 9.4 Duplicate-fact consistency and authority

Where an ATIS summary/fallback property and a native CycloneDX field represent the same semantic fact, the **native detailed representation is authoritative** and the ATIS value MUST be consistent with it. This rule extends the graph-authority principle to duplicate facts such as algorithm parameters or certificate/PKI summaries.

Where two ATIS properties directly assert the same fact from different views, they MUST NOT contradict one another. For example, `pki.authenticationMode = mutual` is inconsistent with `sbi.mutualAuthentication = false` on the same represented subject. The supplied validator enforces machine-comparable cases; producers remain responsible for consistency where equivalent facts cannot be mechanically compared.

## 10. Modeling 5G entities and architectural bindings

### 10.1 Entities, NFs, and reified bindings

5G Network Functions SHOULD be represented as top-level CycloneDX `services[]` objects. Other `entityType` values, such as UE or gNB, MAY be represented as a CycloneDX service or component according to the semantics of the native CycloneDX object being described; `entityType` itself **does not determine** whether the object is a CycloneDX service or component.

A producer MAY omit architectural bindings that are outside the declared inventory scope. **When an architectural binding/interface is represented using this profile, it MUST be reified as a CycloneDX service** so that it has a `bom-ref` and can carry ATIS properties and dependency edges. The reified binding MUST have a `bom-ref` and MUST carry exactly one `atis:telecom5g:bindingType` and exactly one `atis:telecom5g:binding`. Every reified binding MUST be directly associated in the dependency graph with at least one represented `entityType`-classified subject in the same CBOM: at least one represented entity MUST list the binding's `bom-ref` in its `dependsOn` set. v1.0.0 does not require both architectural endpoints to be modeled. This reification is an **implementation-binding technique** and MUST NOT be interpreted as redefining the conceptual 3GPP binding/interface as a network service.

Recommended `bom-ref` patterns are:

- NF service: `nf:<NF_NAME>`;
- non-NF entity when a profile-specific referencable identifier is useful: `entity:<ENTITY_TYPE>[:<INSTANCE>]`;
- binding object: `binding:nf:<NF_NAME>:<BINDING>[:<SCOPE>]`.

Examples include `nf:AMF`, `binding:nf:AMF:N2`, and `binding:nf:SEPP:N32-f:deployed`.

### 10.2 NF identity

When a represented NF has a canonical 3GPP NF label, the NF service `name` SHOULD use that label, e.g., `AMF`, `SMF`, `UPF`, or `SEPP`. If the native service name is instead a vendor product label, producers MAY add `atis:telecom5g:nf.name` and `atis:telecom5g:entityType` to preserve the canonical NF identity.

`entityType` is the preferred 3GPP 5GS entity/NF vocabulary. It intentionally includes non-NF entities such as `UE`, `gNB`, and `ng-eNB`; it is not defined solely by TR 33.938. The older `nfType` property is retained only as a documented migration alias and is prohibited by strict v1.0.0 conformance. Informative conversion guidance for earlier drafts is provided separately in `MIGRATION_GUIDE.md`.

The supplemental `atis:telecom5g:nf.name`, `atis:telecom5g:nf.type`, and `atis:telecom5g:nf.role` properties are **NF-scoped only**. They MUST be used only when the same object is classified by `entityType` (or deprecated `nfType`) as a Network Function according to the taxonomy's NF-classified subset. They MUST NOT be used as generic properties of non-NF entities such as `UE`, `gNB`, `gNB-CU`, `gNB-DU`, or `ng-eNB`.

**5G-EIR note:** `5G-EIR` is a valid 3GPP 5GC Network Function and is retained in `entityType`. It is not currently represented in the TR 33.938 V19.2.0 cryptographic inventory. Its presence in the taxonomy MUST NOT be interpreted as an assertion that TR 33.938 defines cryptographic usage for 5G-EIR.

#### 10.2.1 3GPP release precedence

`atis:telecom5g:baselineRelease` is the BOM-level default release for represented entities and bindings. `atis:telecom5g:3gppSpecRelease`, when present on an entity or binding, is an **explicit object-level override** of that default for that object. A differing object-level value is therefore not inherently contradictory; consumers MUST use `3gppSpecRelease` for that object and otherwise inherit `baselineRelease` when a default is needed.

### 10.3 Generalized binding model

v1.0.0 distinguishes the semantic kind of an **architectural binding/interface** from its identifier. A reified binding MUST include exactly one `atis:telecom5g:bindingType` and exactly one `atis:telecom5g:binding`.

`bindingType` values are:

- `reference-point`;
- `nf-service-interface`;
- `protocol-based-interface`;
- `application-interface`;
- `internal-interface`; and
- `other`.

`binding` carries the architectural binding/interface label, for example `N2`, `N32-f`, `Ua`, `NEF-AF`, or `Nausf_UEAuthentication`.

A protocol or security procedure such as `GTP-C`, `TLS`, or `5G-AKA` MUST NOT be used as the `binding` merely because the source describes a protocol-based interface. Where only a protocol-based interface is named, use `bindingType = protocol-based-interface`, use a source-aligned interface label for `binding`, and model the protocol separately.

#### 10.3.1 Canonical binding names

`binding` remains extensible, but a value covered by the ATIS v1.0.0 canonical binding registry MUST use the registered spelling. Semantically equivalent spelling variants such as `N32f` for `N32-f` or `Nudm-UEAuthentication` for `Nudm_UEAuthentication` are non-conformant.

The initial registry includes: `N1`, `N2`, `N3`, `N4`, `N6`, `N9`, `N11`, `N12`, `N15`, `N22`, `N32`, `N32-c`, `N32-f`, `Xn`, `F1`, `E1`, `Ua`, `NEF-AF`, `Nausf_UEAuthentication`, and `Nudm_UEAuthentication`. The registry is intentionally not exhaustive; other source-aligned binding labels remain permitted.

When a registered binding is used, its `bindingType` MUST also match the registry classification.

The v0.7 `atis:telecom5g:interface`, `interfaces`, `assertion`, `usageContext`, deprecated `nfType`, and compact dotted `iface.*` forms are migration-only syntax and are **prohibited in strict v1.0.0 conformance**.

#### 10.3.2 Architecture-vocabulary source traceability

The canonical ATIS spelling and `bindingType` classification in this profile are normative. The following 3GPP specifications identify the architectural or service-interface source from which the profile vocabulary is derived. An ATIS classification such as `application-interface` is a profile classification and need not be terminology used by the cited 3GPP specification.

| ATIS vocabulary | Source specification | Traceability note |
|---|---|---|
| 5GC NF/entity labels, UE, and `N1`, `N2`, `N3`, `N4`, `N6`, `N9`, `N11`, `N12`, `N15`, `N22`, `N32` | [3GPP-TS23501] | 5GS architecture and reference-point vocabulary |
| `gNB`, `gNB-CU`, `gNB-DU`, `ng-eNB` | [3GPP-TS38401] | NG-RAN architecture/entity vocabulary |
| `N32-c`, `N32-f` | [3GPP-TS33501] | SEPP/inter-PLMN security-specific N32 control/forwarding usage |
| `Xn` | [3GPP-TS38423] | Xn application-protocol/interface vocabulary |
| `F1` | [3GPP-TS38470] | F1 general aspects and principles |
| `E1` | [3GPP-TS38460] | E1 general aspects and principles |
| `Ua` | [3GPP-TS33220] | GBA reference point between UE and NAF |
| `NEF-AF` | [3GPP-TR33938], [3GPP-TS29522] | ATIS source-aligned descriptive label for the NEF/AF application exposure context; it is not asserted to be a formal 3GPP `Nxx` reference-point name |
| `Nausf_UEAuthentication` | [3GPP-TS29509] | AUSF UE Authentication service/API |
| `Nudm_UEAuthentication` | [3GPP-TS29503] | UDM UE Authentication service |

Source traceability does not make the registry closed. A binding label outside the registry remains permitted as specified in Clause 10.3.1, but its producer is responsible for using a source-aligned identifier and appropriate `bindingType`.

### 10.3.3 Semantic subject placement

Strict v1.0.0 constrains properties by the semantic subject they describe:

- `bindingType`, `binding`, `securityObjective`, `protectionContext`, `protocol`, `cryptography`, and all `effective*` summaries apply only to a reified binding service;
- `securityConstruct` MAY identify a referencable construct component or summarize a reified binding, but a service-level value requires a binding service;
- `cryptoUsageType` MAY occur on a native cryptographic algorithm component or as an explicit binding summary; and
- `crypto.supportedProtocols`, `crypto.supportedConstructs`, and `crypto.supportedCryptography` apply only to an `entityType`-classified subject; and
- `cryptographyClass` applies only to a native cryptographic algorithm/construction component, never to an entity, protocol, or binding summary.

These semantic roles MUST be inferred from the properties/native structures themselves, never from `bom-ref` prefixes.

### 10.4 Security objective, protection context, and cryptographic usage type

v1.0.0 separates concepts that were conflated by v0.7 `cryptoFunction`:

- `securityObjective` describes **why** protection exists: `Authentication`, `Authorization`, `Confidentiality`, `Integrity`, or `ReplayProtection`;
- `protectionContext` provides **multi-valued faceted context tags** describing where/in what operational context protection applies; and
- `cryptoUsageType` describes **what cryptographic feature/function** is performed, using the TR 33.938-aligned vocabulary such as `Hash Function`, `Digital Signature`, `Key Agreement`, or `Session Key Derivation`.

These properties are not interchangeable.

`protectionContext` values are **not mutually exclusive peers**. They come from different contextual facets: plane (`control-plane`, `user-plane`), interface/application context (`api`, `service-based-interface`), layer (`application-layer`, `transport`), and operational context (`signaling`, `roaming`). A binding MAY carry multiple values from different facets; for example, `control-plane` and `roaming` can both apply. v1.0.0 intentionally defines no unqualified `other` protection-context value because such a value would not identify which facet is being extended; new context values require an explicitly classified taxonomy extension.

`cryptoUsageType` SHOULD be attached to the cryptographic asset to which the usage applies. It MAY appear on a binding only as a summary. A binding-level `cryptoUsageType` MUST NOT be interpreted as identifying which algorithm performs that function when multiple algorithms are present.

`cryptoUsageType` is **contextual to the represented cryptographic-asset instance**, not a universal statement about the algorithm family. When the same algorithm performs different cryptographic usages in different protocol or binding contexts and those differences need to be preserved, producers SHOULD create separate contextual component instances with distinct `bom-ref` values. A shared algorithm asset MAY be referenced from multiple contexts only when its asserted `cryptoUsageType` set is intended to apply identically in each of those contexts.

## 11. Modeling cryptographic assets and security constructs

### 11.1 Native cryptographic assets

Cryptographic protocols, algorithms, keys, and certificates SHOULD use native CycloneDX 1.7 CBOM structures when the native schema defines a representation for that object type.

A protocol or algorithm asset used as the detailed representation that backs an ATIS `protocol`, `effectiveProtocol`, `crypto.supportedProtocols`, `cryptography`, `effectiveCryptography`, or `crypto.supportedCryptography` summary **MUST** be modeled as a CycloneDX `components[]` object with `type = "cryptographic-asset"` and the appropriate native `cryptoProperties.assetType`. Any other represented object that is semantically a cryptographic protocol or cryptographic algorithm SHOULD use the same native representation.

BOM-level `atis:telecom5g:kdfAlgorithm` is not defined in v1.0.0. KDFs are represented as native cryptographic algorithm assets so multiple contextual KDFs can be modeled without implying one global algorithm.

### 11.1.1 Cryptography class vs cryptographic primitive

The former `atis:telecom5g:cryptoType` property mixed two independent dimensions: high-level cryptography class (`symmetric`, `asymmetric`, `hybrid`) and cryptographic primitive/function (`hash`, `mac`, `signature`, `key-agreement`, etc.). v1.0.0 removes that overloaded property.

`atis:telecom5g:cryptographyClass` MAY be used **only on a native cryptographic algorithm/construction component** for the high-level class `symmetric`, `asymmetric`, `hybrid`, or `unknown`. `hybrid` means that the represented construction itself deliberately combines cryptographic schemes/classes; the mere coexistence of symmetric and asymmetric algorithms within one protocol, binding, entity, or dependency subgraph MUST NOT be labeled `hybrid`. Cryptographic primitive/function **SHOULD use native CycloneDX `cryptoProperties.algorithmProperties.primitive`** (for example `hash`, `mac`, `signature`, `kdf`, `key-agree`, or `ae`). The ATIS class and the native primitive are orthogonal and MUST NOT be treated as substitutes for one another.

#### 11.1.2 Cryptography summary labels

The string values carried by `atis:telecom5g:cryptography`, `atis:telecom5g:crypto.supportedCryptography`, and `atis:telecom5g:effectiveCryptography` are convenience display/index labels. They are intentionally **not a canonical ATIS algorithm vocabulary**. Producers SHOULD choose stable human-readable labels, but consumers performing normalized comparison MUST use the corresponding detailed native CycloneDX cryptographic asset fields (for example algorithm family, primitive, parameter set, mode, and protocol cipher-suite structure) rather than comparing these strings as identifiers.

### 11.2 MILENAGE and TUAK

MILENAGE and TUAK SHOULD be represented as native CycloneDX cryptographic algorithm assets, not as new ATIS algorithm properties. The v1.0.0 UDM/5G-AKA vendor example illustrates native representation of both as supported alternative capabilities.

Because CycloneDX `dependsOn` is a generic edge with no native alternative/choice semantics, a vendor capability CBOM MUST NOT list mutually alternative algorithms as though all were simultaneously required dependencies. The example therefore lists MILENAGE and TUAK as supported cryptographic assets but does not create a conjunctive dependency that falsely requires both.

### 11.3 Non-protocol security constructs

TR 33.938 includes items that are not protocols. v1.0.0 uses:

- `securityConstruct` to identify the construct; and
- `securityConstructType` to classify what the construct **is**.

The controlled construct types are `cryptographic-scheme`, `trust-framework`, `security-format`, `layer-security-function`, `cryptographic-function`, and `authorization-framework`. `protocol-extension` is not used as a security-construct type in v1.0.0; MOBIKE remains represented in the canonical protocol vocabulary and is described semantically as an IKEv2 extension.

`securityConstructType` is **component-only**. A binding/service MAY carry `securityConstruct` as a summary, but MUST NOT carry `securityConstructType`. When a non-protocol construct needs graph identity, producers SHOULD model a distinct referencable component and attach exactly one `securityConstruct` and exactly one `securityConstructType` to that component. The type MUST match the canonical v1.0.0 classification:

| `securityConstruct` | Required `securityConstructType` |
|---|---|
| `ECIES` | `cryptographic-scheme` |
| `PKI` | `trust-framework` |
| `COSE` | `security-format` |
| `PDCP security` | `layer-security-function` |
| `NAS security` | `layer-security-function` |
| `KDF` | `cryptographic-function` |
| `JWE` | `security-format` |
| `JWS` | `security-format` |
| `OAuth 2.0` | `authorization-framework` |

CycloneDX can require a binding-specific representation such as a protocol-like cryptographic asset with type `other`; that serialization choice MUST NOT be interpreted as asserting that the construct is conceptually a protocol. Distinct referencable construct components preserve the construct/type association and avoid ambiguous parallel property lists.

## 12. Canonical protocol/function representation

### 12.1 Canonical protocol labels and CycloneDX normalization

`atis:telecom5g:protocol`, `crypto.supportedProtocols`, and `effectiveProtocol` use canonical labels from the v1.0.0 taxonomy. Producers MUST NOT create spelling variants such as `TLS1.3` or `TLSv1.3`; the canonical label is `TLS 1.3`. **For every canonical protocol listed below, the corresponding native CycloneDX `protocolProperties.type` and any exact version shown in the table are normative and MUST agree with the ATIS canonical label.**

| ATIS canonical protocol label | CycloneDX `protocolProperties.type` | `version` / name guidance |
|---|---|---|
| `TLS 1.2` | `tls` | version `1.2` |
| `TLS 1.3` | `tls` | version `1.3` |
| `DTLS 1.2` | `dtls` | version `1.2` |
| `DTLS 1.3` | `dtls` | version `1.3` |
| `QUIC` | `quic` | version as applicable |
| `MPQUIC` | `quic` | use asset name `MPQUIC`; version as applicable |
| `IKEv2` | `ike` | version `2` |
| `IPsec ESP` | `ipsec` | version/name `ESP` |
| `EAP-AKA'` | `eap-aka-prime` | version as applicable |
| `5G-AKA` | `5g-aka` | version as applicable |
| `PRINS` | `prins` | version as applicable |
| `EAP-TLS` | `other` | asset name `EAP-TLS` |
| `EAP-TTLS` | `other` | asset name `EAP-TTLS` |
| `MIKEY-SAKKE` | `other` | asset name `MIKEY-SAKKE` |
| `MOBIKE` | `other` | asset name `MOBIKE`; dependency on IKEv2 |
| `OCSP` | `other` | asset name `OCSP` |

For selected algorithm display labels registered by the v1.0.0 taxonomy (including the algorithm labels used by the conformance examples), native `algorithmProperties` MUST be consistent with the registered identity. Algorithm labels remain otherwise free-form in v1.0.0 by design; native CycloneDX cryptographic fields are authoritative for normalized comparison.

### 12.2 Complete TR 33.938 V19.2.0 representation mapping

TR 33.938 uses the heading **Protocol/Function**. Its entries are not all the same semantic kind. v1.0.0 maps them according to their nature rather than forcing all entries into the protocol vocabulary.

| TR 33.938 protocol/function | Semantic category | Preferred v1.0.0 representation |
|---|---|---|
| DTLS 1.2 / 1.3 | protocol | canonical `protocol`; native CycloneDX `dtls` protocol asset |
| TLS 1.2 / 1.3 | protocol | canonical `protocol`; native CycloneDX `tls` protocol asset |
| EAP-TLS | authentication protocol/method | canonical `protocol`; CycloneDX protocol asset type `other` |
| ECIES | cryptographic scheme | `securityConstruct = ECIES`; `securityConstructType = cryptographic-scheme`; native algorithm asset where applicable |
| PKI | infrastructure/trust framework | `securityConstruct = PKI`; `securityConstructType = trust-framework`; native certificate/key/trust structures |
| OCSP | protocol | canonical `protocol`; protocol asset type `other` |
| QUIC / MPQUIC | protocol | canonical `protocol`; native CycloneDX `quic` type; model TLS dependency |
| COSE | security format/mechanism | `securityConstruct = COSE`; `securityConstructType = security-format` |
| MIKEY-SAKKE | key-management protocol | canonical `protocol`; protocol asset type `other` |
| IKEv2 | protocol | canonical `protocol`; native CycloneDX `ike` type |
| PDCP security | layer security function | `securityConstruct = PDCP security`; `securityConstructType = layer-security-function`; native algorithm assets |
| NAS security | layer security function | `securityConstruct = NAS security`; `securityConstructType = layer-security-function`; NAS algorithm properties/native assets |
| EAP-AKA' | authentication protocol | canonical `protocol`; native `eap-aka-prime` type |
| 5G-AKA | authentication/key-agreement protocol | canonical `protocol`; native `5g-aka` type; link non-alternative required assets as applicable |
| IPsec ESP | protocol | canonical `protocol`; native `ipsec` type |
| KDF | cryptographic function | `securityConstruct = KDF`; `securityConstructType = cryptographic-function`; native KDF algorithm asset |
| JWE | security format | `securityConstruct = JWE`; `securityConstructType = security-format` |
| JWS | security format | `securityConstruct = JWS`; `securityConstructType = security-format` |
| EAP-TTLS | authentication protocol/method | canonical `protocol`; protocol asset type `other` |
| OAuth 2.0 | authorization framework | `securityConstruct = OAuth 2.0`; `securityConstructType = authorization-framework`; model TLS/JWS dependencies |
| MOBIKE | IKEv2 extension | canonical `protocol`; model generic dependency on IKEv2; richer `extends` semantics are outside the v1.0.0 binding |

### 12.3 PRINS

PRINS is a valid 3GPP 5G security protocol specified in TS 33.501 and has a native CycloneDX 1.7 protocol type (`prins`). PRINS is **not** a separate protocol/function entry in TR 33.938 V19.2.0. It MAY nevertheless be represented because TR 33.938 is the inventory baseline, not the exclusive scope of valid 5G constructs.

Because PRINS is admitted outside the TR 33.938 inventory baseline, the **referencable PRINS component itself MUST carry object-scoped authoritative provenance** using native CycloneDX `externalReferences[]`. For v1.0.0 the authoritative source is 3GPP TS 33.501. If the producer knows the applicable TS 33.501 release or version, the object-scoped reference or its associated comment/metadata SHOULD identify it. BOM-level references or an unrelated object's `spec.*` property do not satisfy this requirement. This rule generalizes to any future protocol/security construct explicitly admitted by the profile outside its declared inventory baseline.

## 13. Dependency graph

The dependency graph SHOULD represent each cryptographic dependency needed to interpret a declared protocol or security construct and its required cryptographic assets, except when the generic CycloneDX edge would violate the alternative/conditional rule below. The common path

`NF service → binding object → protocol/security-construct asset → algorithm asset`

is illustrative, not exclusive.

When a represented protocol or security construct depends on another represented protocol for the declared capability, and a generic `dependsOn` edge does not misstate an alternative or conditional relationship, that dependency SHOULD be represented. Examples include:

- `OAuth 2.0 → TLS`;
- `OAuth 2.0 → JWS`;
- `QUIC → TLS`;
- `MOBIKE → IKEv2`;
- `PRINS → JWE`; and
- `PRINS → JWS`.

CycloneDX `dependencies[].dependsOn` is a **generic dependency edge**. v1.0.0 does not encode richer predicates such as `uses`, `extends`, `protects`, or `negotiates`.

A generic `dependsOn` edge MUST NOT be used when it would represent mutually exclusive or conditional alternatives as simultaneous/conjunctive requirements. When CycloneDX cannot express the required choice or condition without that false implication, preserve the supported assets and omit the edge.

The absence of a dependency edge MUST NOT, by itself, be interpreted as an assertion that no dependency or conditional relationship exists. In particular, an edge can be omitted when the generic CycloneDX dependency relation cannot represent alternative, conditional, or choice semantics without falsely asserting simultaneous/conjunctive dependency.

Richer named relationship semantics can be defined by a future ATIS information-model/ontology layer without changing the Release 1 CycloneDX dependency representation.

## 14. OAuth / JWT / JWS

For 3GPP OAuth usage:

- `atis:telecom5g:oauthTokenType = JWT`;
- `atis:telecom5g:oauthTokenProtection = JWS`.

The actual signing/hash algorithms SHOULD be represented as native CycloneDX cryptographic assets rather than encoded in `oauthTokenProtection`. OAuth 2.0 dependencies on TLS and JWS SHOULD be represented when OAuth is modeled as a referencable security construct.

## 15. PKI, trust, and standards traceability

Detailed certificate, key, trust-anchor, and cryptographic parameter data SHOULD use native CycloneDX CBOM structures where available.

`atis:telecom5g:pki.role` identifies a PKI role such as `client`, `server`, `ca`, or `trust-anchor`. `atis:telecom5g:pki.authenticationMode` separately identifies `one-way` or `mutual` authentication. `mutual` MUST NOT be used as a `pki.role` value. Where `pki.authenticationMode` and `sbi.mutualAuthentication` describe the same subject, they MUST be consistent; in particular, `pki.authenticationMode = mutual` MUST NOT coexist with `sbi.mutualAuthentication = false`.

ATIS properties such as `atis:telecom5g:pki.usage`, `atis:telecom5g:trust.domain`, and `atis:telecom5g:trust.boundary` MAY provide concise telecom-specific context.

When the native CycloneDX object being referenced supports `externalReferences[]`, standards traceability SHOULD use that native field. ATIS `spec.primary` and `spec.crypto` are fallback summary fields for cases in which the applicable native object cannot carry the required reference; they are not replacements for native references.

The TR 33.938 baseline applies to the **cryptographic inventory**, not to every architectural entity or binding vocabulary in this profile. For a protocol or security construct that the profile explicitly admits **outside** its declared TR 33.938 cryptographic-inventory baseline, provenance is stricter: the corresponding referencable component MUST carry the authoritative source in its own native `externalReferences[]`. This object-scoped requirement prevents a BOM-wide citation from obscuring which specification justifies which out-of-baseline construct. CycloneDX 1.7 supports `externalReferences` directly on components.

## 16. PQC / QSC scope

v0.7 `atis:telecom5g:pqcRiskLevel` is **removed** in v1.0.0. The values `High`, `Medium`, `Low`, and `Unknown` had no defined ATIS assessment methodology and could therefore produce subjective, non-interoperable vendor declarations.

This profile does not define or require a PQC/CRQC exposure or risk assessment. Such an assessment can be derived from the declared cryptographic assets only by applying an external methodology that identifies its assessment rules, provenance, and methodology version. A future ATIS profile or PQC Playbook mapping can define interoperable derived exposure/risk semantics.

Detailed PQC/QSC posture fields remain roadmap items until a stable vendor-neutral assessment methodology is defined.

## 17. Validation

A CBOM claiming strict v1.0.0 conformance MUST be validated in two layers:

1. the CBOM MUST validate against the official CycloneDX 1.7 BOM schema; and
2. the CBOM MUST satisfy the ATIS `atis:telecom5g:*` property names, values, placement, and profile-specific semantic rules defined by the normative profile and taxonomy. The supplied overlay and Python helper are reference conformance implementations; equivalent independent validation is permitted.

The supplied ATIS reference validator checks, at minimum:

- the required v1.0.0 profile marker, compatible `taxonomyVersion`, and exactly one mandatory `cbom.scope`;
- strict rejection of deprecated/legacy properties;
- semantic object-role and subject-placement rules independent of `bom-ref` naming;
- explicit `inventoryScopeRef` roots when `inventoryCompleteness=complete`;
- canonical ATIS protocol-to-native CycloneDX mapping consistency;
- recognized property names and placement;
- controlled vocabularies and patterns;
- per-container cardinality;
- `bom-ref` uniqueness and dependency resolution;
- binding objects carry `bindingType` plus `binding`;
- `securityConstructType` appears only on components and matches the canonical type for its `securityConstruct`;
- out-of-baseline protocols/security constructs carry object-scoped authoritative provenance;
- vendor-scope CBOMs do not use `effective*`, and deployed CBOMs with `effective*` carry `metadata.timestamp` as the effective-state snapshot time;
- `cryptographyClass` appears only on native algorithm/construction components and `hybrid` is not a binding/entity aggregation label;
- selected duplicate ATIS/native and ATIS/ATIS facts are mutually consistent;
- every reified binding has a `bom-ref` and a direct dependency association from at least one represented entity;
- removed overloaded `cryptoType` is rejected and `cryptographyClass` uses only the high-level class vocabulary;
- removed experimental/v0.7 properties are rejected; and
- selected native CycloneDX cryptographic enum values used by the package examples are valid.

## Annex A (informative). Reference examples and test material

The distribution accompanying this draft includes non-normative positive examples, negative fixtures, validation helpers, and QA scripts to support implementation and QSCII review. Their recommended use and coverage are described in `TOOLING_GUIDE.md` and `conformance_traceability.md`. These materials do not add requirements to a conforming CBOM and do not define conformance.
