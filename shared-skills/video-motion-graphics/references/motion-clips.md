# Motion over a video (step 7, overlay mode)

Build, check and render the approved motion clips, then lay them over the edited video. Each clip is a small film (`templates/film.html`) timed to the spoken words. Read `references/motion-principles.md` and `references/motion-engine-api.md` before the first clip.

## 1. Inspect
```bash
python3 $SKILL/scripts/inspect_video.py public/edited.mp4 motion/work
```
Look at `motion/work/contact.png` yourself. `video.json` gives the size, the fps and stretches: `full` (the speaker fills the frame) or `boxed` (empty dark space on one side, good for a panel). Clips must match the video's size and fps.

## 2. Build
One film per clip in `motion/films/NN-name.html`. Clip time = word time from `work/edited-words.txt` minus the clip's in-point. Whisper runs 200 to 700 ms ahead of the audio, so land a change on the word's start, not after it.
- **Full-frame cutaway:** a normal background. It covers the speaker.
- **Panel:** `background: null`. It lays over the video with alpha. Keep it inside the empty space, clear of the speaker at every moment.

## 3. Check stills
```bash
node motion/engine/render.mjs stills motion/films/NN-name.html motion/work/NN.png 0.4 1.2 2.1
```
Pick each settled state plus a mid-move moment. Fix anything cramped, clipped, unreadable, off-word, or a cursor leaving the frame. Check again. Panels show on white in the sheet.

## 4. Render
```bash
node motion/engine/render.mjs video motion/films/NN-name.html motion/out/NN-name_0m32s40.mp4 --fps 30
```
- Use the video's fps (for 29.97 pass `--fps 29.97`).
- Panels render to `.mov` (ProRes 4444 with alpha): give the output a `.mov` name.
- Name each file by its timeline in-point (`0m32s40` = 0:32.40).
- Rendering is slower than real time. Run two clips in parallel.

## 5. Composite
Write `motion/plan.json` (schema in `references/motion-engine-api.md`) with `video` set to `../public/edited.mp4`, then:
```bash
mkdir -p out && python3 $SKILL/scripts/composite.py motion/plan.json out/with-motion.mp4
```

## Screen recordings with a face bubble
"Replace the on-screen view" on a screen share with the speaker in a corner bubble means: full-frame clips for the whole window, back to back, cut on sentence breaks, with the speaker's bubble put back on top.
- Find the exact first and last frame of the screen share (a frame-by-frame difference), not the user's rounded times. Measure the bubble box in pixels.
- Keep every clip's content clear of the bubble box at every moment, cursor included.
- Composite with `scripts/composite_bubble.py` instead of `composite.py`: it cuts the bubble out of the source frame by frame (so a zoom at the cut carries over), adds a 2 px ink ring and a soft shadow, and takes the audio from the source. Edit its `FIXED`, `RIGHT`, `BOTTOM` box values and the frame range for each video. Needs `motion/clips.json` with `frame_in` and `frames` per clip.
- Snap each clip's in-point to a whole source frame.

## Gotchas
- Never put `will-change` on something that scales. Text renders blurry.
- Text that swaps inside a moving container needs its own exit before the new text enters, or they overlap.
- A clip ends by holding its last state. The composite holds the last frame if its window is longer.
- Brand fonts: put the files in `motion/fonts/` and load them in `motion/brand.css` with `url('fonts/<file>')`.
