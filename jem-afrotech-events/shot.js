const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  for (const [name, w, h] of [['desk', 1280, 900], ['mob', 390, 844]]) {
    const pg = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('file://' + dir + '/preview.html'); await pg.waitForTimeout(1500);
    await pg.screenshot({ path: `${dir}/${name}-top.png` });
    await pg.evaluate(() => document.querySelector('.at-bar').scrollIntoView());
    await pg.waitForTimeout(300); await pg.screenshot({ path: `${dir}/${name}-list.png` });
    await pg.evaluate(() => document.querySelector('.at-over').scrollIntoView({block:'end'}));
    await pg.waitForTimeout(300); await pg.screenshot({ path: `${dir}/${name}-gate.png` });
    // overflow check
    const ow = await pg.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    // unlock via form
    await pg.fill('input[name=Email]', 'test@example.com'); await pg.selectOption('#at-role', 'Agency');
    await pg.click('input[type=submit]'); await pg.waitForTimeout(400);
    const unlocked = await pg.evaluate(() => document.documentElement.classList.contains('afro-unlocked'));
    await pg.evaluate(() => document.getElementById('nov-4').scrollIntoView()); await pg.waitForTimeout(300);
    await pg.screenshot({ path: `${dir}/${name}-unlocked.png` });
    await pg.click('.at-f[data-f=party]'); await pg.waitForTimeout(200);
    const vis = await pg.evaluate(() => [...document.querySelectorAll('.at-ev')].filter(e => e.style.display !== 'none').length);
    // reload: persistence
    await pg.reload(); await pg.waitForTimeout(800);
    const persisted = await pg.evaluate(() => document.documentElement.classList.contains('afro-unlocked'));
    console.log(name, { overflowX: ow, unlocked, partyVisible: vis, persisted, errs });
  }
  await b.close();
})();
