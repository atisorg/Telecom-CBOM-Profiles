# ATIS Telecom CBOM Roadmap

**A Modular and Interoperable Framework for Telecom Service CBOMs**

Future roadmap informed by the current ATIS Telecom CBOM work.

18 August 2026  
**Editorial/architectural revision:** 8 September 2026

| **Roadmap objective.** Establish a modular and extensible path for expanding the ATIS Telecom CBOM across telecommunications service domains while minimizing the impact of change between implementations. Each service domain can define and evolve its own taxonomy, interfaces, and domain-specific attributes independently, while reusing common CBOM concepts, identifiers, relationships, and structural constraints. A key objective is to evolve toward an interoperable Telecom CBOM information model that can be represented across current and emerging CBOM platforms, enabling consistent exchange and interpretation of cryptographic inventory information without creating unnecessary dependencies between service domains or implementation technologies. Future work may add ontology-based formal semantics and knowledge-graph representations to make selected concepts and relationships more explicitly machine-interpretable and to support richer query, analysis, and reasoning. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 1. Executive Summary

The ATIS Telecom CBOM roadmap is intended to guide the evolution from the initial 5G Core work into a broader, modular family of telecom CBOM service taxonomies. The roadmap is future-focused: the existing 5G CBOM is treated as the starting point and first implementation, rather than as the boundary of the long-term Telecom CBOM architecture.

The principal design goal is change isolation. New services should be introduced within their own domain taxonomy wherever practical, allowing the scope, vocabulary, standards references and service-specific attributes of that domain to evolve without forcing corresponding changes across unrelated Telecom CBOM implementations.

Interoperability is a parallel objective. ATIS should define the telecom-specific concepts, identifiers, attributes, relationship types, constraints, and intended meanings that need to be exchanged - including entities, services, interfaces, cryptographic assets, security purpose and standards traceability - independently of the syntax or data structures of any one CBOM platform. Platform mappings can then represent the same Telecom CBOM information model in current or emerging CBOM technologies. Future ontology and knowledge-graph work may formalize selected concepts and relationships, but it is not part of the current 3GPP-5G 1.0.0 normative profile.

The workbook provides the candidate expansion inventory. Numbered 5G reference points and 5G Service-Based Interfaces are grouped as completion of the 5G Core domain. The remaining tabs are treated as candidate service-domain taxonomies: Access & Non-3GPP, Management & O-RAN, CAPIF, IMS, EPS Interworking and Lawful Intercept. Crypto Inventory, Keys & Certificates, quantum-threat characterization and PQC Migration remain cross-domain tracks rather than independent service taxonomies.

# 2. Roadmap Objectives and Design Principles

## 2.1 Modular service-domain evolution

The Telecom CBOM should be organized as a set of service-domain taxonomies rather than a single continuously expanding telecom namespace. Each domain should own the information that is specific to its services and interfaces, while relying on common Telecom CBOM concepts for information that is shared across domains.

This separation allows ATIS to add, revise or deprecate a service-domain capability without requiring unrelated domains to change at the same time. Cross-domain dependencies should be expressed through stable references and common definitions of concepts and relationship meaning rather than by copying the same entities or cryptographic information into multiple taxonomies.

## 2.2 Interoperable Telecom CBOM information model

A key objective is to support an interoperable Telecom CBOM information model that can be represented across current and emerging CBOM platforms, enabling consistent exchange and interpretation of cryptographic inventory information without creating unnecessary dependencies between service domains or implementation technologies.

The information model should define the telecommunications-specific concepts, identifiers, attributes, typed relationships, cardinalities and other structural constraints, and the intended meanings required to describe cryptographic assets and their use. In this roadmap, those definitions provide **structural and conceptual semantics**: they establish what the modeled elements and relationships mean and how they may be combined, but they do not by themselves constitute a formal logic or inference model. Platform-specific representations should be maintained as mappings to the information model, not as the definition of the model itself. This allows an implementation technology to evolve or be replaced without requiring the Telecom CBOM conceptual model to be redesigned.

### 2.2.1 Future formal semantics, ontologies and knowledge graphs

As the Telecom CBOM matures, ATIS may choose to formalize selected concepts and relationships using an ontology. In that context, **formal semantics** means machine-interpretable class and property definitions, axioms, restrictions and other constraints whose interpretation is sufficiently explicit to support logical inference and consistency checking. This is a stronger notion than the structural and conceptual semantics provided by the information model.

Knowledge graphs may then be used to represent instance-level telecommunications and cryptographic facts and relationships, with stable identifiers, provenance and links back to the governed information model and, where applicable, the ontology. A knowledge graph by itself does not imply formal semantics; where a formal ontology is applied, graph assertions can be interpreted against that ontology. Ontologies and knowledge graphs are therefore potential future representations built on the Telecom CBOM foundation; they are not assumed to exist in the current Release 1.0.0 profile and are not required for CycloneDX conformance.

The roadmap deliberately does not prescribe a particular reasoning engine or implementation architecture. Such implementation choices can evolve independently provided they preserve the governed Telecom CBOM concepts, relationships and constraints.

| **Principle**              | **Roadmap implication**                                                                                                                                                       |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Platform independence      | Define telecom concepts, relationships, constraints and intended meanings first; maintain platform representations as separate mappings.                                      |
| Domain autonomy            | Each service domain has its own scope, controlled vocabulary and version lifecycle.                                                                                           |
| Common definitions         | Reuse shared definitions for entities, interfaces, protocols, algorithms, keys, certificates, trust and cryptographic purpose.                                                |
| Minimal change propagation | A change within one service taxonomy should not require changes to unrelated domains unless the common information model itself changes.                                      |
| Stable relationships       | Use durable identifiers and references so domains can link to common assets or other domains without duplication.                                                             |
| Standards traceability     | Maintain clear linkage from taxonomy terms to the applicable 3GPP, IETF, O-RAN, ETSI or other source specification.                                                           |
| Interoperability testing   | Use common examples and expected conceptual and relationship outcomes to verify equivalent representation across different CBOM platforms.                                    |
| Risk provenance            | Any reported quantum risk level should identify the assessment framework and version used. Unreferenced qualitative ratings should not acquire a standardized interoperable meaning. |

## 2.3 Reuse without coupling

Common cryptographic concepts should be defined once where practical and reused across service domains. Domain taxonomies should add telecom context - for example, the service, interface, endpoint role, trust boundary, usage purpose and standards reference - without creating competing definitions of the same cryptographic protocol, algorithm, key or certificate concept.

