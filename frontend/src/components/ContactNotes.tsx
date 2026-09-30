import { useEffect, useRef, useState } from 'react';
import { deleteRecording, formatDuration, getRecordingBlob, recordingFilename, saveRecording } from '../recordings';
import type { Contact, Recording, Status } from '../types';
import { MicrophoneIcon } from './NoteIcons';

type RecorderState = 'idle' | 'requesting' | 'recording' | 'saving';
type PendingRecording = { clip: Recording; blob: Blob };

function AudioClip({ clip, blob, active, onDelete, deleteLabel = '删除' }: {
  clip: Recording; blob?: Blob; active: boolean; onDelete: () => Promise<void> | void; deleteLabel?: string;
}) {
  const [url, setUrl] = useState(''); const [error, setError] = useState('');
  const [revision, setRevision] = useState(0); const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false); const audio = useRef<HTMLAudioElement>(null);
  useEffect(() => {
    let cancelled = false; let objectUrl = ''; setError('');
    (blob ? Promise.resolve(blob) : getRecordingBlob(clip.id)).then(data => {
      if (cancelled) return;
      objectUrl = URL.createObjectURL(data); setUrl(objectUrl);
    }).catch(e => { if (!cancelled) setError(e instanceof Error ? e.message : '录音加载失败。'); });
    return () => { cancelled = true; if (objectUrl) URL.revokeObjectURL(objectUrl); };
  }, [clip.id, blob, revision]);
  useEffect(() => { if (active) audio.current?.pause(); }, [active]);
  const remove = async () => {
    setDeleting(true); setError('');
    try { await onDelete(); } catch (e) { setError(e instanceof Error ? e.message : '删除失败，请重试。'); }
    finally { setDeleting(false); setConfirmDelete(false); }
  };
  return <article className="audio-clip">
    <div className="audio-clip-heading"><span>{blob ? '临时录音 · 尚未保存' : '语音备注'} <span className="muted">{formatDuration(clip.duration)}</span></span>
      <time dateTime={clip.createdAt}>{new Date(clip.createdAt).toLocaleString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</time></div>
    {url ? <audio ref={audio} controls preload="metadata" src={url} aria-label={`${clip.contactName} 的语音备注`} onError={() => setError('录音无法播放，可以下载后用其他播放器打开。')} /> : !error && <p className="small muted">正在读取录音…</p>}
    <div className="audio-clip-actions">{url && <a className="button" href={url} download={recordingFilename(clip)}>下载录音</a>}
      {confirmDelete ? <><button className="button danger-button" disabled={deleting || active} onClick={() => void remove()}>{deleting ? '正在删除…' : '确认删除'}</button><button className="button" disabled={deleting} onClick={() => setConfirmDelete(false)}>取消</button></>
        : <button className="button" disabled={active} onClick={() => setConfirmDelete(true)}>{deleteLabel}</button>}
      {error && !url && <button className="button" onClick={() => setRevision(v => v + 1)}>重试读取</button>}</div>
    {error && <p className="notes-error" role="alert">{error}</p>}
  </article>;
}

