const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const http = require('http');
(async () => {
  const dir = path.resolve(process.argv[2]); const n = +process.argv[3] || 1; const out = process.argv[4];
  const srv = http.createServer((q, r) => { const f = path.join(dir, q.url.split('?')[0]); 
    r.setHeader('Content-Type', f.endsWith('.js') ? 'text/javascript' : 'text/html'); fs.createReadStream(f).on('error',()=>{r.statusCode=404;r.end()}).pipe(r); }).listen(8765);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const p = await b.newPage(); p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('err:', e.message));
  await p.goto('http://127.0.0.1:8765/crown.html'); await p.waitForFunction('window.ready === true', null, { timeout: 20000 });
  fs.mkdirSync(out, { recursive: true });
  for (let i = 0; i < n; i++) {
    const a = -i / n * Math.PI * 2 / 5;   // 72-degree period (5-fold symmetry); negative: front moves left
    const d = await p.evaluate(a => window.renderFrame(a), a);
    fs.writeFileSync(path.join(out, `f${String(i).padStart(2, '0')}.png`), Buffer.from(d.split(',')[1], 'base64'));
  }
  await b.close(); srv.close();
})();
