"""whisper.cpp captions JSON -> word timestamps for timing motion clips.
Merges sub-word tokens, attaches punctuation to the word before it, drops special tokens like [_BEG_].
One output line per sentence, each word as <seconds>:<word>.
usage: python3 captions_to_words.py public/edited.captions.json > motion/work/words.txt"""
import json, sys
words = []
for c in json.load(open(sys.argv[1])):
    t = c['text']
    if not t.strip() or t.strip().startswith('[_'):
        continue
    if t.startswith(' ') or not words:
        words.append([c['startMs'] / 1000, t.strip()])
    else:
        words[-1][1] += t.strip()
line = []
for s, w in words:
    line.append(f'{s:.2f}:{w}')
    if w[-1] in '.?!':
        print(' '.join(line)); line = []
if line:
    print(' '.join(line))
