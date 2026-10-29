#!/usr/bin/env python3
"""Render infographic sources into canvas artboards, in the user's brand.

Sources are Design Component files with three extras layered on top:

  Palette tokens   @GROUND@, @INK@, @ACCENT@ ...   resolved per theme from brand.json
  Brand tokens     @AUTHOR@, @HANDLE@, @SITE@ ...  resolved from brand.json
  Logo tokens      <!--MARK:claude:40-->           resolved to real app vectors

  Name.dcx.html   -> Name.dc.html                  one artboard
  Name.dcxt.html  -> NameLight.dc.html + NameDark.dc.html
                     Both modes come from ONE source on purpose. Light and dark
                     drift apart the moment they are separate files: a copy fix
                     lands in one and nobody notices the other until it is public.
                     An <!--OUT:Light=Foo,Dark=Bar--> header renames the outputs.

Every colour, font and identity string comes from brand.json. There is no
built-in brand: the bundled brand.default.json is a grayscale placeholder that
exists so the pipeline can be smoke-tested, and the build prints a loud warning
when it is used. Generate a real brand.json from the user's design-system/
folder first (see references/brand-adaptation.md).

Usage:
  python3 build.py --src <dir of sources> --out <dir for artboards>
                   [--brand <brand.json>] [--kit <dir>]

Brand resolution order: --brand flag, then <src>/brand.json, then
./design-system/infographic-brand.json, then the placeholder default.
"""
import argparse, json, os, re, sys

TILE_BG_KEY = "card"   # tile fill comes from the light theme so marks stay readable


