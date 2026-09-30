const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const path = require('node:path');
const fs = require('node:fs');
const root = path.resolve(__dirname, '..');
const dataset = JSON.parse(fs.readFileSync(path.join(root,'data/contacts.json'),'utf8'));
async function main() {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
    headless: true, args: ['--no-sandbox'],
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, acceptDownloads: true });
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    const checks = [];
    const check = (value, label) => { if (!value) throw new Error(label); checks.push(label); };
    await page.goto('file://' + path.join(root, 'index.html'));
    await page.waitForSelector('.contacts-table tbody tr');
    check(await page.locator('tbody tr').count() === 25, 'single-file HTML opens with 25 rows');
    await page.locator('.view-tabs button').filter({ hasText: '近期入职 AP' }).click();
    check(await page.locator('tbody tr').count() === dataset.meta.newAp, 'confirmed recent AP count');
    await page.locator('.view-tabs button').filter({ hasText: '公开合作入口' }).click();
    check(await page.locator('tbody tr').count() === 16, '16 public collaboration routes');
    await page.getByRole('button', { name: '重置筛选', exact: true }).click();
    await page.getByRole('textbox', { name: '搜索导师、学校、方向' }).fill('Judy');
    await page.waitForTimeout(100);
    check((await page.locator('tbody tr').innerText()).includes('UC Irvine'), 'current school correction');
    await page.getByRole('button', { name: '详情', exact: true }).click();
    await page.waitForSelector('dialog.detail-dialog[open]');
    check((await page.locator('dialog.detail-dialog').innerText()).includes('Associate'), 'faculty detail');
    await page.locator('dialog.detail-dialog').getByRole('button', { name: '关闭', exact: true }).click();
    await page.getByRole('button', { name: '收藏 Judy Hoffman', exact: true }).click();
    await page.locator('tbody select').selectOption('已联系');
    await page.reload(); await page.waitForSelector('tbody tr');
    await page.locator('.view-tabs button').filter({ hasText: '我的收藏' }).click();
    check(await page.locator('tbody tr').count() === 1, 'favorite survives reload');
    check(await page.locator('tbody select').inputValue() === '已联系', 'contact status survives reload');
    await page.getByRole('button', { name: '重置筛选', exact: true }).click();
    await page.getByRole('combobox', { name: '每页数量', exact: true }).selectOption('100');
    await page.waitForTimeout(100);
    check(await page.locator('tbody tr').count() === 100, 'all 100 rows accessible');
    await page.getByRole('combobox', { name: '每页数量', exact: true }).selectOption('25');
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: /导出名单/ }).click();
    const download = await downloadPromise;
    const exportPath = '/tmp/summer-research-browser-export.csv'; await download.saveAs(exportPath);
    check(fs.readFileSync(exportPath, 'utf8').split(/\r?\n/).filter(Boolean).length === dataset.meta.total+1, 'export includes every filtered page');
    await page.getByRole('textbox', { name: '搜索导师、学校、方向' }).fill('no-faculty-such-name');
    await page.waitForTimeout(100);
    check(await page.locator('tbody tr').count() === 0, 'search empty state');
    await page.getByRole('button', { name: `查看全部 ${dataset.meta.total} 位`, exact: true }).click();
    await page.waitForTimeout(100);
    await page.screenshot({ path: path.join(root, 'preview-desktop.png') });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: path.join(root, 'preview-mobile.png') });
    const widths = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth }));
    check(widths.document <= widths.viewport, 'mobile has no page overflow');
    await page.getByRole('button', { name: '打开导航', exact: true }).click();
    await page.waitForSelector('dialog#mobile-nav[open]');
    await page.locator('#mobile-nav').getByRole('button', { name: /Medical/ }).click();
    check(await page.locator('dialog#mobile-nav[open]').count() === 0, 'mobile navigation works');
    const server = process.env.TEST_SERVER || 'http://127.0.0.1:8790';
    await page.goto(server); await page.waitForSelector('tbody tr');
    check(await page.locator('tbody tr').count() === 25, 'FastAPI served React page');
    const response = await page.request.get(server + '/api/contacts'); const data = await response.json();
    check(data.contacts.length === dataset.meta.total && data.meta.publicOpenings === dataset.meta.publicOpenings, 'browser receives current FastAPI data');
    const badQuery = await page.request.get(server + '/api/contacts/export?view=invalid');
    check(badQuery.status() === 422, 'API rejects invalid filters');
    check(errors.length === 0, 'no browser script errors');
    const result = { checkedAt: '2026-10-01', checks, mobile: widths, browserErrors: errors };
    fs.writeFileSync(path.join(root, 'verification.json'), JSON.stringify(result, null, 2));
    console.log(JSON.stringify(result));
  } finally { await browser.close(); }
}
main().catch(e => { console.error(e); process.exit(1); });
