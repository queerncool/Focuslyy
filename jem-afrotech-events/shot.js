// Visual + behaviour checks for the category layout against the local Webflow mock
const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  for (const [name, w, h] of [['desk', 1280, 900], ['mob', 390, 844]]) {
    const pg = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('file://' + dir + '/preview.html'); await pg.waitForTimeout(1200);
    await pg.screenshot({ path: `${dir}/${name}-top.png` });
    const vis = () => pg.evaluate(() => [...document.querySelectorAll('.at-ev')].filter(e => e.offsetParent !== null).length);
    const lockedVisible = await vis();
    await pg.evaluate(() => document.getElementById('cat-party').scrollIntoView()); await pg.waitForTimeout(300);
    const fixedBar = await pg.evaluate(() => document.querySelector('.at-bar').classList.contains('at-fixed'));
    await pg.screenshot({ path: `${dir}/${name}-cat.png` });
    await pg.evaluate(() => document.getElementById('cat-networking').scrollIntoView()); await pg.waitForTimeout(300);
    await pg.screenshot({ path: `${dir}/${name}-cat2.png` });
    const ow = await pg.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    await pg.fill('input[name=Email]', 'test@example.com'); await pg.selectOption('#at-role', 'Agency');
    await pg.click('input[type=submit]'); await pg.waitForTimeout(400);
    const unlocked = await pg.evaluate(() => document.documentElement.classList.contains('afro-unlocked'));
    const unlockedVisible = await vis();
    await pg.evaluate(() => document.getElementById('cat-career').scrollIntoView()); await pg.waitForTimeout(300);
    await pg.screenshot({ path: `${dir}/${name}-unlocked.png` });
    await pg.click('.at-f[data-f=d5]'); await pg.waitForTimeout(200);
    const thu = await vis();
    const heads = await pg.evaluate(() => [...document.querySelectorAll('.at-catblock[data-head]')].filter(s => s.style.display !== 'none').map(s => s.id + ':' + s.querySelector('.at-day-n').textContent));
    await pg.click('.at-f[data-f=free]'); await pg.waitForTimeout(200);
    const free = await vis();
    await pg.click('.at-c[data-c=party]'); await pg.waitForTimeout(300);
    const partyFree = await vis();
    await pg.screenshot({ path: `${dir}/${name}-browse.png` });
    await pg.click('.at-f[data-f=all]'); await pg.waitForTimeout(200);
    const party = await vis();
    const shownSecs = await pg.evaluate(() => [...document.querySelectorAll('.at-catblock')].filter(s => s.style.display !== 'none').map(s => s.getAttribute('data-cat')));
    const picksShown = await pg.evaluate(() => document.getElementById('jem-picks').style.display !== 'none');
    await pg.reload(); await pg.waitForTimeout(800);
    const persisted = await pg.evaluate(() => document.documentElement.classList.contains('afro-unlocked'));
    console.log(name, JSON.stringify({ overflowX: ow, lockedVisible, fixedBar, unlocked, unlockedVisible, thu, heads, free, partyFree, party, shownSecs, picksShown, persisted, errs }));
  }
  await b.close();
})();
