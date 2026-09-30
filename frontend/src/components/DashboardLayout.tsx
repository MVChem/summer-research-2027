import { useEffect, useRef, useState, type ReactNode } from 'react';
import type { Dataset, View } from '../types';
import type { PageMode } from '../browsing';
const labels: Record<View, string> = { all: '全部候选', added: '本次新增 100 位', new: '近期入职 AP', opening: '公开合作入口', saved: '我的收藏' };
export function DashboardLayout({ meta, view, theme, savedCount, setView, setTheme, children, actions, pageMode, onMode, directionHref }:
  { meta: Dataset['meta']; view: View; theme: string; savedCount: number; setView: (v: View) => void;
    setTheme: (t: string) => void; children: ReactNode; actions: ReactNode; pageMode: PageMode;
    onMode: (mode: PageMode) => void; directionHref: string }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const drawer = useRef<HTMLDialogElement>(null); const menu = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (menuOpen && !drawer.current?.open) drawer.current?.showModal();
    if (!menuOpen && drawer.current?.open) drawer.current?.close();
  }, [menuOpen]);
  const nav = <>
    <div className="brand"><span className="brand-icon">SR</span><div>Summer Research<span>2027 · United States</span></div></div>
    <p className="nav-label">候选名单</p><nav aria-label="名单范围" className="navigation">{(Object.keys(labels) as View[]).map(v => <button key={v} className={pageMode === 'contacts' && view === v && !theme ? 'active' : ''}
      onClick={() => { onMode('contacts'); setView(v); setTheme(''); setMenuOpen(false); }} aria-current={pageMode === 'contacts' && view === v && !theme ? 'page' : undefined}>
      <span>{labels[v]}</span><span className="nav-count">{v === 'all' ? meta.total : v === 'added' ? meta.added : v === 'new' ? meta.newAp : v === 'opening' ? meta.publicOpenings : savedCount}</span>
    </button>)}</nav>
    <p className="nav-label">按研究方向浏览</p><div className="direction-nav"><button className={`button ${pageMode === 'directions' ? 'primary' : ''}`} onClick={() => { onMode('directions'); setTheme(''); setView('all'); setMenuOpen(false); }}>方向总览</button><a href={directionHref} target="_blank" rel="noreferrer" className="button" aria-label="新标签页打开研究方向">新开 ↗</a></div>
    <nav aria-label="研究方向" className="navigation theme-navigation">{meta.themes.map(t => <button key={t} className={theme === t ? 'active' : ''}
      onClick={() => { onMode('contacts'); setTheme(t); setView('all'); setMenuOpen(false); }}>{t}</button>)}</nav>
    <div className="sidebar-footer"><strong>国科大 CS · 研二</strong><span>可自费 · 线下 / 远程</span><span>核查 {meta.checkedAt}</span></div>
  </>;
  return <><a className="skip-link" href="#main">跳到名单内容</a><aside className="sidebar">{nav}</aside>
    <div className="workspace"><header className="header"><div className="header-title">
      <button ref={menu} className="icon-button menu-button" aria-label="打开导航" aria-controls="mobile-nav" aria-expanded={menuOpen} onClick={() => setMenuOpen(true)}>☰</button>
      <span>研究机会 / <strong>{pageMode === 'directions' ? '研究方向' : '候选名单'}</strong></span></div>{actions}</header><main id="main" tabIndex={-1}>{children}</main></div>
    <dialog ref={drawer} id="mobile-nav" className="nav-dialog" aria-label="研究机会导航" onCancel={() => setMenuOpen(false)} onClose={() => { setMenuOpen(false); menu.current?.focus(); }}>
      <button className="button drawer-close" onClick={() => setMenuOpen(false)}>关闭</button>{nav}
    </dialog></>;
}
