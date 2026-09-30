from typing import Literal
from .models import Contact

ViewFilter = Literal['all', 'added', 'new', 'opening']
FitFilter = Literal['', 'ai-real', 'ai-pending', 'robotics']
IdentityFilter = Literal['', 'chinese', 'white', 'white_male', 'white_female', 'unknown']

def matches_identity(row: Contact, identity: str):
    ethnicity = row.selfReportedEthnicity if row.ethnicitySource else '未知'
    gender = row.selfReportedGender if row.genderSource else '未知'
    if not identity: return True
    if identity == 'unknown': return ethnicity == '未知' or gender == '未知'
    if identity == 'chinese': return ethnicity == '华人'
    if identity == 'white': return ethnicity == '白人'
    return ethnicity == '白人' and gender == ('男性' if identity == 'white_male' else '女性')

def filter_rows(rows: list[Contact], q='', theme='', school='', area='', fit='', view='all', identity='', nationality='', country=''):
    query = q.strip().casefold()
    return [r for r in rows if
        (not query or query in ' '.join([r.name,r.school,r.direction,*r.themes,*r.researchAreas,r.fitReason,r.note,r.joined,r.publicOpening]).casefold())
        and (not theme or theme in r.themes) and (not area or area in r.researchAreas)
        and (not school or r.school == school) and (not fit or r.fitCategory == fit)
        and (view != 'added' or r.batch == '新增 100 位') and (view != 'new' or r.newAp)
        and (view != 'opening' or r.openingEvidence) and matches_identity(r, identity)
        and (not nationality or nationality == (r.nationality if r.nationalitySource else '未知'))
        and (not country or country == r.institutionCountry)]
