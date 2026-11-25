const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, 'out') + '/';
const [,, slug, patch, prefix] = process.argv;
const fd = JSON.parse(fs.readFileSync(OUT + patch)).fieldData;
(async () => {
  const b = await chromium.launch();
  for (const w of [1280, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    await p.route(/cdn\.prod\.website-files\.com/, async route => {
      const u = route.request().url().replace(/^https:\/\/cdn\.prod\.website-files\.com\//, 'https://s3.amazonaws.com/webflow-prod-assets/');
      try { const r = await route.fetch({ url: u }); await route.fulfill({ response: r }); } catch (e) { await route.abort(); }
    });
    await p.goto('https://www.jem.social/blog/' + slug, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {});
    const log = await p.evaluate((fd) => {
      const out = [];
      const body = document.querySelector('.jb-body.w-richtext') || document.querySelector('.jb-body');
      if (!body) out.push('MISSING body'); else body.innerHTML = fd['blog-summary'];
      const h1 = document.querySelector('h1'); if (h1) h1.textContent = fd['name']; else out.push('MISSING h1');
      return out;
    }, fd);
    await p.waitForTimeout(1500);
    const info = await p.evaluate(() => ({ overflowX: document.documentElement.scrollWidth > window.innerWidth, h: document.documentElement.scrollHeight }));
    console.log(w, JSON.stringify(info), log.join(' | ') || 'ok');
    await p.screenshot({ path: OUT + `${prefix}_${w}.png`, fullPage: true });
    await p.close();
  }
  await b.close();
})();
