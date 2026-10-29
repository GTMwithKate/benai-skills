#!/usr/bin/env python3
"""Report artboards whose content overflows its frame.

Overflow is the one failure that is invisible while you work and obvious the
moment somebody looks at the exported PNG: the frame is a fixed 1080x1350, so a
line too many silently clips the footer off the bottom.

It measures twice. Once in Space Grotesk and Montserrat, and once with the fonts
forced to the fallback stack, because PNG export cannot embed Google Fonts and
the fallback sets at slightly different metrics. A layout that only fits in one
of the two is not finished.

Usage:
  python3 check.py <dir holding .dc.html artboards>
"""
import json, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_png import find_chrome, standalone  # noqa: E402

PROBE = """
<script>
function measure() {
  const root = document.body.firstElementChild;
  const read = () => ({ o: root.scrollHeight - root.clientHeight,
                        w: root.scrollWidth - root.clientWidth });
  const web = read();
  const st = document.createElement('style');
  st.textContent = '*{font-family:Arial,Helvetica,sans-serif !important}';
  document.head.appendChild(st);
  void root.offsetHeight;
  const fall = read();
  st.remove();
  document.documentElement.setAttribute('data-fit', JSON.stringify({ web: web, fall: fall }));
}
// 'load' waits for the webfont stylesheet, which is the whole point of measuring twice.
if (document.readyState === 'complete') measure();
else window.addEventListener('load', measure);
</script>
"""

def probe(page):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
        t.write(page + PROBE); tmp = t.name
    out = subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                          "--virtual-time-budget=15000", "--dump-dom", "file://" + tmp],
                         capture_output=True, text=True).stdout
    os.unlink(tmp)
    m = re.search(r'data-fit="([^"]*)"', out)
    if not m:
        return None
    try:
        return json.loads(m[1].replace("&quot;", '"'))
    except Exception:
        return None


def main():
    d = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    boards = sorted(f[:-len(".dc.html")] for f in os.listdir(d) if f.endswith(".dc.html"))
    if not boards:
        sys.exit(f"no .dc.html artboards in {d}. Run build.py first.")
    bad = unknown = 0
    for b in boards:
        r = probe(standalone(d, b))
        if r is None:
            unknown += 1
            print(f"  ?  {b:26} could not measure, so look at this one yourself")
            continue
        w, f = r["web"], r["fall"]
        worst = max(w["o"], f["o"], w["w"], f["w"])
        if worst > 0:
            bad += 1
            print(f"  x  {b:26} overflows by {w['o']}px in the webfont, "
                  f"{f['o']}px in the fallback"
                  + (f", {max(w['w'], f['w'])}px sideways" if max(w['w'], f['w']) > 0 else ""))
        else:
            print(f"  ok {b:26} fits in both fonts")
    if unknown:
        print(f"\n{unknown} artboard(s) could not be measured. Do not treat those as passing.")
    if bad:
        print(f"\n{bad} artboard(s) clip. Trim copy, or tighten the vertical rhythm: "
              f"root gap first, then section padding, then font size. Leave about 5% slack "
              f"so a later copy edit does not push it over again.")
        sys.exit(1)
    if unknown:
        sys.exit(1)
    print(f"\nall {len(boards)} fit in both fonts")


if __name__ == "__main__":
    main()