# 3. Starting Point and Source Basis

The current ATIS 5G Core CBOM Release v1.0 provides the initial implementation and establishes the starting set of telecom CBOM concepts. The roadmap uses that work as the first domain foundation, but does not limit the future Telecom CBOM architecture to the current 5G scope or to its present implementation format.

The ATIS Telecom CBOM Release 1.0.0 uses 3GPP TR 33.938 V19.2.0 as its **primary cryptographic inventory baseline** for the 5G System in Standalone mode. TR 33.938 is not the exclusive authority for valid 5GS architectural entities, interfaces, protocols or security mechanisms: the applicable normative 3GPP Technical Specifications remain authoritative for those definitions. Where a construct required to represent the 5G architecture is defined by a normative 3GPP specification but is absent from the explicit TR 33.938 inventory, its inclusion should be identified and traced to the authoritative specification. TR 33.938 is also not a complete catalogue of every telecom service or interface, and Lawful Interception is explicitly outside its scope. The workbook is therefore used as the candidate expansion inventory for the future roadmap, with each entry requiring standards validation before normative inclusion.

Release 1.0.0 is a concrete CycloneDX 1.7 implementation profile and taxonomy. It provides important implementation experience and candidate common concepts, but it should not be read as an already-complete, platform-independent Telecom CBOM information model.

# 4. Target Telecom CBOM Framework

The target framework separates stable telecom concepts, relationship definitions, structural constraints and intended meanings from domain-specific taxonomies and from the technology used to serialize or exchange a CBOM. Future formal semantic and knowledge-graph work can build on that conceptual foundation without making any one reasoning or representation technology the definition of the Telecom CBOM. This structure is intended to make the roadmap extensible while keeping the impact of change controlled.

| **Framework layer**                   | **Purpose**                                                                                                                                                                                                                | **Change model**                                                                  |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Common Telecom CBOM information model | **Target conceptual layer.** Defines shared concepts, identifiers, attributes, typed relationships, cardinalities/constraints and intended meanings for telecom entities/endpoints, services, interfaces, cryptographic assets, protocols, algorithms, keys/certificates, security purpose, trust context, standards/release and inventory state. | Changes deliberately and infrequently because multiple domains depend on it. |
| Service-domain taxonomies             | Define domain-specific services, interfaces, roles, identifiers, controlled vocabularies and attributes for 5G Core, Access, Management/O-RAN, CAPIF, IMS, EPS Interworking, Lawful Intercept and future domains. | Version independently. A domain change should normally remain within that domain. |
| Formal ontology                       | **Future candidate layer.** May formalize selected common and domain concepts using machine-interpretable classes, properties, axioms and constraints, providing formal semantics suitable for logical inference where required. | Evolves under explicit governance and does not become a requirement of an existing profile merely by being added to the roadmap. |
| Knowledge-graph representations       | **Future candidate layer.** May represent instance-level telecom and cryptographic facts and relationships, with identifiers and provenance aligned to the information model and, where used, the ontology. | Can evolve with operational and analytical needs while preserving the governed conceptual definitions. |
| Platform mappings                     | Describe how the common information model and each domain taxonomy are represented in a particular CBOM platform or exchange format. | Can be added or revised without redefining the conceptual model or any separately governed formal ontology. |
| Cross-domain overlays                 | Shared crypto inventory, keys/certificate context, quantum-threat characterization, risk/migration context and other future cross-cutting views. | Evolve independently and are referenced by relevant domains. |

## 4.1 Domain boundaries

| **Domain**         | **Roadmap treatment**        | **Primary scope**                                                                                      |
|--------------------|------------------------------|--------------------------------------------------------------------------------------------------------|
| 5G Core            | Complete existing domain     | 5G Core NFs, numbered reference points, Service-Based Interfaces and core cryptographic relationships. |
| Access & Non-3GPP  | Separate service taxonomy    | Radio/access, split-RAN, trusted/untrusted non-3GPP, wireline access and sidelink.                     |
| Management & O-RAN | Separate service taxonomy    | Management and orchestration interfaces, Open RAN control/fronthaul, OAM and automation surfaces.      |
| CAPIF              | Separate service taxonomy    | API exposure, discovery, authorization and federation interfaces.                                      |
| IMS                | Separate service taxonomy    | IMS signaling, subscriber-data, media and control interfaces.                                          |
| EPS Interworking   | Separate service taxonomy    | Legacy/EPS interfaces required for 5GS interworking and migration visibility.                          |
| Lawful Intercept   | Separate controlled taxonomy | LI-specific interfaces and governance, sourced outside the TR 33.938 baseline.                         |

# 5. Roadmap at a Glance

| **Stage**                           | **Deliverable**                                                   | **Candidate scope**                                                                                              | **Outcome**                                                                                              |
|-------------------------------------|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Foundation - Interoperability model | Telecom CBOM common information model and domain governance rules | Shared concepts, identifiers, relationships, constraints, versioning, cross-domain references and platform-mapping principles | A stable conceptual foundation that is independent of any one CBOM platform.                            |
| 1 - 5G Core completion              | 5G Core coverage increment                                        | Missing Rel-15/16 numbered reference points and core SBA services; entity vocabulary completion                  | Complete the first Telecom CBOM domain and validate the common information model.                        |
| 2 - Advanced 5G services            | 5G Core feature increment                                         | Rel-17 analytics/data collection, slice services, edge, location, ProSe, TSC/TSN and 5MBS                        | Complete the workbook candidate scope for the 5G Core domain.                                            |
| 3 - Service taxonomy wave A         | Access & Non-3GPP + Management & O-RAN                            | Access, RAN, non-3GPP and operational/management surfaces                                                        | Extend the model to deployment and management domains with distinct trust and lifecycle characteristics. |
| 4 - Service taxonomy wave B         | CAPIF + IMS                                                       | External API/federation and voice/multimedia service layers                                                      | Extend into API exposure and multimedia service domains without coupling them to the 5G Core taxonomy.   |
| 5 - Service taxonomy wave C         | EPS Interworking + Lawful Intercept                               | Legacy interworking and separately governed LI interfaces                                                        | Complete broader telecom service coverage while preserving domain boundaries.                            |
| Parallel track                      | Shared crypto / quantum-risk content                              | Crypto Inventory, Keys & Certificates, quantum-threat characterization, HNDL exposure and PQC Migration          | Reusable cross-domain cryptographic content, quantum-threat context and migration views.                 |
| Future formal-semantic track        | Formal ontology and knowledge-graph representations                | Formalized classes/properties/axioms where needed; instance-level facts, relationships and provenance                       | Enable formal reasoning and graph-based analysis without making ontology/KG technology a requirement of the current 5G profile. |

