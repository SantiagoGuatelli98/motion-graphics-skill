// Frame-exact export of an HTML composition through window.seek(seconds).
// Run it from the project folder (it serves the current directory over localhost).
//
//   node <skill>/toolkit/render.mjs video  <page.html> --size 1080x1920 --duration 15 [--fps 30] [--audio a.wav] [--out out/x.mp4] [--query "format=v"]
//   node <skill>/toolkit/render.mjs stills <page.html> --size 1080x1920 --times 0.5,1.5,7,14 [--out out/stills] [--query "..."]
//
// The page must: set window.ready = true once fonts and images are loaded, expose
// window.seek(seconds), and stop its own clock when the URL contains ?render.
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { basename, dirname, extname, join, normalize, resolve } from 'node:path';
import { launch } from './cdp.mjs';

const [mode, page, ...rest] = process.argv.slice(2);
const opt = {};
for (let i = 0; i < rest.length; i += 2) opt[rest[i].replace(/^--/, '')] = rest[i + 1];
if (!['video', 'stills'].includes(mode) || !page || !opt.size) {
  console.error('Uso: render.mjs <video|stills> <page.html> --size WxH [--duration s] [--times a,b] [--fps 30] [--audio wav] [--out path] [--query q]');
  process.exit(1);
}
const [W, H] = opt.size.split('x').map(Number);
const FPS = Number(opt.fps ?? 30);
const name = basename(page, extname(page));

// file:// blocks web fonts in headless Chrome, so the project is served over localhost
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml' };
const root = resolve('.');
const server = createServer(async (req, res) => {
  try {
    const file = join(root, normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)));
    if (!file.startsWith(root)) throw new Error('outside root');
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': MIME[extname(file)] ?? 'application/octet-stream' });
    res.end(body);
  } catch { res.writeHead(404); res.end(); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const url = `http://127.0.0.1:${port}/${page.replace(/\\/g, '/')}?render${opt.query ? '&' + opt.query : ''}`;

const b = await launch({ width: W, height: H, scale: 1, port: 9300 + (port % 600) });
try {
  await b.goto(url, 800);
  for (let i = 0; i < 150 && !(await b.evaluate('window.ready === true')); i++) await b.sleep(100);
  if (!(await b.evaluate('window.ready === true'))) throw new Error('La página nunca puso window.ready = true. ' + b.logs.join(' | '));

  if (mode === 'stills') {
    const dir = opt.out ?? 'out/stills';
    mkdirSync(dir, { recursive: true });
    for (const t of (opt.times ?? '0').split(',').map(Number)) {
      await b.evaluate(`window.seek(${t})`);
      writeFileSync(join(dir, `${name}-${t.toFixed(2).padStart(5, '0')}.jpg`), await b.shot({ format: 'jpeg', quality: 88 }));
    }
    console.log('stills →', dir);
  } else {
    const duration = Number(opt.duration);
    if (!duration) throw new Error('--duration es obligatorio para video');
    const out = opt.out ?? `out/${name}.mp4`;
    mkdirSync(dirname(out), { recursive: true });
    const audio = opt.audio && existsSync(opt.audio) ? ['-i', opt.audio] : [];
    if (opt.audio && !audio.length) console.warn('No encontré el audio', opt.audio, '— exporto sin sonido');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', ...audio,
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', String(FPS),
      ...(audio.length ? ['-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest'] : []),
      '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg salió con código ' + c))));
    const total = Math.round(FPS * duration);
    for (let f = 0; f < total; f++) {
      await b.evaluate(`window.seek(${f / FPS})`);
      const png = await b.shot();
      if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await done;
    console.log('video →', out, `(${total} frames)`);
  }
  if (b.logs.length) console.log('LOGS DE LA PÁGINA:', b.logs.slice(0, 8));
} finally { await b.close(); server.close(); }
