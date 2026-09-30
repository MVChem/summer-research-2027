"""Curated public-source contact pool, not a list of confirmed summer openings."""
from pathlib import Path
import csv
import json
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'data/source_inputs'
seeds = {r['name']: r for r in csv.DictReader((RESEARCH / 'broad_seed.tsv').open(), delimiter='\t')}
names = (RESEARCH / 'selection_100.txt').read_text().splitlines()
names.remove('Zongwei Zhou')
names.insert(4, 'Zongwei Zhou')
assert len(names) == len(set(names)) == 100

appointments = {}
def appointment(name, label, year, source=None):
    appointments[name] = {'joined': label, 'joinYear': year, 'careerSource': source or seeds[name]['url']}

harvard_dates = 'https://kempnerinstitute.harvard.edu/news/kiante-brantley-yilun-du-and-michael-albergo-to-join-the-kempner-as-institute-investigators/'
appointment('Siddharth Karamcheti', '2026 秋', 2026, 'https://ic.gatech.edu/people/siddharth-karamcheti')
appointment('Michael Albergo', '2026.07', 2026, harvard_dates)
appointment('Haw-Shiuan Chang', '2026.08', 2026, 'https://groups.cs.umass.edu/zamani/')
appointment('Yangruibo (Robin) Ding', '2026.07', 2026)
appointment('Zongwei Zhou', '2026.07；此前 Research Professor', 2026)
appointment('Yilun Du', '2025.07', 2025, harvard_dates)
appointment('Omar Khattab', '2025.07', 2025, 'https://www.eecs.mit.edu/people/omar-khattab/')
appointment('Zhuang Liu', '2025.07', 2025, 'https://www.cs.princeton.edu/people/profile/zhuangl')
appointment('Ruohan Gao', '2025.01；此前 Adjunct', 2025, 'https://ruohangao.github.io/assets/Ruohan_Gao_CV.pdf')
appointment('Unnat Jain', '2025', 2025)
appointment('Xianyi Cheng', '2024', 2024)
appointment('Yuchen Cui', '2024.07', 2024, 'https://yuchencui.cc/CV.pdf')
appointment('Monica Agrawal', '2024', 2024, 'https://scholars.duke.edu/person/monica.agrawal')
appointment('Kianté Brantley', '2024.07', 2024, harvard_dates)
appointment('Randall Balestriero', '2024', 2024, 'https://posts.cs.brown.edu/2024/08/19/randall-balestriero-joins-brown-cs-assistant-professor/')
appointment('Aviral Kumar', '2024', 2024, 'https://scsbusinessoffice.cs.cmu.edu/new-faculty/2024.html')
appointment('Jason Choi', '2025.11', 2025, 'https://www.samueli.ucla.edu/new-faculty-2023-2026/')
appointment('Saadia Gabriel', '2024；此前 NYU Faculty Fellow', 2024, 'https://saadiagabriel.com/cv.pdf')
appointment('Alane Suhr', '2023 秋', 2023, 'https://engineering.berkeley.edu/research-and-faculty/faculty/new-faculty-members/')
appointment('Tianmin Shu', '2023', 2023)
appointment('Andrea Bajcsy', '2023.09', 2023, 'https://www.cs.cmu.edu/~abajcsy/index.html')
appointment('Sherrie Wang', '2023.04', 2023)
appointment('Tengfei Ma', '2023.08', 2023)
appointment('Minchen Li', '2023；此前 UCLA Adjunct', 2023)
appointment('Georgia Gkioxari', '2023', 2023)
appointment('Hao Peng', '2023', 2023)
appointment('Amy Zhang', '2023 春', 2023, 'https://www.cs.utexas.edu/people/faculty-researchers/amy-zhang')
appointment('Chen Wang', '2022', 2022)
appointment('Xuesu Xiao', '2022.08', 2022)
appointment('Daniel Fried', '2022.08', 2022)
appointment('Wenpeng Yin', '2023；此前 2022 在 Temple 任 AP', 2023)
appointment('David Rosen', '2021', 2021, 'https://www.khoury.northeastern.edu/people/david-rosen/')

themes = {}
def tag(label, people):
    for n in people.split('|'):
        themes.setdefault(n.strip(), []).append(label)

