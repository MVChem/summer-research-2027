import { useEffect, useRef } from 'react';
import type { Contact, Dataset } from '../types';
export function ContactDetail({ contact, meta, close, onNotes }: { contact: Contact | null; meta: Dataset['meta']; close: () => void; onNotes: (contact: Contact) => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    if (contact && !dialog.current?.open) dialog.current?.showModal();
    if (!contact && dialog.current?.open) dialog.current?.close();
  }, [contact]);
  return <dialog ref={dialog} className="detail-dialog" aria-labelledby="detail-title" onCancel={close} onClose={close}>
    {contact && <><div className="detail-header"><div><p className="eyebrow">{contact.school} · {contact.rank}</p><h2 id="detail-title">{contact.name}</h2></div><button className="button" onClick={close}>关闭</button></div>
      <p className="detail-direction">{contact.direction}</p><div className="tags">{contact.themes.map(t => <span className="tag" key={t}>{t}</span>)}</div>
      <dl className="detail-grid"><div><dt>联系批次</dt><dd>{contact.priority} <span className="muted">（排序建议，非录取概率）</span></dd></div>
        <div><dt>AI 与真机匹配</dt><dd><strong>{contact.fitLabel}</strong><p>{contact.fitReason}</p><span className="muted">真机线索可来自历史项目或合作，当前设备与接收条件另问。</span></dd></div>
        <div><dt>细分研究方向</dt><dd>{contact.researchAreas.join(' · ')}</dd></div>
        <div><dt>研究依据</dt><dd className="source-links">{contact.sources.map((s,i) => <a key={`${s.url}-${i}`} href={s.url} target="_blank" rel="noreferrer">{s.label} ↗</a>)}</dd></div>
        <div><dt>现校 AP 入职</dt><dd>{contact.joined} · <a href={contact.careerSource} target="_blank" rel="noreferrer">任职来源 ↗</a></dd></div>
        <div><dt>公开招募信息</dt><dd>{contact.publicOpening}</dd></div><div><dt>申请方式</dt><dd>{contact.contactRoute}</dd></div>
        <div><dt>访问时长</dt><dd>{contact.durationNote}</dd></div><div><dt>远程合作</dt><dd>{contact.remote}</dd></div>
        <div><dt>资助与自费</dt><dd>{contact.funding}{contact.school === 'MIT' && <> · <a href={meta.policyLinks[0].url} target="_blank" rel="noreferrer">MIT 规则 ↗</a></>}</dd></div>
        {contact.note && <div><dt>补充说明</dt><dd>{contact.note}</dd></div>}
        <div><dt>公开邮箱</dt><dd>{contact.email ? <a href={`mailto:${contact.email}`}>{contact.email}</a> : '请查看导师主页的联系方式'}</dd></div>
        <div><dt>学校所在地</dt><dd>{contact.institutionCountry}</dd></div>
        <div><dt>本人公开身份</dt><dd>国籍：{contact.nationalitySource ? contact.nationality : '未知'} · 族裔：{contact.ethnicitySource ? contact.selfReportedEthnicity : '未知'} · 性别：{contact.genderSource ? contact.selfReportedGender : '未知'}<p className="muted">仅依据本人明确公开的信息；不由姓名、照片或教育经历推断。</p>{[contact.nationalitySource,contact.ethnicitySource,contact.genderSource].filter(Boolean).map(url => <a key={url} href={url} target="_blank" rel="noreferrer">身份资料来源 ↗ </a>)}</dd></div>
      </dl><div className="detail-actions"><a className="button primary" href={contact.homepage} target="_blank" rel="noreferrer">导师主页 ↗</a>
        {contact.openingUrl && <a className="button" href={contact.openingUrl} target="_blank" rel="noreferrer">招募 / 申请入口 ↗</a>}
        <button className="button" onClick={() => onNotes(contact)}>记录我的看法</button>
      </div><p className="small muted">来源：导师 / 学校公开页面；核查 {contact.checkedAt}。2027 名额、8 周与经费尚未确认。</p></>}
  </dialog>;
}
