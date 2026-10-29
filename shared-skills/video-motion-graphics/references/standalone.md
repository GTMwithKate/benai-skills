# Standalone motion graphics

For a motion graphic that is its own video: an explainer, a logo animation, a product demo, a short-form reel, a chapter card, an intro or outro. There is no source video to edit.

Project layout (from `scripts/setup-motion.sh`): `motion/engine/`, `motion/brand.css`, `motion/films/`, `motion/out/`, `motion/work/`.

Inside a design project folder (one with a `CLAUDE.md`, `design-system/` and use-case subfolders), the job folder is `work/<use-case>/<date>-<job>/` and `motion/` goes inside it. Never build inside the use-case folder itself. When the user approves the film, ask whether to save it as an example; if yes, move only the final MP4 into `<use-case>/examples/`.

## 1. Brief

Ask once, skip what the user already said:
- What it explains or shows, and who watches it.
- Format: 16:9 (1920 x 1080), 9:16 (1080 x 1920) or 1:1 (1080 x 1080).
- Length. Explainers usually 20 to 60 seconds.
- Voice-over or not. With a voice-over file, transcribe it (`scripts/transcribe.ts`) and time every beat to its words.
- Brand: the design system (see `references/brand.md`).

## 2. Script and storyboard (checkpoint)

Write the script and a storyboard table before any code:

| # | Scene | On screen (2 to 6 words) | What moves, and why | Start | End |

- One idea per scene. Scene changes follow the film's one direction (`references/motion-principles.md`).
- Name the carrier across each cut: what leaves one scene and lands in the next.
- Offer 2 or 3 directions when the idea allows more than one (for example: kinetic type only, icons and objects, a one-world camera pan). Keep each to a few lines.

Stop. Wait for the user to pick and approve. No code before the storyboard is approved.

## 3. Build

- Copy `templates/film.html` to `motion/films/<name>.html`. One `<section class="scene" id="...">` per storyboard row, and one entry in `scenes` with the same id, start and end.
- Put the brand colours and fonts in `motion/brand.css` as CSS variables (`--bg --ink --muted --accent --card --line --font`, plus any other tokens the design system has: body font, tints, a dark ground). Also write `brand.json` in the project root (`canvas`, `ink`, `surface`, `accent`, `heading_font`): the canvas step reads it.
- Type sizes for video come from `references/motion-principles.md`, not from the design system's page type scale.
- Real app logos: use the brand's own logo files, a logo kit the user has, or svgl.app. Icons: Lucide paths, inline so they take the text colour.
- Write each scene's `draw(t)` with the engine API (`references/motion-engine-api.md`).
- Preview in a browser: open the file, space pauses, arrow keys step a frame.

## 4. Check stills

```bash
node motion/engine/render.mjs stills motion/films/<name>.html motion/work/sheet.png 0.4 1.2 2.0 ...
```

Pick the settled moment of every scene plus a frame mid-move near each cut. Look at every tile. Fix, then check again. Apply the checks in `references/motion-principles.md`.

## 5. Render

```bash
node motion/engine/render.mjs video  motion/films/<name>.html motion/out/<name>.mp4 --fps 30 --blur 3
node motion/engine/render.mjs scenes motion/films/<name>.html motion/out/scenes --fps 30 --blur 3
```

The first makes the whole film, the second one MP4 per scene. `--blur 1` renders faster for drafts. With a voice-over, mux it on: `ffmpeg -i motion/out/<name>.mp4 -i vo.m4a -c:v copy -c:a aac -shortest motion/out/<name>-vo.mp4`.

## 6. Canvas

Write `motion/plan.json` with one clip per scene (`kind: "scene"`, `in` and `out` in film time, `file` = `out/scenes/<id>.mp4`, `title`, and `line` = the on-screen words). Then follow `references/canvas.md`: the whole film on the Main artboard, each scene on its own artboard. Each canvas comment is a change to that scene: edit its `draw`, re-render that scene and the film, and republish only what changed.
