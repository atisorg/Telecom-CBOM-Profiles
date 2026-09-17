#!/usr/bin/env python3
"""SDO-reviewer publication audit for ATIS Telecom5G CBOM 1.0.0.

This is a publication/conformance quality audit, not a semantic validator.
It intentionally flags issues that a standards editor/rapporteur is likely to
raise even when the CBOM examples are semantically valid.
"""
from pathlib import Path
import argparse, json, re, sys

ap=argparse.ArgumentParser(description='SDO publication-readiness objection audit (reference tooling)')
ap.add_argument('--fail-on', choices=['blocker','major','minor','info','none'], default='info', help='minimum severity that causes nonzero exit; default=info for final-release QA')
args=ap.parse_args()

TESTS_DIR = Path(__file__).resolve().parent
PROFILE_ROOT = TESTS_DIR.parent
DOCUMENTS_DIR = PROFILE_ROOT / "Documents"
VALIDATION_DIR = PROFILE_ROOT / "Validation"
PROFILE = PROFILE_ROOT / "3GPP_5G_CBOM_Profile_CycloneDX1.7_v1.0.0.md"
TAX = PROFILE_ROOT / "atis-telecom5g-property-taxonomy-v1.0.0.md"

p = PROFILE.read_text(encoding="utf-8")
t = TAX.read_text(encoding="utf-8")

findings = []
def add(sev, code, msg): findings.append((sev, code, msg))

# Publication structure expected by standards reviewers.
heads = [m.group(1).strip().lower() for m in re.finditer(r'^#{2,3}\s+(?:\d+(?:\.\d+)*\.?\s+)?(.+)$', p, re.M)]
if (not any('normative references' in h for h in heads) or
    any(token not in p for token in ('bom-1.7.schema.json','RFC 2119','RFC 8174','3GPP TR 33.938 V19.2.0','3GPP TS 33.501'))):
    add('BLOCKER','REF-001','Normative references are missing or incomplete for CycloneDX 1.7, RFC 2119/8174, TR 33.938, or TS 33.501.')
if not any(('terms' in h and 'definition' in h) for h in heads):
    add('MAJOR','TERM-001','No Terms and definitions clause for profile-specific concepts such as reified binding, inventory scope root, effective state, and summary/index property.')
if not any(('abbreviation' in h or 'acronym' in h) for h in heads):
    add('MAJOR','ABBR-001','No Abbreviations/acronyms clause despite extensive use of CBOM, BOM, SBOM, HBOM, NF, 5GS, SBI, PKI, PQC, CRQC, KDF, PRINS, etc.')

# Normative artifact authority / conflict resolution.
combined = p + '\n' + t
if ('Normative artifacts, reference tooling, and precedence' not in p or
    'human-readable taxonomy is authoritative' not in p or
    'reference tooling and informative test material' not in p):
    add('BLOCKER','AUTH-001','Normative-status/precedence or reference-tooling boundary is incomplete for profile, human taxonomy, machine artifacts, and validator.')

# Reference implementation vs normative rule boundary.
if re.search(r'MUST validate.*overlay/helper', p, re.I) or re.search(r'using the ATIS overlay/helper', p, re.I):
    add('MAJOR','TOOL-001','Strict conformance language can be read as requiring a particular helper implementation; normative rules should be implementation-independent and the helper identified as a reference validator.')

# Scope closure must be deterministic and preserve edge-less alternative capabilities.
if ('inventory scope closure' not in p or 'least fixed-point set' not in p or
    'all matching detailed objects are included' not in p or 'summary' not in p):
    add('BLOCKER','SCOPE-001','inventoryCompleteness lacks a deterministic fixed-point scope-closure definition covering summary-backed assets and multiple matches.')

# Architecture vocabulary source authority.
source_tokens=('3GPP TS 23.501','3GPP TS 38.401','3GPP TS 38.423','3GPP TS 38.470','3GPP TS 38.460','3GPP TS 33.220','3GPP TS 29.522','3GPP TS 29.509','3GPP TS 29.503')
if 'Architecture-vocabulary source traceability' not in p or any(x not in p for x in source_tokens):
    add('MAJOR','SRC-001','Architecture/entity/binding vocabulary source traceability is incomplete for 5GS, NG-RAN, GBA Ua, NEF/AF, AUSF, or UDM service-interface vocabulary.')

# External schema needs a pinned normative artifact/reference.
if 'official CycloneDX 1.7 BOM schema' in p and not re.search(r'(schema URI|schema URL|schema artifact|schema identifier|bom-1\.7\.schema)', p, re.I):
    add('MAJOR','CDX-001','CycloneDX 1.7 schema is mandatory but the exact normative schema artifact/identifier is not pinned in the profile.')

# Vague conditions in normative recommendations. Match ambiguous qualifiers, not nouns such as "test material".
vague = []
ambiguous = re.compile(r'\b(materially|sufficiently|where possible|where useful|when available|as applicable|when applicable|when material)\b', re.I)
for ln, line in enumerate(p.splitlines(), 1):
    if re.search(r'\b(MUST|MUST NOT|SHOULD|SHOULD NOT|MAY)\b', line) and ambiguous.search(line):
        vague.append(ln)
if vague:
    add('MAJOR','TEST-001',f'Potentially non-testable/vague normative conditions occur on profile lines {vague}; define the condition or make the guidance explicitly informative.')

