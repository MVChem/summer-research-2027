import type { Contact, Progress, Recordings, Status } from '../types';
import { MicrophoneIcon, PencilIcon } from './NoteIcons';
export function ContactsTable({ rows, progress, recordings, onNotes, onDetail, onSave, onStatus }: { rows: Contact[]; progress: Progress; recordings: Recordings;
  onNotes: (r: Contact, mode: 'record' | 'text') => void;
  onDetail: (r: Contact) => void; onSave: (r: Contact) => void; onStatus: (r: Contact, s: Status) => void }) {
  return <div className="table-scroll" tabIndex={0} aria-label="导师名单，可横向滚动"><table className="contacts-table">
    <thead><tr><th className="number">#</th><th>导师 / 学校</th><th>研究方向</th><th>现校 AP 入职</th><th>访问 / 实习信息</th><th>联系进度</th><th>操作</th></tr></thead>
    <tbody>{rows.map(r => <tr key={r.name}>
      <td className="number muted">{r.id.toString().padStart(2, '0')}</td>
      <td><a className="faculty-name" href={r.homepage} target="_blank" rel="noreferrer">{r.name} <span className="external">↗</span></a><div className="school">{r.school}</div><span className={`badge ${r.priority === '优先联系' ? 'priority' : r.priority === '先确认条件' ? 'conditional' : ''}`}>{r.priority}</span></td>
      <td className="direction-cell"><span className={`badge fit-badge ${r.fitCategory}`}>{r.fitLabel}</span><div>{r.direction}</div><p className="fit-preview" title={r.fitReason}>{r.fitReason}</p>{r.batch === '新增 100 位' && <span className="badge">本次新增</span>}</td><td><span className="rank">{r.rank === 'Assistant Professor' ? 'AP' : r.rank === 'Associate Professor' ? 'Associate' : r.rank}</span><div className="school">{r.joined}</div>{r.newAp && <span className="badge">2024–2026 入职</span>}</td>
      <td className="opening-cell"><div>{r.openingEvidence ? <span className="status-dot" /> : null}{r.publicOpening}</div><div className="school">{r.durationNote}</div></td>
      <td><label className="sr-only" htmlFor={`status-${r.id}`}>{r.name} 联系状态</label><select id={`status-${r.id}`} className="status-select" value={progress[r.name]?.status ?? '未联系'} onChange={e => onStatus(r, e.target.value as Status)}>
        {(['未联系','已联系','已回复','暂不联系'] as Status[]).map(s => <option key={s}>{s}</option>)}
      </select></td><td><div className="row-actions"><button className={`icon-button save-button ${progress[r.name]?.saved ? 'saved' : ''}`} aria-label={`${progress[r.name]?.saved ? '取消收藏' : '收藏'} ${r.name}`} aria-pressed={Boolean(progress[r.name]?.saved)} onClick={() => onSave(r)}>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 2.8 5.8 6.4.9-4.6 4.5 1.1 6.3L12 17.5l-5.7 3 1.1-6.3L2.8 9.7l6.4-.9Z" /></svg>
      </button><button className="button detail-button" onClick={() => onDetail(r)}>详情</button></div>
        <div className="row-actions note-row-actions"><button className="button detail-button note-entry" aria-label={`录音 ${r.name}`} onClick={() => onNotes(r, 'record')}><MicrophoneIcon />录音</button>
          <button className={`button detail-button note-entry ${progress[r.name]?.personalNote?.trim() || recordings[r.name]?.length ? 'has-note' : ''}`} aria-label={`备注 ${r.name}`} onClick={() => onNotes(r, 'text')}><PencilIcon />备注</button></div>
        {Boolean(progress[r.name]?.personalNote?.trim() || recordings[r.name]?.length) && <button className="note-preview" onClick={() => onNotes(r, 'text')} title={progress[r.name]?.personalNote?.slice(0, 160)} aria-label={`查看 ${r.name} 的看法`}>
          {progress[r.name]?.personalNote?.trim() && <span>{progress[r.name]?.personalNote}</span>}{Boolean(recordings[r.name]?.length) && <small>{recordings[r.name].length} 段录音</small>}</button>}
      </td>
    </tr>)}</tbody></table></div>;
}