tag('具身 / Robotics / World model', '''Siddharth Karamcheti|Yilun Du|Ruohan Gao|Unnat Jain|Xianyi Cheng|Yuchen Cui|Jason Choi|Tianmin Shu|Andrea Bajcsy|Mina Konakovic Lukovic|Minchen Li|Amy Zhang|Zhao Han|Chen Wang|Xuesu Xiao|Sanjiban Choudhury|Max Simchowitz|Yunzhu Li|Boyuan Chen|Shenlong Wang|Shubham Tulsiani|Zackory Erickson|Sarah Dean|Tapomayukh Bhattacharjee|Roberto Martin-Martin|Chuang Gan|Dylan Hadfield-Menell|Stefan Lee|David Rosen|Lawson Wong|Dylan Losey|Vincent Sitzmann|Srinath Sridhar|Shuran Song|Jiajun Wu|Jeannette Bohg|Angjoo Kanazawa|David Held|Katerina Fragkiadaki|Oliver Kroemer''')
tag('3D / 重建 / 检测 / Vision', '''Zhuang Liu|Ruohan Gao|Unnat Jain|Sara Beery|Sherrie Wang|Mina Konakovic Lukovic|Minchen Li|Georgia Gkioxari|Chen Wang|Yuyin Zhou|Zongwei Zhou|Shenlong Wang|Shubham Tulsiani|Saining Xie|Felix Heide|James Tompkin|Stefan Lee|David Rosen|Olga Russakovsky|Daniel Ritchie|Vincent Sitzmann|Srinath Sridhar|Shuran Song|Jiajun Wu|Gordon Wetzstein|Angjoo Kanazawa|David Held|Katerina Fragkiadaki|Ioannis Gkioulekas|Judy Hoffman''')
tag('LLM / NLP / Agent', '''Haw-Shiuan Chang|Yangruibo (Robin) Ding|Yilun Du|Omar Khattab|Zhuang Liu|Monica Agrawal|Emily Alsentzer|Kianté Brantley|Aviral Kumar|Saadia Gabriel|Alane Suhr|Tianmin Shu|Tengfei Ma|Georgia Gkioxari|Hao Peng|Yue Zhao|Daniel Fried|Maarten Sap|Yuyin Zhou|Chuang Gan|Saining Xie|He He|Yue Dong|Wenpeng Yin|Zhiting Hu|Robin Jia|Toby Jia-Jun Li|Ziyu Yao|Lichao Sun|Muhao Chen|Yu Su|Lei Cao|Rui Zhang|Yongfeng Zhang|Dylan Hadfield-Menell|Xiang Ren|Yifan Peng|Marzyeh Ghassemi|Pranav Rajpurkar|Faisal Mahmood|Roxana Daneshjou|James Zou|Connor Coley''')
tag('Medical / Healthcare AI', '''Monica Agrawal|Emily Alsentzer|Tengfei Ma|Yuyin Zhou|Zongwei Zhou|Sheng Wang|Lichao Sun|Yifan Peng|Marzyeh Ghassemi|Pranav Rajpurkar|Faisal Mahmood|Roxana Daneshjou|James Zou|Michael Hughes''')
tag('AI for Science / 科学应用', '''Michael Albergo|Zhuang Liu|Eunice Jun|Sherrie Wang|Sara Beery|Mina Konakovic Lukovic|Minchen Li|Hao Peng|Melanie Weber|Joshua Peterson|Shenlong Wang|Wenpeng Yin|Sheng Wang|Rui Zhang|Rebecca Willett|James Zou|Rose Yu|Connor Coley|Tess Smidt''')
tag('通用 ML / Human-AI', '''Randall Balestriero|Aviral Kumar|Eunice Jun|Saadia Gabriel|Kianté Brantley|Yue Zhao|Amy Zhang|Maarten Sap|Max Simchowitz|Melanie Weber|Joshua Peterson|Sarah Dean|Aditi Raghunathan|Toby Jia-Jun Li|Ziyu Yao|Olga Russakovsky|Dylan Losey|Michael Hughes''')
assert set(names) <= themes.keys()