# 6. 5G Core Completion Roadmap

The 5G Core remains the first domain to complete because it provides the primary architectural context for many later telecom service taxonomies. Completion should focus on missing 5G reference points and Service-Based Interfaces, using the common Telecom CBOM information model so that the resulting concepts, relationships and constraints can be represented consistently on more than one CBOM platform.

## 6.1 Numbered reference points - grouped work packages

| **Work package**                                       | **Count** | **Candidate interfaces**                                                                    |
|--------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------|
| Core control, session, subscriber, policy and charging | 19        | N5, N7, N8, N10, N13, N14, N16, N16a, N17, N20, N21, N28, N29, N30, N35, N36, N37, N40, N51 |
| Roaming, interworking and slice/security coordination  | 6         | N24, N26, N27, N31, N34, N38                                                                |
| Analytics, public warning, TSC/TSN and ATSSS           | 6         | N23, N50, N56, N57, N58, N60                                                                |
| External exposure boundary                             | 1         | N33                                                                                         |
| User-plane and 5MBS feature package                    | 5         | N19, MB-N3, MB-N4, MB-N6, MB-N9                                                             |

## 6.2 Service-Based Interfaces - grouped work packages

| **Work package**                          | **Count** | **Candidate services**                       |
|-------------------------------------------|-----------|----------------------------------------------|
| Rel-15/16 core service completion         | 7         | Namf, Nsmf, Nausf, Nnssf, Nchf, Nsmsf, Nucmf |
| Slice, edge and analytics services        | 5         | Nnsacf, Nnssaaf, Neasdf, Ndccf, Nmfaf        |
| Application, location and key services    | 4         | Naf, Naanf, Nlmf, Ngmlc                      |
| Rel-17 ProSe / WLAN / industrial services | 4         | N5gddnmf, Npkmf, Ntsctsf, Nnswo              |
| 5MBS service package                      | 3         | Nmbsmf, Nmbsf, Nmbstf                        |

## 6.4 5G Core completion scope

- Each interface or service has a canonical identifier, defined endpoint/producer and consumer roles, release applicability, primary specification reference and cryptographic reference(s).

- The logical relationships between telecom entity, service/interface binding, protocol and cryptographic assets are defined independently of a particular implementation format.

- Capability information and deployed/effective information can be distinguished consistently across implementations.

- Representative platform-neutral examples and test vectors are provided for the common information model.

- One or more implementation mappings demonstrate how the same defined information and relationships are represented on available CBOM platforms without making those mappings normative to the telecom taxonomy.

- Conformance testing verifies required vocabulary, structural constraints and relationship meaning; mappings identify any information or relationship meaning that cannot be represented without loss.

- Rows marked partial, disputed, legacy, deprecated, vendor-specific or site-dependent in the workbook are standards-checked before normative inclusion.

# 7. Service-Domain Taxonomy Roadmap

After the 5G Core domain is sufficiently stable, the remaining workbook domains should progress as independent taxonomy packages. Each domain should reuse the common Telecom CBOM information model while keeping its service-specific vocabulary, standards references, release lifecycle and implementation mappings within the domain package.

Cross-domain interfaces should reference the appropriate external domain entity or common asset rather than copying the same definition into both taxonomies. This is the principal mechanism for minimizing the impact of change as the Telecom CBOM expands.

| **Domain**         | **Entries** | **Suggested wave**   | **Scope**                                                                       | **Roadmap treatment**                                                                                                                                                            |
|--------------------|-------------|----------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Access & Non-3GPP  | 13          | Wave A - high        | Uu; split-RAN; inter-gNB; untrusted/trusted non-3GPP; wireline access; sidelink | Closely coupled to 5G Core architecture, but should remain an independent domain. Shared interfaces such as Xn/F1/E1 should be specialized or referenced rather than duplicated. |
| Management & O-RAN | 8           | Wave A - high        | O1, O2, A1, E2, Open Fronthaul, vendor OAM, CI/CD, SMO API                      | Independent management-plane taxonomy with its own trust model, operational lifecycle and non-3GPP/O-RAN standards sources.                                                      |
| CAPIF              | 9           | Wave B - medium/high | CAPIF-1/1e, 2/2e, 3-7                                                           | Independent API-exposure taxonomy. Reuse common protocol and trust concepts while keeping API roles and federation-specific definitions in the CAPIF domain.                      |
| IMS                | 9           | Wave B - medium/high | Gm, Mw, Cx, Sh, ISC, Mb, Ut, Mp, Mn                                             | Independent service-layer taxonomy for SIP, Diameter and media/control interfaces, including legacy cryptographic profiles where applicable.                                     |
| EPS Interworking   | 5           | Wave C - medium      | S6a, S5, S8, S1-MME, S1-U                                                       | Keep EPS/legacy definitions and relationship rules separate from 5G Core while enabling cross-domain references for interworking and migration inventories.                     |
| Lawful Intercept   | 7           | Wave C - controlled  | LI-X0/X1/X2/X3 and HI-1/2/3                                                     | Separate controlled taxonomy sourced from LI-specific specifications and governance; not derived from the TR 33.938 5G cryptographic baseline.                                   |

# 8. Interoperability and Change Isolation

Interoperability should be treated as a **meaning-preservation requirement**, not merely as a file-format requirement. Two implementations should be considered interoperable when they can represent and exchange the same governed Telecom CBOM concepts, relationships, constraints and intended meaning, even if the underlying CBOM platforms use different structures, property systems or serialization formats.

