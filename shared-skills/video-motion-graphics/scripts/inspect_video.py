"""Look at a video before planning motion over it: its specs, a contact sheet, and which
stretches leave empty dark space (for example a speaker in a box with black around it).

usage: python3 inspect_video.py video.mp4 out_dir
Writes out_dir/contact.png (16 frames) and out_dir/video.json. Look at the contact sheet yourself.
"""
import json, os, subprocess, sys

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-of', 'json', '-show_streams', '-show_format', video],
                                  capture_output=True, text=True, check=True).stdout)
v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
w, h, dur = int(v['width']), int(v['height']), float(probe['format']['duration'])
step = max(1.0, dur / 16)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-vf',
                f'fps=1/{step:.3f},scale=480:-2,tile=4x4:padding=6:color=gray', '-frames:v', '1', f'{out}/contact.png'], check=True)

# Two frames a second at 64 x 36 grey. A frame "has empty space" when its left or right third is near black.
gw, gh = 64, 36
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-vf', f'fps=2,scale={gw}:{gh},format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
frames = [raw[i:i + gw * gh] for i in range(0, len(raw) - gw * gh + 1, gw * gh)]
def empty_side(f):
    left = [f[r * gw + c] for r in range(gh) for c in range(gw // 3)]
    right = [f[r * gw + c] for r in range(gh) for c in range(2 * gw // 3, gw)]
    avg = lambda xs: sum(xs) / len(xs)
    return 'left' if avg(left) < 10 else 'right' if avg(right) < 10 else None
stretches, cur = [], None
for i, f in enumerate(frames):
    side = empty_side(f)
    if cur and cur['empty'] == side:
        cur['to'] = (i + 1) / 2
    else:
        cur = {'from': i / 2, 'to': (i + 1) / 2, 'empty': side}
        stretches.append(cur)
info = {'width': w, 'height': h, 'fps': v['r_frame_rate'], 'duration': dur,
        'stretches': [dict(s, layout='boxed' if s['empty'] else 'full') for s in stretches]}
json.dump(info, open(f'{out}/video.json', 'w'), indent=1)
print(json.dumps(info, indent=1))
