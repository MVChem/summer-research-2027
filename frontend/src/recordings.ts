import type { Recording, Recordings } from './types';

let database: Promise<IDBDatabase> | undefined;
function openDatabase(): Promise<IDBDatabase> {
  if (!database) {
    database = new Promise((resolve, reject) => {
      if (!window.indexedDB) { reject(new Error('当前浏览器不能保存录音，请换用普通浏览器窗口。')); return; }
      const request = indexedDB.open('summer-research-2027-recordings-v1', 1);
      request.onupgradeneeded = () => {
        request.result.createObjectStore('recordings', { keyPath: 'id' });
        request.result.createObjectStore('audio');
      };
      request.onerror = () => reject(new Error('无法打开录音存储，请检查浏览器的存储权限。'));
      request.onblocked = () => reject(new Error('录音存储被其他页面占用，请关闭旧页面后重试。'));
      request.onsuccess = () => {
        const db = request.result;
        db.onversionchange = () => { db.close(); database = undefined; };
        resolve(db);
      };
    });
    database.catch(() => { database = undefined; });
  }
  return database;
}

export async function listRecordings(): Promise<Recordings> {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const request = db.transaction('recordings').objectStore('recordings').getAll();
    request.onerror = () => reject(new Error('无法读取已保存的录音。'));
    request.onsuccess = () => {
      const grouped: Recordings = {};
      (request.result as Recording[]).sort((a, b) => b.createdAt.localeCompare(a.createdAt)).forEach(clip => {
        (grouped[clip.contactName] ??= []).push(clip);
      });
      resolve(grouped);
    };
  });
}

export async function saveRecording(clip: Recording, blob: Blob): Promise<void> {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(['recordings', 'audio'], 'readwrite');
    transaction.objectStore('recordings').put(clip);
    transaction.objectStore('audio').put(blob, clip.id);
    transaction.oncomplete = () => resolve();
    transaction.onabort = () => reject(new Error('录音未能保存，浏览器空间可能不足。可以先下载这段录音，再重试。'));
    transaction.onerror = () => { /* onabort reports the failed transaction. */ };
  });
}

export async function getRecordingBlob(id: string): Promise<Blob> {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const request = db.transaction('audio').objectStore('audio').get(id);
    request.onerror = () => reject(new Error('无法读取这段录音，请重试。'));
    request.onsuccess = () => request.result instanceof Blob ? resolve(request.result) : reject(new Error('这段录音文件已不存在。'));
  });
}

export async function deleteRecording(id: string): Promise<void> {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(['recordings', 'audio'], 'readwrite');
    transaction.objectStore('recordings').delete(id);
    transaction.objectStore('audio').delete(id);
    transaction.oncomplete = () => resolve();
    transaction.onabort = () => reject(new Error('录音删除失败，请重试。'));
    transaction.onerror = () => { /* onabort reports the failed transaction. */ };
  });
}

export function recordingFilename(clip: Recording): string {
  const extension = clip.mimeType.includes('mp4') ? 'm4a' : clip.mimeType.includes('ogg') ? 'ogg' : 'webm';
  return `${clip.contactName.replace(/[^\p{L}\p{N}_-]/gu, '_')}-${clip.createdAt.replace(/[:.]/g, '-')}.${extension}`;
}
export function formatDuration(seconds: number): string {
  const total = Math.max(0, Math.round(seconds));
  return `${Math.floor(total / 60).toString().padStart(2, '0')}:${(total % 60).toString().padStart(2, '0')}`;
}
