# The plan (step 4)

One table per chosen stage, shown together. No code, no render, until the user approves. Log every change the user makes into `plan.md` in the project root.

## Choices first
Before the tables, show options and wait for a pick:
- **Opening hook** (edit stage): 5 to 10 candidate first sentences from the transcript, each with its timestamp. Every candidate must pass the opening rules in `references/edit-rules.md`.
- **Caption style** (captions stage): 5 options built from the two recipes in `references/captions.md` (frosted pill, bold pill), varied by words per page, position and highlight colour. "TikTok-style" means word highlighting in the frosted pill.

## Table 1: cuts (edit stage)
| # | Label | startMs | endMs | First and last spoken words | audioBufferMs | Why |

Timestamps come only from `work/source-words.txt` and `public/source.captions.json`. Detail per task type: `references/intelligent-editing.md`.

## Table 2: motion clips (motion stage)
Plan against the edited timeline. If the edit stage runs, plan from the cut list, then re-time every clip from `work/edited-words.txt` after step 6.

| # | In to Out | The line it covers | What the shape does, on which words | Treatment | Why |

Pick the treatment per clip and give the reason:
- **Full-frame cutaway.** The frame is all speaker and the line describes something to see: a product, a process, a comparison, a number, a chapter change. 3 to 10 seconds, then give the face back. Never in the first second of the hook, never on personal, emotional or opinion lines. At least 2 seconds of face between cutaways.
- On picture-in-picture sections, use panels. Cut away there only if the user asks.
- **Transparent panel (overlay).** The frame has empty space: a picture-in-picture box, a split, a plain area. Centre it in the empty area, clear of the speaker at every moment. It can run 15 seconds or more as one continuous morph.
- **Nothing.** The line is about the speaker, or it is too close to another clip.

Content rules:
- Show the real objects from the words: the folder, the terminal, the file, the product, the result. Map each idea onto an interaction in `references/motion-engine-api.md`.
- Never invent numbers, quotes, prices or results. Use relative bars, skeleton text or labels from the transcript, and list what is illustrative. Real figures only when the user gives them.
- One idea per clip. One change per spoken beat, about 0.4 to 1.2 seconds apart.

## Table 3: captions (captions stage)
| Setting | Value |
|---|---|
| Style | the user's pick |
| Position | bottom, raised above any panel that sits low |
| During full-frame cutaways | show or hide (ask) |
| Words per page | about 3.5 seconds of speech |
