#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, tempfile, copy
from pathlib import Path
import jsonschema
TESTS_DIR=Path(__file__).resolve().parent
PROFILE_ROOT=TESTS_DIR.parent
VALIDATION_DIR=PROFILE_ROOT/'Validation'
DOCUMENTS_DIR=PROFILE_ROOT/'Documents'
VALID_DIR=PROFILE_ROOT/'Examples'/'Valid'
INVALID_DIR=PROFILE_ROOT/'Examples'/'Invalid'
TAX=PROFILE_ROOT/'atis-telecom5g-taxonomy-1.0.0.json'; SCHEMA=PROFILE_ROOT/'atis-telecom5g-profile-1.0.0.schema.json'
VALID=[VALID_DIR/'CBOM_AMF_N2_vendor_services_v1.0.0_VALID.json',VALID_DIR/'CBOM_SEPP_N32_deployed_services_v1.0.0_VALID.json',VALID_DIR/'CBOM_UDM_5G_AKA_vendor_v1.0.0_VALID.json']
INVALID=list(sorted(INVALID_DIR.glob('CBOM_INVALID_*_v1.0.0.json')))

def vals(obj,name): return [p['value'] for p in obj.get('properties',[]) if p.get('name')==name]
def helper(paths, extra=None):
    cmd=[sys.executable,str(VALIDATION_DIR/'validate_atis_cbom.py'),str(TAX)]
    if extra: cmd+=extra
    cmd += [str(x) for x in paths]
    return subprocess.run(cmd,capture_output=True,text=True)
def tempdoc(d):
    t=tempfile.NamedTemporaryFile('w',suffix='.json',delete=False)
    json.dump(d,t); t.close(); return Path(t.name)

