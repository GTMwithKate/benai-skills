#!/usr/bin/env python3
"""Screenshot one artboard to PNG with headless Chrome.

The canvas has its own PNG export, but it goes through a save dialog nobody can
drive from here. This renders the same pixels straight to a file: unwrap the
<x-dc> shell, inline the images as data URIs so the page stands alone, then let
Chrome shoot it at the artboard's exact size.

Usage:
  python3 render_png.py <dir holding the .dc.html> <ArtboardName> --out <file.png> [--scale 2]
"""
import argparse, base64, os, re, subprocess, sys, tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    sys.exit("No Chrome or Chromium found. Install one, or export the PNG from the "
             "canvas toolbar instead.")


def standalone(d, name):
    src = open(os.path.join(d, f"{name}.dc.html")).read()
    link = re.search(r'<link rel="stylesheet" href="https://fonts[^>]*>', src)
    body = re.search(r"</helmet>(.*?)</x-dc>", src, re.S)
    if not body:
        sys.exit(f"{name}.dc.html does not look like an artboard (no <x-dc> block)")
    body = body[1]
    for root in (d, os.path.dirname(os.path.abspath(__file__)) + "/../assets/kit"):
        if not os.path.isdir(root):
            continue
        for f in os.listdir(root):
            if f.endswith(".png") and f'src="{f}"' in body:
                b64 = base64.b64encode(open(os.path.join(root, f), "rb").read()).decode()
                body = body.replace(f'src="{f}"', f'data:image/png;base64,{b64}"'.join(['src="', '']))
    return ("<!doctype html><meta charset=utf-8>" + (link[0] if link else "") +
            "<style>html,body{margin:0;padding:0;overflow:hidden}</style><body>" + body + "</body>")


def size_of(html):
    w = re.search(r"width:\s*(\d+)px", html)
    h = re.search(r"height:\s*(\d+)px", html)
    if not (w and h):
        sys.exit("Could not read the artboard size. Every root element carries an explicit "
                 "width and height in px; check the source.")
    return int(w[1]), int(h[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("name")
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=2,
                    help="2 gives a crisp 2160x2700 for a 1080x1350 artboard")
    a = ap.parse_args()

    page = standalone(os.path.abspath(a.dir), a.name)
    w, h = size_of(page)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
        t.write(page); tmp = t.name

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={a.scale}", f"--window-size={w},{h}",
                    "--virtual-time-budget=15000", f"--screenshot={os.path.abspath(a.out)}",
                    "file://" + tmp], capture_output=True)
    os.unlink(tmp)
    if not os.path.exists(a.out):
        sys.exit("Chrome produced no file. Try again, or export from the canvas toolbar.")
    print(f"{a.out}  {int(w*a.scale)}x{int(h*a.scale)}  {os.path.getsize(a.out)//1024} KB")


if __name__ == "__main__":
    main()