associate = set('Muhao Chen|Yu Su|Rui Zhang|Yongfeng Zhang|Dylan Hadfield-Menell|Xiang Ren|James Tompkin|Stefan Lee|Lawson Wong|Olga Russakovsky|Dylan Losey|Yifan Peng|Daniel Ritchie|James Zou|Vincent Sitzmann|Tess Smidt|Shuran Song|Jeannette Bohg|Gordon Wetzstein|David Held|Katerina Fragkiadaki|Ioannis Gkioulekas|Oliver Kroemer|Judy Hoffman'.split('|'))
professor = {'Rebecca Willett', 'Rose Yu'}
rank_unspecified = {'Felix Heide', 'Marzyeh Ghassemi', 'Pranav Rajpurkar', 'Faisal Mahmood', 'Connor Coley'}

emails = {}
for line in '''Siddharth Karamcheti|skaramcheti@gatech.edu
Michael Albergo|michaelsalbergo@gmail.com
Haw-Shiuan Chang|hawshiuan@arizona.edu
Yangruibo (Robin) Ding|yrbding@cs.ucla.edu
Yilun Du|ydu@seas.harvard.edu
Omar Khattab|okhattab@mit.edu
Zhuang Liu|zhuangl@princeton.edu
Ruohan Gao|rhgao@umd.edu
Unnat Jain|unnatj@uci.edu
Xianyi Cheng|xianyi.cheng@duke.edu
Yuchen Cui|yuchencui@cs.ucla.edu
Monica Agrawal|monica.agrawal@duke.edu
Kianté Brantley|kdbrantley@seas.harvard.edu
Randall Balestriero|randall_balestriero@brown.edu
Aviral Kumar|aviralku@andrew.cmu.edu
Jason Choi|jjhchoi@g.ucla.edu
Saadia Gabriel|skgabrie@cs.ucla.edu
Eunice Jun|emjun@cs.ucla.edu
Tianmin Shu|tianmin.shu@jhu.edu
Andrea Bajcsy|abajcsy@andrew.cmu.edu
Sara Beery|beery@mit.edu
Mina Konakovic Lukovic|minakl@mit.edu
Tengfei Ma|Tengfei.Ma@stonybrook.edu
Minchen Li|minchernl@gmail.com
Hao Peng|haopeng@illinois.edu
Amy Zhang|amy.zhang@austin.utexas.edu
Chen Wang|cwx@buffalo.edu
Xuesu Xiao|xiao@gmu.edu
Daniel Fried|dfried@cs.cmu.edu
Sanjiban Choudhury|sanjibanc@cornell.edu
Max Simchowitz|msimchow@andrew.cmu.edu
Yuyin Zhou|yzhou284@ucsc.edu
Yunzhu Li|yunzhu.li@columbia.edu
Boyuan Chen|boyuan.chen@duke.edu
Zongwei Zhou|zzhou82@jh.edu
Shenlong Wang|shenlong@illinois.edu
Zackory Erickson|zackory@cmu.edu
Sarah Dean|sdean@cornell.edu
Chuang Gan|chuangg@cs.umass.edu
He He|hhe@nyu.edu
Yue Dong|yue.dong@ucr.edu
Wenpeng Yin|wenpeng@psu.edu
Zhiting Hu|zhh019@ucsd.edu
Robin Jia|robinjia@usc.edu
Aditi Raghunathan|raditi@cmu.edu
Toby Jia-Jun Li|toby.j.li@nd.edu
Ziyu Yao|ziyuyao@gmu.edu
Sheng Wang|swang@cs.washington.edu
Lichao Sun|lis221@lehigh.edu
Muhao Chen|muhchen@ucdavis.edu
Yu Su|su.809@osu.edu
Felix Heide|fheide@cs.princeton.edu
Lei Cao|caolei@arizona.edu
Rui Zhang|rmz5227@psu.edu
Dylan Hadfield-Menell|dhm@csail.mit.edu
Stefan Lee|leestef@oregonstate.edu
David Rosen|d.rosen@northeastern.edu
Olga Russakovsky|olgarus@princeton.edu
Dylan Losey|losey@vt.edu
Daniel Ritchie|daniel_ritchie@brown.edu
Vincent Sitzmann|sitzmann@mit.edu
Rose Yu|roseyu@ucsd.edu
Connor Coley|ccoley@mit.edu
Tess Smidt|tsmidt@mit.edu
Ioannis Gkioulekas|igkioule@andrew.cmu.edu
Oliver Kroemer|okroemer@andrew.cmu.edu
Judy Hoffman|judy.hoffman@uci.edu'''.splitlines():
    name, email = line.split('|'); emails[name] = email

