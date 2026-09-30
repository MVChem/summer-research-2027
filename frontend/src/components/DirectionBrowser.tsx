import { browseHref } from '../browsing';
import type { Contact } from '../types';

export function DirectionBrowser({ rows, areas, area, school, fit, onArea, onSchool }: {
  rows: Contact[]; areas: string[]; area: string; school: string; fit: string;
  onArea: (area: string) => void; onSchool: (school: string) => void;
}) {
  return <section className="direction-browser" aria-label="细分研究方向">
    <div className="direction-heading"><div><h3>选择研究方向</h3><p>方向可以交叉归类；人数随学校、匹配和其他筛选更新。</p></div>
      {area && <button className="button" onClick={() => onArea('')}>全部方向</button>}</div>
    <div className="direction-grid">{areas.map(label => {
      const contacts = rows.filter(r => r.researchAreas.includes(label));
      const schools = [...new Set(contacts.map(r => r.school))];
      const real = contacts.filter(r => r.fitCategory === 'ai-real').length;
      return <article className={`direction-card ${area === label ? 'selected' : ''}`} key={label}>
        <button className="direction-select" aria-pressed={area === label} onClick={() => onArea(area === label ? '' : label)}>
          <span>{label}</span><strong>{contacts.length}<small> 位</small></strong>
          <span className="direction-description">{real} 位有 AI + 真机线索 · {schools.length} 所学校</span>
        </button>
        <div className="direction-card-footer"><span>{schools.slice(0, 2).join(' · ') || '当前筛选无候选'}</span>
          <a href={browseHref('directions', { area: label, school, fit })} target="_blank" rel="noreferrer" aria-label={`新标签页浏览 ${label}`}>新开 ↗</a></div>
      </article>;
    })}</div>
    {school && <p className="school-context">当前只看 <strong>{school}</strong> <button onClick={() => onSchool('')}>查看全部学校</button></p>}
  </section>;
}
