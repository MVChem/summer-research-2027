"""Build the 200-person edition from the preserved first edition and 100 additions."""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
FIT_LABELS = {'ai-real': 'AI + 真机线索', 'ai-pending': 'AI 相关 · 真机待核实', 'robotics': '机器人方法 / 系统'}
AREA_RULES = [
    ('VLA / 机器人基础模型', r'foundation|\bvla\b'),
    ('World model / 物理推理', r'world model|physical reasoning|self-model|physical simulation|physics'),
    ('视频学习 / 模仿学习', r'video|imitation|demonstration|human experience'),
    ('强化学习 / 泛化', r'reinforcement|\brl\b|meta-learning|generalization|adaptation'),
    ('语言 / 多模态 Agent', r'\bllm\b|language|multimodal|neuro-symbolic|\bagent'),
    ('3D / 视觉 / 空间智能', r'vision|visual|perception|\b3d\b|spatial|reconstruction|geometry'),
    ('人机协作 / 对齐', r'human|interactive|alignment|collaborat|feedback'),
    ('医疗 / 辅助机器人', r'medical|health|surg|assistive'),
    ('学习控制 / 规划 / 安全', r'control|planning|safe|reliable|dynamics|navigation'),
    ('AI for Science', r'science|scientific|climate|ecolog|physical sciences'),
]

def areas(direction, themes):
    tags = [label for label, pattern in AREA_RULES if re.search(pattern, direction, re.I)]
    if 'Medical / Healthcare AI' in themes and '医疗 / 辅助机器人' not in tags:
        tags.append('医疗 / 辅助机器人')
    if 'AI for Science / 科学应用' in themes and 'AI for Science' not in tags:
        tags.append('AI for Science')
    return tags or ['通用 AI / 方法迁移']

RANKS = {}
for title, people in {
    'Assistant Professor': 'Benjamin Eysenbach|Jiayuan Mao|Danfei Xu|Sehoon Ha|Abhishek Gupta|Dinesh Jayaraman|Guanya Shi|Jeffrey Ichnowski|Bernadette Bucher|Wei-Chiu Ma|Andreea Bobu|Rachel Holladay|Manling Li|Harish Ravichandar|Ahmed Qureshi',
    'Associate Professor': 'Sergey Levine|Dorsa Sadigh|Anca Dragan|Pulkit Agrawal|Yuke Zhu|Hao Su|Nikolai Matni|Saurabh Gupta|Katherine Driggs-Campbell|Cheng Zhang|Jia-Bin Huang|Luca Carlone|Chuchu Fan|Robert Platt|Heni Ben Amor|Carlo Pinciroli|Sicun Gao|Christopher Amato|Shiqi Zhang',
    'Research Associate Professor': 'Eric Eaton',
    'Professor': 'Pieter Abbeel|Trevor Darrell|Abhinav Gupta|Ken Goldberg|Peter Stone|Scott Niekum|Sonia Chernova|Byron Boots|Dieter Fox|Siddhartha Srinivasa|Henrik Christensen|Kostas Daniilidis|Vijay Kumar|George Pappas|Hod Lipson|George Konidaris|Chad Jenkins|Dmitry Berenson|Kris Hauser|Zico Kolter|Fei-Fei Li|Leonidas Guibas|Dinesh Manocha|Yiannis Aloimonos|Daniela Rus|Nick Roy|Julie Shah|Brian Williams|Frank Dellaert|Seth Hutchinson|Taskin Padir|Ayanna Howard|Jana Kosecka|Hadas Kress-Gazit|Mark Campbell|Michael Yip|Karen Liu|Alyosha Efros|Jitendra Malik|Mohit Bansal',
}.items():
    for name in people.split('|'):
        RANKS[name] = title
RANKS.update({'Deepak Pathak': 'Associate Professor', 'Carl Vondrick': 'Associate Professor', 'Patricio Vela': 'Associate Professor', 'Tony Dear': 'Teaching Faculty', 'Zachary Manchester': 'Faculty（职级待核实）', 'Navid Azizan': 'Associate Professor'})

APPOINTMENTS = {
    'Andreea Bobu': ('2024 秋', 2024, 'https://www.mit.edu/~abobu/'),
    'Bernadette Bucher': ('2024', 2024, 'https://robotics.umich.edu/news/2024/new-faculty-joining-michigan-robotics/'),
}