openings = {}
def opening(name, text, url, route, duration='未确认；询问 2027 夏季约 8 周是否可行', remote='未确认', restriction=False):
    openings[name] = {'publicOpening': text, 'openingEvidence': True, 'openingUrl': url, 'contactRoute': route,
                      'durationNote': duration, 'remote': remote, 'restriction': restriction}

opening('Yilun Du', '公开欢迎 visiting researchers', 'https://embodied-minds-lab.github.io/contact/', '优先填写 lab contact 页链接的访问研究表单')
opening('Haw-Shiuan Chang', '明确欢迎 unpaid research interns', 'https://ken77921.github.io/', '邮件发送 CV 到 hawshiuan@arizona.edu；有合适项目时会联系')
opening('Zhuang Liu', 'Research intern 表单；强调长期合作', 'https://forms.gle/2F3Vpw4Xk5KxhNUw8', '优先填写主页 Research Interns 表单', '强调长期 research projects；8 周需确认')
opening('Yuyin Zhou', '主页明确招 PhD / interns', 'https://ucsc-vlaa.github.io/opening.html', '先按 VLAA opening 页申请，再按主页说明邮件联系')
opening('Yunzhu Li', '明确欢迎 visiting students', 'https://yunzhuli.github.io/', '邮件，附 CV')
opening('Shenlong Wang', '明确欢迎 visiting students', 'https://shenlong.web.illinois.edu/', '邮件，附 CV 与成绩单')
opening('Sara Beery', '兴趣表单包含 Visitor', 'https://forms.gle/WkofxoM4q5upNtSn8', '填写兴趣表单；主页说通常不会回复单独的邮件')
opening('Lichao Sun', '明确欢迎 remote / onsite visiting students', 'https://lichao-sun.github.io/index.html', '邮件，附 CV；说明 2027 时间窗口', remote='主页明确提到远程；2027 名额未确认')
opening('Wenpeng Yin', '明确欢迎 research interns；偏长期合作', 'https://www.wenpengyin.org/', '邮件介绍具体兴趣，附 CV', '主页偏好长期合作；8 周需确认')
opening('Muhao Chen', '有 Summer Visit 专门联系说明', 'https://luka-group.github.io/openings.html', '邮件标题使用 [PRSP Summer Visit]；按页内材料要求', '页面建议 4 月底前联系；年份通用，2027 名额未确认')
opening('Lei Cao', '明确欢迎 research interns', 'https://www2.cs.arizona.edu/~caolei/', '邮件，附 CV 与 AI/数据系统项目简介')
opening('Minchen Li', '欢迎 visiting 与 summer internship / volunteer', 'https://www.cs.cmu.edu/~minchenl/', '使用主页 Group 部分的申请表', '常规访学通常 6–12 月；另有 summer internship 表单，8 周需询问')
opening('Chuang Gan', '有 visiting students 申请入口', 'https://embodied-agi.cs.umass.edu/opportunity/', '先阅读 opportunity 页，再按其入口申请', '访学至少 6 个月；8 周线下不满足公开要求', restriction=True)
opening('Zongwei Zhou', 'BodyMaps 结构化研究项目', 'https://www.zongweiz.com/opportunity', '先核对 opportunity 页的项目时长，再询问独立短期合作', '所列项目为 9–12 个月；不等于 8 周暑研', restriction=True)
opening('Aviral Kumar', '公开提到可考虑远程合作；说明针对 2024–25', 'https://cmu-aire.github.io/pages/join_us.html', '访问/远程请求可邮件介绍兴趣与背景；不要把本校学生表单当外校入口', '2024–25 页面不支持线下访客；2027 需重新询问', '旧年度页面提到远程；2027 未确认', True)
opening('Max Simchowitz', '仅 exceptional circumstances 考虑 visiting students', 'https://msimchowitz.github.io/', '可询问，但优先本校本科/硕士或博士；至少 2 周后再跟进', '外校硕士访学属于例外；8 周未确认', restriction=True)