| **Interoperability requirement** | **Roadmap expectation**                                                                                                                                              |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Canonical conceptual definitions  | ATIS defines the concepts, relationship types, constraints and intended meanings for entities, services, interfaces, cryptographic assets, purposes, trust context and standards references independently of platform syntax. |
| Stable identifiers               | Common and domain identifiers remain stable across platform mappings so the same object or relationship can be correlated between implementations.                   |
| Independent platform mappings    | Each supported CBOM platform has a mapping document or machine-readable binding that translates the common information model and domain taxonomy into that platform. |
| Loss visibility                  | A mapping must identify information or relationship meaning that is unsupported, approximated or lost rather than silently dropping it.                                    |
| Meaning-preservation tests       | A common set of test vectors expresses expected conceptual, structural and relationship outcomes; multiple platform representations can be tested against the same expected outcome. |
| Independent versioning           | The common information model, each service taxonomy and each platform mapping carry separate versions so a mapping update does not force a domain taxonomy revision. |
| Extension governance             | New information is added to the common model only when it is broadly reusable; otherwise it remains in the relevant service domain.                                  |

## 8.1 Common Telecom CBOM concepts

- Telecommunications entity, network function, endpoint or external role.

- Service and interface/reference-point identity, including producer/consumer or endpoint relationships.

- Cryptographic protocol, algorithm, key, certificate and other cryptographic asset concepts.

- Cryptographic purpose and usage context, such as authentication, integrity, confidentiality, channel protection, API protection and key management.

- Trust domain, trust boundary and certificate/PKI context where relevant.

- Standards source, release applicability and profile/version traceability.

- Inventory state, including supported capability versus deployed/effective use.

- Quantum-threat and migration context, including threat type, HNDL exposure and risk classification when sufficiently stable interoperable definitions and an agreed assessment framework are available.

## 8.2 Versioning and dependency rules

A domain taxonomy should be able to release a new version without requiring other domain taxonomies to change unless a shared conceptual, structural or relationship dependency has genuinely changed. Platform mappings should also be versioned independently, allowing ATIS to add support for an emerging CBOM platform or update an existing mapping without redefining the Telecom CBOM information model.

# 9. Cross-Domain Workbook Tracks

The Crypto Inventory, Keys & Certificates and PQC Migration tabs are better treated as common content and overlays that can be referenced by every service domain. The cross-domain model should also support quantum-threat characterization, including HNDL exposure and future risk classification. Keeping these capabilities cross-cutting avoids duplicated cryptographic definitions and allows threat and migration information to be applied consistently across the broader Telecom CBOM.

| **Workbook track** | **Candidate rows** | **Roadmap role**                                                        | **Recommended handling**                                                                                                                                                                                                                                                                      |
|--------------------|--------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Crypto Inventory   | 18                 | Shared protocol/algorithm component library and normalization catalogue | Maintain a common protocol/algorithm catalogue so TLS, IKEv2/IPsec, OAuth, NAS/AS security, SUCI, SRTP, SSH, MACsec and similar assets are not redefined in each service taxonomy.                                                                                                            |
| Keys & Certs       | 35                 | Example key/certificate asset inventory and PKI/trust mapping           | Define common key/certificate and PKI/trust concepts and relationship rules. Platform mappings determine how those assets are represented in a particular CBOM technology.                                                                                                                     |
| PQC Migration      | 11                 | Quantum-threat characterization, risk and migration overlay             | Use PQC information as a cross-domain migration view. Support threat type and HNDL exposure using common governed definitions. Add an interoperable risk level only when it is derived from an appropriate standardized or industry-agreed assessment framework, with the framework and version identified. |

## 9.1 Quantum Threat Characterization and Risk Classification

The Telecom CBOM information model should support characterization of quantum-related threats associated with a specific cryptographic asset and, where relevant, the service, interface or usage in which that cryptography is applied. This is a cross-domain capability: the same governed threat definitions should be reusable across 5G Core, Access, Management/O-RAN, CAPIF, IMS, interworking and future service taxonomies.

The purpose is not to predict when a Cryptographically Relevant Quantum Computer (CRQC) will become available. Instead, the CBOM should identify the nature of the quantum exposure so that cryptographic inventory information can support risk assessment and migration prioritization. Threat susceptibility and operational risk should be treated separately: a cryptographic primitive may be susceptible to a quantum attack, while the operational risk also depends on how it is used, the information protected, its required confidentiality lifetime, exposure and the expected migration horizon.

**Quantum threat type.** The initial common threat vocabulary should be informed by the ATIS report "Preparing 5G for the Quantum Era: An Analysis of 3GPP Architecture and the Transition to Quantum-Resistant Cryptography" and should support one or more applicable threat types.

- **Harvest-Now, Decrypt-Later (HNDL):** encrypted information is captured today and retained for future decryption when sufficient quantum computing capability becomes available. It is particularly relevant where protected information must remain confidential for an extended period.

- **Quantum Decryption:** a CRQC is used to compromise vulnerable cryptographic mechanisms and recover protected information.

- **Quantum Impersonation:** compromise of public-key signature or authentication mechanisms enables an attacker to impersonate a legitimate user, network function, service or organization.

- **Quantum Man-in-the-Middle (QMITM):** quantum-enabled compromise of authentication, key-establishment or signature mechanisms permits active interception, modification or forgery of communications.

- **Other cryptographic threats:** additional threats, such as side-channel attacks, may be represented where relevant, but should be distinguished from threats that specifically depend on a CRQC.

**HNDL exposure.** HNDL should be explicitly identifiable because it represents a present-day exposure to a future cryptographic capability. The HNDL indicator should be associated with the cryptographic usage context and the information being protected rather than inferred from the algorithm alone. Where practical, the assessment may also record the confidentiality-lifetime context that makes the exposure relevant.

**Quantum threat risk level.** The roadmap should provide for a quantum threat risk level to support future prioritization, but it should not prescribe an authoritative High, Medium or Low rating in the absence of an appropriate standardized or industry-agreed assessment methodology. NIST cryptographic guidance and security-strength information can inform an assessment, but should not be directly interpreted as a Telecom CBOM operational risk scale unless an agreed framework defines that mapping.

Once the industry agrees an appropriate risk framework, the Telecom CBOM common information model should define how the resulting risk classification is represented and should require the framework name, version or profile to accompany the rating. Until then, an interoperable risk value should remain Unknown or Not Assessed. Any existing implementation-specific qualitative rating should be treated as provisional rather than as a standardized cross-platform meaning.

**Candidate common information elements**

