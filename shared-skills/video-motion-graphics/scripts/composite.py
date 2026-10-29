"""Lay rendered motion clips over a video, each in its time window, and keep the video's audio.

usage: python3 composite.py motion/plan.json out/with-motion.mp4

plan.json: {"video": "../public/edited.mp4", "clips": [{"id", "file", "in", "out", "kind"}]}
Paths are relative to plan.json. A .mov clip with alpha lays over the video as a panel; an
.mp4 clip covers the frame. A clip shorter than its window holds its last frame.
"""
import json, pathlib, subprocess, sys

plan_path, out = pathlib.Path(sys.argv[1]), sys.argv[2]
plan = json.loads(plan_path.read_text())
here = plan_path.parent
path = lambda f: str(f if pathlib.Path(f).is_absolute() else (here / f).resolve())

args = ['ffmpeg', '-loglevel', 'error', '-y', '-i', path(plan['video'])]
graph, below = [], '0:v'
for n, clip in enumerate(plan['clips'], start=1):
    args += ['-i', path(clip['file'])]
    hold = max(0.0, clip['out'] - clip['in'])
    graph.append(f"[{n}:v]format=yuva420p,tpad=stop_mode=clone:stop_duration={hold:.3f},setpts=PTS-STARTPTS+{clip['in']:.3f}/TB[m{n}]")
    graph.append(f"[{below}][m{n}]overlay=eof_action=pass:enable='between(t,{clip['in']:.3f},{clip['out']:.3f})'[o{n}]")
    below = f'o{n}'
graph.append(f'[{below}]format=yuv420p[vout]')
args += ['-filter_complex', ';'.join(graph), '-map', '[vout]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '18',
         '-preset', 'medium', '-c:a', 'copy', '-movflags', '+faststart', '-shortest', out]
subprocess.run(args, check=True)
print('wrote', out)