EXTRA_SOURCES = {
    'Sergey Levine': ['https://engineering.berkeley.edu/news/2022/10/step-by-step/'],
    'Pieter Abbeel': ['https://vcresearch.berkeley.edu/news/learning-learn'],
    'Chelsea Finn': ['https://arxiv.org/abs/1910.11215'],
    'Dorsa Sadigh': ['https://iliad.stanford.edu/research/', 'https://arxiv.org/abs/2103.05910'],
    'Anca Dragan': ['https://vcresearch.berkeley.edu/faculty/anca-dragan'],
    'Ken Goldberg': ['https://autolab.berkeley.edu/'],
    'Deepak Pathak': ['https://www.cs.cmu.edu/~dpathak/', 'https://www.cs.cmu.edu/news/2023/VRB_robot_tasks'],
    'Abhinav Gupta': ['https://www.cs.cmu.edu/news/2023/VRB_robot_tasks'],
    'Yuke Zhu': ['https://ut-austin-rpl.github.io/rpl.github.io/people/'],
    'Lerrel Pinto': ['https://www.lerrelpinto.com/'],
    'Erdem Biyik': ['https://liralab.usc.edu/'],
    'Danfei Xu': ['https://rl2.cc.gatech.edu/'],
    'Sonia Chernova': ['https://www.gt-rail.com/'],
    'Dinesh Jayaraman': ['https://www.seas.upenn.edu/~dineshj/'],
    'Carl Vondrick': ['https://www.cs.columbia.edu/~vondrick/'],
    'Guanya Shi': ['https://lecar-lab.github.io/'],
    'Bernadette Bucher': ['https://midas.umich.edu/directory/bernadette-bucher/'],
    'Dinesh Manocha': ['https://www.cs.umd.edu/article/2023/10/dinesh-manocha-receives-google-faculty-award'],
    'Julie Shah': ['https://news.mit.edu/2013/humans-robots-interaction-cross-training-0211'],
    'Heni Ben Amor': ['https://news.asu.edu/20161103-discoveries-asu-robot-teaches-itself-how-shoot-hoops-matter-hours'],
    'Ayanna Howard': ['https://engineering.osu.edu/news/2021/07/robotics-and-ai-qa-dean-ayanna-howard'],
    'Michael Yip': ['https://ucsdarclab.com/'],
    'Jitendra Malik': ['https://people.eecs.berkeley.edu/~malik/'],
}

def public_fields(row):
    # No demographic inference from names, portraits, pronouns, birthplaces or education.
    row.update(institutionCountry='美国', nationality='未知', nationalitySource='',
               selfReportedEthnicity='未知', ethnicitySource='', selfReportedGender='未知', genderSource='')

