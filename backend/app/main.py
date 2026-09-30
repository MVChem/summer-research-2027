from pathlib import Path
import csv
import io
import json

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from .models import Dataset, BrowseResult, DirectionSummary
from .filtering import FitFilter, IdentityFilter, ViewFilter, filter_rows

ROOT = Path(__file__).resolve().parents[2]
DATA = Dataset.model_validate(json.loads((ROOT / 'data/contacts.json').read_text()))
app = FastAPI(title='2027 Summer Research — 200 Faculty Contacts')

@app.get('/api/health')
def health():
    return {'status': 'ok', 'contacts': len(DATA.contacts)}

@app.get('/api/contacts', response_model=Dataset)
def contacts():
    return DATA

@app.get('/api/browse', response_model=BrowseResult)
def browse(q: str = '', theme: str = '', school: str = '', area: str = '', fit: FitFilter = '',
           view: ViewFilter = 'all', identity: IdentityFilter = '', nationality: str = '', country: str = ''):
    rows = filter_rows(DATA.contacts, q, theme, school, area, fit, view, identity, nationality, country)
    return BrowseResult(total=len(rows), contacts=rows)

@app.get('/api/directions', response_model=list[DirectionSummary])
def directions(school: str = '', fit: FitFilter = '', view: ViewFilter = 'all'):
    rows = filter_rows(DATA.contacts, school=school, fit=fit, view=view)
    return [DirectionSummary(area=a, total=sum(a in r.researchAreas for r in rows),
        aiReal=sum(a in r.researchAreas and r.fitCategory == 'ai-real' for r in rows),
        schools=sorted({r.school for r in rows if a in r.researchAreas})) for a in DATA.meta.researchAreas]

@app.get('/api/contacts/export')
def export(q: str = '', theme: str = '', school: str = '', area: str = '', fit: FitFilter = '',
           view: ViewFilter = 'all', identity: IdentityFilter = '', nationality: str = '', country: str = ''):
    rows = filter_rows(DATA.contacts, q, theme, school, area, fit, view, identity, nationality, country)
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(['编号', '导师', '学校', '方向', '主页', '职级', '现校AP入职', '公开访学信息', '招募链接', '公开邮箱', '时长', '远程', '经费', '备注', '核查日期', '名单批次', '细分方向', 'AI与真机匹配', '匹配理由', '学校所在国家', '本人公开国籍', '本人自述族裔', '本人自述性别', '身份资料来源', '研究来源'])
    for r in rows:
        writer.writerow([r.id, r.name, r.school, r.direction, r.homepage, r.rank, r.joined, r.publicOpening, r.openingUrl, r.email, r.durationNote, r.remote, r.funding, r.note, r.checkedAt, r.batch, ' / '.join(r.researchAreas), r.fitLabel, r.fitReason, r.institutionCountry, r.nationality if r.nationalitySource else '未知', r.selfReportedEthnicity if r.ethnicitySource else '未知', r.selfReportedGender if r.genderSource else '未知', '; '.join(s for s in [r.nationalitySource,r.ethnicitySource,r.genderSource] if s), '; '.join(s.url for s in r.sources)])
    return Response('\ufeff' + output.getvalue(), media_type='text/csv; charset=utf-8',
                    headers={'Content-Disposition': 'attachment; filename="summer-research-contacts.csv"'})

frontend = ROOT / 'frontend/dist'
if frontend.exists():
    app.mount('/', StaticFiles(directory=frontend, html=True), name='frontend')
