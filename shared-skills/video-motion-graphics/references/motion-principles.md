# Motion principles

The rules for any motion graphic: an explainer, a video overlay, a logo animation, a product demo, a short-form reel. Read this before the storyboard. Each rule comes from a real review.

## Story first

- **Start from the problem, not the product.** Show the pain the viewer knows, then the fix. A walkthrough of the app's screens is not a demo. A product demo that opened on the UI was rejected; the ones that work open on the problem.
- **One idea per beat.** A beat is 1 to 2 seconds. If a scene holds two ideas, make it two scenes.
- **Every motion explains something.** Ask of each move: what does it tell the viewer? If nothing, cut it. No decoration for its own sake.
- **Words on screen are labels, not sentences.** 2 to 6 words at a time. The voice or the viewer's reading carries the rest.
- **Use the real objects.** Real app logos in their own colours, real file and folder shapes, real UI when the point is the UI. Never invent numbers, quotes or results. Mark anything illustrative.

## How it moves

- **One direction for the whole film.** Pick the way the film travels (default: to the left). Every ordinary scene change follows it. Keep other directions for moments that mean something: rising up for a conclusion, zooming in to go deeper.
- **Exit and entry match.** A scene that leaves moving left hands over to one that enters moving left, at about the same speed. Cut while things are still moving on both sides. Never let a scene settle to a full stop just before a cut.
- **Something carries the eye across a cut.** A word, a card, a cursor or a shape that leaves one scene and lands in the next. A plain crossfade carries nothing.
- **Cause and effect.** A click makes something happen on the same frame. Big things react slowly, small things snap.
- **A short pause before the payoff.** Hold 0.3 to 0.7 seconds of stillness before the result lands. Then land it hard.
- **No idle motion.** No breathing, floating, drifting or pulsing to fill time. If a scene has nothing left to do, it is too long: cut it or add the next piece of the story.
- **Eases.** Exponential ease-out for entrances (`BAI.ease.out`), ease-in for exits that leave mid-motion (`BAI.ease.in`). No bounce, no elastic, no wobble.
- **Stagger groups.** Items in a list enter 60 to 120 ms apart, in reading order.
- **One-world camera rule.** In a film that pans across one big world (`BAI.camera`), anything knocked away leaves the frame upward or disappears. Otherwise it lands on top of the next station.
- **Cuts in a one-world film.** The engine shows one scene at a time, so anything still on screen at a cut vanishes in one frame. At the exact cut, the frame must hold only things drawn in `always(t)` (the carrier, a line, the logo). Space stations at least one frame width plus the content width apart.
- **Switch states on a frame.** An icon swap or a tick happens on a frame boundary (`BAI.after`), or crossfades over 2 frames. Otherwise motion blur shows both at once.

## How it looks

- **Use the design system.** Colours, fonts, logos and components come from the brand's design system. If a design project folder exists, read `design-system/README.md`, `design-system/anti-slop.md` and the use case's `feedback.md` and `examples/`.
- **One accent colour, for one job.** Usually "this is the thing to look at".
- **Big, readable type.** On a 1920 x 1080 frame: headlines 96 px or more, labels 40 px or more. Nothing under 28 px.
- **Kinetic type with icons.** A word and its icon enter together. One icon set, one stroke weight.
- **Alternate stages.** Dark and light stages can alternate to mark a change of section, not every scene.
- **Faces.** Use only real cutouts of real photos. Never cut a face with a circle mask or from a thumbnail.
- **Banned:** particles, glows, lens flares, gradient text, glass as decoration, bouncy easing, fake UI noise, stock "AI" looks (blue-purple gradients).

## Checks before anyone sees it

- Contact sheet of stills: every scene's settled state plus a mid-move frame. Look at every one: nothing cramped, clipped, unreadable, off-brand or overlapping.
- Pause test: at any second something meaningful is happening or has just landed. No dead holds longer than the planned pause.
- The first frame and the last frame look intentional on their own (they become the thumbnail and the hold).
