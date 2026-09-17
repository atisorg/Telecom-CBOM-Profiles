#!/usr/bin/env python3
"""ATIS telecom5g CBOM v1.0.0 reference profile-validation helper.

This non-normative helper performs the ATIS profile layer. Full strict v1.0.0 conformance also
requires validation against the official CycloneDX 1.7 schema. The integrated
run_qscii_checks.py runner can invoke an independently installed CycloneDX CLI; alternatively,
provide --cyclonedx-schema to this helper to run a supplied official schema in the same invocation.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from collections import Counter, deque

PROTOCOL_TYPES={"tls","ssh","ipsec","ike","sstp","wpa","dtls","quic","eap-aka","eap-aka-prime","prins","5g-aka","other","unknown"}
PRIMITIVES={"drbg","mac","block-cipher","stream-cipher","signature","hash","pke","xof","kdf","key-agree","kem","ae","combiner","key-wrap","other","unknown"}
KNOWN_ALGORITHM_FAMILIES={"AES","HMAC","SHA-1","SHA-2","SHA-3","ECDH","ECDSA","ECIES","MILENAGE","TUAK","SNOW3G","ZUC","ML-KEM","ML-DSA","SLH-DSA","RSAES-OAEP","RSAES-PKCS1","RSASSA-PKCS1","RSASSA-PSS","HKDF","SP800-108","IKE-PRF","CMAC","3GPP-XOR"}


def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def compile_taxonomy(tax):
    exact={p['name']:p for p in tax['properties']}
    patterns=[(re.compile(pp['pattern']),pp) for pp in tax.get('pattern_properties',[])]
    return exact,patterns

def match_tax_property(name,exact,patterns):
    if name in exact: return exact[name]
    for rx,pp in patterns:
        if rx.fullmatch(name): return pp
    return None

def check_value(value,rule):
    spec=rule.get('value',{})
    if not isinstance(value,str): return f"value must be string, got {type(value).__name__}"
    if 'enum' in spec and value not in spec['enum']: return f"value {value!r} not in enum {spec['enum']}"
    if 'pattern' in spec and re.fullmatch(spec['pattern'],value) is None: return f"value {value!r} does not match {spec['pattern']!r}"
    return None

def walk_properties(doc):
    for item in (doc.get('metadata') or {}).get('properties',[]) or []: yield 'metadata','metadata',doc.get('metadata'),item
    for i,obj in enumerate(doc.get('services',[]) or []):
        for item in obj.get('properties',[]) or []: yield 'service',f'services[{i}]',obj,item
    for i,obj in enumerate(doc.get('components',[]) or []):
        for item in obj.get('properties',[]) or []: yield 'component',f'components[{i}]',obj,item

def pvals(obj,name): return [p.get('value') for p in obj.get('properties',[]) or [] if p.get('name')==name]
def has_prop(obj,name): return bool(pvals(obj,name))
def norm_identifier(value): return re.sub(r'[^A-Za-z0-9]+','',value).lower()

def canonical_curve(value):
    if not isinstance(value,str): return None
    v=value.strip().lower()
    aliases={
        'p-256':'P-256','secp256r1':'P-256','prime256v1':'P-256',
        'p-384':'P-384','secp384r1':'P-384',
        'p-521':'P-521','secp521r1':'P-521',
        'x25519':'X25519','x448':'X448'
    }
    if v in aliases: return aliases[v]
    for token,canon in [('p-256','P-256'),('p-384','P-384'),('p-521','P-521'),('x25519','X25519'),('x448','X448')]:
        if token in v: return canon
    return None

def native_key_size_bits(algorithm_properties):
    if not isinstance(algorithm_properties,dict): return None
    fam=algorithm_properties.get('algorithmFamily'); ps=algorithm_properties.get('parameterSetIdentifier')
    if fam=='AES' and isinstance(ps,str) and ps.isdigit(): return ps
    if fam in {'ECDH','ECDSA','ECIES'}:
        c=canonical_curve(ps)
        if c and c.startswith('P-'): return c.split('-',1)[1]
    return None

def graph_descendants(start,deps):
    seen=set(); q=deque(deps.get(start,[]))
    while q:
        x=q.popleft()
        if x in seen: continue
        seen.add(x); q.extend(deps.get(x,[]))
    return seen

def detailed_indexes(components):
    protocols={}; constructs={}; crypto={}
    for c in components:
        ref=c.get('bom-ref')
        if not ref: continue
        cp=c.get('cryptoProperties') or {}; at=cp.get('assetType')
        sc=pvals(c,'atis:telecom5g:securityConstruct')
        if at=='protocol' and not sc and isinstance(c.get('name'),str): protocols[ref]={c['name']}
        if sc: constructs[ref]=set(sc)
        vals=set()
        if at=='algorithm' and isinstance(c.get('name'),str): vals.add(c['name'])
        pp=cp.get('protocolProperties') or {}
        for suite in pp.get('cipherSuites',[]) or []:
            if isinstance(suite,dict) and isinstance(suite.get('name'),str): vals.add(suite['name'])
        if vals: crypto[ref]=vals
    return protocols,constructs,crypto

def reverse_detailed_index(index):
    out={}
    for ref,values in index.items():
        for value in values:
            out.setdefault(value,set()).add(ref)
    return out

def compute_inventory_scope_closure(doc,tax,scope_refs=None):
    """Compute the profile-defined inventory scope closure for inspection/audit.

    This is reference-tooling behavior, not the normative definition itself. The
    normative definition is in the profile. It implements the least fixed-point
    closure over declared roots, dependency reachability, and summary-backed
    detailed assets.
    """
    objects=[]
    for placement,coll in [('service',doc.get('services',[]) or []),('component',doc.get('components',[]) or [])]:
        for obj in coll:
            if obj.get('bom-ref'): objects.append((placement,obj))
    refmap={obj['bom-ref']:obj for _,obj in objects}
    roles={obj['bom-ref']:semantic_roles(obj,placement,tax) for placement,obj in objects}
    deps={d.get('ref'):set(d.get('dependsOn',[]) or []) for d in doc.get('dependencies',[]) or [] if d.get('ref')}
    if scope_refs is None:
        mdprops=(doc.get('metadata') or {}).get('properties',[]) or []
        scope_refs=[x.get('value') for x in mdprops if isinstance(x,dict) and x.get('name')=='atis:telecom5g:inventoryScopeRef' and isinstance(x.get('value'),str)]
    components=doc.get('components',[]) or []
    prot_idx,construct_idx,crypto_idx=detailed_indexes(components)
    rev_protocol=reverse_detailed_index(prot_idx); rev_construct=reverse_detailed_index(construct_idx); rev_crypto=reverse_detailed_index(crypto_idx)
    closure={r for r in scope_refs if r in refmap}
    changed=True
    while changed:
        changed=False
        for ref in list(closure):
            # Generic dependency reachability.
            for target in deps.get(ref,set()):
                if target in refmap and target not in closure:
                    closure.add(target); changed=True
            obj=refmap.get(ref)
            if obj is None: continue
            rr=roles.get(ref,set())
            summary_specs=[]
            if 'entity' in rr:
                summary_specs += [
                    ('atis:telecom5g:crypto.supportedProtocols',rev_protocol),
                    ('atis:telecom5g:crypto.supportedConstructs',rev_construct),
                    ('atis:telecom5g:crypto.supportedCryptography',rev_crypto),
                ]
            if 'binding' in rr:
                summary_specs += [
                    ('atis:telecom5g:protocol',rev_protocol),
                    ('atis:telecom5g:effectiveProtocol',rev_protocol),
                    ('atis:telecom5g:securityConstruct',rev_construct),
                    ('atis:telecom5g:effectiveConstruct',rev_construct),
                    ('atis:telecom5g:cryptography',rev_crypto),
                    ('atis:telecom5g:effectiveCryptography',rev_crypto),
                ]
            reachable=graph_descendants(ref,{k:list(v) for k,v in deps.items()})
            for prop,rev in summary_specs:
                for value in pvals(obj,prop):
                    matches=set(rev.get(value,set()))
                    if not matches: continue
                    narrower=matches & reachable
                    chosen=narrower if narrower else matches
                    for target in chosen:
                        if target in refmap and target not in closure:
                            closure.add(target); changed=True
    return closure

def semantic_roles(obj,placement,tax):
    """Return semantic roles from properties/native structures, never bom-ref syntax."""
    roles=set()
    et=pvals(obj,'atis:telecom5g:entityType') or pvals(obj,'atis:telecom5g:nfType')
    if et: roles.add('entity')
    if has_prop(obj,'atis:telecom5g:binding') or has_prop(obj,'atis:telecom5g:bindingType'): roles.add('binding')
    cp=obj.get('cryptoProperties') or {}
    if obj.get('type')=='cryptographic-asset' and cp.get('assetType')=='algorithm': roles.add('algorithm')
    if obj.get('type')=='cryptographic-asset' and cp.get('assetType')=='protocol': roles.add('protocol-asset')
    if has_prop(obj,'atis:telecom5g:securityConstruct') or has_prop(obj,'atis:telecom5g:securityConstructType'): roles.add('construct')
    return roles

def validate_atis(doc,tax,legacy_compat=False):
    errors=[]; warnings=[]
    exact,patterns=compile_taxonomy(tax)
    if doc.get('bomFormat')!='CycloneDX': errors.append('bomFormat must be CycloneDX')
    if doc.get('specVersion')!='1.7': errors.append('specVersion must be 1.7')

    per_location={}
    for placement,where,obj,item in walk_properties(doc):
        if not isinstance(item,dict): errors.append(f'{where}: property item is not an object'); continue
        name,value=item.get('name'),item.get('value')
        if not isinstance(name,str): errors.append(f'{where}: property name missing/not string'); continue
        if not name.startswith('atis:telecom5g:'): continue
        rule=match_tax_property(name,exact,patterns)
        if rule is None: errors.append(f'{where}: unrecognized ATIS property {name}'); continue
        if rule.get('deprecated') or rule.get('strictConformance')=='prohibited':
            msg=f'{where}: deprecated/legacy property {name} is prohibited in strict v1.0.0 conformance'
            if legacy_compat: warnings.append(msg+' (accepted only because --legacy-compat was requested)')
            else: errors.append(msg)
        if placement not in rule.get('appliesTo',[]): errors.append(f'{where}: {name} not allowed at {placement}; allowed={rule.get("appliesTo",[])}')
        msg=check_value(value,rule)
        if msg: errors.append(f'{where}: {name}: {msg}')
        per_location.setdefault(where,Counter())[name]+=1
        if isinstance(value,str) and ',' in value and name!='atis:telecom5g:interfaces' and 'multiple' in rule.get('cardinality',''):
            errors.append(f'{where}: {name} is multi-valued; repeat property objects instead of comma-concatenating {value!r}')

    mdprops=(doc.get('metadata') or {}).get('properties',[]) or []
    markers=[x.get('value') for x in mdprops if isinstance(x,dict) and x.get('name')=='atis:telecom5g:profile']
    if markers != [tax['profileMarker']]: errors.append(f'metadata must contain exactly one profile marker {tax["profileMarker"]!r}; found {markers}')
    taxonomy_versions=[x.get('value') for x in mdprops if isinstance(x,dict) and x.get('name')=='atis:telecom5g:taxonomyVersion']
    compatible=(tax.get('artifact_versions') or {}).get('profileCompatibleTaxonomyVersions',[tax.get('version')])
    if len(taxonomy_versions)!=1 or taxonomy_versions[0] not in compatible:
        errors.append(f'metadata must contain exactly one compatible taxonomyVersion from {compatible!r}; found {taxonomy_versions}')
    binding=(tax.get('artifact_versions') or {}).get('implementationBinding',{})
    if binding.get('format') and doc.get('bomFormat')!=binding.get('format'): errors.append(f'implementation binding requires bomFormat {binding.get("format")!r}')
    if binding.get('specVersion') and doc.get('specVersion')!=binding.get('specVersion'): errors.append(f'implementation binding requires specVersion {binding.get("specVersion")!r}')

    # #1: scope is mandatory because vendor/deployed changes semantics throughout the profile.
    scope_values=[x.get('value') for x in mdprops if isinstance(x,dict) and x.get('name')=='atis:telecom5g:cbom.scope']
    if len(scope_values)!=1: errors.append(f'metadata must contain exactly one atis:telecom5g:cbom.scope; found {scope_values}')
    scope=scope_values[0] if len(scope_values)==1 else None

    # v1.0.0 #10: baselineRelease is a BOM default; object-level 3gppSpecRelease explicitly overrides it.
    # Different values are therefore permitted and are not a contradiction.

    # Effective-state semantics retained and sharpened in v1.0.0: metadata.timestamp is the as-of snapshot time.
    effective_names={'atis:telecom5g:effectiveProtocol','atis:telecom5g:effectiveConstruct','atis:telecom5g:effectiveCryptography'}
    effective_locations=[]
    for placement,where,obj,item in walk_properties(doc):
        if isinstance(item,dict) and item.get('name') in effective_names: effective_locations.append((where,item.get('name'),item.get('value')))
    if effective_locations:
        if scope!='deployed': errors.append(f'effective* assertions require cbom.scope=deployed; found scope={scope!r}')
        if not (doc.get('metadata') or {}).get('timestamp'): errors.append('deployed CBOM containing effective* assertions must include native CycloneDX metadata.timestamp')

    for where,counts in per_location.items():
        for name,n in counts.items():
            rule=exact.get(name)
            if rule and 'once' in rule.get('cardinality','').lower() and n>1: errors.append(f'{where}: {name} appears {n} times but cardinality is {rule["cardinality"]}')

    canonical=tax.get('canonical_bindings',{}); norm_to_canonical={norm_identifier(k):k for k in canonical}; nf_entity_types=set(tax.get('nf_entity_types',[]))

    # Build object/reference indexes and semantic roles before role-dependent checks.
    refs=[]; refmap={}; placements={}; roles={}
    for coll,placement in [('services','service'),('components','component')]:
        for i,obj in enumerate(doc.get(coll,[]) or []):
            where=f'{coll}[{i}]'
            ref=obj.get('bom-ref')
            if ref is not None:
                refs.append(ref); refmap[ref]=obj; placements[ref]=placement; roles[ref]=semantic_roles(obj,placement,tax)
            et=pvals(obj,'atis:telecom5g:entityType'); nt=pvals(obj,'atis:telecom5g:nfType')
            if et and nt: errors.append(f'{where}: use entityType or deprecated nfType, not both')
            nfprops=[n for n in ('atis:telecom5g:nf.name','atis:telecom5g:nf.type','atis:telecom5g:nf.role') if pvals(obj,n)]
            if nfprops:
                cls=et or nt
                if len(cls)!=1 or cls[0] not in nf_entity_types: errors.append(f'{where}: NF-scoped properties {nfprops} require exactly one NF-classified entityType/nfType; found {cls}')

    dup=[r for r,c in Counter(refs).items() if c>1]
    if dup: errors.append(f'duplicate bom-ref values: {dup}')

    # #2/#3: semantic object typing and semantic placement, independent of bom-ref prefixes.
    binding_only=set((tax.get('semantic_placement_rules') or {}).get('bindingServiceOnly',[]))
    entity_only=set((tax.get('semantic_placement_rules') or {}).get('entitySubjectOnly',[]))
    algorithm_only=set((tax.get('semantic_placement_rules') or {}).get('algorithmComponentOnly',[]))
    for coll,placement in [('services','service'),('components','component')]:
        for i,obj in enumerate(doc.get(coll,[]) or []):
            where=f'{coll}[{i}]'; r=semantic_roles(obj,placement,tax)
            propnames={p.get('name') for p in obj.get('properties',[]) or [] if isinstance(p,dict)}
            if 'binding' in r:
                bt=pvals(obj,'atis:telecom5g:bindingType'); bv=pvals(obj,'atis:telecom5g:binding')
                if placement!='service': errors.append(f'{where}: reified architectural binding must be a CycloneDX service in strict v1.0.0')
                if not obj.get('bom-ref'): errors.append(f'{where}: reified architectural binding must have a bom-ref for entity association and graph semantics')
                if len(bt)!=1: errors.append(f'{where}: binding object must contain exactly one bindingType')
                if len(bv)!=1: errors.append(f'{where}: binding object must contain exactly one binding')
                if len(bv)==1 and isinstance(bv[0],str):
                    b=bv[0]; canon=norm_to_canonical.get(norm_identifier(b))
                    if canon and b!=canon: errors.append(f'{where}: non-canonical binding {b!r}; use {canon!r}')
                    if canon and len(bt)==1 and bt[0]!=canonical[canon]: errors.append(f'{where}: binding {canon!r} requires bindingType {canonical[canon]!r}, found {bt[0]!r}')
            if (propnames & binding_only) and 'binding' not in r:
                errors.append(f'{where}: binding-semantic properties {sorted(propnames & binding_only)} require a reified binding service (bindingType + binding)')
            if (propnames & entity_only) and 'entity' not in r:
                errors.append(f'{where}: entity capability summary properties {sorted(propnames & entity_only)} require an entityType-classified subject')
            if (propnames & algorithm_only) and 'algorithm' not in r:
                errors.append(f'{where}: algorithm-only properties {sorted(propnames & algorithm_only)} require a native cryptographic algorithm component')
            if has_prop(obj,'atis:telecom5g:securityConstruct'):
                if placement=='service' and 'binding' not in r: errors.append(f'{where}: service-level securityConstruct is a binding summary and requires a reified binding service')
            if has_prop(obj,'atis:telecom5g:cryptoUsageType'):
                if placement=='service' and 'binding' not in r: errors.append(f'{where}: service-level cryptoUsageType is summary-only and requires a reified binding service')
                if placement=='component' and 'algorithm' not in r: errors.append(f'{where}: component-level cryptoUsageType requires a native cryptographic algorithm asset')

    # v1.0.0 #9: selected duplicate-fact consistency checks. Native detailed representation is authoritative.
    for coll,placement in [('services','service'),('components','component')]:
        for i,obj in enumerate(doc.get(coll,[]) or []):
            where=f'{coll}[{i}]'
            if 'mutual' in pvals(obj,'atis:telecom5g:pki.authenticationMode') and 'false' in pvals(obj,'atis:telecom5g:sbi.mutualAuthentication'):
                errors.append(f'{where}: pki.authenticationMode=mutual is inconsistent with sbi.mutualAuthentication=false')
            cp=obj.get('cryptoProperties') or {}
            if placement=='component' and cp.get('assetType')=='algorithm':
                ap=cp.get('algorithmProperties') or {}
                native_bits=native_key_size_bits(ap)
                for k in pvals(obj,'atis:telecom5g:keyLength'):
                    if native_bits is not None and k!=native_bits:
                        errors.append(f'{where}: keyLength={k!r} is inconsistent with native algorithmProperties (derived key size {native_bits!r})')
                native_curve=canonical_curve(ap.get('parameterSetIdentifier'))
                for cval in pvals(obj,'atis:telecom5g:curve'):
                    stated=canonical_curve(cval)
                    if native_curve is not None and stated!=native_curve:
                        errors.append(f'{where}: curve={cval!r} is inconsistent with native parameterSetIdentifier={ap.get("parameterSetIdentifier")!r}')

    # Security construct canonical pairing + provenance.
    construct_type_map=tax.get('security_construct_type_map',{})
    for i,c in enumerate(doc.get('components',[]) or []):
        sc=pvals(c,'atis:telecom5g:securityConstruct'); st=pvals(c,'atis:telecom5g:securityConstructType')
        if sc or st:
            if len(sc)!=1 or len(st)!=1: errors.append(f'components[{i}]: referencable security construct must carry exactly one securityConstruct and one securityConstructType')
            elif sc[0] in construct_type_map and st[0]!=construct_type_map[sc[0]]: errors.append(f'components[{i}]: securityConstruct {sc[0]!r} requires securityConstructType {construct_type_map[sc[0]]!r}, found {st[0]!r}')
        cp=c.get('cryptoProperties') or {}; at=cp.get('assetType'); identities=[]
        if at=='protocol' and isinstance(c.get('name'),str): identities.append(('protocol',c['name']))
        if len(sc)==1: identities.append(('securityConstruct',sc[0]))
        for rule in tax.get('out_of_baseline_provenance',[]):
            if (rule.get('kind'),rule.get('identifier')) not in identities: continue
            ext=c.get('externalReferences') or []; wanted_url=rule.get('authoritativeUrl'); wanted_type=rule.get('externalReferenceType')
            matched=[r for r in ext if isinstance(r,dict) and (not wanted_type or r.get('type')==wanted_type) and (not wanted_url or r.get('url')==wanted_url)]
            if not matched: errors.append(f'components[{i}]: out-of-baseline {rule.get("kind")} {rule.get("identifier")!r} requires object-scoped authoritative provenance via externalReferences ({rule.get("authoritativeSource")})')
            elif rule.get('sourceVersionRequired'):
                text=' '.join(str(r.get('comment','')) for r in matched)
                if not re.search(r'(?i)(?:Release\s*\d+|Rel-\d+|V\d+\.\d+(?:\.\d+)?)',text): warnings.append(f'components[{i}]: provenance for {rule.get("identifier")!r} should identify the applicable source release/version when available')

    refset=set(refs); dep_source=set(); deps={}
    for d in doc.get('dependencies',[]) or []:
        src=d.get('ref'); targets=d.get('dependsOn',[]) or []
        if src in dep_source: errors.append(f'duplicate dependencies[] source ref {src!r}')
        dep_source.add(src); deps[src]=targets
        if src not in refset: errors.append(f'dependency source {src!r} does not resolve')
        for target in targets:
            if target not in refset: errors.append(f'dependency target {target!r} does not resolve')

    # v1.0.0 #12: each reified binding must be directly associated from at least one represented entity.
    entity_refs={ref for ref,rr in roles.items() if 'entity' in rr}
    binding_refs={ref for ref,rr in roles.items() if 'binding' in rr}
    for bref in sorted(binding_refs):
        owners=[eref for eref in entity_refs if bref in deps.get(eref,[])]
        if not owners:
            errors.append(f'reified binding {bref!r} is orphaned; it must be a direct dependsOn target of at least one represented entity')

    # #6: completeness has explicit machine-readable scope roots.
    completeness=[x.get('value') for x in mdprops if isinstance(x,dict) and x.get('name')=='atis:telecom5g:inventoryCompleteness']
    scope_refs=[x.get('value') for x in mdprops if isinstance(x,dict) and x.get('name')=='atis:telecom5g:inventoryScopeRef']
    if completeness==['complete']:
        if not scope_refs: errors.append('inventoryCompleteness=complete requires at least one metadata atis:telecom5g:inventoryScopeRef')
        for sr in scope_refs:
            obj=refmap.get(sr)
            if obj is None: errors.append(f'inventoryScopeRef {sr!r} does not resolve to a represented object'); continue
            rr=roles.get(sr,set())
            if not ({'entity','binding'} & rr): errors.append(f'inventoryScopeRef {sr!r} must reference a represented entity or reified binding, not roles {sorted(rr)}')
    else:
        for sr in scope_refs:
            if sr not in refmap: errors.append(f'inventoryScopeRef {sr!r} does not resolve to a represented object')
            elif not ({'entity','binding'} & roles.get(sr,set())): errors.append(f'inventoryScopeRef {sr!r} must reference a represented entity or reified binding')

    # Summary/index properties must be consistent with detailed assets. Semantic roles, not bom-ref names, control application.
    components=doc.get('components',[]) or []; prot_idx,construct_idx,crypto_idx=detailed_indexes(components)
    all_protocols=set().union(*prot_idx.values()) if prot_idx else set(); all_constructs=set().union(*construct_idx.values()) if construct_idx else set(); all_crypto=set().union(*crypto_idx.values()) if crypto_idx else set()
    for coll,placement in [('services','service'),('components','component')]:
        for i,obj in enumerate(doc.get(coll,[]) or []):
            where=f'{coll}[{i}]'; ref=obj.get('bom-ref'); r=semantic_roles(obj,placement,tax)
            if 'entity' in r:
                for prop,index,label in [('atis:telecom5g:crypto.supportedProtocols',all_protocols,'protocol'),('atis:telecom5g:crypto.supportedConstructs',all_constructs,'security construct'),('atis:telecom5g:crypto.supportedCryptography',all_crypto,'cryptography')]:
                    for v in pvals(obj,prop):
                        if v not in index: errors.append(f'{where}: summary {prop}={v!r} has no corresponding detailed {label} asset/construct')
            if 'binding' in r and ref:
                reachable=graph_descendants(ref,deps); rp=set().union(*(prot_idx.get(z,set()) for z in reachable)) if reachable else set(); rc=set().union(*(construct_idx.get(z,set()) for z in reachable)) if reachable else set(); rk=set().union(*(crypto_idx.get(z,set()) for z in reachable)) if reachable else set()
                for prop,index,label in [('atis:telecom5g:protocol',rp,'reachable protocol'),('atis:telecom5g:effectiveProtocol',rp,'reachable protocol'),('atis:telecom5g:securityConstruct',rc,'reachable security construct'),('atis:telecom5g:effectiveConstruct',rc,'reachable security construct'),('atis:telecom5g:cryptography',rk,'reachable cryptographic asset/suite'),('atis:telecom5g:effectiveCryptography',rk,'reachable cryptographic asset/suite')]:
                    for v in pvals(obj,prop):
                        if v not in index: errors.append(f'{where}: summary {prop}={v!r} is inconsistent with detailed graph; no {label} matches')

    # #4: ATIS canonical protocol label must agree with native CycloneDX protocol properties.
    pnorm=tax.get('protocol_normalization',{})
    algnorm=tax.get('canonical_algorithm_identities',{})
    for i,c in enumerate(components):
        if c.get('type')!='cryptographic-asset': continue
        cp=c.get('cryptoProperties')
        if not isinstance(cp,dict): errors.append(f'components[{i}] cryptographic-asset lacks cryptoProperties'); continue
        at=cp.get('assetType')
        if at not in {'algorithm','certificate','protocol','related-crypto-material'}: errors.append(f'components[{i}] invalid cryptoProperties.assetType {at!r}')
        if at=='protocol':
            pp=cp.get('protocolProperties') or {}; pt=pp.get('type')
            if pt not in PROTOCOL_TYPES: errors.append(f'components[{i}] invalid CycloneDX 1.7 protocol type {pt!r}')
            name=c.get('name')
            if name in pnorm:
                rule=pnorm[name]
                if pt!=rule.get('type'): errors.append(f'components[{i}]: canonical protocol {name!r} requires native protocolProperties.type={rule.get("type")!r}, found {pt!r}')
                if 'version' in rule and pp.get('version')!=rule['version']: errors.append(f'components[{i}]: canonical protocol {name!r} requires native protocolProperties.version={rule["version"]!r}, found {pp.get("version")!r}')
        if at=='algorithm':
            ap=cp.get('algorithmProperties') or {}; prim=ap.get('primitive'); fam=ap.get('algorithmFamily')
            if prim is not None and prim not in PRIMITIVES: errors.append(f'components[{i}] invalid CycloneDX 1.7 primitive {prim!r}')
            if fam and fam not in KNOWN_ALGORITHM_FAMILIES: warnings.append(f'components[{i}] algorithmFamily {fam!r} not in helper selected set; official schema is authoritative')
            name=c.get('name')
            if name in algnorm:
                rule=algnorm[name]
                for k,v in rule.items():
                    if k=='parameterSetIdentifierAny':
                        if ap.get('parameterSetIdentifier') not in v: errors.append(f'components[{i}]: canonical algorithm label {name!r} requires parameterSetIdentifier in {v!r}, found {ap.get("parameterSetIdentifier")!r}')
                    elif ap.get(k)!=v: errors.append(f'components[{i}]: canonical algorithm label {name!r} requires algorithmProperties.{k}={v!r}, found {ap.get(k)!r}')

    if isinstance(doc.get('metadata'),dict) and 'externalReferences' in doc['metadata']: errors.append('metadata.externalReferences is invalid here; use top-level externalReferences')
    return errors,warnings

def validate_official_schema(doc,schema_path):
    try:
        import jsonschema
        schema=load_json(schema_path); jsonschema.Draft7Validator(schema).validate(doc); return [],[]
    except Exception as e: return [f'official CycloneDX schema validation failed or could not resolve referenced schemas: {e}'],[]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--version',action='version',version='ATIS telecom5g CBOM reference validator 1.0.0'); ap.add_argument('taxonomy',type=Path); ap.add_argument('cbom',type=Path,nargs='+'); ap.add_argument('--cyclonedx-schema',type=Path,default=None); ap.add_argument('--legacy-compat',action='store_true',help='accept deprecated v0.x migration properties with warnings; output is not strict v1.0.0 conformant'); ap.add_argument('--show-scope-closure',action='store_true',help='print the reference-computed inventory scope closure for each CBOM that declares inventoryScopeRef')
    a=ap.parse_args(); tax=load_json(a.taxonomy); overall=0
    for path in a.cbom:
        try: doc=load_json(path)
        except Exception as e: print(f'FAIL {path}: JSON parse error: {e}'); overall=1; continue
        errs,warns=validate_atis(doc,tax,legacy_compat=a.legacy_compat)
        official_checked=bool(a.cyclonedx_schema)
        if official_checked:
            e2,w2=validate_official_schema(doc,a.cyclonedx_schema); errs+=e2; warns+=w2
        else:
            warns.append('official CycloneDX 1.7 schema validation was not run; ATIS-layer PASS alone does not establish strict v1.0.0 conformance')
        if errs:
            print(f'FAIL {path}'); [print('  ERROR:',x) for x in errs]; overall=1
        elif official_checked:
            print(f'PASS STRICT {path}')
        else:
            print(f'PASS ATIS-LAYER {path}')
        [print('  WARN:',x) for x in warns]
        if a.show_scope_closure:
            closure=compute_inventory_scope_closure(doc,tax)
            scope_vals=[p.get('value') for p in (doc.get('metadata') or {}).get('properties',[]) or [] if isinstance(p,dict) and p.get('name')=='atis:telecom5g:inventoryScopeRef']
            if scope_vals:
                print('  SCOPE-CLOSURE:', ', '.join(sorted(closure)))
            else:
                print('  SCOPE-CLOSURE: <no inventoryScopeRef declared>')
    return overall

if __name__=='__main__': raise SystemExit(main())
