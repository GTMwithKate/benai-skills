// Ben AI motion renderer. Renders a film page frame by frame with Chrome and ffmpeg.
//
//   node render.mjs video  <film.html> <out.mp4|out.mov> [--fps 30] [--blur 3] [--from s] [--to s]
//   node render.mjs stills <film.html> <sheet.png> <t1> <t2> ...      (a contact sheet, each tile labelled with its time)
//   node render.mjs frame  <film.html> <out.png> <t>                   (one full-size frame)
//   node render.mjs scenes <film.html> <out-dir>  [--fps 30] [--blur 3] (one MP4 per scene)
//
// --blur N averages N sub-frames per frame for motion blur (1 = off). A film with
// background: null renders to .mov with alpha (ProRes 4444); others to H.264 .mp4.
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

function loadChromium() {
  const req = createRequire(import.meta.url);
  const tries = [process.env.NODE_PATH, path.resolve('motion/node_modules'), path.resolve('node_modules')].filter(Boolean);
  const npx = path.join(os.homedir(), '.npm/_npx');
  if (fs.existsSync(npx)) for (const d of fs.readdirSync(npx)) tries.push(path.join(npx, d, 'node_modules'));
  for (const base of tries) for (const name of ['playwright-core', 'playwright']) {
    try { return req(path.join(base, name)).chromium; } catch {}
  }
  throw new Error('playwright-core not found. Run scripts/setup-motion.sh first.');
}

async function openFilm(html) {
  const chromium = loadChromium();
  let browser;
  try { browser = await chromium.launch({ channel: 'chrome' }); }
  catch { browser = await chromium.launch(); }
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(pathToFileURL(path.resolve(html)).href + '?render');
  // Load every font face the page declares, not only the ones the first layout used.
  await page.evaluate(() => Promise.all([...document.fonts].map((f) => f.load().catch(() => null))));
  await page.evaluate(() => document.fonts.ready);
  const info = await page.evaluate(() => window.__motion);
  if (!info) throw new Error('No window.__motion: the page must call BAI.film(...)');
  await page.setViewportSize({ width: info.width, height: info.height });
  return { browser, page, info, errors };
}

const shot = (page, alpha) => page.screenshot({ type: 'png', omitBackground: alpha });

function ffmpeg(args) {
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', ...args]);
  ff.stderr.on('data', (d) => process.stderr.write(d));
  return ff;
}

async function video(html, out, o) {
  const { browser, page, info, errors } = await openFilm(html);
  const fps = +o.fps || info.fps, K = Math.max(1, +o.blur || 3);
  const t0 = +o.from || 0, t1 = o.to != null ? +o.to : info.duration;
  const n = Math.round((t1 - t0) * fps);
  const alpha = out.endsWith('.mov') && info.alpha;
  const enc = alpha
    ? ['-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le']
    : ['-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'];
  // Sub-frames arrive at fps*K; tmix averages K of them, then every Kth frame is kept.
  const vf = K > 1 ? `format=${alpha ? 'gbrap' : 'gbrp'},tmix=frames=${K},select='not(mod(n+1\\,${K}))',setpts=N/${fps}/TB` : `setpts=N/${fps}/TB`;
  const ff = ffmpeg(['-f', 'image2pipe', '-framerate', String(fps * K), '-c:v', 'png', '-i', '-', '-vf', vf, '-r', String(fps), ...enc, out]);
  const shutter = 0.5 / fps; // 180 degree shutter
  for (let f = 0; f < n; f++) {
    for (let k = 0; k < K; k++) {
      const t = Math.min(t1, Math.max(t0, t0 + f / fps + (K > 1 ? (k / (K - 1) - 0.5) * shutter : 0)));
      await page.evaluate((t) => window.__seek(t), t);
      const buf = await shot(page, alpha);
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    }
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  await browser.close();
  console.log(`rendered ${out}: ${n} frames at ${fps} fps${errors.length ? ' | PAGE ERROR: ' + errors[0] : ''}`);
}

async function stills(html, out, times) {
  const { browser, page, info, errors } = await openFilm(html);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'bai-stills-'));
  const files = [];
  for (const [i, t] of times.entries()) {
    await page.evaluate((t) => {
      window.__seek(t);
      let tag = document.getElementById('__bai_time');
      if (!tag) { tag = document.createElement('div'); tag.id = '__bai_time'; document.getElementById('stage').appendChild(tag);
        tag.style.cssText = 'position:absolute;left:24px;top:24px;z-index:99999;padding:8px 16px;border-radius:10px;background:#111;color:#fff;font:600 48px/1 system-ui,sans-serif'; }
      tag.textContent = t.toFixed(2) + 's';
    }, +t);
    const f = path.join(dir, `${String(i).padStart(3, '0')}.png`);
    fs.writeFileSync(f, await shot(page, false));
    files.push(f);
  }
  await browser.close();
  // Tile the stills 3 across, at a third of their size, and list the times.
  const cols = Math.min(3, files.length), rows = Math.ceil(files.length / cols);
  const w = Math.round(info.width / 3), h = Math.round(info.height / 3);
  const inputs = files.flatMap((f) => ['-i', f]);
  const scaled = files.map((_, i) => `[${i}:v]scale=${w}:${h}[s${i}]`).join(';');
  const layout = files.map((_, i) => `${(i % cols) * w}_${Math.floor(i / cols) * h}`).join('|');
  const graph = files.length > 1 ? `${scaled};${files.map((_, i) => `[s${i}]`).join('')}xstack=inputs=${files.length}:layout=${layout}:fill=gray` : `[0:v]scale=${w}:${h}`;
  await new Promise((r) => ffmpeg([...inputs, '-filter_complex', graph, '-frames:v', '1', out]).on('close', r));
  console.log(`stills ${out}: ${cols} across, times in order: ${times.join(', ')}${errors.length ? ' | PAGE ERROR: ' + errors[0] : ''}`);
  void rows;
}

async function frame(html, out, t) {
  const { browser, page, errors } = await openFilm(html);
  await page.evaluate((t) => window.__seek(t), +t);
  fs.writeFileSync(out, await shot(page, false));
  await browser.close();
  console.log(`frame ${out} at ${t}s${errors.length ? ' | PAGE ERROR: ' + errors[0] : ''}`);
}

async function scenes(html, dir, o) {
  const { browser, info } = await openFilm(html);
  await browser.close();
  fs.mkdirSync(dir, { recursive: true });
  for (const s of info.scenes) await video(html, path.join(dir, `${s.id}.mp4`), { ...o, from: s.start, to: s.end });
}

const [cmd, html, out, ...rest] = process.argv.slice(2);
const opts = {};
const pos = [];
for (let i = 0; i < rest.length; i++) rest[i].startsWith('--') ? (opts[rest[i].slice(2)] = rest[++i]) : pos.push(rest[i]);
if (cmd === 'video') await video(html, out, opts);
else if (cmd === 'stills') await stills(html, out, pos);
else if (cmd === 'scenes') await scenes(html, out, opts);
else if (cmd === 'frame') await frame(html, out, pos[0]);
else { console.log(fs.readFileSync(new URL(import.meta.url)).toString().split('\n').slice(0, 10).join('\n')); process.exit(1); }
