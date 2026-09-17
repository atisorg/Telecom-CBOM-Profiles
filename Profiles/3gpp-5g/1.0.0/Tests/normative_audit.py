#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
TESTS_DIR=Path(__file__).resolve().parent
PROFILE_ROOT=TESTS_DIR.parent
DOCUMENTS_DIR=PROFILE_ROOT/'Documents'
VALIDATION_DIR=PROFILE_ROOT/'Validation'
PROFILE=PROFILE_ROOT/'3GPP_5G_CBOM_Profile_CycloneDX1.7_v1.0.0.md'
TAXMD=PROFILE_ROOT/'atis-telecom5g-property-taxonomy-v1.0.0.md'
TAXJSON=PROFILE_ROOT/'atis-telecom5g-taxonomy-1.0.0.json' 

LOWER_MODAL=re.compile(r'\b(shall|must|should|may)\b')
SEMVER_RE=re.compile(r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$')

def md_property_rows(text:str):
    rows={}
    for line in text.splitlines():
        if not line.startswith('| `atis:telecom5g:'):
            continue
        cells=[c.strip() for c in line.strip('|').split('|')]
        if len(cells)>=5:
            rows[cells[0].strip('`')]={'description':cells[1],'value_type':cells[2],'cardinality':cells[3],'appliesTo':cells[4]}
    return rows

def run():
    fail=[]
    profile=PROFILE.read_text()
    taxmd=TAXMD.read_text()
    tax=json.loads(TAXJSON.read_text())

    # RFC 2119/RFC 8174 declaration must cover every keyword actually used.
    required=['**MUST**','**MUST NOT**','**SHOULD**','**SHOULD NOT**','**MAY**']
    kw_para=next((ln for ln in profile.splitlines() if 'RFC 2119' in ln and 'RFC 8174' in ln), '')
    for k in required:
        if k not in kw_para: fail.append(f'profile conformance-keyword clause missing {k}')
    if 'Lower-case modal verbs are descriptive' not in kw_para:
        fail.append('profile does not state lower-case modal verbs are non-normative')
    if 'Lower-case modal verbs are descriptive' not in taxmd:
        fail.append('taxonomy does not inherit/declare lower-case modal treatment')

    # Avoid accidental lower-case RFC-style modals in normative source documents.
    for label,text in [('profile',profile),('taxonomy',taxmd)]:
        for i,line in enumerate(text.splitlines(),1):
            if LOWER_MODAL.search(line):
                fail.append(f'{label}:{i}: lower-case modal verb can be mistaken for normative language: {line.strip()}')

    # Mandatory two-layer validation must be stated consistently with section 1.
    if 'MUST be validated in two layers' not in profile:
        fail.append('profile validation section is not mandatory')
    if 'the CBOM MUST validate against the official CycloneDX 1.7 BOM schema' not in profile:
        fail.append('profile does not make official CycloneDX schema validation mandatory')
    if 'the CBOM MUST satisfy the ATIS `atis:telecom5g:*`' not in profile:
        fail.append('profile does not make ATIS-layer normative requirements mandatory')

    # SDO blocker closure: formal references, artifact authority, and scope-closure definition.
    for token in ('### 3.1 Normative references','[CDX-1.7]','[RFC2119]','[RFC8174]','[3GPP-TR33938]','[3GPP-TS33501]','[SEMVER]'):
        if token not in profile: fail.append(f'profile missing normative reference/status token {token}')
    if '## 6. Normative artifacts, reference tooling, and precedence' not in profile:
        fail.append('profile missing normative artifact authority/precedence clause')
    for phrase in ('This profile is authoritative for profile-level modeling', 'human-readable taxonomy is authoritative for ATIS property names', 'reference tooling and informative test material', 'An implementation MAY use any validator'):
        if phrase not in profile: fail.append(f'profile artifact/tooling authority wording missing: {phrase}')
    if 'inventory scope closure' not in profile or 'least fixed-point set' not in profile or 'all matching detailed objects are included' not in profile:
        fail.append('profile does not precisely define inventoryScopeRef fixed-point scope closure')
    if 'Semantic Versioning 2.0.0' not in profile or '1.0.0' not in profile:
        fail.append('profile does not declare SemVer 2.0.0 use for final version')
    # Retained SDO-major cleanup: defined terminology, abbreviations, source traceability, and PQC non-requirement.
    for heading in ('## 4. Terms and definitions','## 5. Abbreviations'):
        if heading not in profile: fail.append(f'profile missing publication structure: {heading}')
    for term in ('reified binding','inventory scope root','inventory scope closure','summary/index property','effective state','strict conformance'):
        if f'**{term}**' not in profile: fail.append(f'profile missing defined term: {term}')
    for abbr in ('CBOM','BOM','SBOM','HBOM','NF','5GS','SBI','PKI','PQC','CRQC','KDF','PRINS'):
        if f'| {abbr} |' not in profile: fail.append(f'profile abbreviations clause missing {abbr}')
    if 'Architecture-vocabulary source traceability' not in profile:
        fail.append('profile missing architecture-vocabulary source traceability clause')
    for src in ('3GPP TS 23.501','3GPP TS 38.401','3GPP TS 38.423','3GPP TS 38.470','3GPP TS 38.460','3GPP TS 33.220','3GPP TS 29.522','3GPP TS 29.509','3GPP TS 29.503'):
        if src not in profile: fail.append(f'profile missing architecture/service source traceability: {src}')
    if 'This profile does not define or require a PQC/CRQC exposure or risk assessment.' not in profile:
        fail.append('PQC/QSC clause still implies a reproducibility requirement without a defined methodology')
    if not tax.get('architecture_source_references') or not tax.get('canonical_binding_sources') or not tax.get('entity_type_sources'):
        fail.append('machine taxonomy missing architecture vocabulary source traceability metadata')
    if not tax.get('terms_and_definitions') or not tax.get('abbreviations'):
        fail.append('machine taxonomy missing terms/abbreviations metadata')

    if not SEMVER_RE.fullmatch(tax.get('version','')):
        fail.append(f'machine taxonomy version is not valid SemVer 2.0.0 syntax: {tax.get("version")!r}')
    if tax.get('profileMarker','').rsplit('/',1)[-1] != tax.get('version'):
        fail.append('profile marker version and taxonomy version diverge')
    status=tax.get('artifact_status_and_precedence',{})
    if not status or 'not normative' not in status.get('pythonTooling',''):
        fail.append('machine taxonomy does not identify Python tooling as non-normative reference implementation')
    scope_closure=(tax.get('inventory_completeness_semantics') or {}).get('scopeClosure',{})
    if not scope_closure or 'least fixed-point' not in scope_closure.get('definition','') or not scope_closure.get('multipleMatches'):
        fail.append('machine taxonomy missing precise inventory scope-closure semantics')

    # A represented architectural binding has one normative representation.
    if 'When an architectural binding/interface is represented using this profile, it MUST be reified as a CycloneDX service' not in profile:
        fail.append('profile leaves binding representation form ambiguous')
    if 'When an architectural binding/interface is represented using this profile, it MUST be represented as a reified CycloneDX service' not in taxmd:
        fail.append('taxonomy leaves binding representation form ambiguous')

    # Human and machine cardinalities must agree exactly for exact properties.
    mdrows=md_property_rows(taxmd)
    for prop in tax.get('properties',[]):
        name=prop['name']
        if name in mdrows and mdrows[name]['cardinality']!=prop.get('cardinality'):
            fail.append(f'cardinality mismatch {name}: Markdown={mdrows[name]["cardinality"]!r}, JSON={prop.get("cardinality")!r}')
    for n in ('atis:telecom5g:binding','atis:telecom5g:bindingType'):
        p=next(x for x in tax['properties'] if x['name']==n)
        if p.get('cardinality')!='MUST appear once per reified binding':
            fail.append(f'{n} machine cardinality is not mandatory per reified binding')

    # Migration-only properties must never carry strict-mode SHOULD guidance.
    for p in tax['properties']:
        if p.get('deprecated') or p.get('strictConformance')=='prohibited':
            if 'MUST NOT appear in a strict v1.0.0 CBOM' not in p.get('description',''):
                fail.append(f'{p["name"]}: migration-only machine description does not state strict prohibition')
            if p.get('cardinality','') != 'MUST NOT appear in strict v1.0.0':
                fail.append(f'{p["name"]}: migration-only cardinality can be misread as permission in strict mode: {p.get("cardinality")!r}')
    for n in ('nfType','interface','interfaces','assertion','usageContext'):
        token=f'atis:telecom5g:{n}'
        lines=[ln for ln in taxmd.splitlines() if f'`{token}`' in ln and ln.startswith('|')]
        if not lines or 'MUST NOT appear in a strict v1.0.0 CBOM' not in lines[0]:
            fail.append(f'{token}: Markdown property row does not state strict prohibition')

    # Retained publication cleanup: normative/tooling separation, package notice, and CycloneDX namespace coordination.
    if 'Migration tooling MAY' in profile or re.search(r'MAY appear (?:once|multiple times) in migration mode', taxmd):
        fail.append('migration-tool behavior remains normative instead of informative')
    if 'implementation package SHOULD' in profile:
        fail.append('implementation-package test guidance remains normative')
    for fn in ('MIGRATION_GUIDE.md','IPR_AND_LICENSE_NOTICE.md','CYCLONEDX_PROPERTY_TAXONOMY_COORDINATION.md'):
        if not (DOCUMENTS_DIR/fn).exists(): fail.append(f'publication-cleanup artifact missing: {fn}')
    if not (VALIDATION_DIR/'cyclonedx_property_taxonomy_manifest.json').exists(): fail.append('publication-cleanup artifact missing: cyclonedx_property_taxonomy_manifest.json')
    if '(Draft v' in profile or '(Draft v' in taxmd:
        fail.append('final normative artifacts still carry a Draft designation')
    if '(Version 1.0.0)' not in profile.splitlines()[0] or '(Version 1.0.0)' not in taxmd.splitlines()[0]:
        fail.append('final Version 1.0.0 designation missing from normative artifact titles')
    if 'Release Candidate' in profile.splitlines()[0] or 'Release Candidate' in taxmd.splitlines()[0]:
        fail.append('final normative artifact title still carries a release-candidate designation')

    # Summary-backed protocol/algorithm detail must be native because normalization rules depend on native fields.
    if 'A protocol or algorithm asset used as the detailed representation that backs an ATIS' not in profile or '**MUST** be modeled as a CycloneDX `components[]` object' not in profile:
        fail.append('profile does not make native detailed backing representation mandatory')
    if 'A protocol or algorithm asset that backs these summaries MUST use the applicable native CycloneDX cryptographic-asset representation.' not in taxmd:
        fail.append('taxonomy does not make native detailed backing representation mandatory')

    if fail:
        print('NORMATIVE AUDIT FAILED')
        for x in fail: print(' -',x)
        return 1
    print('NORMATIVE AUDIT PASSED')
    print('  RFC 2119/RFC 8174 keyword declaration: complete')
    print('  Lower-case modal ambiguity: none')
    print('  Mandatory two-layer validation wording: aligned')
    print('  Normative references + artifact authority/precedence: aligned')
    print('  inventoryScopeRef fixed-point closure: aligned')
    print('  SemVer 1.0.0 stable-release declaration: aligned')
    print('  Publication/tooling separation: aligned')
    print('  Terms/definitions + abbreviations: aligned')
    print('  Architecture/service source traceability: aligned')
    print('  PQC/QSC methodology wording: informative/non-normative')
    print('  Binding representation conditionality: aligned')
    print('  Markdown/machine cardinality alignment: passed')
    print('  Migration-only strict prohibitions: aligned')
    print('  Native backing representation requirement: aligned')
    return 0

if __name__=='__main__': raise SystemExit(run())
