#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
VALIDATION_DIR=Path(__file__).resolve().parent
PROFILE_ROOT=VALIDATION_DIR.parent
TAX=PROFILE_ROOT/'atis-telecom5g-taxonomy-1.0.0.json'
OUT=PROFILE_ROOT/'atis-telecom5g-profile-1.0.0.schema.json'

def value_schema(v):
    out={'type':'string'}
    if 'enum' in v: out['enum']=v['enum']
    if 'pattern' in v: out['pattern']=v['pattern']
    return out

def prop_rule(p):
    return {
      'type':'object',
      'properties':{'name':{'const':p['name']},'value':value_schema(p.get('value',{}))},
      'required':['name','value']
    }

def placement_items(tax, placement):
    allowed=[]
    for p in tax['properties']:
        if placement in p.get('appliesTo',[]) and not p.get('deprecated') and p.get('strictConformance')!='prohibited':
            allowed.append(prop_rule(p))
    # pattern properties are migration-only in v1.0.0 and intentionally excluded.
    return {
      'type':'object',
      'properties':{'name':{'type':'string'},'value':{'type':'string'}},
      'required':['name','value'],
      'allOf':[{
        'if':{'properties':{'name':{'pattern':'^atis:telecom5g:'}},'required':['name']},
        'then':{'anyOf':allowed}
      }]
    }

def object_with_props(items):
    return {'type':'object','properties':{'properties':{'type':'array','items':items}}}

tax=json.loads(TAX.read_text())
overlay={
 '$schema':'http://json-schema.org/draft-07/schema#',
 '$id':'https://atis.org/schemas/atis-telecom5g-profile-1.0.0.schema.json',
 'title':'ATIS telecom5g CBOM profile overlay for CycloneDX 1.7 (v1.0.0)',
 'description':'Derived strict ATIS property-placement and controlled-vocabulary overlay for profile 1.0.0. Additional semantic graph, scope-closure, native-normalization, duplicate-fact consistency, release-precedence, snapshot-time, and binding-association rules are defined normatively by the profile/taxonomy; validate_atis_cbom.py is a non-normative reference implementation of those checks. Deprecated/legacy properties are intentionally excluded from strict overlay conformance.',
 'allOf':[
   {'$ref':'http://cyclonedx.org/schema/bom-1.7.schema.json'},
   {
    'type':'object',
    'properties':{
      'bomFormat':{'const':'CycloneDX'},
      'specVersion':{'const':'1.7'},
      'metadata':object_with_props(placement_items(tax,'metadata')),
      'services':{'type':'array','items':object_with_props(placement_items(tax,'service'))},
      'components':{'type':'array','items':object_with_props(placement_items(tax,'component'))}
    }
   }
 ]
}
OUT.write_text(json.dumps(overlay,indent=2)+'\n')
print(OUT)