| **Information element**  | **Roadmap intent**                                                                                                     | **Interoperability rule**                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| Quantum threat type      | One or more threat categories associated with a cryptographic asset or its telecom usage.                              | Use a governed common vocabulary; initial categories include HNDL, Quantum Decryption, Quantum Impersonation and QMITM. |
| HNDL exposure            | Indicates that the usage may be exposed to present-day capture for future decryption.                                  | Determine from usage and protected-information context; do not infer solely from the algorithm.                         |
| Quantum risk level       | Provides a prioritization classification when an agreed assessment method is available.                                | Populate only from an approved standardized or industry-agreed framework; otherwise use Unknown / Not Assessed.         |
| Risk framework reference | Identifies the methodology used to derive the risk classification.                                                     | Framework name and version/profile should accompany any non-unknown risk level.                                         |
| Assessment date          | Records when the risk assessment was made.                                                                             | Supports reassessment as quantum technology, standards and migration guidance evolve.                                   |
| Assessment context       | Describes the service/interface usage, protected-information context and other assumptions relevant to the assessment. | Provides the basis needed to interpret the risk value consistently across platforms and organizations.                  |

These elements should be defined in the common Telecom CBOM information model rather than independently inside each service taxonomy. Service-domain taxonomies can then reference the common definitions and add only the context required by that domain.

# 10. Standard Deliverable Set for Each Service Taxonomy

- Scope and architecture statement, including in-scope and explicitly out-of-scope services and interfaces.

- Domain-specific taxonomy and controlled vocabularies for entities, endpoints, interfaces, services and domain attributes.

- Mapping of domain concepts to the common Telecom CBOM information model.

- Relationship rules covering how the domain links to common cryptographic assets and to entities in other service domains.

- Standards traceability, release applicability and source references for each normative taxonomy term.

- Platform-neutral canonical examples and conceptual/relationship test vectors that support meaning-preservation testing.

- Separate implementation mappings for one or more supported CBOM platforms, with any representation limitations documented.

- Conformance and interoperability tests, including positive, negative and cross-platform equivalence cases where practical.

- Independent versioning, deprecation and backward-compatibility guidance for the domain taxonomy.

- Quantum-threat characterization and PQC migration considerations where relevant, including HNDL exposure. Where a quantum risk level is reported, the assessment framework and version should also be identified.

# 11. Roadmap Implementation Priorities

The roadmap is intended to be a living, contribution-driven plan rather than a fixed implementation sequence. Work should progress according to the priorities identified by the ATIS Telecom CBOM community and the level of active contribution available for each service domain or cross-domain work area.

Candidate domains may therefore progress at different rates or in parallel. The work packages and suggested waves elsewhere in this roadmap are planning aids rather than a fixed delivery sequence. A work area should move into active development when there is a clear industry need, sufficient technical contribution to define and validate the required information, and contributors willing to review, implement and maintain the resulting taxonomy and interoperability material.

Implementation priorities should take account of:

Industry need and the value of the CBOM coverage to telecom operators, vendors and other ecosystem participants.

The level of active contributor commitment and availability of subject-matter expertise for the proposed domain.

The maturity and stability of the applicable standards, interfaces and cryptographic requirements, including any assessment framework required to support interoperable quantum-risk classification.

Dependencies on common Telecom CBOM concepts or other service domains, with preference for work that can be progressed without creating unnecessary coupling.

The ability to produce a complete and implementable package, including the taxonomy, examples, platform mappings and interoperability or conformance tests needed to support adoption.

This approach allows the roadmap to respond to contributor and industry priorities while preserving a consistent architectural direction. Items that do not yet have sufficient contribution can remain visible as candidate roadmap work without blocking domains that are ready to progress.

## 11.1 Community Participation and GitHub Collaboration

Development of the ongoing roadmap should be managed transparently through the ATIS Telecom CBOM GitHub repository. Interested participants can participate in the community by creating a GitHub account if needed, watching the repository for updates, and following the project contribution instructions. Contributions can include opening or commenting on issues, participating in GitHub Discussions where enabled, reviewing proposed changes, and submitting pull requests. Where project membership or write access is required, the repository should provide instructions for requesting access.

The repository should include clear contribution guidance, for example through a CONTRIBUTING.md file, describing how to propose new roadmap work, contribute taxonomy changes, review draft material, and submit implementation mappings or test artifacts. GitHub issues, labels, milestones or project views can be used to make active priorities, work in progress, and areas seeking contributors visible to the community.

To participate in development of the roadmap, contributors should use the ATIS Telecom CBOM GitHub repository and follow the contribution instructions provided with the project. Participation through GitHub should complement, and not replace, any applicable ATIS participation, contribution, licensing or intellectual property requirements.

# Appendix A - Candidate 5G Core Numbered Reference-Point Expansion

The following candidate items are taken from the workbook Reference Points tab for future 5G Core coverage. N18 is omitted because the workbook marks it deprecated. Entries should be standards-checked before normative inclusion.

