"""Put the finished video and every motion clip on a Claude Design canvas.

Two steps, with the asset upload in between (the upload is an Artifact tool call, not a script):

  python3 make_canvas.py prep  motion/plan.json out/final.mp4 canvas
      Makes browser-playable review files under 14 MB each in canvas/assets/ and lists them in
      canvas/assets/manifest.json. Transparent .mov panels become on-black MP4s. When the final
      video is too big for one upload, it is replaced by one short segment around each clip.

  python3 make_canvas.py build motion/plan.json canvas "<canvas title>"
      Reads canvas/assets/urls.json ({"<file name>": "/_blob/<id>", ...}, from the upload results)
      and writes canvas/project/canvas.json plus one .dc.html artboard per clip and a Main artboard.
      Re-running build after a clip changes rewrites every artboard; publish only the changed ones.
"""
import html, json, os, pathlib, subprocess, sys
from datetime import datetime, timezone

LIMIT = 14 * 1024 * 1024
KIND = {'panel': 'transparent panel', 'full': 'full-frame cutaway', 'scene': 'scene'}
PAD = 5.0  # seconds of context around a clip in a segment


def run(cmd):
    subprocess.run(cmd, check=True)


def probe(f):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=width,height:format=duration', '-of', 'json', str(f)],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    return j['streams'][0]['width'], j['streams'][0]['height'], float(j['format']['duration'])


def web(src, dst, start=None, dur=None, crf=28, width=1280, on_black=False):
    cmd = ['ffmpeg', '-loglevel', 'error', '-y']
    if on_black:
        w, h, _ = probe(src)
        cmd += ['-f', 'lavfi', '-i', f'color=black:s={w}x{h}']
    if start is not None:
        cmd += ['-ss', f'{start:.2f}']
    cmd += ['-i', str(src)]
    if dur is not None:
        cmd += ['-t', f'{dur:.2f}']
    vf = f'scale=\'min({width},iw)\':-2'
    if on_black:
        cmd += ['-filter_complex', f'[0][1]overlay=shortest=1,{vf}']
    else:
        cmd += ['-vf', vf]
    cmd += ['-c:v', 'libx264', '-crf', str(crf), '-preset', 'medium', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', str(dst)]
    run(cmd)
    return dst


def fit(src, dst, **kw):
    """Encode, then step quality and size down until the file fits one upload."""
    for crf, width in [(18, 1920), (23, 1920), (28, 1280), (32, 1280), (32, 960), (35, 854), (38, 640)]:
        web(src, dst, crf=crf, width=width, **kw)
        if dst.stat().st_size <= LIMIT:
            return True
    return False


def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def prep(plan_p, final, canvas):
    plan_p, final, canvas = pathlib.Path(plan_p), pathlib.Path(final), pathlib.Path(canvas)
    P = json.load(open(plan_p)); base = plan_p.parent
    a = canvas / 'assets'; a.mkdir(parents=True, exist_ok=True)
    files = {'clips': {}, 'final': None, 'segments': {}}
    for c in P['clips']:
        src = (base / c['file']).resolve(); dst = a / f"clip-{c['id']}.mp4"
        if not fit(src, dst, on_black=src.suffix.lower() == '.mov'):
            sys.exit(f'clip {c["id"]} will not fit under 14 MB')
        files['clips'][c['id']] = dst.name
    if final.exists():
        dst = a / 'final.mp4'
        if fit(final, dst):
            files['final'] = dst.name
        else:
            dst.unlink(missing_ok=True)
            _, _, dur = probe(final)
            for c in P['clips']:
                s = max(0, c['in'] - PAD); e = min(dur, c['out'] + PAD)
                seg = a / f"segment-{c['id']}.mp4"
                if not fit(final, seg, start=s, dur=e - s):
                    sys.exit(f'segment {c["id"]} will not fit under 14 MB')
                files['segments'][c['id']] = {'file': seg.name, 'from': s, 'to': e}
    json.dump(files, open(a / 'manifest.json', 'w'), indent=1)
    names = list(files['clips'].values()) + ([files['final']] if files['final'] else []) + \
        [s['file'] for s in files['segments'].values()]
    print('upload these to the canvas asset store (Artifact publish, asset: true, file_paths):')
    for n in names:
        print(' ', (a / n).resolve(), f'{(a / n).stat().st_size / 1e6:.1f} MB')


def brand(root):
    b = {'canvas': '#E9E7E2', 'ink': '#0B0B0B', 'surface': '#FFFFFF', 'accent': '#FF5A1F', 'font': 'Geist'}
    p = root / 'brand.json'
    if p.exists():
        k = json.load(open(p))
        b.update({x: k[x] for x in b if x in k})
        b['font'] = k.get('heading_font', k.get('font', b['font']))
    return b


def page(title, w, h, body, B):
    fam = B['font'].replace(' ', '+')
    props = json.dumps({'$preview': {'width': w, 'height': h}})
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fam}:wght@400;600;700&amp;display=swap">
<style>
body{{margin:0;font-family:'{B['font']}',system-ui,sans-serif;color:{B['ink']};background:{B['canvas']}}}
</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: 48px; display: flex; flex-direction: column; gap: 24px; background: {B['canvas']}">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{props}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''


