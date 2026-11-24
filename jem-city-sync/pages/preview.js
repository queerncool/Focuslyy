const { chromium } = require('playwright');
const fs = require('fs');
const [,, slug, patch, outPrefix] = process.argv;
const SP = require('path').join(__dirname, 'out') + '/';
const fd = JSON.parse(fs.readFileSync(SP + patch)).fieldData;
(async () => {
  const b = await chromium.launch();
  for (const w of [1280, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    await p.route(/cdn\.prod\.website-files\.com/, async route => {
      const u = route.request().url().replace(/^https:\/\/cdn\.prod\.website-files\.com\//, 'https://s3.amazonaws.com/webflow-prod-assets/');
      try { const r = await route.fetch({ url: u }); await route.fulfill({ response: r }); } catch (e) { await route.abort(); }
    });
    await p.goto('https://www.jem.social/find-influencers/' + slug, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {});
    const res = await p.evaluate((fd) => {
      const log = [];
      const set = (sel, html) => { const el = document.querySelector(sel); if (!el) { log.push('MISSING ' + sel); return; } el.innerHTML = html; };
      const tmp = document.createElement('div'); tmp.innerHTML = fd['hero-description'];
      const embed = tmp.querySelector('[data-rt-embed-type]');
      embed.querySelectorAll('link').forEach(l => document.head.appendChild(l.cloneNode(true)));
      document.head.appendChild(embed.querySelector('style').cloneNode(true));
      embed.remove();
      set('.hero-section-1 .rich-text-block-16', tmp.innerHTML);
      set('.hero-section-1 .heading-63', fd['hero-title']);
      set('.hero-section-1 .paragraph-39', fd['hero-lead']);
      set('.text-block-54', fd['hero-badge']);
      set('.hero-section-1 a.button._1 .text-block-92', fd['hero-button-1-text']);
      set('.section-47 .w-richtext', fd['editors-note-content']);
      set('.section-53 .heading-76', fd['guide-section-heading']);
      set('.section-53 .rich-text-block-14', fd['guide-section-content']);
      set('.section-54 .heading-74', fd['cta-section-heading']);
      set('.section-54 .rich-text-block-15', fd['cta-section-description']);
      const qs = [...document.querySelectorAll('.section-bg-color1 .text-size-medium.text-bold')];
      const as = [...document.querySelectorAll('.section-bg-color1 .text-block-98')];
      if (qs.length !== 7 || as.length !== 7) log.push('FAQ count ' + qs.length + '/' + as.length);
      const keys = [['faq-1-question-2','faq-1-answer-3'],['faq-2-question-2','faq-2-answer-3'],['faq-3-question-2','faq-3-answer-3'],['faq-4-question-2','faq-4-answer-3'],['faq-5-question','faq-5-answer-2'],['faq-6-question','faq-6-answer-2'],['faq-7-question','faq-7-answer-2']];
      keys.forEach(([q, a], i) => { if (qs[i]) qs[i].textContent = fd[q]; if (as[i]) as[i].textContent = fd[a]; });
      return log;
    }, fd);
    await p.waitForTimeout(1500);
    const info = await p.evaluate(() => ({ overflowX: document.documentElement.scrollWidth > window.innerWidth, h: document.documentElement.scrollHeight }));
    console.log(w, JSON.stringify(info), res.length ? res.join(' | ') : 'all selectors ok');
    await p.screenshot({ path: SP + `${outPrefix}_${w}.png`, fullPage: true });
    await p.close();
  }
  await b.close();
})();