notes = {
    'Haw-Shiuan Chang': 'University of Arizona 的 College of Information Science；不是 ASU，也不是 Arizona CS 系。',
    'Jason Choi': '又名 Jason Jangho Choi；ECE，SCI Autonomy Lab。',
    'Emily Alsentzer': 'Biomedical Data Science，CS courtesy；医疗 NLP 与临床工作流。入职年份未进一步核实。',
    'Saadia Gabriel': 'UCLA 2024 入职；此前在 NYU 任 Faculty Fellow / Assistant Professor。公开 2027 招募主要是 PhD/postdoc，短期访学需另问。',
    'Eunice Jun': '偏 Human-AI、科学计算和 HCI；是扩大方向后的候选。',
    'Unnat Jain': '当前 UC Irvine AP，之前在 Skild AI；主页本校学生/PhD 说明不是外校访问承诺。',
    'Ruohan Gao': '2025.01 开始 AP；不要把此前 Adjunct 年份计为 AP 入职年。',
    'Minchen Li': '常规访客经费有限，建议本校/第三方支持；summer internship/volunteer 另有申请入口。',
    'Yunzhu Li': '当前 Columbia；此前 UIUC AP。属于转校，未将其标为首次新 AP。',
    'Judy Hoffman': '2026.01 从 Georgia Tech 转到 UC Irvine；现任 Associate，不是新 AP。',
    'Stefan Lee': 'Oregon State 现任 Associate；不是 Harsh Agrawal。',
    'Joshua Peterson': 'Boston University Computing & Data Sciences；不是 Stevens。',
    'Saining Xie': 'NYU AP，同时担任 AMI Labs cofounder / CSO；实际指导和访学安排需询问。',
    'Robin Jia': '主页 Google 表单面向 USC 在校本科/硕士；外校 UCAS 学生应另问访问，不把本校表单当开放实习。',
    'Tianmin Shu': 'SCAI 招募页主要是 PhD 与本校学生；8 周外校访问需单独确认。',
    'Pranav Rajpurkar': '公开 predoc 岗位为 1–2 年且要求人在美国，表单受理；不是面向大陆硕士的 8 周暑研岗位。',
    'Faisal Mahmood': '公开 RA/postdoc 和 Harvard/MIT rotation 招募不等于外校短期暑研。',
    'Wenpeng Yin': 'Penn State 现机构入职为 2023；此前 2022 已在 Temple 任 AP。',
    'Sherrie Wang': '遥感/卫星视觉、农业与地球科学应用；扩大 AI4Science 的切入点。',
    'Sara Beery': '生态/生物多样性视觉、检测与分布偏移；优先兴趣表单。',
    'Aviral Kumar': '公开远程说明属于 2024–25 学年；不可推定当前或 2027 必有远程位置。',
    'Zongwei Zhou': '2026.07 起 Assistant Professor；此前 Research Professor 不作为相同任职起点。',
}

rows = []
for idx, name in enumerate(names, 1):
    seed = seeds[name]
    rank = 'Associate Professor' if name in associate else ('Professor' if name in professor else ('Faculty（未细查职级）' if name in rank_unspecified else 'Assistant Professor'))
    ap = appointments.get(name, {'joined': '未核实', 'joinYear': None, 'careerSource': seed['url']})
    new = rank == 'Assistant Professor' and ap['joinYear'] in (2024, 2025, 2026)
    info = openings.get(name, {})
    restricted = info.get('restriction', False) or name == 'Pranav Rajpurkar'
    priority = '先确认条件' if restricted else ('优先联系' if new or name in openings else '广泛尝试')
    funding = '2027 经费未确认；可询问 unpaid / self-funded 是否符合学校政策'
    if seed['school'] == 'MIT':
        funding = '未确认；MIT 国际 visiting student 的 J-1 资助规则要求至少 51% 非个人/家庭来源，不能纯自费替代'
    if name == 'Minchen Li':
        funding = '主页明确访问经费有限，建议本校/第三方支持；8 周暑研资助需询问'
    if name == 'Haw-Shiuan Chang':
        funding = '主页明确 unpaid research intern；2027 项目、时长与访问安排仍需确认'
    row = dict(id=idx, name=name, school=seed['school'], direction=seed['direction'], themes=themes[name],
               homepage=seed['url'], rank=rank, newAp=new, **ap, priority=priority,
               publicOpening=info.get('publicOpening', '未查到面向外校短期访问的明确招募；可主动询问'),
               openingEvidence=bool(info), openingUrl=info.get('openingUrl', ''),
               email=emails.get(name, ''), contactRoute=info.get('contactRoute', '从主页联系方式询问 summer research / visiting student；附 CV 与简短研究简介'),
               durationNote=info.get('durationNote', '未确认；询问 2027 夏季约 8 周是否可行'),
               remote=info.get('remote', '未确认；可在联系时询问远程合作'),
               funding=funding, note=notes.get(name, ''), checkedAt='2026-10-01')
    if name == 'Pranav Rajpurkar':
        row.update(openingUrl='https://rajpurkarlab.hms.harvard.edu/join', contactRoute='先核对 Join 页；岗位申请走结构化表单，不通过邮件审材料', durationNote='公开 predoc 为 1–2 年且要求人在美国；8 周机会未查到')
    if name == 'Robin Jia':
        row['contactRoute'] = '外校访问可邮件另问；不要填写仅面向 USC 在校本科/硕士的表单'
    rows.append(row)

