#!/usr/bin/env python3
"""Scaffold a working folder from a kit template.

Templates are copied, never edited in place. The kit is the source of truth for
everyone using this skill, so a one-off post must not be able to mutate it. When
a one-off turns out to be worth keeping, it gets promoted back deliberately
(see references/improving-the-kit.md).

Alongside the template source, this copies the brand into the working folder:
brand.json plus any image files it names (avatar, brand marks). That makes a
working folder self-contained, so a build next week uses the brand the artboard
was designed under, not whatever the design system has become since.

Usage:
  python3 new_project.py --template Quote --into ~/work/my-post
                         [--brand <brand.json>] [--name Hook]
"""
import argparse, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "assets", "kit")


def find_brand(flag):
    for p in (flag, os.path.join(os.getcwd(), "design-system", "infographic-brand.json")):
        if p and os.path.exists(p):
            return p, False
    return os.path.join(KIT, "brand.default.json"), True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True,
                    help="Quote, QuoteBoxed, CheatSheet, DecisionTree or LogoLibrary")
    ap.add_argument("--into", required=True)
    ap.add_argument("--brand", help="brand.json generated from the user's design system")
    ap.add_argument("--name", help="rename the source in the working folder")
    a = ap.parse_args()

    src = None
    for ext in (".dcxt.html", ".dcx.html"):
        p = os.path.join(KIT, a.template + ext)
        if os.path.exists(p):
            src = p; break
    if not src:
        have = sorted(f.split(".dc")[0] for f in os.listdir(KIT) if ".dc" in f)
        sys.exit(f"no template called '{a.template}'. Available: {', '.join(have)}")

    work = os.path.abspath(a.into)
    out = os.path.join(work, "src")
    os.makedirs(out, exist_ok=True)
    ext = ".dcxt.html" if src.endswith(".dcxt.html") else ".dcx.html"
    dest = os.path.join(out, (a.name or a.template) + ext)
    shutil.copy(src, dest)

    brand_path, is_default = find_brand(a.brand)
    shutil.copy(brand_path, os.path.join(out, "brand.json"))
    if is_default:
        print("WARNING: copied the grayscale placeholder brand. Generate the user's real")
        print("         brand.json before building anything they will see")
        print("         (references/brand-adaptation.md), then replace src/brand.json.")

    # Bring along the images the brand names, so the artboards render standalone.
    b = json.load(open(brand_path))
    brand_dir = os.path.dirname(os.path.abspath(brand_path))
    for img in {b.get("author", {}).get("avatar", ""),
                b.get("brandmark", {}).get("light", ""),
                b.get("brandmark", {}).get("dark", "")}:
        if img:
            p = os.path.join(brand_dir, img)
            if os.path.exists(p):
                shutil.copy(p, work)
            else:
                print(f"note: brand.json names '{img}' but it is not next to brand.json. "
                      f"Copy it into {work} yourself before rendering.")

    print(f"source:  {dest}")
    print(f"brand:   {os.path.join(out, 'brand.json')}")
    print(f"next:    python3 {os.path.join(HERE, 'build.py')} --src {out} --out {work}")


if __name__ == "__main__":
    main()
