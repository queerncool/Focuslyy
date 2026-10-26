// Renders each slide HTML to a 1080x1350 PNG and flags any text overflowing the slide
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const dir = process.argv[2], out = process.argv[3];
  const m = JSON.parse(fs.readFileSync(dir + '/manifest.json'));
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [k, files] of Object.entries(m)) for (const f of files) {
    await pg.goto('file://' + dir + '/' + f); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(250);
    const bad = await pg.evaluate(() => { const foot = document.querySelector('.foot').getBoundingClientRect().top; let max = 0;
      document.querySelectorAll('.z *').forEach(e => { const r = e.getBoundingClientRect(); if (r.height) max = Math.max(max, r.bottom) }); return max > foot - 24 ? Math.round(max - foot) : 0 });
    const fonts = await pg.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i).join(','));
    await pg.screenshot({ path: `${out}/${f.replace('.html', '.png')}` });
    if (bad) console.log('OVERFLOW', f, bad);
  }
  console.log('fonts:', await pg.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i).join(', ')));
  await b.close();
})();