# Implementation-package and migration-tool behavior belong in informative companion material, not normative CBOM requirements.
if re.search(r'implementation package SHOULD', p):
    add('MINOR','SCOPE-TOOL-001','Normative implementation-package example/test guidance remains in the profile instead of informative companion material.')
if re.search(r'Migration tooling MAY', p) or re.search(r'MAY appear (?:once|multiple times) in migration mode', t):
    add('MINOR','SCOPE-TOOL-002','Migration-tool behavior remains expressed normatively in the profile/taxonomy rather than informative migration guidance.')
mg=DOCUMENTS_DIR/'MIGRATION_GUIDE.md'
if not mg.exists() or 'Informative. This document does not define strict conformance.' not in mg.read_text(encoding='utf-8'):
    add('MINOR','SCOPE-TOOL-003','Informative migration guidance is missing or does not clearly disclaim normative status.')
if '## Annex A (informative). Reference examples and test material' not in p:
    add('MINOR','SCOPE-TOOL-004','Reference examples/tests are not clearly identified as informative material in the profile package.')

# PQC recommendation without methodology.
if re.search(r'PQC/CRQC exposure SHOULD', p) and re.search(r'methodology', p):
    add('MAJOR','PQC-001','PQC/CRQC exposure has a SHOULD recommendation while the profile states the assessment methodology is separately defined/future; this is difficult to conform to reproducibly.')


# Public namespace registration is optional in CycloneDX; the coordination package closes the local publication finding.
coord=DOCUMENTS_DIR/'CYCLONEDX_PROPERTY_TAXONOMY_COORDINATION.md'
manifest=VALIDATION_DIR/'cyclonedx_property_taxonomy_manifest.json'
if 'atis:telecom5g' in combined:
    if not coord.exists() or not manifest.exists():
        add('MINOR','REG-001','Public namespace coordination/registration-ready inventory is missing for the ATIS CycloneDX property namespace.')
    else:
        try:
            rm=json.loads(manifest.read_text(encoding='utf-8'))
            if rm.get('namespace')!='atis:telecom5g' or 'optional' not in coord.read_text(encoding='utf-8').lower():
                add('MINOR','REG-001','CycloneDX coordination material is present but incomplete or mis-scoped.')
        except Exception as e:
            add('MINOR','REG-001',f'CycloneDX coordination manifest is unreadable: {e}')

# Publication package governance. Do not invent a public software license; require an explicit working-package IPR/licensing notice.
ipr=DOCUMENTS_DIR/'IPR_AND_LICENSE_NOTICE.md'
if not any((DOCUMENTS_DIR/x).exists() for x in ('IPR_AND_LICENSE_NOTICE.md','LICENSE','LICENSE.txt','COPYRIGHT','NOTICE')):
    add('MINOR','IPR-001','No package-level IPR/copyright/licensing notice is present for machine-readable schemas, scripts, and examples.')
elif ipr.exists():
    iprt=ipr.read_text(encoding='utf-8')
    if 'does **not** itself grant' not in iprt or 'QSCII' not in iprt:
        add('MINOR','IPR-001','Working-package IPR/licensing notice does not clearly state rights boundary and QSCII review use.')

# Conformance traceability.
if not any(DOCUMENTS_DIR.glob('*traceability*')) and not any(DOCUMENTS_DIR.glob('*requirements*matrix*')):
    add('MAJOR','TRACE-001','No requirement-to-test/conformance traceability matrix is included; an SDO reviewer may ask how each normative requirement maps to schema/helper/tests.')

# Final publication designation. Normative artifacts must carry Version 1.0.0 rather than Draft or Release Candidate status.
p_title=p.splitlines()[0] if p.splitlines() else ''
t_title=t.splitlines()[0] if t.splitlines() else ''
if '(Draft v' in p_title or '(Draft v' in t_title:
    add('INFO','PUB-001','A final normative artifact still carries a Draft designation.')
elif 'Release Candidate' in p_title or 'Release Candidate' in t_title:
    add('INFO','PUB-001','A final normative artifact still carries a release-candidate designation.')
elif '(Version 1.0.0)' not in p_title or '(Version 1.0.0)' not in t_title:
    add('INFO','PUB-001','Version 1.0.0 designation is missing from one or more normative artifact titles.')

rank = {'BLOCKER':0,'MAJOR':1,'MINOR':2,'INFO':3}
findings.sort(key=lambda x: (rank[x[0]], x[1]))
for sev, code, msg in findings:
    print(f'{sev:7} {code}: {msg}')
counts = {s: sum(1 for x in findings if x[0]==s) for s in rank}
print('\nSDO REVIEW AUDIT SUMMARY')
for s in ('BLOCKER','MAJOR','MINOR','INFO'):
    print(f'  {s}: {counts[s]}')

# Configurable quality gate. This script is reference tooling, not a normative conformance definition.
threshold={'blocker':0,'major':1,'minor':2,'info':3,'none':99}[args.fail_on]
fail=any(rank[sev] <= threshold for sev,_,_ in findings) if args.fail_on!='none' else False
print(f'  Gate: fail-on={args.fail_on} -> {"FAIL" if fail else "PASS"}')
sys.exit(1 if fail else 0)