| **Roadmap package**                                    | **Interface** | **Endpoints**   | **Layer / protocol** | **Release** | **Workbook spec ref**        | **Workbook note**                                     |
|--------------------------------------------------------|---------------|-----------------|----------------------|-------------|------------------------------|-------------------------------------------------------|
| Core control, session, subscriber, policy and charging | N5            | PCF ↔ AF        | AF policy            | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N7            | SMF ↔ PCF       | SBA-derived          | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N8            | UDM ↔ AMF       | Subscriber           | R15         | TS 23.501 §4.2.3             | Implemented via Nudm SBA                              |
| Core control, session, subscriber, policy and charging | N10           | UDM ↔ SMF       | Subscriber           | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N13           | UDM ↔ AUSF      | Auth                 | R15         | TS 23.501 §4.2.3 / TS 33.501 | Long-term key material derivation path                |
| Core control, session, subscriber, policy and charging | N14           | AMF ↔ AMF       | Mobility             | R15         | TS 23.501 §4.2.3             | Carries security context — handover-sensitive         |
| Core control, session, subscriber, policy and charging | N16           | SMF ↔ SMF       | Session              | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N16a          | SMF ↔ I-SMF     | Session              | R16         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N17           | AMF ↔ 5G-EIR    | EIR check            | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N20           | AMF ↔ SMSF      | SMS                  | R15         | TS 23.501 §4.2.3             | SMS content is sensitive                              |
| Core control, session, subscriber, policy and charging | N21           | SMSF ↔ UDM      | Subscriber           | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N28           | PCF ↔ CHF       | Charging             | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N29           | NEF ↔ SMF       | Exposure             | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N30           | PCF ↔ NEF       | Exposure             | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N35           | UDM ↔ UDR       | Data                 | R15         | TS 23.501 §4.2.3             | All subscriber data lives in UDR                      |
| Core control, session, subscriber, policy and charging | N36           | PCF ↔ UDR       | Data                 | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N37           | NEF ↔ UDR       | Data                 | R15         | TS 23.501 §4.2.3             |                                                       |
| Core control, session, subscriber, policy and charging | N40           | SMF ↔ CHF       | Charging             | R15         | TS 23.501 §4.2.3 / TS 32.290 |                                                       |
| Core control, session, subscriber, policy and charging | N51           | AMF ↔ NEF       | Exposure             | R16         | TS 23.501                    |                                                       |
| Roaming, interworking and slice/security coordination  | N24           | V-PCF ↔ H-PCF   | Roaming              | R15         | TS 23.501                    | Always traverses N32 in practice                      |
| Roaming, interworking and slice/security coordination  | N26           | AMF ↔ MME       | Interworking         | R15         | TS 23.501 §5.17 / TS 29.413  | GTPv2-C based                                         |
| Roaming, interworking and slice/security coordination  | N27           | NRF ↔ NRF       | Discovery            | R15         | TS 23.501 §4.2.3             | Topology disclosure risk — minimize attributes        |
| Roaming, interworking and slice/security coordination  | N31           | NSSF ↔ NSSF     | Slice                | R15         | TS 23.501 §4.2.3             |                                                       |
| Roaming, interworking and slice/security coordination  | N34           | NSSAAF ↔ AAA-S  | Slice auth           | R16         | TS 23.501 / TS 33.501        |                                                       |
| Roaming, interworking and slice/security coordination  | N38           | (I-SMF) ↔ UPF   | PFCP                 | R16-partial | TS 23.501                    | Treat as N4-equivalent                                |
| Analytics, public warning, TSC/TSN and ATSSS           | N23           | NWDAF ↔ PCF     | Analytics            | R16         | TS 23.501 / TS 23.288        | ML model output — bias / poisoning concerns           |
| Analytics, public warning, TSC/TSN and ATSSS           | N50           | AMF ↔ CBCF      | PWS                  | R16         | TS 23.501                    | False-alarm/spoofing risk — high public-safety impact |
| Analytics, public warning, TSC/TSN and ATSSS           | N56           | AMF ↔ TSCTSF    | TSN/TSC              | R17         | TS 23.501                    | Industrial 5G / private network use                   |
| Analytics, public warning, TSC/TSN and ATSSS           | N57           | PCF ↔ TSCTSF    | TSN/TSC              | R17         | TS 23.501                    |                                                       |
| Analytics, public warning, TSC/TSN and ATSSS           | N58           | NEF ↔ TSCTSF    | TSN/TSC              | R17         | TS 23.501                    |                                                       |
| Analytics, public warning, TSC/TSN and ATSSS           | N60           | AMF ↔ AMF/SMF   | ATSSS                | R16-R17     | TS 23.501                    | Partial / vendor-specific numbering                   |
| External exposure boundary                             | N33           | NEF ↔ AF        | Exposure             | R15         | TS 23.501 / TS 23.222        | Often called T8 in earlier specs                      |
| User-plane and 5MBS feature package                    | N19           | UPF ↔ UPF       | GTP-U                | R16         | TS 23.501                    | Specific to HR-SBO architectures                      |
| User-plane and 5MBS feature package                    | MB-N3         | (R)AN ↔ MB-UPF  | GTP-U                | R17         | TS 23.247                    | 5MBS architecture                                     |
| User-plane and 5MBS feature package                    | MB-N4         | MB-SMF ↔ MB-UPF | PFCP                 | R17         | TS 23.247                    |                                                       |
| User-plane and 5MBS feature package                    | MB-N6         | MB-UPF ↔ MBSTF  | L3                   | R17         | TS 23.247                    |                                                       |
| User-plane and 5MBS feature package                    | MB-N9         | MB-UPF ↔ MB-UPF | GTP-U                | R17         | TS 23.247                    |                                                       |

# Appendix B - Candidate 5G Core Service-Based Interface Expansion

The following candidate items are taken from the workbook Service-Based Interfaces tab for future 5G Core coverage. Entries should be standards-checked before normative inclusion.

| **Roadmap package**                       | **SBI**  | **Producer** | **Common consumers**       | **Release** | **Workbook spec ref** | **Information exchanged**                                              |
|-------------------------------------------|----------|--------------|----------------------------|-------------|-----------------------|------------------------------------------------------------------------|
| Rel-15/16 core service completion         | Namf     | AMF          | SMF, NEF, NSSF, AUSF       | R15         | TS 29.518             | UE context mgmt, communication, event exposure, location, MT messaging |
| Rel-15/16 core service completion         | Nsmf     | SMF          | AMF, PCF, NEF              | R15         | TS 29.502             | PDU session mgmt, event exposure, NIDD                                 |
| Rel-15/16 core service completion         | Nausf    | AUSF         | AMF                        | R15         | TS 29.509             | UE authentication, SoR protection, UPU protection                      |
| Rel-15/16 core service completion         | Nnssf    | NSSF         | AMF                        | R15         | TS 29.531             | Slice selection, NS-AvailabilityInfo notification                      |
| Rel-15/16 core service completion         | Nchf     | CHF          | SMF, AMF, PCF              | R15         | TS 32.291             | Converged charging, spending-limit control, quota mgmt                 |
| Rel-15/16 core service completion         | Nsmsf    | SMSF         | AMF, UDM                   | R15         | TS 29.540             | SMS over NAS service                                                   |
| Rel-15/16 core service completion         | Nucmf    | UCMF         | AMF                        | R16         | TS 29.575             | UE Capability Match Request — radio capability ID dictionary           |
| Slice, edge and analytics services        | Nnsacf   | NSACF        | AMF, SMF                   | R17         | TS 29.536             | Network Slice Admission Control — UE/PDU session counts per slice      |
| Slice, edge and analytics services        | Nnssaaf  | NSSAAF       | AMF                        | R16         | TS 29.526             | Slice-specific Auth (EAP relay) + AAA-SBO for slice authentication     |
| Slice, edge and analytics services        | Neasdf   | EASDF        | SMF                        | R17         | TS 29.558             | Edge App Server Discovery — DNS resolution for edge computing          |
| Slice, edge and analytics services        | Ndccf    | DCCF         | NWDAF, OAM, NFs            | R17         | TS 29.574             | Data Collection Coordination Function — aggregates analytics inputs    |
| Slice, edge and analytics services        | Nmfaf    | MFAF         | DCCF, NWDAF, AFs           | R17         | TS 29.576             | Messaging Framework Adaptor — bus interface for analytics              |
| Application, location and key services    | Naf      | AF           | NEF (or direct if trusted) | R15         | TS 29.522             | Application Function as SBA producer (trusted AFs only)                |
| Application, location and key services    | Naanf    | AAnF         | AF                         | R17         | TS 29.522             | AKMA — application-layer keys derived from K_AKMA                      |
| Application, location and key services    | Nlmf     | LMF          | AMF                        | R16         | TS 29.572             | Location Management Function — positioning measurements                |
| Application, location and key services    | Ngmlc    | GMLC         | AMF, NEF, AF               | R16         | TS 29.515             | Gateway Mobile Location Centre — location service entry                |
| Rel-17 ProSe / WLAN / industrial services | N5gddnmf | 5G-DDNMF     | UE (via PC5), PCF          | R17         | TS 29.555             | ProSe Direct Discovery name management                                 |
| Rel-17 ProSe / WLAN / industrial services | Npkmf    | PKMF         | UE (via PC5), AMF          | R17         | TS 33.503             | ProSe Key Management Function — direct-discovery key material          |
| Rel-17 ProSe / WLAN / industrial services | Ntsctsf  | TSCTSF       | PCF, NEF, AF               | R17         | TS 29.565             | Time-Sensitive Communication / TSN AF                                  |
| Rel-17 ProSe / WLAN / industrial services | Nnswo    | NSWO-F       | AUSF                       | R17         | TS 29.234             | Non-Seamless WLAN Offload authentication                               |
| 5MBS service package                      | Nmbsmf   | MB-SMF       | AF, MB-UPF, AMF            | R17         | TS 29.532             | MBS session control                                                    |
| 5MBS service package                      | Nmbsf    | MBSF         | AF                         | R17         | TS 29.581             | MBS function — service-layer of MBS                                    |
| 5MBS service package                      | Nmbstf   | MBSTF        | MB-SMF, AF                 | R17         | TS 29.582             | Content ingest and packaging for MBS                                   |

