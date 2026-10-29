# Edit rules (step 5)

Rules for every cut, the composition pattern, and platform specs. Source: the repurposing skill, field-tested on a LinkedIn publishing pipeline.

## Contents
1. Cut rules
2. Timestamps
3. Composition
4. Tool choice
5. Key lessons
6. Render

## 1. Cut rules

**Teasers:** only put a teaser in front when the user asks for one, even where another reference file says always.

**Opening Clip (CRITICAL):**
- The first clip is the hook - it must grab attention immediately
- Must start at the start of a complete sentence or idea with an explicit subject
- NEVER start with joining words ("But", "And", "So", "Now", "Then", "However")
- NEVER start with pronouns without context ("It", "This", "That", "They", "These", "There")
- NEVER start with filler, hedging, or weak openers ("I think", "You know", "Basically")
- Review the full transcript and deliberately select the strongest possible opening - a hook, an insight, a bold statement, or a compelling question

**Closing Clip (CRITICAL):**
- Must end at the natural conclusion of a thought - never trailing off, never a hard stop mid-idea
- Should leave the viewer with a takeaway, a call-to-action, or a sense of closure
- If the last word sounds like it leads into something else, keep going until it resolves
- Good endings: a summary statement, a strong opinion, a forward-looking insight
- Bad endings: trailing off, abrupt cuts, filler, unrelated tangents

**Clean Cut Points (every cut, no exceptions):**
- Cuts happen at a natural pause in the content - never mid-sentence, never mid-word
- Respect the idea, not just the words: a cut is clean when the speaker just finished a complete thought and there is a natural breath after the last word
- Every clip must be a complete, standalone thought with an explicit subject
- The stitched video must tell a coherent story, not feel like random fragments

**Editing modes - pick ONE in intake:**

1. **Hard-cut mode (DEFAULT for social clips: LinkedIn, TikTok, Reels).** No transitions. Ever. No fades on video or audio, no crossfades, no dissolves. Clip ends on one frame, the next begins on the very next frame. Audio starts and stops at full volume. Clean hard cuts read as confident and native on social feeds; fades read as template-ware. Build with plain `<Sequence>` blocks + `premountFor={60}` (see Composition Rules below). **Do not use `TransitionSeries`** - it has a null-props bug that crashes Studio in current Remotion versions.
2. **Crossfade mode (optional, for trailers/teasers/montages when the user explicitly wants blended transitions).** NEVER allow overlapping audio noise: cosine curves only (audio fade-out 1.5s, fade-in 1.2s, visual crossfade 1s), no fade-in on the first clip, no fade-out on the last. See [references/transitions.md](transitions.md) for the `createVolumeFn` pattern and the TransitionSeries bug workaround.

## 2. Timestamps

**Transcription-first timestamps (CRITICAL - the single source of truth):**
- All clip boundaries come from whisper word-level timestamps, never from scrubbing or guessing
- `startMs`/`endMs` = whisper timestamps of the first and last spoken words → these define the captions
- Audio/video cut points DERIVE from those: `audioEndMs = endMs + audioBufferMs` per clip. Whisper timestamps run ~200-700ms ahead of actual speech, so without the buffer the last word gets clipped
- Punctuation tokens (".", ",") have timestamps but are NOT spoken - never use them as `endMs`
- Captions are filtered by the raw transcript boundaries, NOT the buffered audio end, so words from the next sentence never flash on screen during the buffer zone
- Always verify by ear in Studio: the last word resolves fully, the next sentence doesn't bleed in
- Full pattern with code in [references/transcription.md](transcription.md)

## 3. Composition

- One composition per project video, in `src/compositions/<platform>/`
- Clip config lives in a clearly marked `CONFIG` block at the top - the only place to edit. Document every timestamp with the actual spoken words as a comment
- Export duration as a constant; register every composition in `src/Root.tsx`

**The hard-cut pattern (default):**

```tsx
const CLIPS = [
  {
    label: 'Hook',
    startMs: 148_920,   // "The reason most automations fail..." (whisper timestamp of first word)
    endMs: 238_340,     // "...and that's what makes it work." (whisper timestamp of last spoken word)
    audioBufferMs: 200, // per-clip: small when the next sentence starts fast, up to 700 when there's a gap
  },
] as const;

const clips = CLIPS.map((c) => {
  const audioEndMs = c.endMs + c.audioBufferMs;
  return {...c, audioEndMs, startFrame: msToFrames(c.startMs), endFrame: msToFrames(audioEndMs),
          duration: msToFrames(audioEndMs - c.startMs)};
});

// premountFor={60} is MANDATORY on every Sequence - it preloads the next clip 2s early.
// Without it OffthreadVideo hasn't decoded the next clip's first frame and you get a black flash at the cut.
<Sequence from={0} durationInFrames={clips[0].duration} premountFor={60}>
  <OffthreadVideo src={staticFile('source.mp4')} startFrom={clips[0].startFrame} endAt={clips[0].endFrame} />
</Sequence>
```

Total duration = sum of clip durations. No overlap, no subtraction.

**Captions:** never `import` the captions JSON (bloats the bundle, kills hot reload) - `fetch(staticFile(...))` with `delayRender`/`continueRender`, pre-filtered to clip ranges. Full pattern + the frosted-pill recipe: [references/captions.md](captions.md).

---

### Platform specs

| Platform | Resolution | FPS | Max duration | Notes |
|---|---|---|---|---|
| LinkedIn | 1920x1080 (16:9) | 30 | 10 min | H.264 MP4; native-feeling hard cuts |
| TikTok / Reels / Shorts | 1080x1920 (9:16) | 30 | 60-90s | word-highlight captions carry sound-off viewing |
| Square feed | 1080x1080 (1:1) | 30 | - | |

---

## 4. Tool choice

| Task | FFmpeg | Remotion |
|------|--------|----------|
| Stitching | Same codec, no styling | Anything styled or previewed |
| Captions | SRT burn-in | TikTok-style word highlighting |
| Teasers | Quick cuts | Text overlays, branded elements |

FFmpeg = fast CLI, batch, format conversion. Remotion = styled content, preview-before-render, React.

---

## 5. Key lessons

- **Transcription:** `@remotion/install-whisper-cpp`, NOT Python whisper (10x faster, Metal GPU). `base.en` for speed, `medium.en` for final quality. `whisperCppVersion: '1.5.5'` and `tokenLevelTimestamps: true` are required
- **Whisper drift:** timestamps run 200-700ms ahead of audio - per-clip `audioBufferMs` always, verify by ear
- **Black flash between clips** = missing `premountFor={60}`
- **Studio loading slowly** = moov atom at the end of the file - remux with `+faststart`
- **Studio crash on transitions** = `TransitionSeries` null-props bug - use plain `Sequence` hard cuts
- **Teasers (teaser jobs only, see teasers.md):** 3-4 clips totaling 25-30s; 1.3x playback for energy (1.5x is too fast); first teaser clip must NOT overlap the intro start
- **Captions:** pill container behind text beats stroke/shadow for legibility on any footage; same colors on all clips so contrast normalizes

- `fps` in `work/cuts.json` must equal the composition fps, or the remapped captions drift.

## 6. Render (step 9, only on approval)

```bash
npx remotion render CompositionName out/final.mp4 --video-bitrate 50M --audio-bitrate 320k
```