assert len(rows) == len({r['name'] for r in rows}) == 100
assert all(r['homepage'].startswith('https://') for r in rows)
assert not any('xiangren.org' in r['homepage'] for r in rows)

scope = {
    'title': '2027 美国暑研 · 100 位导师候选', 'checkedAt': '2026-10-01',
    'profile': '国科大 CS · 研二 · 2027 夏季线下约 8 周；远程也可讨论；可接受自费',
    'statement': '这是联系候选池。公开招募不代表已确认 2027 名额、8 周时长、远程资格或 paid / 自费许可。',
    'newApDefinition': '新 AP 筛选：公开资料确认现校 Assistant Professor 入职在 2024–2026；转校和此前职务另作备注。未核实年份不算入。',
    'total': len(rows), 'schools': len({r['school'] for r in rows}), 'newAp': sum(r['newAp'] for r in rows),
    'publicOpenings': sum(r['openingEvidence'] for r in rows),
    'themes': list(dict.fromkeys(t for r in rows for t in r['themes'])),
    'policyLinks': [{'label': 'MIT 国际 visiting student 资助与办理规则', 'url': 'https://iso.mit.edu/getting-started/visiting-students-faq/'}],
    'emailTemplate': '''Subject: Summer 2027 research visit / remote collaboration — UCAS CS master's student

Dear Professor [Name],

I am a second-year master's student in Computer Science at the University of Chinese Academy of Sciences (UCAS). I am writing to ask whether you would consider a research visit of approximately eight weeks in summer 2027, or a remote collaboration.

My recent project work involves [your verified contribution to the medical world-model / clinical-agent project]. I am particularly interested in your work on [specific paper or project] and would like to explore [one concrete research question]. I would be happy to share a short project summary and discuss a small, well-defined project.

I am open to an unpaid or self-funded research visit, subject to your university's policies. I would also be happy to discuss remote collaboration if an in-person visit is not feasible.

I have attached my CV and a one-page research summary. Thank you for considering my inquiry.

Best regards,
[Name]
[University email / project link]''',
}
dataset = {'meta': scope, 'contacts': rows}
(ROOT / 'data/contacts.json').write_text(json.dumps(dataset, ensure_ascii=False, indent=2))
(ROOT / 'frontend/src/contacts.snapshot.json').write_text(json.dumps(dataset, ensure_ascii=False, indent=2))