def run():
    fail=[]; alljson=[TAX,SCHEMA,*VALID,*INVALID]
    for p in alljson:
        try: json.loads(p.read_text())
        except Exception as e: fail.append(f'{p.name}: JSON parse failed: {e}')
    tax=json.loads(TAX.read_text()); schema=json.loads(SCHEMA.read_text())
    try: jsonschema.Draft7Validator.check_schema(schema)
    except Exception as e: fail.append(f'overlay schema invalid Draft 7: {e}')
    na=subprocess.run([sys.executable,str(TESTS_DIR/'normative_audit.py')],capture_output=True,text=True)
    if na.returncode: fail.append('normative-language audit failed:\n'+na.stdout+na.stderr)
    sdo=subprocess.run([sys.executable,str(TESTS_DIR/'sdo_reviewer_audit.py'),'--fail-on','info'],capture_output=True,text=True)
    if sdo.returncode or any(x not in sdo.stdout for x in ('BLOCKER: 0','MAJOR: 0','MINOR: 0','INFO: 0')):
        fail.append('SDO final-release audit failed:\n'+sdo.stdout+sdo.stderr)
    ov=jsonschema.Draft7Validator(schema['allOf'][1])
    for p in VALID:
        errs=list(ov.iter_errors(json.loads(p.read_text())))
        if errs: fail.append(f'{p.name}: ATIS overlay errors: {[e.message for e in errs]}')
    # Strict overlay must reject exact/dotted legacy syntax and service-level cryptographyClass.
    for p in [INVALID_DIR/'CBOM_INVALID_deprecated_property_strict_v1.0.0.json',INVALID_DIR/'CBOM_INVALID_legacy_dotted_strict_v1.0.0.json',INVALID_DIR/'CBOM_INVALID_cryptographyClass_on_binding_v1.0.0.json']:
        if not list(ov.iter_errors(json.loads(p.read_text()))): fail.append(f'{p.name}: strict overlay unexpectedly accepted prohibited placement/syntax')
    q=helper(VALID)
    if q.returncode: fail.append('helper rejected valid examples:\n'+q.stdout+q.stderr)
    if 'PASS ATIS-LAYER' not in q.stdout or 'does not establish strict v1.0.0 conformance' not in q.stdout:
        fail.append('validator output does not distinguish ATIS-layer PASS from full strict conformance when official schema is omitted')
    for p in INVALID:
        q=helper([p])
        if q.returncode==0: fail.append(f'helper unexpectedly accepted {p.name}')

    profile=(PROFILE_ROOT/'3GPP_5G_CBOM_Profile_CycloneDX1.7_v1.0.0.md').read_text()
    md=(PROFILE_ROOT/'atis-telecom5g-property-taxonomy-v1.0.0.md').read_text()
    for prop in tax['properties']:
        if f"`{prop['name']}`" not in md: fail.append(f'Markdown taxonomy missing {prop["name"]}')

    # Retain v0.97 conformance-closure checks (#1-#6).
    cb=next(p for p in tax['properties'] if p['name']=='atis:telecom5g:cbom.scope')
    if cb['cardinality']!='MUST appear once': fail.append('cbom.scope is not mandatory')
    if 'inventoryScopeRef' not in profile: fail.append('profile missing explicit completeness roots')
    if not tax.get('protocol_normalization'): fail.append('protocol normalization missing')
    if not tax.get('canonical_algorithm_identities'): fail.append('selected algorithm identity registry missing')
    deprecated=[p for p in tax['properties'] if p.get('deprecated')]
    if not deprecated or any(p.get('strictConformance')!='prohibited' for p in deprecated): fail.append('deprecated properties not prohibited in strict conformance')

    # 1.0.0 SDO blocker closure: references, artifact authority, and precise scope closure.
    if not tax.get('normative_references'): fail.append('machine taxonomy missing normative references metadata')
    ast=tax.get('artifact_status_and_precedence',{})
    if 'not normative' not in ast.get('pythonTooling',''): fail.append('Python tooling not marked non-normative reference implementation')
    scope_sem=(tax.get('inventory_completeness_semantics') or {}).get('scopeClosure',{})
    if not scope_sem.get('steps') or not scope_sem.get('multipleMatches'): fail.append('machine taxonomy missing fixed-point/multiple-match scope closure semantics')
    # The reference checker must include edge-less MILENAGE/TUAK alternatives in an entity-rooted closure.
    d=json.loads(VALID[2].read_text())
    for mp in d['metadata']['properties']:
        if mp['name']=='atis:telecom5g:inventoryCompleteness': mp['value']='complete'
    d['metadata']['properties'].append({'name':'atis:telecom5g:inventoryScopeRef','value':'nf:UDM'})
    tmp=tempdoc(d); q=helper([tmp],extra=['--show-scope-closure']); tmp.unlink(missing_ok=True)
    if q.returncode: fail.append('reference checker rejected temporary complete UDM scope:\n'+q.stdout+q.stderr)
    for ref in ['nf:UDM','binding:nf:UDM:Nudm_UEAuthentication','crypto/protocol/5g-aka','crypto/alg/milenage','crypto/alg/tuak','crypto/alg/hmac-sha-256-kdf']:
        if ref not in q.stdout: fail.append(f'scope closure output omitted {ref}')

    # #7 cryptographyClass is algorithm-component-only; hybrid is a construction, not aggregate binding state.
    cc=next(p for p in tax['properties'] if p['name']=='atis:telecom5g:cryptographyClass')
    if cc['appliesTo']!=['component']: fail.append('cryptographyClass is not component-only')
    if 'atis:telecom5g:cryptographyClass' not in tax.get('semantic_placement_rules',{}).get('algorithmComponentOnly',[]): fail.append('cryptographyClass missing algorithmComponentOnly semantic rule')
    if 'mere coexistence of symmetric and asymmetric algorithms' not in profile: fail.append('profile missing non-aggregate hybrid semantics')

    # #8 free-form crypto summaries are noncanonical labels, native representation is normalization authority.
    ss=tax.get('cryptography_summary_semantics',{})
    if ss.get('status')!='noncanonical display/index labels': fail.append('machine taxonomy does not mark crypto summary strings noncanonical')
    if 'noncanonical display/index labels' not in profile: fail.append('profile missing noncanonical crypto summary semantics')
    if 'canonical cross-vendor algorithm identifiers' not in profile: fail.append('profile missing warning against treating crypto summary strings as canonical identifiers')

    # #9 consistency checks: dedicated negative fixtures must exist and fail (already run); machine semantics must declare them.
    dfr=tax.get('duplicate_fact_consistency',{})
    if 'native detailed representation is authoritative' not in dfr.get('authority',''): fail.append('machine taxonomy missing duplicate-fact native authority rule')
    for n in ['CBOM_INVALID_pki_mutual_conflict_v1.0.0.json','CBOM_INVALID_keyLength_native_mismatch_v1.0.0.json','CBOM_INVALID_curve_native_mismatch_v1.0.0.json']:
        if not (INVALID_DIR/n).exists(): fail.append(f'missing duplicate-fact negative fixture {n}')
    if 'pki.authenticationMode = mutual' not in profile: fail.append('profile missing explicit PKI/SBI consistency example')

    # #10 baselineRelease default and object 3gppSpecRelease override. Deliberate mismatch must pass.
    rs=tax.get('release_semantics',{})
    if 'overrides' not in rs.get('precedence',''): fail.append('machine taxonomy missing release precedence')
    d=json.loads(VALID[0].read_text())
    # AMF already has Rel-17; set BOM default to Rel-15 and object override to Rel-19.
    next(p for p in d['metadata']['properties'] if p['name']=='atis:telecom5g:baselineRelease')['value']='Rel-15'
    ent=next(s for s in d['services'] if vals(s,'atis:telecom5g:entityType'))
    next(p for p in ent['properties'] if p['name']=='atis:telecom5g:3gppSpecRelease')['value']='Rel-19'
    tmp=tempdoc(d); q=helper([tmp]); tmp.unlink(missing_ok=True)
    if q.returncode: fail.append('object-level 3gppSpecRelease override was incorrectly rejected:\n'+q.stdout)
    if 'explicit object-level override' not in profile: fail.append('profile missing release override wording')

    # #11 effective timestamp means snapshot-as-of time.
    es=tax.get('effective_snapshot_semantics',{})
    if 'as-of time' not in es.get('timestamp',''): fail.append('machine taxonomy missing effective snapshot-time semantics')
    if 'as-of time of the effective-state snapshot' not in profile: fail.append('profile missing effective snapshot timestamp semantics')
    sepp=json.loads(VALID[1].read_text())
    if not sepp.get('metadata',{}).get('timestamp'): fail.append('deployed effective positive example lacks metadata.timestamp')

    # #12 every reified binding has direct represented-entity association.
    ba=tax.get('binding_association_semantics',{})
    if 'dependency target of at least one represented entity' not in ba.get('rule',''): fail.append('machine taxonomy missing binding/entity association rule')
    for vp in VALID:
        d=json.loads(vp.read_text()); deps={x['ref']:set(x.get('dependsOn',[])) for x in d.get('dependencies',[])}
        entities=[s for s in d.get('services',[]) if vals(s,'atis:telecom5g:entityType')]
        bindings=[s for s in d.get('services',[]) if vals(s,'atis:telecom5g:binding')]
        entity_refs=[e.get('bom-ref') for e in entities if e.get('bom-ref')]
        for b in bindings:
            br=b.get('bom-ref')
            if not br: fail.append(f'{vp.name}: binding lacks bom-ref')
            elif not any(br in deps.get(er,set()) for er in entity_refs): fail.append(f'{vp.name}: binding {br} lacks direct entity association')
    if 'at least one represented entity MUST list the binding' not in profile: fail.append('profile missing normative direct entity-to-binding association')

    # Retained SDO major-finding closures.
    for heading in ('## 4. Terms and definitions','## 5. Abbreviations'):
        if heading not in profile: fail.append(f'RC package missing {heading}')
    if 'Architecture-vocabulary source traceability' not in profile: fail.append('RC package missing architecture vocabulary source traceability')
    for src in ('3GPP TS 23.501','3GPP TS 38.401','3GPP TS 38.423','3GPP TS 38.470','3GPP TS 38.460','3GPP TS 33.220','3GPP TS 29.522','3GPP TS 29.509','3GPP TS 29.503'):
        if src not in profile: fail.append(f'RC package missing source traceability for {src}')
    if 'This profile does not define or require a PQC/CRQC exposure or risk assessment.' not in profile: fail.append('RC package PQC/QSC wording still normative without methodology')
    if not tax.get('canonical_binding_sources') or not tax.get('entity_type_sources'): fail.append('RC machine source traceability missing')
    if not tax.get('terms_and_definitions') or not tax.get('abbreviations'): fail.append('RC machine terms/abbreviations metadata missing')

    # Retain publication cleanup and verify final Version 1.0.0 designation.
    for fn in ('IPR_AND_LICENSE_NOTICE.md','CYCLONEDX_PROPERTY_TAXONOMY_COORDINATION.md','cyclonedx_property_taxonomy_manifest.json','MIGRATION_GUIDE.md'):
        if not ((VALIDATION_DIR/fn).exists() if fn=='cyclonedx_property_taxonomy_manifest.json' else (DOCUMENTS_DIR/fn).exists()): fail.append(f'RC package missing publication-cleanup artifact {fn}')
    if 'implementation package SHOULD' in profile: fail.append('RC package still normatively constrains implementation package tests')
    if 'Migration tooling MAY' in profile or 'MAY appear once in migration mode' in md or 'MAY appear multiple times in migration mode' in md:
        fail.append('RC package still expresses migration-tool behavior normatively')
    if '(Draft v' in profile.splitlines()[0] or '(Draft v' in md.splitlines()[0]: fail.append('final normative artifact still carries Draft designation')
    if '(Version 1.0.0)' not in profile.splitlines()[0] or '(Version 1.0.0)' not in md.splitlines()[0]: fail.append('final Version 1.0.0 designation missing from normative artifacts')
    if 'Release Candidate' in profile.splitlines()[0] or 'Release Candidate' in md.splitlines()[0]: fail.append('final normative artifact still carries release-candidate designation')
    reg=json.loads((VALIDATION_DIR/'cyclonedx_property_taxonomy_manifest.json').read_text())
    if reg.get('namespace')!='atis:telecom5g' or len(reg.get('properties',[]))!=len(tax.get('properties',[])):
        fail.append('CycloneDX coordination manifest is not synchronized with machine taxonomy')

    # Final-release tooling integration: the one-command runner invokes the independent native
    # CycloneDX CLI with the exact 1.7 validation arguments for all three positives.
    import importlib.util
    spec=importlib.util.spec_from_file_location('qscii_runner', TESTS_DIR/'run_qscii_checks.py')
    runner=importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
    if runner.VERSION!='1.0.0': fail.append('QSCII runner version is not 1.0.0')
    sv=tax.get('semantic_versioning',{})
    if sv.get('version')!='1.0.0' or sv.get('preRelease') is not False:
        fail.append('machine taxonomy does not identify 1.0.0 as a stable SemVer release')
    if runner.resolve_cyclonedx(str(Path(sys.executable))) is None: fail.append('QSCII runner explicit executable override is not resolvable')
    calls=[]
    class FakeResult:
        def __init__(self, code=0, out=''):
            self.returncode=code; self.stdout=out; self.stderr=''
    original_run=runner.subprocess.run
    try:
        def fake_pass(cmd, **kwargs):
            calls.append(cmd)
            if '--version' in cmd: return FakeResult(0,'CycloneDX CLI 0.31.0')
            return FakeResult(0,'BOM validated successfully.')
        runner.subprocess.run=fake_pass
        if not runner.run_native_cyclonedx('cyclonedx-test', quiet=True): fail.append('QSCII runner native CycloneDX pass path failed')
        validate_calls=[c for c in calls if len(c)>1 and c[1]=='validate']
        if len(validate_calls)!=3: fail.append(f'QSCII runner invoked native validator {len(validate_calls)} times instead of 3')
        for c in validate_calls:
            required=['--input-format','json','--input-version','v1_7','--fail-on-errors']
            if any(x not in c for x in required): fail.append('QSCII runner native command missing required CycloneDX 1.7 validation arguments')
        def fake_fail(cmd, **kwargs):
            if '--version' in cmd: return FakeResult(0,'CycloneDX CLI test')
            return FakeResult(1,'validation failed') if 'CBOM_SEPP' in ' '.join(cmd) else FakeResult(0,'ok')
        runner.subprocess.run=fake_fail
        if runner.run_native_cyclonedx('cyclonedx-test', quiet=True): fail.append('QSCII runner native failure path incorrectly returned PASS')
    finally:
        runner.subprocess.run=original_run
    runner_text=(TESTS_DIR/'run_qscii_checks.py').read_text()
    for marker in ('STRICT TWO-LAYER VALIDATION: PASS','STRICT TWO-LAYER VALIDATION: NOT ESTABLISHED','--require-cyclonedx','CYCLONEDX_CLI'):
        if marker not in runner_text: fail.append(f'QSCII runner missing integrated-native-validation marker: {marker}')

    # Core semantic regressions retained.
    udm=json.loads(VALID[2].read_text())
    dep=next(x for x in udm['dependencies'] if x['ref']=='crypto/protocol/5g-aka')
    if {'crypto/alg/milenage','crypto/alg/tuak'} & set(dep['dependsOn']): fail.append('5G-AKA falsely depends conjunctively on MILENAGE/TUAK')
    if 'other' in tax['controlled_vocabularies']['securityConstructType']: fail.append('securityConstructType other returned')
    if 'other' in tax['controlled_vocabularies']['protectionContext']: fail.append('protectionContext other returned')
    if 'cryptoType' in tax['controlled_vocabularies']: fail.append('removed cryptoType returned')

    if fail:
        print('TESTS FAILED'); [print(' -',x) for x in fail]; return 1
    print('ALL 1.0.0 FINAL-RELEASE TESTS PASSED')
    print(f'  JSON parse: {len(alljson)} files')
    print('  Draft-07 strict ATIS overlay schema: valid')
    print(f'  Positive CBOM examples: {len(VALID)} passed')
    print(f'  Negative examples: {len(INVALID)} correctly rejected')
    print('  Retained v0.97 conformance closure (#1-#6): passed')
    print('  #7 algorithm-only cryptographyClass + hybrid semantics: passed')
    print('  #8 noncanonical crypto summary labels/native normalization authority: passed')
    print('  #9 duplicate-fact consistency rules: passed')
    print('  #10 baselineRelease/object-release override semantics: passed')
    print('  #11 effective-state snapshot timestamp semantics: passed')
    print('  #12 mandatory entity association for reified bindings: passed')
    print('  RFC 2119/RFC 8174 normative-language audit: passed')
    print('  SDO publication audit: 0 blockers / 0 major / 0 minor / 0 informational')
    print('  Normative references + artifact authority/precedence: passed')
    print('  inventoryScopeRef fixed-point closure + reference output: passed')
    print('  SemVer 1.0.0 transition: passed')
    print('  Terms/definitions + abbreviations: passed')
    print('  Architecture/service source traceability: passed')
    print('  Vague normative-condition cleanup: passed')
    print('  PQC/QSC methodology wording: passed')
    print('  IPR/license packaging notice: passed')
    print('  CycloneDX property-taxonomy coordination package: passed')
    print('  Informative example/test + migration guidance separation: passed')
    print('  Final Version 1.0.0 designation: passed')
    print('  Markdown/machine cardinality alignment: passed')
    print('  Validator PASS/full-conformance messaging distinction: passed')
    print('  Integrated native CycloneDX CLI runner invocation: passed')
    print('  Strict two-layer vs ATIS-only result distinction: passed')
    return 0
if __name__=='__main__': raise SystemExit(run())
