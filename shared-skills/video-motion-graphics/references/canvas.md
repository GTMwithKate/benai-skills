# The design canvas (last step)

Every run ends on a Claude Design canvas: one Main artboard with the final video and the timing list, then one artboard per motion clip with the clip playing, its in and out points, the line it covers and its treatment. The user reviews and comments there. The motion clip source stays local; the canvas shows the renders.

Tested 2026-09-28: `<video>` from an uploaded MP4 plays on a canvas artboard.

## Build it
1. Create the canvas once per video: Artifact `publish` with the Design type `type_url` (get it from Artifact `quickstart`, intent `design`), `title` = the video's name, `auto_open: "after_first_write"`. Keep the returned `url` in the project `plan.md`. Never create a second canvas for the same video.
2. `python3 $SKILL/scripts/make_canvas.py prep motion/plan.json <final video> canvas` (over a video: `out/final.mp4`; standalone: `motion/out/<name>.mp4`)
   It makes review MP4s under 14 MB each in `canvas/assets/`. A final video too big for one upload is replaced by one segment around each clip, so the canvas shows every changed spot.
3. Upload every file it lists in ONE call: Artifact `publish`, `url` = the canvas, `asset: true`, `file_paths` = the listed paths (25 at most per call).
4. Write `canvas/assets/urls.json`: `{"<file name>": "<the /_blob/... url from the upload result>"}` for every file.
5. `python3 $SKILL/scripts/make_canvas.py build motion/plan.json canvas "<canvas title>"`
6. Publish in ONE call: `url` = the canvas, `root` = the `canvas` folder (absolute), `file_path` = `<root>/project/canvas.json`, `files` = `{"project/Main.dc.html": "project/Main.dc.html", "project/clip-NN.dc.html": "project/clip-NN.dc.html", ...}`.
7. Give the user the link. Do not open, screenshot or re-read the canvas unless the user asks.

## Revise from comments
1. Read the canvas comments with the ArtifactComments tool. Each comment on a clip artboard is a change request for that clip.
2. Change that scene or clip in `motion/films/`, check stills, re-render it (`references/motion-clips.md` or `references/standalone.md`), and re-composite or re-render the film.
3. Re-run `prep`, upload only the changed files, update their entries in `urls.json`, re-run `build`.
4. Publish only the changed artboards (plus `project/canvas.json` only if clips were added or removed). Read each changed artboard from the canvas first: the user may have edited its text there, and their edits win.

## Rules
- No motion clip HTML on the canvas. The canvas only runs its own artboard format, so clips appear as videos.
- The board text (titles, lines, timings) is live text. The user can retype it on the canvas.
- The canvas is private. Say so, and that sharing is done from its Share menu.
