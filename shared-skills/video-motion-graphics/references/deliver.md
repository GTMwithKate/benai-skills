# Deliver (step 9)

## Order
1. Run `references/qa-testing.md` section 1, 2 and 4 on the Remotion project. Then check each stage file:
   - `public/edited.mp4`: every cut lands after the last word resolves, no black flash.
   - `public/edited.captions.json`: first and last words of each clip match the cut table.
   - `out/with-motion.mp4`: stills at each clip in-point, motion lands on its word.
   - `out/final.mp4`: no caption sits on top of a panel, and no motion clip covers the first second of the hook.
2. Preview. Captions: Remotion Studio (`npm run dev`). Motion: the design canvas (`references/canvas.md`), or open a film page in a browser.
3. Wait for an explicit yes. With captions, render the captions composition to `out/final.mp4` (command in `references/edit-rules.md`, section 6). Without captions, `out/final.mp4` is the copy made in step 8.

## What the user gets, all in `out/`
| File | What it is |
|---|---|
| `final.mp4` | edited video with motion clips and captions |
| `with-motion.mp4` | edited video with motion clips, no captions |
| `motion/out/*.mp4`, `*.mov` | each motion clip, named by timeline in-point, for their own editor |
| `TIMING.md` | every clip: in, out, the line, the treatment, what is illustrative |

Say plainly: the composite is for review. For full control, place the clips in their own editor.

Then put everything on the design canvas (`references/canvas.md`) and give the link.

Finish with a summary table: stages run, canvas link, video length, number of cuts, number of motion clips, caption style, total time.