def build():
    dataset = json.loads((ROOT / 'data/archive/contacts_100.v1.json').read_text())
    old = dataset['contacts']
    additions = list(csv.DictReader((ROOT / 'data/source_inputs/expansion_100.tsv').open(), delimiter='\t'))
    assert len(additions) == len({r['name'] for r in additions}) == 100
    assert not {r['name'] for r in old} & {r['name'] for r in additions}
    for row in old:
        row.update(batch='原始 100 位', fitCategory='ai-pending', fitLabel=FIT_LABELS['ai-pending'],
                   fitReason='保留原版候选；本轮未为该导师补充真机证据，请按详情中的公开主页逐项核实。',
                   researchAreas=areas(row['direction'], row['themes']),
                   sources=[{'label': '原版导师 / 学校主页', 'url': row['homepage']}])
        public_fields(row)
    for idx, seed in enumerate(additions, 101):
        rank = RANKS.get(seed['name'], 'Faculty（职级待核实）')
        joined, year, career = APPOINTMENTS.get(seed['name'], ('未核实', None, seed['homepage']))
        tags = areas(seed['direction'], [])
        themes = ['具身 / Robotics / World model']
        if '3D / 视觉 / 空间智能' in tags: themes.append('3D / 重建 / 检测 / Vision')
        if '语言 / 多模态 Agent' in tags: themes.append('LLM / NLP / Agent')
        if '医疗 / 辅助机器人' in tags: themes.append('Medical / Healthcare AI')
        if 'AI for Science' in tags: themes.append('AI for Science / 科学应用')
        if seed['fit'] == 'ai-pending': themes.append('通用 ML / Human-AI')
        fit = seed['fit']
        row = dict(id=idx, name=seed['name'], school=seed['school'], direction=seed['direction'], themes=themes,
            homepage=seed['homepage'], rank=rank, joined=joined, joinYear=year,
            newAp=rank == 'Assistant Professor' and year in (2024, 2025, 2026), careerSource=career,
            priority='广泛尝试', publicOpening='本轮未核实外校短期访问招募；可按主页说明询问',
            openingEvidence=False, openingUrl='', email='',
            contactRoute='从学校 / 导师主页获取本人联系方式；介绍具体论文切入点、UCAS 硕士背景及 2027 时间窗口',
            durationNote='未确认；询问 2027 夏季约 8 周是否可行', remote='未确认；可询问远程研究合作',
            funding='2027 经费与自费许可未确认；按学校正式访问规则询问',
            note='', checkedAt='2026-10-01', batch='新增 100 位', researchAreas=tags,
            fitCategory=fit, fitLabel=FIT_LABELS[fit], fitReason=seed['evidence'],
            sources=[{'label': '导师 / 学校主页', 'url': seed['homepage']}] +
                    [{'label': '研究 / 真机线索', 'url': u} for u in EXTRA_SOURCES.get(seed['name'], [])])
        if row['school'] == 'MIT': row['funding'] = old[0]['funding'] if old[0]['school'] == 'MIT' else '未确认；MIT 国际 visiting student 的 J-1 资助规则要求至少 51% 非个人/家庭来源，不能纯自费替代'
        if row['newAp']: row['priority'] = '优先联系'
        if seed['name'] in ('Lerrel Pinto', 'Xiaolong Wang'):
            row['note'] = '本人主页同时说明 Meta 产业岗位与学校研究组；2027 学校指导、在校时间与接收访问能力需确认。'
        if seed['name'] == 'Tony Dear': row['note'] = '学校官网明确是 teaching faculty；研究指导与外校访问能力需单独询问。'
        if seed['name'] == 'Jiayuan Mao':
            row['priority'] = '先确认条件'
            row['note'] = '主页说明 PhD 申请走正式流程，无法回复流程外个别询问；这不是短期访问招募。'
        public_fields(row)
        old.append(row)
    meta = dataset['meta']
    meta.update(title='2027 美国暑研：200 位导师联系候选', total=len(old), schools=len({r['school'] for r in old}),
                newAp=sum(r['newAp'] for r in old), publicOpenings=sum(r['openingEvidence'] for r in old),
                version='v2', added=100, fitCounts=dict(Counter(r['fitCategory'] for r in old)),
                researchAreas=list(dict.fromkeys(t for r in old for t in r['researchAreas'])),
                identityNote='族裔、性别、国籍仅记录本人明确公开且有来源的信息；当前名单未核实这些自述信息，均标为未知。学校所在地为美国，不代表导师国籍。',
                fitNote='匹配分组是基于公开研究内容的人工判断；真机线索包括历史项目和合作，不保证 2027 组内设备、在校指导或接收名额。原始 100 位的真机证据本轮未重新核实。')
    text = json.dumps(dataset, ensure_ascii=False, indent=2)
    for p in ('data/contacts.json', 'frontend/src/contacts.snapshot.json'):
        (ROOT / p).write_text(text)
    fields = ['id','name','school','batch','direction','researchAreas','fitLabel','fitReason','homepage','rank','joined','newAp',
              'careerSource','priority','publicOpening','openingEvidence','openingUrl','email','contactRoute','durationNote',
              'remote','funding','note','checkedAt','institutionCountry','nationality','nationalitySource',
              'selfReportedEthnicity','ethnicitySource','selfReportedGender','genderSource','sources']
    labels = ['编号','导师','学校','名单批次','方向','细分方向','AI与真机匹配','匹配理由','主页','职级','入职','新AP',
              '任职来源','联系批次','公开访问说明','公开合作入口','招募链接','公开邮箱','联系方式','时长','远程','经费',
              '备注','核查日期','学校所在国家','本人公开国籍','国籍来源','本人自述族裔','族裔来源','本人自述性别','性别来源','研究来源']
    def value(r, k):
        v = r[k]
        if isinstance(v, list): return ' | '.join(f"{x['label']}: {x['url']}" if isinstance(x, dict) else x for x in v)
        if isinstance(v, bool): return '是' if v else '否'
        return v
    table = [[value(r,k) for k in fields] for r in old]
    with (ROOT / 'contacts_200.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f); writer.writerow(labels); writer.writerows(table)
    sys.path.insert(0, '/tmp/codex_summer_research_xlsx')
    try:
        import xlsxwriter
    except ImportError:
        pass
    else:
        book = xlsxwriter.Workbook(ROOT / 'contacts_200.xlsx')
        sheet = book.add_worksheet('200位候选'); sheet.freeze_panes(1,3)
        sheet.add_table(0,0,len(old),len(fields)-1, {'columns':[{'header':x} for x in labels], 'data':table, 'style':'Table Style Light 8'})
        sheet.set_column(0,0,6); sheet.set_column(1,2,25); sheet.set_column(3,len(fields)-1,35)
        book.close()
    md = [f"# {meta['title']}", '', f"原始 100 位 + 新增 100 位；{meta['schools']} 所学校。核查 2026-10-01。", '', meta['fitNote'], '', meta['identityNote'], '',
          '| # | 导师 | 学校 | 批次 | 匹配 | 方向 | 理由与来源 |', '|---|---|---|---|---|---|---|']
    for r in old:
        links = ' / '.join(f"[{s['label']}]({s['url']})" for s in r['sources'])
        md.append(f"| {r['id']} | [{r['name']}]({r['homepage']}) | {r['school']} | {r['batch']} | {r['fitLabel']} | {r['direction']} | {r['fitReason']} {links} |")
    (ROOT / 'shortlist_200.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({k:meta[k] for k in ['total','added','schools','newAp','fitCounts']},ensure_ascii=False))

if __name__ == '__main__': build()
