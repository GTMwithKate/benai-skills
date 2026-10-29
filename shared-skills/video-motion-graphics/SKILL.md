---
name: video-motion-graphics
description: "Makes any kind of motion graphic in code, with no image or video model: explainer animations, logo animations, product demos, short-form reels, intros, chapter cards, and motion over an existing video (full-frame cutaways, transparent overlay panels, replacing a CTA or a screen share). For existing videos it can also edit (cuts, teasers, social clips), transcribe locally with whisper.cpp and burn in word-level captions. Every job ends on a Claude Design canvas: the whole film plus each scene or clip on its own artboard. Use it whenever the user says 'motion graphic', 'animate', 'explainer video', 'animated explainer', 'logo animation', 'product demo video', 'kinetic type', 'add motion graphics', 'add B-roll', 'add overlays', 'add captions', 'edit this video', 'make a clip from this video', or gives an .mp4/.mov and wants any mix of editing, captions, overlays and motion. By Ben AI."
---

# Video Motion Graphics

Makes motion graphics in code: HTML scenes drawn from time alone, rendered frame by frame with Chrome and ffmpeg. It works in two modes. Pick one in intake.

- **Standalone.** The motion graphic is the video: an explainer, a logo animation, a product demo, a reel, an intro. Follow `references/standalone.md`.
- **Over a video.** A talking-head or screen recording gets up to four stages, in this order: edit, transcribe, motion, captions.

Both modes follow `references/motion-principles.md` and use the engine in `engine/` (`references/motion-engine-api.md`). Both end on a design canvas.

`$SKILL` is this skill's folder. Work in one project folder. The motion files live in `motion/`: `engine/`, `brand.css`, `films/`, `out/`, `work/`. Inside a design project folder (a `CLAUDE.md`, `design-system/` and use-case subfolders), work in `work/<use-case>/<date>-<job>/`, never inside a use-case folder, and move a final into `<use-case>/examples/` only after the user says yes.

## Standalone mode

```
Task Progress:
- [ ] 1. Set up: bash $SKILL/scripts/setup-motion.sh ./motion
- [ ] 2. Brief and brand (references/standalone.md, references/brand.md)
- [ ] 3. Script and storyboard: stop for approval
- [ ] 4. Build each scene from templates/film.html
- [ ] 5. Check stills
- [ ] 6. Render the film and each scene
- [ ] 7. Design canvas: the film plus one artboard per scene
```

## Over-a-video mode

File chain: `public/source.mp4` -> `public/edited.mp4` -> `out/with-motion.mp4` -> `out/final.mp4`. Word times: `public/source.captions.json` -> `public/edited.captions.json` -> `work/edited-words.txt`.

```
Task Progress:
- [ ] 1. Set up (first run only)
- [ ] 2. Intake
- [ ] 3. Prep and transcribe the source
- [ ] 4. Plan every stage in one table, get approval
- [ ] 5. Edit stage -> public/edited.mp4
- [ ] 6. Move word times onto the edited timeline
- [ ] 7. Motion stage -> out/with-motion.mp4
- [ ] 8. Captions stage -> out/final.mp4
- [ ] 9. QA, preview, final render on approval
- [ ] 10. Put the final video and every motion clip on a design canvas
```

### 1. Set up
Only the parts the chosen stages need. Read `references/setup.md`.

### 2. Intake
One round of questions, skip what the user already said. Collect the brand kit once. Read `references/intake.md` and `references/brand.md`.

### 3. Prep and transcribe the source
Transcode to H.264 with faststart as `public/source.mp4`. Run ffprobe. Transcribe: `npx ts-node scripts/transcribe.ts source.mp4` (file name only, it reads from `public/`). Make readable word times for planning:
`mkdir -p work && python3 $SKILL/scripts/captions_to_words.py public/source.captions.json > work/source-words.txt`
Read `references/video-analysis.md` and `references/transcription.md`.

### 4. Plan
Write one plan that covers every chosen stage: the cuts, each motion clip with its treatment, the caption style. Offer 2 or 3 options where the user must choose. Wait for approval. Read `references/plan.md`.

