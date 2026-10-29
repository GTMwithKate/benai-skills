#!/usr/bin/env python3
"""Add a brand mark to the kit's logo library.

Nobody should hand-draw an app logo. It always looks slightly wrong and the brand
owner notices. This pulls the real vector from the public logo sets, in this order:

  svgl -> gilbarbara/logos -> vectorlogo.zone -> Simple Icons (single colour)

Two guards, both learned the hard way:
  Ids are namespaced with the slug, because a dozen inlined SVGs that all define
  #a fight over the same gradient and the page renders garbage.
  Anything wider than 1.75:1 is rejected as a wordmark. HubSpot and Zapier both
  came back as full text logos squeezed into a 40px icon slot.

Usage:
  python3 add_logo.py <slug> [--title "Display Name"] [--url <explicit svg url>]
  python3 add_logo.py --list
"""
import argparse, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "assets", "kit"))
MONO_P, COLOR_P = os.path.join(KIT, "logos.json"), os.path.join(KIT, "logos-color.json")


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "infographic-builder/1.0"})
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")


def clean(slug, svg):
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    m = re.search(r"<svg\b([^>]*)>(.*)</svg>", svg, flags=re.S)
    if not m:
        return None
    attrs, inner = m[1], m[2]
    vb = re.search(r'viewBox="([^"]+)"', attrs)
    if vb:
        view = vb[1]
    else:
        w, h = re.search(r'width="([\d.]+)', attrs), re.search(r'height="([\d.]+)', attrs)
        if not (w and h):
            return None
        view = f"0 0 {w[1]} {h[1]}"
    for i in set(re.findall(r'id="([^"]+)"', inner)):
        n = f"{slug}-{i}"
        inner = inner.replace(f'id="{i}"', f'id="{n}"').replace(f"url(#{i})", f"url(#{n})")
        inner = inner.replace(f'href="#{i}"', f'href="#{n}"')
    return {"viewBox": view, "inner": re.sub(r"\s+", " ", inner).strip()}


def aspect(view):
    try:
        _, _, w, h = (float(v) for v in view.replace(",", " ").split())
        return w / h if h else 99
    except Exception:
        return 99


def candidates(slug, explicit):
    if explicit:
        return [explicit]
    out = []
    try:
        sv = {x["title"].lower(): x for x in json.loads(get("https://api.svgl.app"))}
        hit = sv.get(slug) or next((v for k, v in sv.items() if k.replace(" ", "") == slug), None)
        if hit:
            r = hit["route"]
            out.append(r if isinstance(r, str) else (r.get("light") or r.get("dark")))
    except Exception:
        pass
    for stem in (slug + "-icon", slug):
        out.append(f"https://cdn.jsdelivr.net/gh/gilbarbara/logos/logos/{stem}.svg")
    out.append(f"https://www.vectorlogo.zone/logos/{slug}/{slug}-icon.svg")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--title"); ap.add_argument("--url")
    ap.add_argument("--hex", default="4A4A52", help="fallback brand colour, no leading #")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    mono = json.load(open(MONO_P))
    if a.list:
        print(f"{len(mono)} marks:\n  " + "\n  ".join(
            f"{k:18} {mono[k]['title']}" for k in sorted(mono)))
        return
    if not a.slug:
        sys.exit("give a slug, e.g. add_logo.py attio")
    if a.slug in mono and not a.url:
        print(f"'{a.slug}' is already in the library. Pass --url to replace it.")
        return

    best = None
    for u in candidates(a.slug, a.url):
        try:
            c = clean(a.slug, get(u))
        except Exception:
            continue
        if not c or len(c["inner"]) >= 60000:
            continue
        c["src"], c["aspect"] = u, aspect(c["viewBox"])
        if best is None or abs(c["aspect"] - 1) < abs(best["aspect"] - 1):
            best = c
    if not best:
        sys.exit(f"no vector found for '{a.slug}'. Some companies publish none at all "
                 f"(Attio and Fireflies are two). Use a bordered name chip in the layout "
                 f"instead of drawing a fake mark.")
    if best["aspect"] > 1.75:
        sys.exit(f"the only vector found for '{a.slug}' is {best['aspect']:.1f}:1 wide, which is "
                 f"a wordmark, not an icon. Pass --url with an icon-only file.")

    mono[a.slug] = {"title": a.title or a.slug.title(), "hex": "#" + a.hex.lstrip("#"),
                    "slug": a.slug, "d": None}
    color = json.load(open(COLOR_P))
    color[a.slug] = {k: best[k] for k in ("viewBox", "inner")}
    json.dump(mono, open(MONO_P, "w"))
    json.dump(color, open(COLOR_P, "w"))
    print(f"added '{a.slug}' from {best['src']}  (aspect {best['aspect']:.2f})")
    print(f"use it as <!--MARK:{a.slug}:40-->")


if __name__ == "__main__":
    main()