def video(url, w, h, at=None):
    # at: a media-fragment start time, so the artboard shows a settled frame instead of an empty first one
    if at is not None:
        url = f'{url}#t={at:.2f}'
    return (f'<video src="{url}" controls="controls" loop="loop" muted="muted" preload="metadata" '
            f'style="width: {w}px; height: {h}px; display: block; background: #0B0B0B; border-radius: 12px"></video>')


def build(plan_p, canvas, title):
    plan_p, canvas = pathlib.Path(plan_p), pathlib.Path(canvas)
    P = json.load(open(plan_p)); base = plan_p.parent; a = canvas / 'assets'
    M = json.load(open(a / 'manifest.json')); U = json.load(open(a / 'urls.json'))
    B = brand(base.parent)
    proj = canvas / 'project'; proj.mkdir(parents=True, exist_ok=True)
    w0, h0, _ = probe(a / next(iter(M['clips'].values())))
    vw = 1280 if w0 >= h0 else 608; vh = round(vw * h0 / w0)
    e = html.escape
    boards, order = {}, []

    # Main: the final video (or the segments) plus the timing list
    rows = ''.join(
        f'<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; padding: 12px 0; border-top: 1px solid rgba(11,11,11,.12); font-size: 18px">'
        f'<div style="font-weight: 600">{e(c["id"])} {e(c["title"])}</div><div>{fmt(c["in"])} to {fmt(c["out"])}</div>'
        f'<div>{KIND.get(c.get("kind"), "scene")}</div><div>{e(c.get("line", ""))}</div></div>'
        for c in P['clips'])
    if M['final']:
        media = video(U[M['final']], vw, vh); media_h = vh
    else:
        sw = vw // 2 - 12; sh = round(sw * h0 / w0)
        cells = ''.join(f'<div style="display: flex; flex-direction: column; gap: 8px"><div style="font-size: 16px">Around clip {e(k)}: {fmt(s["from"])} to {fmt(s["to"])}</div>{video(U[s["file"]], sw, sh)}</div>'
                        for k, s in M['segments'].items())
        media = f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px">{cells}</div>'
        media_h = ((len(M['segments']) + 1) // 2) * (sh + 32) + 24
    mw = vw + 96; mh = 96 + 60 + 24 + media_h + 24 + 40 + len(P['clips']) * 64 + 48
    body = (f'<h1 style="margin: 0; font-size: 48px; line-height: 60px">{e(title)}</h1>{media}'
            f'<div style="font-size: 20px; font-weight: 700">{"Scenes" if all(c.get("kind") == "scene" for c in P["clips"]) else "Motion clips"}</div><div>{rows}</div>')
    (proj / 'Main.dc.html').write_text(page(title, mw, mh, body, B))
    boards['Main.dc.html'] = {'x': 0, 'y': 0, 'w': mw, 'h': mh, 'title': 'Final video'}; order.append('Main.dc.html')

    # One artboard per clip, in a row under Main
    cw = vw + 96; ch = 96 + 48 + 24 + vh + 24 + 150
    for i, c in enumerate(P['clips']):
        name = f"clip-{c['id']}.dc.html"
        body = (f'<div style="font-size: 32px; font-weight: 700; line-height: 48px">{e(c["id"])} {e(c["title"])}</div>'
                f'{video(U[M["clips"][c["id"]]], vw, vh, at=c.get("poster", (c["out"] - c["in"]) * 0.6))}'
                f'<div style="display: flex; flex-direction: column; gap: 8px; font-size: 20px">'
                f'<div>{fmt(c["in"])} to {fmt(c["out"])} · {KIND.get(c.get("kind"), "scene")}</div>'
                f'<div style="font-style: italic">{e(c.get("line", ""))}</div>'
                f'<div style="opacity: .6">{e(os.path.basename(c["file"]))}</div></div>')
        (proj / name).write_text(page(f'Clip {c["id"]}', cw, ch, body, B))
        boards[name] = {'x': i * (cw + 80), 'y': mh + 120 + 223, 'w': cw, 'h': ch, 'title': f'Clip {c["id"]}: {c["title"]}'}
        order.append(name)

    idx = proj / 'canvas.json'
    if idx.exists():
        C = json.load(open(idx)); C['boards'].update(boards)
        C['order'] = [o for o in C['order'] if o not in order] + order
    else:
        C = {'v': 3, 'createdOnFiles': {'v': 1, 'at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
             'title': title, 'launch': {'view': 'canvas'}, 'pages': [], 'boards': boards, 'order': order,
             'notes': {'clips': {'x': 0, 'y': mh + 120, 'text': 'Motion clips', 'kind': 'title1', 'maxW': len(P['clips']) * (cw + 80)}},
             'designSystems': []}
    json.dump(C, open(idx, 'w'), indent=1)
    print('wrote', idx, 'and', len(order), 'artboards')


if __name__ == '__main__':
    if sys.argv[1] == 'prep':
        prep(*sys.argv[2:5])
    elif sys.argv[1] == 'build':
        build(*sys.argv[2:5])
    else:
        sys.exit(__doc__)
