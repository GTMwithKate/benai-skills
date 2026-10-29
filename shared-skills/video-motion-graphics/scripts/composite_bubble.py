"""Section composite: motion clips full-frame, Ben's face bubble from the source on top.

usage: python3 motion/composite_bubble.py out/tip1-motion.mp4 [first_frame last_frame]

The bubble is cut out of the source frame by frame, so it keeps the source's own zoom at
the cut (it grows from the small bubble into its settled spot over the first second).
Before the first motion frame (the few frames that carry Ben's first word) clip 1's
empty first frame stands in for the screen.
"""
import json, subprocess, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1920, 1080, 24000 / 1001
ROOT = pathlib.Path(__file__).resolve().parent.parent
CLIPS = json.load(open(ROOT / 'motion/clips.json'))
OUT = sys.argv[1]
F0 = int(sys.argv[2]) if len(sys.argv) > 2 else 3446          # section start (source frame)
F1 = int(sys.argv[3]) if len(sys.argv) > 3 else CLIPS[-1]['frame_in'] + CLIPS[-1]['frames'] - 1
N = F1 - F0 + 1
FIXED = (1308, 712, 560, 315)          # settled bubble box in the source
RIGHT, BOTTOM = 1867, 1026.5           # the zoom keeps the bubble's bottom-right corner here
INK = np.array([10, 12, 12], np.float32)
SS = 4                                  # supersampling for smooth mask edges


def reader(path, sel=None, n=None):
    vf = ['-vf', f"select='between(n\\,{sel[0]}\\,{sel[1]})'", '-vsync', '0'] if sel else []
    cmd = ['ffmpeg', '-loglevel', 'error', '-i', str(path), *vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
    got = 0
    while n is None or got < n:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        got += 1
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    p.kill()


def motion_frames():
    for c in CLIPS:
        f = ROOT / 'motion' / c['file']
        k = 0
        for fr in reader(f, n=c['frames']):
            yield fr; k += 1
        last = fr
        while k < c['frames']:       # a clip one frame short holds its last frame
            yield last; k += 1


def bubble_box(fr, n):
    if n > 3490:
        return FIXED
    col = fr[550:1080, 1700].mean(axis=1)
    top = None
    for i in range(3, len(col)):
        if col[i - 3] > 200 and col[i] < 110:
            top = 550 + i; break
    if top is None:
        return FIXED
    h = BOTTOM - top; w = h * 16 / 9
    return (RIGHT - w, top, w, h)


def rrect_alpha(box, r, region):
    """Soft-edged rounded-rect alpha for a box, over the crop region (x0, y0, x1, y1)."""
    x, y, w, h = box
    x0, y0, x1, y1 = region
    im = Image.new('L', ((x1 - x0) * SS, (y1 - y0) * SS), 0)
    ImageDraw.Draw(im).rounded_rectangle([(x - x0) * SS, (y - y0) * SS, (x + w - x0) * SS, (y + h - y0) * SS], r * SS, fill=255)
    im = im.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255


cache = {}


def layers(box):
    key = tuple(round(v, 1) for v in box)
    if key in cache:
        return cache[key]
    x, y, w, h = box
    k = w / 560                                   # scale corner, border, shadow with the bubble
    PAD = int(60 * k) + 8
    inner = (x + 2, y + 2, w - 4, h - 4)
    outer = (x - 3 * k, y - 3 * k, w + 6 * k, h + 6 * k)
    region = (max(0, int(x) - PAD), max(0, int(y) - PAD), min(W, int(x + w) + PAD + 1), min(H, int(y + h) + PAD + 1))
    a_in = rrect_alpha(inner, 13 * k, region)
    a_out = rrect_alpha(outer, 17 * k, region)
    sh = Image.fromarray((a_out * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22 * k))
    sh = np.roll(np.asarray(sh, np.float32) / 255, int(10 * k), axis=0) * 0.30
    res = (region, a_in[..., None], a_out[..., None], sh[..., None])
    if len(cache) < 64:
        cache[key] = res
    return res


enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-framerate', '24000/1001', '-i', '-',
                        '-ss', f'{F0 / FPS:.5f}', '-t', f'{N / FPS:.5f}', '-i', str(ROOT / 'public/source.mp4'),
                        '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', OUT], stdin=subprocess.PIPE)

src = reader(ROOT / 'public/source.mp4', sel=(F0, F1))
mot = motion_frames()
m0 = next(mot)                                             # clip 1, frame 0
boxes = []
for i, s in enumerate(src):
    n = F0 + i
    m = m0 if n <= CLIPS[0]['frame_in'] else next(mot)
    out = m.astype(np.float32)
    box = bubble_box(s, n); boxes.append([n, *[round(v, 1) for v in box]])
    (x0, y0, x1, y1), a_in, a_out, sh = layers(box)
    reg = out[y0:y1, x0:x1]
    reg *= (1 - sh)                                        # soft shadow
    reg[:] = reg * (1 - a_out) + INK * a_out               # 2px ink border ring
    srcr = s[y0:y1, x0:x1].astype(np.float32)
    reg[:] = reg * (1 - a_in) + srcr * a_in                # Ben
    enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
    if i % 240 == 0:
        print(f'{i}/{N}', flush=True)
enc.stdin.close(); enc.wait()
json.dump(boxes[:60], open(ROOT / 'motion/work/bubble-boxes.json', 'w'))
print('wrote', OUT, len(boxes), 'frames')