# Appendix C - Service-Domain Candidate Inventories

These entries are taken from the corresponding workbook tabs. They define candidate scope for future service-domain taxonomy work and are not a statement that every row has already been independently validated against the latest external standard.

## Access & Non-3GPP

| **Interface** | **Endpoint A** | **Endpoint B** | **Layer / protocol** | **Release** | **Workbook spec ref**           | **Workbook note** |
|---------------|----------------|----------------|----------------------|-------------|---------------------------------|-------------------|
| Uu            | UE             | gNB            | Radio                | R15         | TS 38.331 / TS 33.501           |                   |
| F1-C          | gNB-CU-CP      | gNB-DU         | Transport            | R15         | TS 38.470 / TS 33.501 §9.8      |                   |
| F1-U          | gNB-CU-UP      | gNB-DU         | Transport            | R15         | TS 38.470                       |                   |
| E1            | gNB-CU-CP      | gNB-CU-UP      | Transport            | R15         | TS 38.460                       |                   |
| Xn-C          | gNB            | gNB            | Transport            | R15         | TS 38.420                       |                   |
| Xn-U          | gNB            | gNB            | Transport            | R15         | TS 38.420                       |                   |
| X2            | eNB            | gNB            | Transport            | legacy      | TS 36.420                       | NSA only          |
| NWu           | UE             | N3IWF          | IKEv2/IPsec          | R15         | TS 23.501 §4.2.8 / TS 33.501 §7 |                   |
| Y1            | UE             | TNAN           | L2                   | R16         | TS 23.501 §4.2.8.2              |                   |
| Y2            | TNAN           | TNGF           | L3                   | R16         | TS 23.501 §4.2.8.2              |                   |
| Yt            | UE             | TNGF           | IKEv2                | R16         | TS 23.501                       |                   |
| W-AGF         | Residential GW | 5GC            | Transport            | R16         | TS 23.501 / BBF TR-470          |                   |
| PC5           | UE             | UE             | Sidelink             | R16         | TS 23.287 / TS 33.503           |                   |

## Management & O-RAN

| **Interface** | **Endpoint A** | **Endpoint B**      | **Layer / protocol** | **Release** | **Workbook spec ref**       | **Workbook note**                      |
|---------------|----------------|---------------------|----------------------|-------------|-----------------------------|----------------------------------------|
| O1            | NF             | SMO                 | Mgmt                 | R15+        | O-RAN.WG10.O1-Interface     |                                        |
| O2            | SMO            | O-Cloud             | Mgmt                 | R16+        | O-RAN.WG6.O2                |                                        |
| A1            | Non-RT RIC     | Near-RT RIC         | Policy               | R16+        | O-RAN.WG2.A1AP              |                                        |
| E2            | Near-RT RIC    | E2 Node (gNB-CU/DU) | Control              | R16+        | O-RAN.WG3.E2                |                                        |
| Open FH       | O-DU           | O-RU                | L2 (eCPRI)           | R15+        | O-RAN.WG4.CUS / IEEE 1914.3 | Often unprotected in early deployments |
| OAM (vendor)  | EMS/NMS        | NFs                 | Mgmt                 | n/a         | vendor-specific             |                                        |
| CI/CD         | Pipeline       | NF targets          | Mgmt                 | n/a         | DevSecOps                   |                                        |
| SMO API       | SMO            | external orch/BSS   | API                  | n/a         | TM Forum APIs               |                                        |

## CAPIF

| **Interface** | **Endpoint A**    | **Endpoint B**   | **Layer / protocol** | **Release** | **Workbook spec ref** | **Workbook note** |
|---------------|-------------------|------------------|----------------------|-------------|-----------------------|-------------------|
| CAPIF-1       | API Invoker       | CAPIF Core       | Auth/discovery       | R16         | TS 23.222             |                   |
| CAPIF-1e      | API Invoker (ext) | CAPIF Core       | Auth/discovery       | R16         | TS 23.222             | External-facing   |
| CAPIF-2       | API Invoker       | AEF (NEF)        | API calls            | R16         | TS 23.222             |                   |
| CAPIF-2e      | API Invoker (ext) | AEF (NEF)        | API calls            | R16         | TS 23.222             |                   |
| CAPIF-3       | AEF               | CAPIF Core       | Logging/discovery    | R16         | TS 23.222             |                   |
| CAPIF-4       | APF (Publisher)   | CAPIF Core       | Publish              | R16         | TS 23.222             |                   |
| CAPIF-5       | AMF (API Mgmt)    | CAPIF Core       | Mgmt                 | R16         | TS 23.222             |                   |
| CAPIF-6       | CAPIF Core        | CAPIF Core       | Federation           | R16         | TS 23.222             |                   |
| CAPIF-7       | CAPIF Core        | CAPIF Core (ext) | Federation           | R16         | TS 23.222             |                   |

