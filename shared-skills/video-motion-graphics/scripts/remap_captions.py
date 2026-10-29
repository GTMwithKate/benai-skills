"""Move source word timestamps onto the cut timeline, so the edited video needs no second transcription.
Keeps only words inside each clip's raw startMs..endMs (never the audio buffer), then shifts them to where
the clip sits in the edited video, using the same frame rounding as the hard-cut composition.
cuts.json: {"fps": 30, "clips": [{"startMs": 148920, "endMs": 238340, "audioBufferMs": 200}, ...]}  (same values as CLIPS)
usage: python3 remap_captions.py public/source.captions.json work/cuts.json > public/edited.captions.json"""
import json, sys
caps = json.load(open(sys.argv[1])); cuts = json.load(open(sys.argv[2])); fps = cuts['fps']
frames = lambda ms: round(ms / 1000 * fps)
out, offset_f = [], 0
for c in cuts['clips']:
    shift = offset_f * 1000 / fps - frames(c['startMs']) * 1000 / fps
    for w in caps:
        if w['startMs'] >= c['startMs'] and w['endMs'] <= c['endMs']:
            out.append({**w, 'startMs': round(w['startMs'] + shift), 'endMs': round(w['endMs'] + shift),
                        'timestampMs': round(w.get('timestampMs', w['startMs']) + shift)})
    offset_f += frames(c['endMs'] + c['audioBufferMs'] - c['startMs'])
print(json.dumps(out, indent=1))