fields = [('id','编号'),('priority','联系批次'),('name','导师'),('school','学校'),('direction','方向'),('themes','方向标签'),('homepage','导师主页'),('rank','职级'),('joined','现校AP入职'),('newAp','2024至2026新AP'),('careerSource','任职来源'),('publicOpening','公开访学信息'),('openingEvidence','公开访问合作入口'),('openingUrl','申请或招募链接'),('email','公开邮箱'),('contactRoute','联系方式'),('durationNote','时长说明'),('remote','远程说明'),('funding','经费说明'),('note','备注'),('checkedAt','核查日期')]
with (ROOT / 'contacts_100.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w=csv.writer(f); w.writerow([v for _,v in fields] + ['联系状态','首次联系日期','回复记录'])
    for r in rows:
        w.writerow([(' / '.join(r[k]) if isinstance(r[k], list) else ('是' if r[k] else '否') if isinstance(r[k], bool) else r[k]) for k,_ in fields] + ['未联系','',''])

md = [f"# {scope['title']}", '', scope['profile'], '', f"核查日期：{scope['checkedAt']}。{scope['statement']}", '',
      f"共 {scope['total']} 位、{scope['schools']} 所学校；{scope['newAp']} 位有 2024–2026 现校 AP 入职记录。{scope['newApDefinition']}", '',
      '优先联系：新 AP 或有公开访问合作入口。广泛尝试：方向合适但未看到外校短期招募。先确认条件：公开项目时长/对象与你当前计划有明显差异。批次不代表录取概率。', '',
      '| # | 导师 / 主页 | 学校 | 方向 | 职级 / 现校 AP 入职 | 联系批次 / 公开信息 |', '|---|---|---|---|---|---|']
for r in rows:
    md.append(f"| {r['id']} | [{r['name']}]({r['homepage']}) | {r['school']} | {r['direction']} | {r['rank']} / {r['joined']} | {r['priority']}；{r['publicOpening']} |")
md += ['', '## 申请入口与限制', '']
for r in rows:
    if r['openingEvidence'] or r['note'] or r['school']=='MIT':
        link = f"[招募 / 申请入口]({r['openingUrl']})；" if r['openingUrl'] else ''
        md.append(f"- **{r['name']}**：{link}{r['contactRoute']}。{r['durationNote']}。{r['remote']}。{r['note']}")
md += ['', '## 自费与材料', '', '上面的 100 位没有任何一位被确认提供 2027 夏季有薪名额。自费可以作为可讨论的选项，学校仍需同意正式访问安排。', '',
       '[MIT visiting student FAQ](https://iso.mit.edu/getting-started/visiting-students-faq/) 要求国际 J-1 visiting student 至少 51% 经费来自非个人/家庭来源；完全自费不能直接替代该规则。其他学校单独确认。', '',
       '第一轮材料：英文 CV、1 页研究简介、项目/论文/代码链接、2027 时间窗口。成绩单和导师推荐联系方式可以先备好，按组要求提供。不要把草稿或待投稿论文写成已录用，也不要把尚未确认的个人贡献写入 CV。', '',
       '建议每批 10–15 位，针对每组改写一段具体研究兴趣。有表单的按主页要求走表单。先联系 2024–2026 AP 和公开欢迎 visiting / interns 的组，再扩大到成熟组。', '',
       '## 英文询问模板', '', '```text', scope['emailTemplate'], '```', '']
(ROOT / 'shortlist_100.md').write_text('\n'.join(md))

sys.path.insert(0, '/tmp/codex_summer_research_xlsx')
try:
    import xlsxwriter
except ImportError:
    pass
else:
    workbook=xlsxwriter.Workbook(ROOT / 'contacts_100.xlsx')
    ws=workbook.add_worksheet('100位候选')
    wrap=workbook.add_format({'text_wrap':True,'valign':'top','font_name':'Arial','font_size':11})
    linkfmt=workbook.add_format({'font_color':'#2563eb','underline':1,'valign':'top'})
    cols=[{'header':label} for _,label in fields]+[{'header':'联系状态'},{'header':'首次联系日期'},{'header':'回复记录'}]
    table=[]
    for r in rows:
        table.append([(' / '.join(r[k]) if isinstance(r[k],list) else ('是' if r[k] else '否') if isinstance(r[k],bool) else r[k]) for k,_ in fields]+['未联系','',''])
    ws.add_table(0,0,100,len(cols)-1,{'columns':cols,'data':table,'style':'Table Style Light 8'})
    ws.freeze_panes(1,3); ws.set_column(0,0,6); ws.set_column(1,1,13,wrap); ws.set_column(2,3,26,wrap); ws.set_column(4,len(cols)-1,35,wrap)
    for i,r in enumerate(rows,1):
        ws.set_row(i,58)
        for k in ['homepage','careerSource','openingUrl']:
            if r[k]: ws.write_url(i,[f for f,_ in fields].index(k),r[k],linkfmt)
    about=workbook.add_worksheet('使用说明'); about.set_column(0,0,100,wrap)
    for i,text in enumerate([scope['profile'],scope['statement'],scope['newApDefinition'],'公开邮箱来自个人/学校公开页面；尚未发送邮件。','学校经费、8 周时长、正式访问身份均需逐一确认。']):
        about.write(i,0,text,wrap);about.set_row(i,42)
    workbook.close()
print(json.dumps({k:scope[k] for k in ['total','schools','newAp','publicOpenings']}, ensure_ascii=False))
print(Counter(r['priority'] for r in rows))

# Extend the preserved first edition with the independently researched second batch.
from extend_dataset import build
build()