export function ContactNotes({ contact, mode, note, clips, storageError, status, saved, onNote, onStatus, onSave,
  onAdded, onDeleted, close }: {
  contact: Contact; mode: 'record' | 'text'; note: string; clips: Recording[]; storageError: string;
  status: Status; saved: boolean; onNote: (value: string) => void; onStatus: (value: Status) => void; onSave: () => void;
  onAdded: (clip: Recording) => void; onDeleted: (id: string) => void; close: () => void;
}) {
  const dialog = useRef<HTMLDialogElement>(null); const textarea = useRef<HTMLTextAreaElement>(null);
  const alive = useRef(false); const stream = useRef<MediaStream | null>(null);
  const recorder = useRef<MediaRecorder | null>(null); const closeAfterSave = useRef(false);
  const stateRef = useRef<RecorderState>('idle'); const [state, setState] = useState<RecorderState>('idle');
  const [seconds, setSeconds] = useState(0); const startedAt = useRef(0);
  const [error, setError] = useState(''); const [message, setMessage] = useState('');
  const [pending, setPending] = useState<PendingRecording | null>(null);
  const transition = (next: RecorderState) => { stateRef.current = next; if (alive.current) setState(next); };
  const releaseMicrophone = () => { stream.current?.getTracks().forEach(track => { track.onended = null; track.stop(); }); stream.current = null; };
  const persist = async (value: PendingRecording) => {
    transition('saving'); setError('');
    try {
      await saveRecording(value.clip, value.blob);
      if (!alive.current) return;
      onAdded(value.clip); setPending(null); setMessage('录音已保存，可以回放或继续录一段。'); transition('idle');
      if (closeAfterSave.current) close();
    } catch (e) {
      if (alive.current) { setError(e instanceof Error ? e.message : '录音保存失败，请先下载再重试。'); transition('idle'); }
    } finally { closeAfterSave.current = false; }
  };
  const start = async () => {
    if (stateRef.current !== 'idle' || pending) return;
    setError(''); setMessage(''); setSeconds(0);
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === 'undefined') {
      setError('当前页面无法使用麦克风。请用 Chrome、Edge 或 Firefox 打开本地应用（http://127.0.0.1:8790），也可以直接填写文字备注。'); return;
    }
    transition('requesting');
    try {
      const input = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!alive.current) { input.getTracks().forEach(track => track.stop()); return; }
      stream.current = input;
      const mimeType = ['audio/webm;codecs=opus', 'audio/mp4', 'audio/ogg;codecs=opus', 'audio/webm'].find(type => MediaRecorder.isTypeSupported(type));
      const capture = new MediaRecorder(input, mimeType ? { mimeType } : undefined);
      recorder.current = capture; const chunks: Blob[] = [];
      capture.ondataavailable = event => { if (event.data.size) chunks.push(event.data); };
      capture.onerror = () => { if (alive.current) setError('录音中断，将尝试保存已录制的部分。'); if (capture.state !== 'inactive') stop(); };
      capture.onstop = () => {
        releaseMicrophone(); recorder.current = null;
        if (!alive.current) return;
        const blob = new Blob(chunks, { type: capture.mimeType || chunks[0]?.type || 'audio/webm' });
        if (!blob.size) { transition('idle'); setError('没有录到声音，请检查麦克风后重试。'); closeAfterSave.current = false; return; }
        const clip: Recording = { id: crypto.randomUUID(), contactName: contact.name, createdAt: new Date().toISOString(),
          duration: Math.max(1, (performance.now() - startedAt.current) / 1000), mimeType: blob.type };
        const value = { clip, blob }; setPending(value); void persist(value);
      };
      input.getAudioTracks().forEach(track => { track.onended = () => { if (capture.state !== 'inactive') stop(); }; });
      startedAt.current = performance.now(); capture.start(1000); transition('recording');
    } catch (e) {
      releaseMicrophone();
      if (!alive.current) return;
      const name = e instanceof DOMException ? e.name : '';
      setError(name === 'NotAllowedError' || name === 'SecurityError' ? '麦克风权限未开启，请在浏览器中允许此页面使用麦克风，再重试。文字备注仍可使用。'
        : name === 'NotFoundError' ? '没有找到麦克风，请连接麦克风后重试。文字备注仍可使用。'
        : name === 'NotReadableError' ? '麦克风暂时无法使用，请关闭占用麦克风的其他应用后重试。'
        : '无法开始录音，请检查麦克风后重试。文字备注仍可使用。');
      transition('idle');
    }
  };
  const stop = (thenClose = false) => {
    closeAfterSave.current = thenClose;
    if (recorder.current?.state !== 'inactive' && recorder.current) { transition('saving'); recorder.current.stop(); }
  };
  const requestClose = () => {
    if (stateRef.current === 'saving') return;
    if (stateRef.current === 'recording') { stop(true); return; }
    if (pending) { setError('这段录音还未保存，请重试保存或先下载。下载后可选择放弃这段录音。'); return; }
    close();
  };
  useEffect(() => {
    alive.current = true; dialog.current?.showModal();
    const timer = window.setTimeout(() => { if (mode === 'record') void start(); else textarea.current?.focus(); }, 0);
    return () => {
      window.clearTimeout(timer); alive.current = false;
      const capture = recorder.current;
      if (capture) { capture.ondataavailable = null; capture.onstop = null; capture.onerror = null; if (capture.state !== 'inactive') capture.stop(); }
      releaseMicrophone();
    };
  }, []);
  useEffect(() => {
    if (state !== 'recording') return;
    const timer = window.setInterval(() => setSeconds(Math.floor((performance.now() - startedAt.current) / 1000)), 250);
    return () => window.clearInterval(timer);
  }, [state]);
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => { event.preventDefault(); event.returnValue = ''; };
    if (state !== 'idle' || pending) window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [state, pending]);
  const busy = state !== 'idle';
  return <dialog ref={dialog} className="detail-dialog notes-dialog" aria-labelledby="notes-title" onCancel={event => { event.preventDefault(); requestClose(); }}>
    <div className="detail-header"><div><p className="eyebrow">我的看法 · {contact.school}</p><h2 id="notes-title">{contact.name}</h2></div>
      <button className="button" disabled={state === 'saving'} onClick={requestClose}>{state === 'recording' ? '停止并关闭' : '完成'}</button></div>
    <p className="detail-direction">{contact.direction}</p>
    <section className={`recorder-panel ${state === 'recording' ? 'is-recording' : ''}`} aria-label="录音备注">
      <div className="recorder-copy"><strong>{state === 'recording' ? '正在录音' : state === 'requesting' ? '等待麦克风权限…' : state === 'saving' ? '正在保存录音…' : '说说你对这位导师的看法'}</strong>
        <p>{state === 'recording' ? '可以一边说，一边补充下面的文字。' : '研究是否合适、想合作的课题、联系前要确认的事。'}</p></div>
      <div className="recorder-controls">{state === 'recording' && <span className="recording-clock"><span className="recording-dot" />{formatDuration(seconds)}</span>}
        <button className={`button ${state === 'recording' ? 'record-stop' : 'primary'}`} disabled={state === 'requesting' || state === 'saving' || Boolean(pending)} onClick={() => state === 'recording' ? stop() : void start()}>
          {state === 'recording' ? <span aria-hidden="true" className="stop-icon" /> : <MicrophoneIcon />}{state === 'recording' ? '停止并保存' : state === 'requesting' ? '等待权限…' : state === 'saving' ? '保存中…' : '开始录音'}</button></div>
    </section>
    <p className="small muted notes-hint">录音保存原音。点击“停止并保存”后可回放；文字备注会自动保存。</p>
    {error && <p className="notes-error" role="alert">{error}</p>}
    {pending && state !== 'saving' && <div className="pending-recording"><AudioClip clip={pending.clip} blob={pending.blob} active={busy} deleteLabel="放弃这段录音" onDelete={() => { setPending(null); setError(''); }} />
      <button className="button primary" onClick={() => void persist(pending)}>重试保存录音</button></div>}
    <div className="note-label"><label htmlFor="personal-note">文字备注</label><span className={storageError ? 'notes-error' : 'muted'} role="status">{storageError ? '未能保存' : '自动保存到此浏览器'}</span></div>
    <textarea ref={textarea} id="personal-note" className="personal-note-input" value={note} onChange={event => onNote(event.target.value)} rows={6}
      placeholder="例如：方向很匹配，想进一步看他的机器人学习论文；联系时问一下能否接受 8 周暑研。" />
    {storageError && <p className="notes-error" role="alert">{storageError}</p>}
    <div className="notes-followup"><label htmlFor="notes-contact-status">联系进度</label><select id="notes-contact-status" className="status-select" value={status} onChange={event => onStatus(event.target.value as Status)}>
      {(['未联系', '已联系', '已回复', '暂不联系'] as Status[]).map(value => <option key={value}>{value}</option>)}</select>
      <button className={`button ${saved ? 'note-saved' : ''}`} aria-pressed={saved} onClick={onSave}>{saved ? '已收藏 · 点击取消' : '收藏，稍后联系'}</button></div>
    <div className="saved-recordings"><h3>已保存的录音 <span className="muted">{clips.length}</span></h3>
      {!clips.length ? <p className="small muted">还没有录音。也可以只写文字备注。</p> : clips.map(clip => <AudioClip key={clip.id} clip={clip} active={busy}
        onDelete={async () => { await deleteRecording(clip.id); onDeleted(clip.id); }} />)}</div>
    <p className="small muted notes-storage">文字与录音保存在当前浏览器。导出名单包含文字备注；录音请单独下载。可用“有备注 / 录音”筛选回看。</p>
    <div className="sr-only" role="status" aria-live="polite">{message}</div>
  </dialog>;
}
