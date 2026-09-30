"""Check dataset integrity and concrete intersections used by the browser filters."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.app.main import DATA
from backend.app.filtering import filter_rows, matches_identity

original = json.loads((ROOT / 'data/archive/contacts_100.v1.json').read_text())['contacts']
assert len(DATA.contacts) == len({r.name for r in DATA.contacts}) == 200
assert [(r.id,r.name) for r in DATA.contacts[:100]] == [(r['id'],r['name']) for r in original]
assert len(filter_rows(DATA.contacts, view='added')) == 100
assert len({r.school for r in DATA.contacts}) == DATA.meta.schools
assert sum(r.newAp for r in DATA.contacts) == DATA.meta.newAp
assert sum(r.openingEvidence for r in DATA.contacts) == DATA.meta.publicOpenings
assert json.loads((ROOT / 'data/contacts.json').read_text()) == json.loads((ROOT / 'frontend/src/contacts.snapshot.json').read_text())
by_name = {r.name:r for r in DATA.contacts}
assert by_name['Zachary Manchester'].school == 'MIT'
assert by_name['Seth Hutchinson'].school == 'Northeastern'
assert 'c-karen-liu' in by_name['Karen Liu'].homepage
assert 'Tianyi Zhou' not in by_name and 'Devi Parikh' not in by_name
assert all(r.school == 'MIT' and r.fitCategory == 'ai-real' for r in filter_rows(DATA.contacts, school='MIT', fit='ai-real'))
assert 'Pulkit Agrawal' in {r.name for r in filter_rows(DATA.contacts, school='MIT', fit='ai-real', area='强化学习 / 泛化')}
for r in DATA.contacts:
    assert r.sources and r.researchAreas and r.fitReason
    assert all(s.url.startswith('https://') for s in r.sources)
    assert r.selfReportedEthnicity == '未知' or r.ethnicitySource
    assert r.selfReportedGender == '未知' or r.genderSource
    assert r.nationality == '未知' or r.nationalitySource
synthetic = by_name['Sergey Levine'].model_copy(update={'selfReportedEthnicity':'白人','selfReportedGender':'男性','ethnicitySource':'','genderSource':''})
assert not matches_identity(synthetic,'white_male'), 'Unsourced identity labels must not enter demographic filters'
assert len(filter_rows(DATA.contacts, identity='unknown')) == 200
print('Dataset checks passed: 200 unique candidates, preserved IDs, corrected affiliations, filters and sourced identity rules.')