def _rgba(hexv, a):
    r, g, b = (int(hexv.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{a})"


def _lighten(hexv, amt):
    v = hexv.lstrip("#")
    r, g, b = (min(255, int(v[i:i + 2], 16) + amt) for i in (0, 2, 4))
    return f"#{r:02X}{g:02X}{b:02X}"


def _lum(hexv):
    r, g, b = (int(hexv.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def load_brand(path):
    b = json.load(open(path))
    for key in ("fonts", "light", "dark"):
        if key not in b:
            sys.exit(f"brand.json is missing the '{key}' block. "
                     f"See references/brand-adaptation.md for the schema.")
    return b


def themes_from(brand):
    """Expand the brand's primitive colours into the full token set.

    The derived tokens (gradients, borders, the numeral style) are computed
    rather than stored, so a brand.json only has to answer the questions a
    design system can actually answer: ground, ink, muted, hairline, surfaces,
    one accent pair, and the semantic success/danger pair.
    """
    fonts = brand["fonts"]
    out = {}
    for mode in ("Light", "Dark"):
        c = brand[mode.lower()]
        dark = mode == "Dark"
        ink, ground, hair = c["ink"], c["ground"], c["hair"]
        t = {
            "GROUND": ground,
            "GROUNDBG": (f"linear-gradient(180deg, {_lighten(ground, 8)} 0%, {ground} 46%)"
                         if dark else ground),
            "INK": ink, "MUTED": c["muted"], "LINE": ink, "HAIR": hair,
            "BOX": f"1px solid {_rgba(ink, 0.30)}" if dark else f"2px solid {ink}",
            "PANEL": c["panel"], "PANEL2": c["panel2"], "CARD": c["card"],
            "SHADOW": c["shadow"],
            "ACCENT": c["accent"], "ACCENT2": c["accent2"],
            "SUCCESS": c["success"], "DANGER": c["danger"],
            "ONACCENT": c["onaccent"],
            "NUMC": c["accent2"] if dark else ink,
            "DISPLAYFONT": fonts["display"], "BODYFONT": fonts["body"],
            "MONOFONT": fonts["mono"], "FONTLINK": fonts["link"],
            "SITE": brand.get("site", ""),
            "AUTHOR": brand.get("author", {}).get("name", ""),
            "HANDLE": brand.get("author", {}).get("handle", ""),
            "AVATAR": brand.get("author", {}).get("avatar", ""),
            "BRANDMARK": brand.get("brandmark", {}).get(mode.lower(), ""),
        }
        t["NUM"] = (f"font-family: {fonts['display']}; font-weight: 700; font-size: 42px; "
                    f"line-height: 1; color: {t['NUMC']}; flex: none; min-width: 34px;")
        if dark:
            t["RULE"] = (f"linear-gradient(90deg, {_rgba(ink, 0.22)} 0%, "
                         f"{_rgba(ink, 0.07)} 55%, {_rgba(ink, 0)} 100%)")
            t["RULE2"] = (f"linear-gradient(90deg, {_rgba(ink, 0.72)} 0%, "
                          f"{_rgba(ink, 0.24)} 62%, {_rgba(ink, 0)} 100%)")
        else:
            t["RULE"] = (f"linear-gradient(90deg, {hair} 0%, {_lighten(hair, 12)} 55%, "
                         f"{_rgba(hair, 0)} 100%)")
            t["RULE2"] = (f"linear-gradient(90deg, {ink} 0%, {_rgba(ink, 0.55)} 62%, "
                          f"{_rgba(ink, 0)} 100%)")
        out[mode] = t
    return out


class Logos:
    """Real app marks, swapped in for the logo comment tokens.

    Full colour wherever a colour vector exists. A mark whose artwork is
    essentially black (Notion, X, GitHub, Apple) vanishes on a dark ground, so
    on dark it falls back to that brand's single-colour glyph drawn in the dark
    theme's ink. Tiled marks keep their colour in both modes because the light
    tile carries them.
    """

    def __init__(self, kit, themes):
        self.mono = json.load(open(os.path.join(kit, "logos.json")))
        self.color = json.load(open(os.path.join(kit, "logos-color.json")))
        self.dark_ink = themes["Dark"]["INK"]
        self.tile_bg = themes["Light"]["CARD"]
        self.tile_border = themes["Light"]["INK"]
        self.body_font = themes["Light"]["BODYFONT"]

    def names(self):
        return sorted(self.mono)

    def mark(self, slug, size, dark=False, tiled=False):
        if slug not in self.mono:
            sys.exit(f"unknown logo '{slug}'. Run add_logo.py first, or check spelling. "
                     f"Available: {', '.join(self.names())}")
        i = self.mono[slug]
        black = _lum(i["hex"]) < 0.22
        swap = dark and black and not tiled
        if slug in self.color and not swap:
            c = self.color[slug]
            return (f'<svg viewBox="{c["viewBox"]}" role="img" aria-label="{i["title"]}" '
                    f'style="display:block;flex:none;height:{size}px;width:auto;'
                    f'max-width:{round(size * 1.45)}px;">{c["inner"]}</svg>')
        fill = self.dark_ink if swap else i["hex"]
        return (f'<svg viewBox="0 0 24 24" role="img" aria-label="{i["title"]}" '
                f'style="display:block;flex:none;height:{size}px;width:{size}px;">'
                f'<path fill="{fill}" d="{i["d"]}"/></svg>')

    def tile(self, slug, t, ic):
        return (f'<div style="display:flex;align-items:center;justify-content:center;width:{t}px;'
                f'height:{t}px;background:{self.tile_bg};border:2px solid {self.tile_border};'
                f'border-radius:8px;flex:none;">{self.mark(slug, ic, tiled=True)}</div>')

    def labelled(self, inner, label):
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:10px;'
                f'flex:none;">{inner}<span style="font-family:{self.body_font};'
                f'font-size:15px;font-weight:600;letter-spacing:0.02em;'
                f'color:inherit;">{label}</span></div>')

    def render(self, src, dark=False):
        src = re.sub(r'<!--MARK:([a-z0-9]+):(\d+)-->',
                     lambda m: self.mark(m[1], int(m[2]), dark), src)
        src = re.sub(r'<!--MARKW:([a-z0-9]+):(\d+):([^>]+?)-->',
                     lambda m: self.labelled(self.mark(m[1], int(m[2]), dark), m[3]), src)
        src = re.sub(r'<!--TILE:([a-z0-9]+):(\d+):(\d+)-->',
                     lambda m: self.tile(m[1], int(m[2]), int(m[3])), src)
        src = re.sub(r'<!--TILEW:([a-z0-9]+):(\d+):(\d+):([^>]+?)-->',
                     lambda m: self.labelled(self.tile(m[1], int(m[2]), int(m[3])), m[4]), src)
        return src


def theme(src, tokens):
    # A brand with no corner mark just loses the element, instead of rendering
    # a broken image. Same for a missing avatar.
    for key in ("BRANDMARK", "AVATAR"):
        if not tokens.get(key):
            src = re.sub(r'<img[^>]*src="@' + key + r'@"[^>]*>', "", src)
    for k, v in tokens.items():
        src = src.replace("@" + k + "@", v)
    return src


def find_brand(flag, srcdir, here):
    for p in (flag,
              os.path.join(srcdir, "brand.json"),
              os.path.join(os.getcwd(), "design-system", "infographic-brand.json")):
        if p and os.path.exists(p):
            return p, False
    return os.path.join(here, "..", "assets", "kit", "brand.default.json"), True


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="directory holding .dcx.html / .dcxt.html sources")
    ap.add_argument("--out", required=True, help="directory to write .dc.html artboards into")
    ap.add_argument("--brand", help="brand.json produced from the user's design system")
    ap.add_argument("--kit", default=os.path.join(here, "..", "assets", "kit"),
                    help="directory holding logos.json and logos-color.json")
    a = ap.parse_args()

    brand_path, is_default = find_brand(a.brand, a.src, here)
    if is_default:
        print("WARNING: no brand.json found, building with the grayscale placeholder brand.\n"
             "         This output is a pipeline test, not a deliverable. Generate the\n"
             "         user's brand.json first: references/brand-adaptation.md.")
    THEMES = themes_from(load_brand(brand_path))
    L = Logos(os.path.abspath(a.kit), THEMES)
    os.makedirs(a.out, exist_ok=True)

    def write(path, body, label):
        left = re.findall(r'@[A-Z0-9]+@|<!--(?:MARK|MARKW|TILE|TILEW):[^>]*-->', body)
        if left:
            sys.exit(f"unresolved token in {label}: {left[:3]}")
        open(path, "w").write(body)
        print("wrote", os.path.basename(path), f"{len(body)//1024} KB")

    n = 0
    for f in sorted(os.listdir(a.src)):
        p = os.path.join(a.src, f)
        if f.endswith(".dcx.html"):
            write(os.path.join(a.out, f.replace(".dcx.html", ".dc.html")),
                  L.render(theme(open(p).read(), THEMES["Light"])), f)
            n += 1
        elif f.endswith(".dcxt.html"):
            src = open(p).read()
            names = dict(re.findall(r'(\w+)=(\w+)', re.search(r'<!--OUT:([^>]*)-->', src)[1])) \
                    if "<!--OUT:" in src else {}
            src = re.sub(r'<!--OUT:[^>]*-->\n?', '', src)
            stem = f.replace(".dcxt.html", "")
            for t in THEMES:
                write(os.path.join(a.out, names.get(t, stem + t) + ".dc.html"),
                      L.render(theme(src, THEMES[t]), dark=(t == "Dark")), f"{f} [{t}]")
                n += 1
    if not n:
        sys.exit(f"no .dcx.html or .dcxt.html sources found in {a.src}")
    print(f"{n} artboards -> {a.out}  (brand: {os.path.abspath(brand_path)})")


if __name__ == "__main__":
    main()
