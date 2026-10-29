/* Ben AI motion engine.
   A film is a list of scenes. Every scene draws itself from time alone: draw(t) sets every
   style from t, with no CSS transitions, timers or random numbers. So any frame can be
   rendered on its own, and the preview and the render always match. */
(function () {
  const B = (window.BAI = {});

  // ---- numbers -------------------------------------------------------------------------
  const clamp = (B.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)));
  B.lerp = (a, b, u) => a + (b - a) * u;

  // Eases. `out` is the default: fast start, long soft landing. No bounce or elastic.
  B.ease = {
    linear: (x) => x,
    out: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)), // exponential ease-out
    in: (x) => (x <= 0 ? 0 : Math.pow(2, 10 * x - 10)), // for exits that leave mid-motion
    inOut: (x) => (x < 0.5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2),
    soft: (x) => 1 - Math.pow(1 - x, 3), // cubic out, for small moves
  };

  // Progress 0..1 of a move that starts at t0 and lasts dur.
  B.p = (t, t0, dur, ease = B.ease.out) => ease(clamp((t - t0) / dur));

  // Keyframes: [[time, value, ease?], ...]. Holds the first value before, the last after.
  B.keys = (t, ks) => {
    if (t <= ks[0][0]) return ks[0][1];
    for (let i = 0; i < ks.length - 1; i++) {
      const [t0, v0] = ks[i], [t1, v1, e] = ks[i + 1];
      if (t < t1) return B.lerp(v0, v1, (e || B.ease.inOut)((t - t0) / (t1 - t0)));
    }
    return ks[ks.length - 1][1];
  };

  // Colour blend between two hex colours.
  const rgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  B.mix = (a, b, u) => {
    const x = rgb(a), y = rgb(b);
    return `rgb(${x.map((v, i) => Math.round(B.lerp(v, y[i], clamp(u)))).join(',')})`;
  };

  // ---- elements --------------------------------------------------------------------------
  B.$ = (sel, root = document) => root.querySelector(sel);
  B.$$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  // Set position, scale, rotation, opacity and blur in one call.
  B.set = (el, s) => {
    if (!el) return;
    const o = s.o ?? 1;
    el.style.opacity = o.toFixed(4);
    el.style.visibility = o < 0.002 ? 'hidden' : 'visible';
    el.style.transform = `translate(${(s.x || 0).toFixed(2)}px,${(s.y || 0).toFixed(2)}px) scale(${(s.s ?? 1).toFixed(4)}) rotate(${(s.r || 0).toFixed(2)}deg)`;
    el.style.filter = s.blur > 0.05 ? `blur(${s.blur.toFixed(2)}px)` : 'none';
  };

  // In and out in one call. `from` is where it enters from, `to` where it leaves to.
  // Enter: rises into place from `from` with a short blur. Exit: keeps moving as it fades,
  // so a cut can land mid-motion.
  B.show = (el, t, tin, tout = Infinity, o = {}) => {
    const din = o.din ?? 0.5, dout = o.dout ?? 0.35;
    const from = { y: 24, s: 1, blur: 6, ...(o.from || {}) };
    const to = { y: -16, s: 1, blur: 4, ...(o.to || {}) };
    const a = B.p(t, tin, din), b = B.p(t, tout, dout, B.ease.in);
    B.set(el, {
      o: a * (1 - b),
      x: (from.x || 0) * (1 - a) + (to.x || 0) * b,
      y: from.y * (1 - a) + to.y * b,
      s: B.lerp(from.s, 1, a) * B.lerp(1, to.s, b),
      blur: from.blur * (1 - a) + to.blur * b,
    });
    return a * (1 - b);
  };

  // A group that enters one after another, `gap` seconds apart.
  B.stagger = (els, t, tin, gap = 0.08, tout = Infinity, o = {}) =>
    els.forEach((el, i) => B.show(el, t, tin + i * gap, tout, o));

  // Split an element's text into word spans once, for word-by-word reveals. Child elements
  // (a highlight span, a bold word) are kept: their words are split inside them.
  B.words = (el) => {
    if (!el._words) {
      const split = (node) => {
        for (const child of [...node.childNodes]) {
          if (child.nodeType === 3) {
            const frag = document.createDocumentFragment();
            child.textContent.split(/(\s+)/).forEach((part) => {
              if (!part) return;
              if (/^\s+$/.test(part)) frag.appendChild(document.createTextNode(part));
              else { const w = document.createElement('span'); w.className = 'bai-w'; w.style.display = 'inline-block'; w.textContent = part; frag.appendChild(w); }
            });
            child.replaceWith(frag);
          } else if (child.nodeType === 1) split(child);
        }
      };
      split(el);
      el._words = B.$$('.bai-w', el);
    }
    return el._words;
  };

  // Highlight a phrase like a marker, left to right. The element needs a background colour
  // set in CSS (background-color); this sweeps it in with background-size.
  B.highlight = (el, t, t0, dur = 0.45) => {
    const u = B.p(t, t0, dur, B.ease.inOut);
    el.style.backgroundImage = `linear-gradient(${getComputedStyle(el).getPropertyValue('--hl') || 'var(--accent)'}, ${getComputedStyle(el).getPropertyValue('--hl') || 'var(--accent)'})`;
    el.style.backgroundRepeat = 'no-repeat';
    el.style.backgroundSize = `${(u * 100).toFixed(2)}% 100%`;
    return u;
  };

  // A camera over one big world. keys = [[t, x, y, scale?, ease?], ...] in world pixels:
  // the point (x, y) is put at the centre of the frame. Use it on one #world element.
  B.camera = (world, t, keys, width, height) => {
    const pick = (i, d) => keys.map((k) => [k[0], k[i] ?? d, k[4]]);
    const x = B.keys(t, pick(1, 0)), y = B.keys(t, pick(2, 0)), s = B.keys(t, pick(3, 1));
    world.style.transformOrigin = '0 0';
    world.style.transform = `translate(${(width / 2 - x * s).toFixed(2)}px,${(height / 2 - y * s).toFixed(2)}px) scale(${s.toFixed(4)})`;
    return { x, y, s };
  };

  // A state that switches at a moment (an icon swap, a tick) must switch on a frame boundary,
  // or motion blur shows both states at once. BAI.after(t, t0) is true from the frame of t0 on.
  B.after = (t, t0, fps = 30) => Math.floor(t * fps + 1e-6) >= Math.round(t0 * fps);

  // Draw an SVG path or line on, like a pen. Call once per frame.
  B.draw = (path, t, t0, dur, ease = B.ease.inOut) => {
    if (!path._len) path._len = path.getTotalLength();
    const u = B.p(t, t0, dur, ease);
    path.style.strokeDasharray = path._len;
    path.style.strokeDashoffset = (path._len * (1 - u)).toFixed(2);
    return u;
  };

  // Count a number up. fmt turns the value into text.
  B.count = (el, t, t0, dur, from, to, fmt = (v) => Math.round(v).toLocaleString('en-US')) => {
    const s = fmt(B.lerp(from, to, B.p(t, t0, dur)));
    if (el._s !== s) { el.textContent = s; el._s = s; }
  };

  // Type text on at `cps` characters a second, with a caret while typing.
  B.type = (el, t, t0, text, cps = 28) => {
    const n = Math.max(0, Math.min(text.length, Math.floor((t - t0) * cps)));
    const typing = t >= t0 && n < text.length;
    const s = text.slice(0, n) + (typing ? '|' : '');
    if (el._s !== s) { el.textContent = s; el._s = s; }
    return n / text.length;
  };

  // Cursor that travels between points [[t, x, y], ...] with an eased path, plus clicks.
  B.cursor = (el, t, pts, clicks = []) => {
    const x = B.keys(t, pts.map((p) => [p[0], p[1]]));
    const y = B.keys(t, pts.map((p) => [p[0], p[2]]));
    let s = 1;
    for (const c of clicks) if (t > c - 0.08 && t < c + 0.16) s = Math.min(s, 1 - 0.14 * Math.sin(Math.PI * clamp((t - c + 0.08) / 0.24)));
    el.style.transform = `translate(${x.toFixed(2)}px,${y.toFixed(2)}px) scale(${s.toFixed(3)})`;
  };

  // ---- the film --------------------------------------------------------------------------
  // cfg = { width, height, fps, background: '#hex' | null (transparent),
  //         scenes: [{ id, start, end, draw(lt, el, t) }] }
  // Each scene's element is #<id>. Only the scene whose window holds t is visible (hard cut).
  // draw gets scene-local time lt, the scene element and film time t.
  B.film = (cfg) => {
    const stage = B.$('#stage');
    stage.style.width = cfg.width + 'px';
    stage.style.height = cfg.height + 'px';
    stage.style.background = cfg.background || 'transparent';
    const duration = cfg.duration ?? Math.max(...cfg.scenes.map((s) => s.end));
    const scenes = cfg.scenes.map((s) => ({ ...s, el: B.$('#' + s.id) }));
    const seek = (t) => {
      for (const s of scenes) {
        const on = t >= s.start && (t < s.end || (s.end === duration && t <= duration));
        s.el.style.display = on ? '' : 'none';
        if (on) s.draw(t - s.start, s.el, t);
      }
      if (cfg.always) cfg.always(t);
    };
    const fps = cfg.fps || 30;
    window.__motion = { duration, width: cfg.width, height: cfg.height, fps: cfg.fps || 30, alpha: !cfg.background,
      scenes: cfg.scenes.map(({ id, start, end, title }) => ({ id, start, end, title: title || id })) };
    window.__seek = seek;

    // Preview in a normal browser: fit to the window, loop, space pauses, arrows step.
    if (!location.search.includes('render')) {
      document.body.classList.add('preview');
      const fit = () => { const k = Math.min(innerWidth / cfg.width, innerHeight / cfg.height); stage.style.transform = `scale(${k})`; };
      fit(); addEventListener('resize', fit);
      let t = 0, playing = true, last = performance.now();
      addEventListener('keydown', (e) => {
        if (e.code === 'Space') playing = !playing;
        if (e.code === 'ArrowRight') t = Math.min(duration, t + 1 / 30);
        if (e.code === 'ArrowLeft') t = Math.max(0, t - 1 / 30);
      });
      const loop = (now) => { if (playing) t = (t + (now - last) / 1000) % (duration + 0.6); last = now; seek(Math.min(t, duration)); requestAnimationFrame(loop); };
      requestAnimationFrame(loop);
    } else seek(0);
    return seek;
  };
})();