## IMS

| **Interface** | **Endpoint A** | **Endpoint B** | **Layer / protocol** | **Release** | **Workbook spec ref** | **Workbook note** |
|---------------|----------------|----------------|----------------------|-------------|-----------------------|-------------------|
| Gm            | UE (IMS)       | P-CSCF         | SIP                  | legacy/R15  | TS 23.228 / TS 33.203 | IMS AKA           |
| Mw            | P-CSCF         | S-CSCF/I-CSCF  | SIP                  | legacy/R15  | TS 23.228             |                   |
| Cx            | S-CSCF         | HSS/UDM        | Diameter             | legacy/R15  | TS 29.228             |                   |
| Sh            | AS             | HSS/UDM        | Diameter             | legacy/R15  | TS 29.328             |                   |
| ISC           | S-CSCF         | AS             | SIP                  | legacy/R15  | TS 23.228             |                   |
| Mb            | UE/Media       | MGW/MRFP       | RTP/SRTP             | legacy/R15  | TS 23.228             |                   |
| Ut            | UE             | AS             | HTTPS                | legacy/R15  | TS 23.228             |                   |
| Mp            | MGCF           | IMS-MGW        | H.248                | legacy      | TS 23.228             |                   |
| Mn            | IMS-AGW        | P-CSCF         | H.248                | legacy      | TS 23.228             |                   |

## EPS Interworking

| **Interface** | **Endpoint A** | **Endpoint B** | **Layer / protocol** | **Release** | **Workbook spec ref** | **Workbook note**    |
|---------------|----------------|----------------|----------------------|-------------|-----------------------|----------------------|
| S6a           | MME            | HSS            | Diameter             | legacy      | TS 29.272             | EPS-5GS interworking |
| S5            | S-GW           | P-GW           | GTP-C/U              | legacy      | TS 23.401             |                      |
| S8            | S-GW           | P-GW           | GTP-C/U              | legacy      | TS 23.401             |                      |
| S1-MME        | eNB            | MME            | S1AP                 | legacy      | TS 36.413             |                      |
| S1-U          | eNB            | S-GW           | GTP-U                | legacy      | TS 36.414             |                      |

## Lawful Intercept

| **Interface** | **Endpoint A** | **Endpoint B** | **Layer / protocol** | **Release** | **Workbook spec ref** | **Workbook note**                         |
|---------------|----------------|----------------|----------------------|-------------|-----------------------|-------------------------------------------|
| LI-X0         | ADMF           | LIPF           | Provisioning         | R15+        | TS 33.127 / TS 33.128 | Reveals targets — extreme confidentiality |
| LI-X1         | LIPF           | POI/TPF        | Provisioning         | R15+        | TS 33.127 / TS 33.128 |                                           |
| LI-X2         | POI            | MDF2           | IRI delivery         | R15+        | TS 33.127 / TS 33.128 |                                           |
| LI-X3         | POI            | MDF3           | CC delivery          | R15+        | TS 33.127 / TS 33.128 |                                           |
| HI-1          | ADMF           | LEMF           | Handover             | R15+        | ETSI TS 102 232       | Jurisdiction-controlled                   |
| HI-2          | MDF2           | LEMF           | Handover             | R15+        | ETSI TS 102 232       |                                           |
| HI-3          | MDF3           | LEMF           | Handover             | R15+        | ETSI TS 102 232       |                                           |

## Quantum Threat Type and Risk Classification

| **Quantum Threat Type**                 | **Description**                                                                      | **Cryptographic Exposure / Applicability**                                               | **Primary Security Impact**               | **HNDL Relevance**                               | **Quantum Risk Level**             |
|-----------------------------------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|-------------------------------------------|--------------------------------------------------|------------------------------------|
| Harvest-Now, Decrypt-Later (HNDL)       | Capture encrypted data now for future quantum decryption.                            | Quantum-vulnerable encryption or key establishment protecting long-lived sensitive data. | Confidentiality, privacy.                 | Primary HNDL threat.                             | Not Assessed / Framework Dependent |
| Quantum Decryption                      | Use a CRQC to break vulnerable cryptography and recover protected data.              | Mainly RSA, ECC and other factoring/discrete-log based cryptography.                     | Confidentiality, key exposure.            | Yes, where previously captured data is retained. | Not Assessed / Framework Dependent |
| Quantum Impersonation                   | Break signature or authentication mechanisms to impersonate a trusted entity.        | Public-key signatures, certificates and PKI authentication.                              | Authentication, integrity, trust.         | Limited / indirect.                              | Not Assessed / Framework Dependent |
| Quantum Man-in-the-Middle (QMITM)       | Compromise authentication or key establishment to intercept or alter communications. | Public-key authentication, signatures and key-establishment mechanisms.                  | Integrity, authenticity, confidentiality. | Indirect. Primarily an active attack.            | Not Assessed / Framework Dependent |
| Quantum Search / Symmetric-Key Exposure | Quantum search reduces the effective brute-force strength of symmetric keys.         | Symmetric algorithms such as AES; impact depends on key strength.                        | Confidentiality, integrity.               | Context dependent.                               | Not Assessed / Framework Dependent |

# Appendix D - Source Documents

| **Source**                                      | **Roadmap use**                                                                                                                                                       |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 3GPP TR 33.938 version 19.2.0 Release 19        | Cryptographic inventory baseline for 5G Standalone; provides protocol usage and identifies Lawful Interception as outside its scope.                                  |
| ATIS Telecom5G property taxonomy v1.0           | Existing 5G taxonomy used as the starting point for telecom terminology and current implementation experience.                                                        |
| ATIS 3GPP 5G Architecture CBOM profile v1.0     | Existing CycloneDX 1.7 implementation profile used as an input to the roadmap; the future Telecom CBOM conceptual model, and any separately governed formal semantic layer, are intended to remain independent of any one platform representation. |

