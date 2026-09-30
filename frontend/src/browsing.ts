import type { Contact, View } from './types';

export type PageMode = 'contacts' | 'directions';
export const fitLabels = { 'ai-real': 'AI + 真机线索', 'ai-pending': 'AI 相关 · 真机待核实', robotics: '机器人方法 / 系统' };
export const identityLabels: Record<string, string> = { chinese: '华人', white: '白人', white_male: '白男', white_female: '白女', unknown: '身份资料未知' };
export function matchesIdentity(r: Contact, identity: string) {
  if (!identity) return true;
  const ethnicity = r.ethnicitySource ? r.selfReportedEthnicity : '未知';
  const gender = r.genderSource ? r.selfReportedGender : '未知';
  if (identity === 'unknown') return ethnicity === '未知' || gender === '未知';
  if (identity === 'chinese') return ethnicity === '华人';
  if (identity === 'white') return ethnicity === '白人';
  return ethnicity === '白人' && (identity === 'white_male' ? gender === '男性' : gender === '女性');
}
export function readRoute() {
  const [path, search = ''] = window.location.hash.slice(1).split('?');
  const p = new URLSearchParams(search);
  const view = p.get('view') ?? 'all';
  return { mode: (path === 'directions' ? 'directions' : 'contacts') as PageMode,
    school: p.get('school') ?? '', fit: p.get('fit') ?? '', area: p.get('area') ?? '', theme: p.get('theme') ?? '',
    query: p.get('q') ?? '', identity: p.get('identity') ?? '', nationality: p.get('nationality') ?? '',
    country: p.get('country') ?? '', view: (['all','added','new','opening','saved'].includes(view) ? view : 'all') as View };
}
export function browseHref(mode: PageMode, values: Record<string, string> = {}) {
  const p = new URLSearchParams();
  Object.entries(values).forEach(([k, v]) => { if (v && !(k === 'view' && v === 'all')) p.set(k, v); });
  return `#${mode}${p.size ? '?' + p.toString() : ''}`;
}
