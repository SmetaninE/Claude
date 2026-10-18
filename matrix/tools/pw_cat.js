const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [,, url, out] = process.argv;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy, args:['--ignore-certificate-errors-spki-list'] });
  const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36', locale:'ru-RU', viewport:{width:1366,height:900} });
  const p = await ctx.newPage();
  try {
    const r = await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await p.waitForTimeout(9000);
    try { await p.mouse.wheel(0, 4000); await p.waitForTimeout(3000);} catch(e){}
    const html = await p.content();
    require('fs').writeFileSync(out, html);
    console.log(url, r && r.status(), p.url(), html.length, await p.title());
  } catch (e) { console.log(url, 'ERR', e.message.split('\n')[0]); }
  await b.close();
})();
