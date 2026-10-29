# Setup (step 1)

Install only what the chosen stages need. Check first, install second.

## Always
- `which ffmpeg || brew install ffmpeg`. The motion stage needs the `prores_ks` encoder for transparent panels (standard in Homebrew builds).
- Node 18+ and Python 3.

## Remotion project (edit and captions stages, and whisper)
1. If the project folder has no Remotion project, create one per `references/remotion-setup.md` (Remotion `^4.0.242`, React `^18.x`).
2. Install the extras: `npm i -D ts-node typescript && npm i @remotion/install-whisper-cpp @remotion/captions @remotion/google-fonts` (same version as `remotion`). Add a `tsconfig.json` if the project has none.
3. Copy `$SKILL/scripts/setup-whisper.ts` and `$SKILL/scripts/transcribe.ts` into the project's `scripts/`.
4. Run `npx ts-node scripts/setup-whisper.ts`. It installs whisper.cpp and the `base.en` model into `.whisper/`. For final quality, set `WHISPER_MODEL=medium.en` for both this and `transcribe.ts`.
5. Never use Python whisper or faster-whisper. whisper.cpp is 10x faster on the Mac GPU and its output feeds both the captions and the motion stage.

## Motion engine (motion stage, and every standalone film)
`bash $SKILL/scripts/setup-motion.sh ./motion`
It makes `motion/{films,out,work}`, copies the engine to `motion/engine/`, writes a `motion/brand.css` to fill in, and installs playwright-core. It renders with Google Chrome; without Chrome it installs Playwright's Chromium.

## YouTube source
Download with the latest yt-dlp through uvx, H.264 so Remotion can seek:
`uvx yt-dlp -f "bv*[vcodec^=avc1]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 -o public/source-raw.mp4 "<url>"`
Then prep it as `public/source.mp4` (step 3). A 429 from YouTube on captions does not matter: whisper makes the transcript.
