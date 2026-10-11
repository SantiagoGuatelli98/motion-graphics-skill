// Shared harness for the reels: one paused GSAP timeline, window.seek(seconds), ?render, ?guides.
// Each reel calls Reel.start({ duration, build(T, h) }) and only describes its own scenes.
// Markup (logo, end card) lives in each HTML file; this script only animates it.
(() => {
  const W = 1080, H = 1920;
  const qs = new URLSearchParams(location.search);
  const RENDER = qs.has('render');
  if (qs.has('guides')) document.body.classList.add('guides');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const counters = [];

  function helpers(T) {
    const h = {
      $, $$,
      linesIn: (sel, at, o = {}) => T.fromTo(sel, { yPercent: 120 }, { yPercent: 0, duration: o.d ?? 0.8, stagger: o.s ?? 0.1, ease: 'power4.out' }, at),
      linesOut: (sel, at) => T.to(sel, { yPercent: -120, duration: 0.4, stagger: 0.04, ease: 'power3.in' }, at),
      up: (sel, at, o = {}) => T.fromTo(sel, { autoAlpha: 0, y: o.y ?? 44 }, { autoAlpha: 1, y: 0, duration: o.d ?? 0.6, stagger: o.s ?? 0.09, ease: 'power3.out' }, at),
      out: (sel, at, o = {}) => T.to(sel, { autoAlpha: 0, y: o.y ?? -36, duration: o.d ?? 0.34, stagger: o.s ?? 0.03, ease: 'power2.in' }, at),
      pop: (sel, at, o = {}) => T.fromTo(sel, { autoAlpha: 0, scale: o.from ?? 0.6 }, { autoAlpha: 1, scale: 1, duration: o.d ?? 0.5, stagger: o.s ?? 0.1, ease: `back.out(${o.back ?? 1.9})` }, at),
      strike: (sel, at, o = {}) => T.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: o.d ?? 0.36, stagger: o.s ?? 0.16, ease: 'power3.inOut' }, at),
      show: (id, at) => T.set(id, { autoAlpha: 1 }, at),
      hide: (id, at) => T.set(id, { autoAlpha: 0 }, at),
      // Scene transitions
      circleIn(id, at, o = {}) {
        T.set(id, { autoAlpha: 1 }, at);
        T.fromTo(id, { clipPath: `circle(0% at ${o.x ?? 50}% ${o.y ?? 50}%)` }, { clipPath: `circle(130% at ${o.x ?? 50}% ${o.y ?? 50}%)`, duration: o.d ?? 0.8, ease: 'power3.inOut' }, at);
      },
      wipeIn(id, at, from = 'bottom', d = 0.65) {
        const start = { bottom: 'inset(100% 0% 0% 0%)', top: 'inset(0% 0% 100% 0%)', right: 'inset(0% 0% 0% 100%)', left: 'inset(0% 100% 0% 0%)' }[from];
        T.set(id, { autoAlpha: 1 }, at);
        T.fromTo(id, { clipPath: start }, { clipPath: 'inset(0% 0% 0% 0%)', duration: d, ease: 'power4.inOut' }, at);
      },
      logo(root, at) {
        T.fromTo(`${root} .lo-c`, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.7, ease: 'power2.inOut' }, at);
        T.fromTo(`${root} .lo-t`, { autoAlpha: 0, scale: 0, transformOrigin: '50% 0%' }, { autoAlpha: 1, scale: 1, duration: 0.22 }, at + 0.54);
        T.fromTo(`${root} .lo-s`, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.4, ease: 'power2.out' }, at + 0.64);
        T.fromTo(`${root} .lo-w`, { autoAlpha: 0, x: -22 }, { autoAlpha: 1, x: 0, duration: 0.55, stagger: 0.1 }, at + 0.4);
      },
      // Closing card: revealed through an expanding "O", then holds for the read
      endCard(at) {
        h.circleIn('#end', at - 0.35);
        h.logo('#end', at + 0.05);
        h.linesIn('#end h2 .ln > span', at + 0.4, { s: 0.12 });
        h.up('#end .eyebrow', at + 0.85, { y: 20, d: 0.45 });
        T.fromTo('#end .btn', { autoAlpha: 0, y: 40, scale: 0.86 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.65, ease: 'back.out(1.8)' }, at + 1.05);
        T.fromTo('#end .btn svg', { x: 0 }, { x: 12, duration: 0.5, yoyo: true, repeat: 3, ease: 'sine.inOut' }, at + 1.7);
        h.up('#end .url', at + 1.3, { y: 16, d: 0.45 });
      },
      // Counter that survives seeking in any order
      counter(el, from, to, at, d, fmt = v => String(Math.round(v)), ease = 'power2.inOut') {
        const o = { v: from };
        T.to(o, { v: to, duration: d, ease }, at);
        counters.push(() => { el.textContent = fmt(o.v); });
      },
    };
    return h;
  }

  function fit() {
    const stage = $('#stage');
    const s = RENDER ? 1 : Math.min(innerWidth / W, innerHeight / H);
    stage.style.transform = `scale(${s})`;
    stage.style.left = RENDER ? '0' : (innerWidth - W * s) / 2 + 'px';
    stage.style.top = RENDER ? '0' : (innerHeight - H * s) / 2 + 'px';
  }

  window.Reel = {
    start({ duration, build }) {
      const guides = document.createElement('div');
      guides.id = 'guides';
      $('#stage').appendChild(guides);
      const images = $$('img').map(i => i.decode ? i.decode().catch(() => {}) : Promise.resolve());
      Promise.all([document.fonts.load('600 40px "Space Grotesk"'), document.fonts.load('400 20px "Geist"'), document.fonts.load('500 20px "JetBrains Mono"'), ...images])
        .then(() => document.fonts.ready).then(() => {
          fit(); addEventListener('resize', fit);
          const T = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
          gsap.set('.scene', { autoAlpha: 0 });
          gsap.set($$('.scene')[0], { autoAlpha: 1 });
          $$('.blob').forEach((b, i) => T.fromTo(b, { x: 0, y: 0 }, { x: (i % 2 ? -1 : 1) * 60, y: (i % 3 ? 1 : -1) * 50, duration, ease: 'none' }, 0));
          build(T, helpers(T));
          T.set({}, {}, duration);
          window.seek = t => { T.time(Math.max(0, Math.min(duration, t)), false); counters.forEach(f => f()); };
          window.seek(0);
          window.ready = true;
          if (!RENDER) {
            const t0 = performance.now();
            const tick = now => { window.seek(((now - t0) / 1000) % duration); requestAnimationFrame(tick); };
            requestAnimationFrame(tick);
          }
        });
    },
  };
})();
