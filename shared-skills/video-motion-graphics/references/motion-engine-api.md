# Motion engine API

The Ben AI motion engine is `engine/motion.js` (the `BAI` object) plus `engine/render.mjs` (Chrome plus ffmpeg). A film page is plain HTML: one `#stage`, one `<section class="scene">` per scene, and one `BAI.film(...)` call. Start from `templates/film.html`.

## The one rule

Every style is set from time inside `draw(t)`. No CSS transitions, no CSS animations, no timers, no `Math.random()`. That is what lets the renderer jump to any frame and get the same picture as the preview.

## The film

```js
BAI.film({
  width: 1920, height: 1080, fps: 30,
  background: '#FAF7F0',          // or null for a transparent overlay (renders to .mov with alpha)
  scenes: [
    { id: 's1', title: 'The problem', start: 0, end: 3.4, draw(t, el, filmTime) { /* ... */ } },
    { id: 's2', title: 'The fix',     start: 3.4, end: 7, draw(t) { /* ... */ } },
  ],
  always(t) { /* optional: things that live across scenes, like a persistent logo */ },
});
```

- `t` inside `draw` is scene time: 0 at the scene's start.
- Only the scene whose window holds the frame is shown. That is a hard cut, so make the exit and the entry match (`references/motion-principles.md`).
- A thing that must carry across a cut (a word, a card, a cursor) lives outside the scenes and is drawn in `always(t)`.

## Helpers

| Call | What it does |
|---|---|
| `BAI.p(t, t0, dur, ease?)` | Progress 0 to 1 of a move from `t0` lasting `dur`. Default ease is `BAI.ease.out` |
| `BAI.keys(t, [[t0, v0], [t1, v1, ease?], ...])` | A value through keyframes. Holds the ends |
| `BAI.lerp(a, b, u)`, `BAI.clamp(x, a, b)` | Plain maths |
| `BAI.mix('#hex', '#hex', u)` | Blend two colours |
| `BAI.set(el, {x, y, s, r, o, blur})` | Move, scale, rotate, fade and blur an element in one call |
| `BAI.show(el, t, tin, tout?, {din, dout, from, to})` | Enter at `tin` from `from` (default rises 24 px with a blur), leave at `tout` towards `to`. Returns visibility 0 to 1 |
| `BAI.stagger(els, t, tin, gap, tout?, opts)` | `show` for a group, `gap` seconds apart |
| `BAI.words(el)` | Splits an element's text into word spans (once), keeping child elements like a highlight span. Use with `stagger` for word-by-word type |
| `BAI.highlight(el, t, t0, dur?)` | Sweeps a marker highlight across a phrase, left to right. Set `--hl` (the colour) on the element in CSS |
| `BAI.camera(world, t, [[t, x, y, scale?, ease?], ...], width, height)` | A camera over one big `#world` element: puts world point (x, y) at the frame centre |
| `BAI.after(t, t0)` | True from the frame of `t0` on. Use it for any state that switches at a moment (an icon swap, a tick), so motion blur never shows both states |
| `BAI.draw(path, t, t0, dur)` | Draws an SVG path or line on like a pen |
| `BAI.count(el, t, t0, dur, from, to, fmt?)` | Counts a number up |
| `BAI.type(el, t, t0, text, cps?)` | Types text with a caret |
| `BAI.cursor(el, t, [[t, x, y], ...], [clickTimes])` | Moves a cursor along points, with a press at each click |
| `BAI.$(sel)`, `BAI.$$(sel)` | Query one or all |

Eases: `BAI.ease.out` (entrances), `BAI.ease.in` (exits that leave mid-motion), `BAI.ease.inOut` (moves from one place to another), `BAI.ease.soft` (small nudges), `BAI.ease.linear`.

## One owner per property

`BAI.set`, `show` and `stagger` write the whole `transform`, `opacity` and `filter` of an element every frame. Never centre or place an element with a CSS transform (for example `translateX(-50%)`): use `left`, `top` and `width`. Never call two helpers that both move the same element: wrap it in a parent and move the parent.

## Patterns

- **Word-by-word headline, leaving left:** `BAI.stagger(BAI.words(h), t, 0.1, 0.07, 2.6, { to: { x: -140, y: 0 } })`.
- **Card that slides into its slot:** `BAI.set(card, { x: BAI.lerp(400, 0, BAI.p(t, 0.5, 0.7)), o: BAI.p(t, 0.5, 0.3) })`.
- **A line that connects two boxes:** an SVG `<path>` from edge to edge, `BAI.draw(path, t, 1.0, 0.6)`. It must touch both boxes.
- **A number that lands:** hold 0.4 s, then `BAI.count(...)` over 0.8 s, then a small scale-up of 1.04 over 0.2 s.
- **Transparent overlay panel:** `background: null`, then render to `.mov`.

## Render commands

```bash
node motion/engine/render.mjs video  <film.html> <out.mp4|out.mov> [--fps 30] [--blur 3] [--from s] [--to s]
node motion/engine/render.mjs scenes <film.html> <out-dir> [--fps 30] [--blur 3]
node motion/engine/render.mjs stills <film.html> <sheet.png> <t1> <t2> ...   # tiles labelled with their time
node motion/engine/render.mjs frame  <film.html> <out.png> <t>                # one full-size frame, to check small text and logos
```

- `--blur` averages that many sub-frames per frame for motion blur. 3 is the default; 1 is off (fast drafts).
- Uses Google Chrome through playwright-core. If Chrome is missing, `setup-motion.sh` installs Playwright's Chromium.
- A 10-second 1080p film at `--blur 3` takes about 40 seconds. Render the scenes and the film in parallel.

## plan.json

Used by `scripts/composite.py` (overlays) and `scripts/make_canvas.py` (canvas).

```json
{ "video": "../public/edited.mp4",
  "clips": [ { "id": "01", "title": "The problem", "in": 0, "out": 3.4, "kind": "scene",
               "file": "out/scenes/s1.mp4", "line": "Designs drift" } ] }
```

`kind` is `scene` (a part of a standalone film), `full` (a full-frame cutaway over a video) or `panel` (a transparent overlay). `video` is only needed for overlays.
