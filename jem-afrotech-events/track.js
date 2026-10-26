// Attribution + conversion-event test against the local preview
const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const ctx = await b.newContext();
  await ctx.addInitScript(() => {
    window.__ev = [];
    window.gtag = (...a) => window.__ev.push(['ga', a[1], a[2]]);
    window.plausible = (n, o) => window.__ev.push(['pl', n, o && o.props]);
    window.fbq = (...a) => window.__ev.push(['fb', a[1]]);
    window.ttq = { track: (n) => window.__ev.push(['tt', n]) };
  });
  const pg = await ctx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + dir + '/preview.html?utm_source=instagram&utm_medium=social&utm_campaign=afrotech26&utm_content=creators');
  await pg.waitForTimeout(800);
  const hidden = await pg.evaluate(() => Object.fromEntries([...document.querySelectorAll('[data-afro=card] input[type=hidden]')].map(i => [i.name, i.value])));
  // restored unlock must not count as a lead; real submit must count once
  await pg.fill('input[name=Email]', 'test@example.com'); await pg.selectOption('#at-role', 'Brand or marketer');
  await pg.click('input[type=submit]'); await pg.waitForTimeout(300);
  await pg.evaluate(() => { document.querySelectorAll('a').forEach(a => a.addEventListener('click', e => e.preventDefault())) });
  await pg.click('#jem-picks .at-ev-h a'); await pg.click('a[href*="source=afrotech_2026_brand"]');
  const ev = await pg.evaluate(() => window.__ev);
  // second visit, no UTMs, already unlocked via storage: no lead event
  const pg2 = await ctx.newPage(); await pg2.goto('file://' + dir + '/preview.html'); await pg2.waitForTimeout(600);
  const ev2 = await pg2.evaluate(() => window.__ev.filter(e => e[1] === 'generate_lead').length);
  // ?unlock=1 on a fresh browser
  const ctx3 = await b.newContext(); const pg3 = await ctx3.newPage(); await pg3.goto('file://' + dir + '/preview.html?unlock=1'); await pg3.waitForTimeout(600);
  const emailUnlock = await pg3.evaluate(() => document.documentElement.classList.contains('afro-unlocked'));
  console.log(JSON.stringify({ hidden, ev, leadOnRestore: ev2, emailUnlock, errs }, null, 1));
  await b.close();
})();
