import type { Dataset, View } from '../types';
export function MetricCards({ meta, onView }: { meta: Dataset['meta']; onView: (v: View) => void }) {
  return <div className="metrics" aria-label="整份名单统计">
    <button className="metric" onClick={() => onView('all')}><span className="metric-label">导师候选</span><strong>{meta.total}</strong><span className="metric-note">覆盖 {meta.schools} 所美国高校</span></button>
    <button className="metric" onClick={() => onView('new')}><span className="metric-label">近期入职 AP</span><strong>{meta.newAp}</strong><span className="metric-note">已确认现校 2024–2026 入职</span></button>
    <button className="metric" onClick={() => onView('opening')}><span className="metric-label">公开合作入口</span><strong>{meta.publicOpenings}</strong><span className="metric-note">含短期、长期及限制性入口</span></button>
    <article className="metric"><span className="metric-label">线下目标时长</span><strong>8 <small>周左右</small></strong><span className="metric-note">远程也可讨论 · 2027 夏季</span></article>
  </div>;
}
