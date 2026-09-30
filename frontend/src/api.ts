import snapshot from './contacts.snapshot.json';
import type { Contact, Dataset, Progress, Recordings } from './types';
import { recordingFilename } from './recordings';

export const offlineDataset = snapshot as Dataset;
export async function loadDataset(signal: AbortSignal): Promise<Dataset> {
  if (window.location.protocol === 'file:') return offlineDataset;
  const response = await fetch('/api/contacts', { signal });
  if (!response.ok) throw new Error(`名单加载失败（HTTP ${response.status}）`);
  const data: Dataset = await response.json();
  if (!Array.isArray(data.contacts) || data.contacts.length !== data.meta.total || data.meta.version !== 'v2') throw new Error('名单版本或数据不完整，请重试或使用内置名单。');
  return data;
}
export function downloadCsv(rows: Contact[], progress: Progress, recordings: Recordings) {
  const headers = ['编号','导师','学校','方向','主页','职级','现校AP入职','新AP','公开访学信息','招募链接','公开邮箱','联系方式','时长','远程','经费','资料备注','核查日期','联系状态','收藏','我的看法','看法更新时间','录音数量','录音文件名（需单独下载）','名单批次','细分方向','AI与真机匹配','匹配理由','学校所在国家','本人公开国籍','本人自述族裔','本人自述性别','身份资料来源','研究来源'];
  const escape = (value: unknown) => {
    let s = String(value ?? '');
    if (/^[=+@-]/.test(s)) s = `'${s}`;
    return `"${s.replace(/"/g, '""')}"`;
  };
  const lines = [headers, ...rows.map(r => [r.id,r.name,r.school,r.direction,r.homepage,r.rank,r.joined,r.newAp?'是':'否',r.publicOpening,r.openingUrl,r.email,r.contactRoute,r.durationNote,r.remote,r.funding,r.note,r.checkedAt,progress[r.name]?.status??'未联系',progress[r.name]?.saved?'是':'否',progress[r.name]?.personalNote ?? '',progress[r.name]?.noteUpdatedAt ?? '',recordings[r.name]?.length ?? 0,(recordings[r.name] ?? []).map(recordingFilename).join('; '),r.batch,r.researchAreas.join(' / '),r.fitLabel,r.fitReason,r.institutionCountry,r.nationality,r.selfReportedEthnicity,r.selfReportedGender,[r.nationalitySource,r.ethnicitySource,r.genderSource].filter(Boolean).join('; '),r.sources.map(s => s.url).join('; ')])];
  const blob = new Blob(['\ufeff' + lines.map(l => l.map(escape).join(',')).join('\r\n')], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a'); anchor.href = url; anchor.download = `summer-research-${rows.length}-contacts.csv`;
  document.body.append(anchor); anchor.click(); anchor.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
}
