import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { downloadCsv, loadDataset, offlineDataset } from './api';
import { DashboardLayout } from './components/DashboardLayout';
import { MetricCards } from './components/MetricCards';
import { ContactsTable } from './components/ContactsTable';
import { ContactDetail } from './components/ContactDetail';
import { ContactNotes } from './components/ContactNotes';
import { DirectionBrowser } from './components/DirectionBrowser';
import { browseHref, fitLabels, identityLabels, matchesIdentity, readRoute, type PageMode } from './browsing';
import { listRecordings } from './recordings';
import type { Contact, ContactProgress, Dataset, Progress, Recordings, View } from './types';

const STORAGE = 'summer-research-2027-progress-v1';
const labels: Record<View, string> = { all: '全部候选', added: '本次新增 100 位', new: '近期入职 AP', opening: '公开合作入口', saved: '我的收藏' };
function readProgress(): Progress {
  try { const data: unknown = JSON.parse(localStorage.getItem(STORAGE) ?? '{}'); return typeof data === 'object' && data !== null && !Array.isArray(data) ? data as Progress : {}; }
  catch { return {}; }
}

export default function App() {
  const initial = readRoute();
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [error, setError] = useState(''); const [revision, setRevision] = useState(0);
  const [snapshotMode, setSnapshotMode] = useState(window.location.protocol === 'file:');
  const [view, setView] = useState<View>(initial.view); const [theme, setTheme] = useState(initial.theme);
  const [query, setQuery] = useState(initial.query); const [school, setSchool] = useState(initial.school);
  const [pageMode, setPageMode] = useState<PageMode>(initial.mode); const [area, setArea] = useState(initial.area);
  const [fit, setFit] = useState(initial.fit); const [identity, setIdentity] = useState(initial.identity);
  const [nationality, setNationality] = useState(initial.nationality); const [country, setCountry] = useState(initial.country);
  const [status, setStatus] = useState(''); const [priority, setPriority] = useState('');
  const [noteFilter, setNoteFilter] = useState(''); const [recordings, setRecordings] = useState<Recordings>({});
  const [recordingError, setRecordingError] = useState(''); const [storageError, setStorageError] = useState('');
  const [notesTarget, setNotesTarget] = useState<{ contact: Contact; mode: 'record' | 'text' } | null>(null);
  const [sort, setSort] = useState('fit'); const [page, setPage] = useState(1); const [size, setSize] = useState(25);
  const [progress, setProgress] = useState<Progress>(readProgress);
  const progressRef = useRef(progress);
  const [selected, setSelected] = useState<Contact | null>(null); const [notice, setNotice] = useState('');
  useEffect(() => {
    const controller = new AbortController(); setError('');
    loadDataset(controller.signal).then(setDataset).catch(e => { if (!controller.signal.aborted) setError(e instanceof Error ? e.message : '无法读取名单'); });
    return () => controller.abort();
  }, [revision]);
  useEffect(() => {
    let cancelled = false;
    listRecordings().then(value => { if (!cancelled) setRecordings(value); }).catch(e => {
      if (!cancelled) setRecordingError(e instanceof Error ? e.message : '无法读取录音。');
    });
    return () => { cancelled = true; };
  }, []);
  useEffect(() => { setPage(1); }, [query, school, theme, view, status, priority, sort, size, noteFilter, area, fit, identity, nationality, country, pageMode]);
  useEffect(() => {
    const onRoute = () => {
      const r = readRoute(); setPageMode(r.mode); setSchool(r.school); setFit(r.fit); setArea(r.area); setTheme(r.theme);
      setView(r.view); setQuery(r.query); setIdentity(r.identity); setNationality(r.nationality); setCountry(r.country);
    };
    window.addEventListener('hashchange', onRoute); window.addEventListener('popstate', onRoute);
    return () => { window.removeEventListener('hashchange', onRoute); window.removeEventListener('popstate', onRoute); };
  }, []);
  useEffect(() => {
    const hash = browseHref(pageMode, { school, fit, area, theme, view, q: query, identity, nationality, country });
    try { window.history.replaceState(null, '', hash); } catch { /* Some file viewers disable history mutation. */ }
  }, [pageMode, school, fit, area, theme, view, query, identity, nationality, country]);
  useEffect(() => { if (!notice) return; const id = setTimeout(() => setNotice(''), 5000); return () => clearTimeout(id); }, [notice]);
  const meta = dataset?.meta ?? offlineDataset.meta;
  const rows = dataset?.contacts ?? [];
  const savedCount = rows.filter(r => progress[r.name]?.saved).length;
  const contextRows = useMemo(() => {
    const q = query.trim().toLocaleLowerCase();
    return rows.filter(r => (!q || [r.name, r.school, r.direction, ...r.themes, ...r.researchAreas, r.fitReason, r.note, r.joined, r.publicOpening, progress[r.name]?.personalNote ?? ''].join(' ').toLocaleLowerCase().includes(q))
      && (!theme || r.themes.includes(theme)) && (!school || school === r.school)
      && (!fit || r.fitCategory === fit) && matchesIdentity(r, identity)
      && (!country || country === r.institutionCountry) && (!nationality || nationality === (r.nationalitySource ? r.nationality : '未知'))
      && (!status || (progress[r.name]?.status ?? '未联系') === status) && (!priority || priority === r.priority)
      && (!noteFilter || (noteFilter === 'any' ? Boolean(progress[r.name]?.personalNote?.trim() || recordings[r.name]?.length)
        : noteFilter === 'text' ? Boolean(progress[r.name]?.personalNote?.trim()) : noteFilter === 'audio' ? Boolean(recordings[r.name]?.length)
        : !progress[r.name]?.personalNote?.trim() && !recordings[r.name]?.length))
      && (view !== 'added' || r.batch === '新增 100 位') && (view !== 'new' || r.newAp) && (view !== 'opening' || r.openingEvidence) && (view !== 'saved' || progress[r.name]?.saved));
  }, [rows, query, theme, school, status, priority, view, progress, noteFilter, recordings, fit, identity, nationality, country]);
  const filtered = useMemo(() => contextRows.filter(r => !area || r.researchAreas.includes(area))
      .sort((a, b) => sort === 'fit' ? ['ai-real','ai-pending','robotics'].indexOf(a.fitCategory) - ['ai-real','ai-pending','robotics'].indexOf(b.fitCategory) || a.id - b.id
        : sort === 'name' ? a.name.localeCompare(b.name) : sort === 'school' ? a.school.localeCompare(b.school) || a.id - b.id
        : sort === 'priority' ? ['优先联系','广泛尝试','先确认条件'].indexOf(a.priority) - ['优先联系','广泛尝试','先确认条件'].indexOf(b.priority) || a.id - b.id : a.id - b.id)
  , [contextRows, area, sort]);
  const pages = Math.max(1, Math.ceil(filtered.length / size)); const currentPage = Math.min(page, pages);
  const visible = filtered.slice((currentPage - 1) * size, currentPage * size);
  const setItem = useCallback((r: Contact, update: Partial<ContactProgress>) => {
    const next = { ...progressRef.current, [r.name]: { ...progressRef.current[r.name], ...update } };
    progressRef.current = next; setProgress(next);
    try { localStorage.setItem(STORAGE, JSON.stringify(next)); setStorageError(''); }
    catch { setStorageError('当前浏览器未能保存文字和标记；请导出 CSV 保留本次输入，再检查浏览器存储权限或可用空间。'); }
  }, []);
  const changeView = (v: View) => { setView(v); setTheme(''); setArea(''); };
  const changeMode = (mode: PageMode) => {
    const href = browseHref(mode, { school, fit, area, view, q: query, identity, nationality, country });
    if (mode !== pageMode) { try { window.history.pushState(null, '', href); } catch { /* File viewers can disable history. */ } }
    setPageMode(mode);
  };
  const reset = () => { setView('all'); setTheme(''); setArea(''); setFit(''); setQuery(''); setSchool(''); setStatus(''); setPriority(''); setSort('fit'); setNoteFilter(''); setIdentity(''); setNationality(''); setCountry(''); };
  const directionHref = browseHref('directions', { school, fit, area, q: query, identity, nationality, country });
  return <DashboardLayout meta={meta} view={view} theme={theme} savedCount={savedCount} setView={changeView} setTheme={setTheme}
    pageMode={pageMode} onMode={changeMode} directionHref={directionHref}
    actions={<button className="button primary" disabled={!dataset || filtered.length === 0} onClick={() => { downloadCsv(filtered, progress, recordings); setNotice(`已导出当前筛选的 ${filtered.length} 位，包含文字备注和所有分页。录音请在备注中单独下载。`); }}>导出名单 <span aria-hidden="true">↓</span></button>}>
    <section className="intro"><div><p className="eyebrow">SUMMER 2027 · RESEARCH CONTACTS · V2</p><h1>{pageMode === 'directions' ? '按研究方向浏览' : '2027 美国暑研导师名单'}</h1><p className="intro-text">{meta.total} 位候选 · 新增 {meta.added} 位 · 优先关注 AI 方法与真实机器人交叉团队。</p><a className="intro-link" href={directionHref} target="_blank" rel="noreferrer">研究方向页，新标签页打开 ↗</a></div>
      <div className="checked"><span className="badge">核查 {meta.checkedAt}</span><span>{snapshotMode ? '内置名单 · 可直接打开' : '公开资料 · 导师联系候选'}</span></div></section>
    {pageMode === 'contacts' ? <MetricCards meta={meta} onView={changeView} /> : <div className="direction-summary"><span><strong>{meta.total}</strong> 位导师候选</span><span><strong>{meta.schools}</strong> 所美国高校</span><span><strong>{meta.fitCounts['ai-real']}</strong> 位有 AI + 真机线索</span></div>}
    <div className="fit-shortcuts" aria-label="AI与真机匹配快捷筛选">{Object.entries(fitLabels).map(([key, label]) => <button key={key} aria-pressed={fit === key} className={fit === key ? 'active' : ''} onClick={() => setFit(fit === key ? '' : key)}><span>{label}</span><strong>{meta.fitCounts[key] ?? 0}</strong></button>)}</div>
    <div className="scope-note"><strong>线下约两个月，远程也可讨论。</strong><span>{meta.statement}</span></div>
    <section className="list-panel" aria-labelledby="list-heading">
      <div className="panel-top"><div><h2 id="list-heading">{area || theme || labels[view]}</h2><p>{dataset ? `${filtered.length} 位符合当前筛选` : '正在加载公开资料名单'} · 点击导师姓名打开主页，详情里有研究依据和条件。</p></div><button className="button" onClick={reset}>重置筛选</button></div>
      <div className="filters"><label className="search"><span className="sr-only">搜索导师、学校、方向</span><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" /><path d="m16 16 5 5" /></svg><input placeholder="搜索导师、学校、方向、我的备注…" value={query} onChange={e => setQuery(e.target.value)} /></label>
        <label className="visible-filter"><span>学校</span><select aria-label="学校" value={school} onChange={e => setSchool(e.target.value)}><option value="">全部学校 · {meta.schools} 所</option>{[...new Set(rows.map(r => r.school))].sort().map(s => <option key={s} value={s}>{s} · {rows.filter(r => r.school === s).length} 位</option>)}</select></label>
        <label className="visible-filter"><span>AI 与真机</span><select aria-label="AI与真机匹配" value={fit} onChange={e => setFit(e.target.value)}><option value="">全部匹配类型</option>{Object.entries(fitLabels).map(([key,label]) => <option key={key} value={key}>{label}</option>)}</select></label>
        <label className="visible-filter"><span>细分方向</span><select aria-label="细分研究方向" value={area} onChange={e => setArea(e.target.value)}><option value="">全部细分方向</option>{meta.researchAreas.map(a => <option key={a}>{a}</option>)}</select></label>
        <label><span className="sr-only">联系批次</span><select aria-label="联系批次" value={priority} onChange={e => setPriority(e.target.value)}><option value="">全部批次</option>{['优先联系','广泛尝试','先确认条件'].map(p => <option key={p}>{p}</option>)}</select></label>
        <label><span className="sr-only">联系进度筛选</span><select aria-label="联系进度筛选" value={status} onChange={e => setStatus(e.target.value)}><option value="">全部进度</option>{['未联系','已联系','已回复','暂不联系'].map(s => <option key={s}>{s}</option>)}</select></label>
        <label><span className="sr-only">备注筛选</span><select aria-label="备注筛选" value={noteFilter} onChange={e => setNoteFilter(e.target.value)}><option value="">全部备注</option><option value="any">有备注 / 录音</option><option value="text">有文字备注</option><option value="audio">有录音</option><option value="empty">尚未记录</option></select></label>
        <label><span className="sr-only">排序</span><select aria-label="排序" value={sort} onChange={e => setSort(e.target.value)}><option value="fit">AI + 真机线索优先</option><option value="id">名单顺序</option><option value="priority">联系批次优先</option><option value="name">导师 A–Z</option><option value="school">学校 A–Z</option></select></label>
      </div>
      <details className="identity-filters"><summary>本人公开身份与国别 <span>仅使用有来源的自述资料</span></summary><p>{meta.identityNote}</p><div className="filters">
        <label className="visible-filter"><span>本人公开族裔 / 性别</span><select aria-label="本人公开族裔与性别" value={identity} onChange={e => setIdentity(e.target.value)}><option value="">全部身份</option>{Object.entries(identityLabels).map(([key,label]) => <option key={key} value={key}>{label} · {rows.filter(r => matchesIdentity(r,key)).length} 位</option>)}</select></label>
        <label className="visible-filter"><span>本人公开国籍</span><select aria-label="本人公开国籍" value={nationality} onChange={e => setNationality(e.target.value)}><option value="">全部国籍</option>{[...new Set(rows.map(r => r.nationalitySource ? r.nationality : '未知'))].map(n => <option key={n}>{n}</option>)}</select></label>
        <label className="visible-filter"><span>学校所在国家</span><select aria-label="学校所在国家" value={country} onChange={e => setCountry(e.target.value)}><option value="">全部学校所在地</option>{[...new Set(rows.map(r => r.institutionCountry))].map(c => <option key={c}>{c}</option>)}</select></label>
      </div></details>
      <div className="view-tabs" aria-label="名单快捷筛选">{(Object.keys(labels) as View[]).map(v => <button key={v} className={view === v ? 'active' : ''} aria-pressed={view === v} onClick={() => changeView(v)}>{labels[v]}<span>{v === 'all' ? meta.total : v === 'added' ? meta.added : v === 'new' ? meta.newAp : v === 'opening' ? meta.publicOpenings : savedCount}</span></button>)}</div>
      {pageMode === 'directions' && dataset && <DirectionBrowser rows={contextRows} areas={meta.researchAreas} area={area} school={school} fit={fit} onArea={setArea} onSchool={setSchool} />}
      {(school || area || fit || identity) && <p className="active-filter-note">当前：{[school,area,fitLabels[fit as keyof typeof fitLabels],identityLabels[identity]].filter(Boolean).join(' · ')} <span>· {filtered.length} 位</span></p>}
      {(storageError || recordingError) && <p className="notes-error storage-banner" role="alert">{storageError || recordingError}</p>}
      {error ? <div className="empty" role="alert"><h3>名单暂时无法加载</h3><p>{error}</p><div className="detail-actions"><button className="button" onClick={() => setRevision(v => v + 1)}>重试</button><button className="button primary" onClick={() => { setDataset(offlineDataset); setSnapshotMode(true); setError(''); }}>打开内置的 {meta.total} 位名单</button></div></div>
        : !dataset ? <div className="empty" role="status">正在读取导师名单…</div>
        : !filtered.length ? <div className="empty"><h3>{view === 'saved' ? '还没有收藏导师' : '没有符合筛选条件的导师'}</h3><p>{identity && identity !== 'unknown' ? '当前名单尚未核实符合该分类的本人自述身份资料；未知不会被自动归类。' : view === 'saved' ? '点击名单里的星形按钮，保存想优先联系的导师。' : '试试缩短关键词，或清除学校和方向筛选。'}</p><button className="button" onClick={reset}>查看全部 {meta.total} 位</button></div>
        : <ContactsTable rows={visible} progress={progress} recordings={recordings} onNotes={(contact, mode) => setNotesTarget({ contact, mode })} onDetail={setSelected} onSave={r => setItem(r, { saved: !progress[r.name]?.saved })} onStatus={(r, s) => setItem(r, { status: s })} />}
      <div className="pagination"><span>{filtered.length ? `${(currentPage - 1) * size + 1}–${Math.min(currentPage * size, filtered.length)}` : '0'} / {filtered.length} 位<span className="desktop-inline"> · {savedCount} 位已收藏</span></span>
        <div className="pagination-controls"><label>每页 <select aria-label="每页数量" value={size} onChange={e => setSize(Number(e.target.value))}>{[25,50,100].map(n => <option value={n} key={n}>{n}</option>)}</select></label><span>{currentPage} / {pages}</span><button className="button" aria-label="上一页" disabled={currentPage <= 1} onClick={() => setPage(p => p - 1)}>←</button><button className="button" aria-label="下一页" disabled={currentPage >= pages} onClick={() => setPage(p => p + 1)}>→</button></div>
      </div>
    </section>
    <div className="reading-grid"><section className="reading-card"><p className="eyebrow">HOW TO USE</p><h2>先联系一批，再扩大范围。</h2><p>先看近期 AP 和公开合作入口，每批选 10–15 位。邮件里写一个具体研究兴趣，附英文 CV、1 页研究简介和项目链接。</p><p>点击每位导师后面的“录音”或“备注”，记下方向匹配、想合作的课题和待确认的问题。之后可筛选“有备注 / 录音”，收藏想联系的人。</p><p>“优先联系”是排序建议；“先确认条件”包含公开项目时长较长、仅例外接收外校硕士等情况。</p><details><summary>新 AP 的判断范围</summary><p>{meta.newApDefinition}</p></details><p className="small muted">收藏、联系状态、文字和录音保存在当前浏览器。导出 CSV 包含文字看法和录音数量，录音可单独下载。</p></section>
      <section className="reading-card"><p className="eyebrow">FUNDING & VISITING</p><h2>自费可以提出，安排要逐组确认。</h2><p>未确认任何 2027 有薪名额。学校可能要求正式访问身份、经费证明和其他材料；有公开 intern 招募也不等于接受八周访问。</p><p>MIT 国际 J-1 visiting student 的规则要求至少 51% 资助来自非个人或家庭来源，不能完全靠自费满足。</p><a href={meta.policyLinks[0].url} target="_blank" rel="noreferrer">查看 MIT 的 visiting student 规则 ↗</a><details><summary>可用于邮件的英文表述</summary><p className="quote">I am open to an unpaid or self-funded research visit, subject to your university’s policies. I would also be happy to discuss remote collaboration.</p></details></section></div>
    <section className="template-card"><details><summary>展开英文联系邮件模板 <span className="muted">填写个人贡献、具体论文与研究问题后再发送</span></summary><pre>{meta.emailTemplate}</pre></details></section>
    <p className="classification-note">{meta.fitNote}</p>
    <footer className="page-footer">2027 Summer Research · {meta.total} faculty contacts<span>任职、方向与招募说明来自公开主页 · {meta.checkedAt}</span></footer>
    <ContactDetail contact={selected} meta={meta} close={() => setSelected(null)} onNotes={contact => { setSelected(null); setNotesTarget({ contact, mode: 'text' }); }} />
    {notesTarget && <ContactNotes key={notesTarget.contact.name} contact={notesTarget.contact} mode={notesTarget.mode}
      note={progress[notesTarget.contact.name]?.personalNote ?? ''} clips={recordings[notesTarget.contact.name] ?? []} storageError={storageError}
      status={progress[notesTarget.contact.name]?.status ?? '未联系'} saved={Boolean(progress[notesTarget.contact.name]?.saved)}
      onNote={personalNote => setItem(notesTarget.contact, { personalNote, noteUpdatedAt: new Date().toISOString() })}
      onStatus={value => setItem(notesTarget.contact, { status: value })} onSave={() => setItem(notesTarget.contact, { saved: !progress[notesTarget.contact.name]?.saved })}
      onAdded={clip => { setRecordings(current => ({ ...current, [clip.contactName]: [clip, ...(current[clip.contactName] ?? [])] })); setRecordingError(''); }}
      onDeleted={id => setRecordings(current => ({ ...current, [notesTarget.contact.name]: (current[notesTarget.contact.name] ?? []).filter(clip => clip.id !== id) }))}
      close={() => setNotesTarget(null)} />}
    <div aria-live="polite" role="status" className={`toast ${notice ? 'visible' : ''}`}>{notice}</div>
  </DashboardLayout>;
}