### 5. Edit stage
- No cuts: `cp public/source.mp4 public/edited.mp4 && cp public/source.captions.json public/edited.captions.json`, then go to step 6.
- Cuts: build the hard-cut composition from the approved cut table. Save the same clip values to `work/cuts.json` (`{"fps": 30, "clips": [{startMs, endMs, audioBufferMs}]}`). Show the cut in Remotion Studio and get a yes, because every later stage builds on it. Then render it: `npx remotion render <Composition> public/edited.mp4`.
Read `references/edit-rules.md`. Social clip or full edit: also `references/stitching.md`. Teaser or trailer: `references/teasers.md`. Crossfade mode: `references/transitions.md`. Chapter cards and bumpers: `references/title-cards.md`.

### 6. Move word times onto the edited timeline
With cuts: `python3 $SKILL/scripts/remap_captions.py public/source.captions.json work/cuts.json > public/edited.captions.json`. Do not transcribe the edited video again: it picks up words from the audio buffers.
Then: `python3 $SKILL/scripts/captions_to_words.py public/edited.captions.json > work/edited-words.txt`

### 7. Motion stage
Skip if no motion: `mkdir -p out && cp public/edited.mp4 out/with-motion.mp4`. Otherwise inspect, build clips timed from `work/edited-words.txt`, check stills, render, and composite onto `public/edited.mp4`. Read `references/motion-clips.md`.

### 8. Captions stage
Skip if no captions: `cp out/with-motion.mp4 out/final.mp4`. Otherwise `cp out/with-motion.mp4 public/with-motion.mp4` (Remotion only reads from `public/`) and build the captions composition over it with `public/edited.captions.json`. To hide captions during full-frame cutaways, read the `kind: full` windows from `motion/plan.json`. Read `references/captions.md`.

### 9. QA, preview, render
Run QA before the user sees anything. Preview, then render `out/final.mp4` only on approval. Read `references/qa-testing.md` and `references/deliver.md`.

### 10. Design canvas
Publish the final video on a Main artboard and each motion clip on its own artboard, then take revisions from the canvas comments. Read `references/canvas.md`.

## Human checkpoints
- The brand kit, first run only.
- The storyboard (standalone) or the plan (over a video). No code before approval.
- The cut, in Studio, before `edited.mp4` is rendered.
- The preview. Never render the final without an explicit yes.
- Comments on the canvas. Each one is a change request for that artboard.
- At each choice, show 2 or 3 options by default and wait for a pick.

## Self-improvement
This skill is never finished. Improve it as you use it.
- When the user corrects a step, update the reference file that step reads (or this SKILL.md) so the correction sticks. Rules about how motion should look or move go in `references/motion-principles.md`.
- When the user says an output was good, save its film page and plan to `references/examples/<date>-<name>/`.
- When you add something, cut what no longer changes behaviour.

## Routing
| Step | Reference |
|------|-----------|
| Motion rules (always) | `references/motion-principles.md` |
| Engine and render commands | `references/motion-engine-api.md`, `templates/film.html` |
| Standalone films | `references/standalone.md`, `references/examples/` |
| Setup | `references/setup.md`, `references/remotion-setup.md` |
| Intake and brand | `references/intake.md`, `references/brand.md` |
| Prep | `references/video-analysis.md`, `references/transcription.md` |
| Plan | `references/plan.md`, `references/intelligent-editing.md` |
| Edit | `references/edit-rules.md`, `references/stitching.md`, `references/teasers.md`, `references/transitions.md`, `references/title-cards.md` |
| Motion over a video | `references/motion-clips.md` |
| Captions | `references/captions.md`, `references/remotion-tips.md` |
| Deliver | `references/qa-testing.md`, `references/deliver.md` |
| Canvas | `references/canvas.md` |
| FFmpeg errors | `references/ffmpeg-basics.md` |
| Stuck on Remotion code | `references/reference-implementation.md` |
| Thumbnails or stills | `references/graphics-generation.md` |
