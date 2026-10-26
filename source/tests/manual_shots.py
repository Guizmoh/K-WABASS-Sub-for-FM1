#!/usr/bin/env python3
"""Every screen of the manual, from the emulator (build/web/ksub.wasm): ../docs/img/NAME.png at 480 x 480.
   python3 tests/manual_shots.py   (after web/make_emulator.sh)"""
import subprocess, os
from pathlib import Path
from PIL import Image
OUT = Path("../docs/img"); OUT.mkdir(parents=True, exist_ok=True)
T = [0]
def run(lines, tag):
    Path(f"build/{tag}.txt").write_text("\n".join(lines) + "\nend\n")
    subprocess.run(["node", "tests/shots.mjs", f"build/{tag}.txt"], check=True, capture_output=True, env={**os.environ, "WASM": "build/web/ksub-b.wasm"})   # (the 8-engine build shows everything)
class S:
    def __init__(s): s.l, s.t, s.names = [], 100, []
    def c(s, cmd, dt=120): s.l.append(f"{s.t} {cmd}"); s.t += dt
    def btn(s, b, dt=120): s.c(f"btn {b}", dt)
    def enc(s, e, n, dt=120): s.c(f"enc {e} {n}", dt)
    def hold(s, b, ms): s.c(f"down {b}", ms); s.c(f"up {b}", 150)
    def shot(s, name, wait=1150):
        s.t += wait - 120; s.c(f"shot {name}", 200); s.names.append(name)
HOME, EDIT, ENV, SEQ, LFO, FX, ARP, GLO, SEL, SAVE, PLAY = 8, 6, 4, 11, 5, 2, 10, 7, 3, 9, 12
def finish(s, tag):
    run(s.l, tag)
    for n in s.names:
        b = Path(f"build/shots/{n}.raw").read_bytes()
        im = Image.new("RGB", (240, 240))
        im.putdata([((v >> 11) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31) for v in (b[i] | b[i + 1] << 8 for i in range(0, len(b), 2))])
        im.resize((480, 480), Image.NEAREST).save(OUT / f"{n}.png")
    print(tag, len(s.names), "screens")

# 1. the pages, the views, the windows (CLASSIC, NEON)
s = S(); s.shot("x-ask", 300); s.btn(SEL, 400)   # (the first start's question: SEL = CLASSIC)
s.c("on 12", 300); s.c("on 14", 10); s.shot("p-home", 300); s.c("off 12", 50); s.c("off 14", 50)
def views(page_btn, names):
    s.btn(page_btn, 200)
    for i, n in enumerate(names):
        if i: s.btn(page_btn, 200)
        s.shot(n, 300)
views(HOME, ["v-home", "v-livemix"][:1]); s.btn(HOME, 200); s.shot("v-livemix", 300)
views(EDIT, ["v-osca", "v-oscb", "v-sub", "v-combine", "v-sample"])
views(ENV, ["v-env-amp", "v-env-filter", "v-env-mod"])
views(SEQ, ["v-filter", "v-filtermod", "v-seq"])
views(LFO, ["v-lfo1", "v-lfo2", "v-step", "v-matrix"])
views(FX, ["v-sat", "v-ott", "v-comp", "v-eq", "v-delay", "v-reverb", "v-chorus", "v-phaser", "v-crush", "v-master"])
views(ARP, ["v-presets-a", "v-presets-b", "v-arp"])
views(GLO, ["v-system", "v-midi"])
s.btn(HOME, 200); s.btn(SEL, 300); s.c("on 12", 100); s.enc(2, 60, 100); s.enc(3, 30, 100); s.shot("w-perform", 300)
s.c("down 1", 200); s.c("on 9", 100); s.c("on 13", 100); s.shot("w-perform-pads", 200); s.c("off 9", 50); s.c("off 13", 50); s.c("up 1", 100); s.c("off 12", 50)
s.btn(SEL, 200); s.enc(2, 40, 100); s.enc(3, -30, 100); s.shot("w-morph-xy", 300)
s.btn(SEL, 300); s.shot("w-fxlive", 300); s.btn(SEL, 200); s.shot("w-macros", 300)
s.btn(SEL, 200); s.enc(2, 50, 100); s.shot("w-morph-ab", 300)
s.btn(SEL, 200); s.btn(ARP, 300); s.enc(5, 2, 200); s.shot("v-presets-tag", 300)
s.btn(EDIT, 300); s.btn(EDIT, 100); s.btn(EDIT, 100); s.btn(EDIT, 100); s.btn(EDIT, 300); s.c("on 12", 200); s.enc(0, 4, 100); s.enc(1, 1, 100)
s.t += 3200; s.c("off 12", 200); s.shot("v-resample", 600)
s.btn(HOME, 200); s.btn(EDIT, 300)
s.enc(2, 6, 100); s.shot("pop-value", 400)
s.enc(0, 3, 100); s.c("down 5", 100); s.enc(4, 1, 200); s.c("up 5", 100); s.btn(LFO, 300); s.enc(0, 3, 100); s.enc(1, 2, 100); s.shot("pop-dest", 400)
s.hold(FX, 900); s.c("on 2", 150); s.c("on 12", 150); s.shot("w-pads", 200); s.c("off 2", 80); s.c("off 12", 80)
s.btn(HOME, 300); s.c("down 9", 400); s.shot("h-undo", 150); s.c("up 9", 100)
s.c("down 12", 700); s.shot("h-hold", 150); s.c("up 12", 100)
finish(s, "m1")

# 2. SHIFT (three columns: the menu, OCT- held in the middle, OCT+ held on the right)
s = S(); s.btn(SEL, 400); s.hold(GLO, 1100); s.btn(HOME, 300)
for page, nm in ((HOME, "s-home"), (EDIT, "s-osc"), (ENV, "s-env"), (SEQ, "s-filter"), (LFO, "s-lfo"), (FX, "s-fx")):
    s.btn(page, 300); s.shot(nm, 300)
s.btn(EDIT, 300); s.c("down 0", 150); s.enc(3, 6, 100); s.shot("s-osc-mid", 250); s.c("up 0", 150)
s.c("down 1", 150); s.enc(4, 5, 100); s.shot("s-osc-right", 250); s.c("up 1", 150)
s.c("down 0", 400); s.shot("s-hold-undo", 150); s.c("up 0", 100)
finish(s, "m2")

# 3. the themes: the same screen in every palette
s = S(); s.btn(SEL, 400); s.btn(HOME, 200)
combos = [(t, p) for t in range(6) for p in (0, 1)] + [(0, p) for p in range(2, 11)] + [(4, p) for p in (8, 9, 10, 2, 7)] + [(5, p) for p in (2, 8, 9, 7)]
NM = {(0, 0): "neon", (0, 1): "amber", (1, 0): "studio", (1, 1): "ocean", (2, 0): "pure", (2, 1): "purered", (3, 0): "rack", (3, 1): "magma",
      (0, 2): "synthwave", (0, 3): "mint", (0, 4): "blackwhite", (0, 5): "inverted", (0, 6): "red", (0, 7): "ice", (0, 8): "fluo", (0, 9): "pink", (0, 10): "gold",
      (4, 0): "glow-green", (4, 1): "glow-toxic", (5, 0): "tech-volt", (5, 1): "tech-cyber", (5, 2): "tech-synthwave", (5, 8): "tech-fluo", (5, 9): "tech-pink", (5, 7): "tech-ice", (4, 8): "glow-fluo", (4, 9): "glow-pink", (4, 10): "glow-gold", (4, 2): "glow-synthwave", (4, 7): "glow-ice"}
for t, p in combos:
    s.btn(GLO, 200); s.enc(0, -30, 100); s.enc(0, 4, 100); s.enc(1, -8, 100); s.enc(1, t, 100)
    s.enc(0, 1, 100); s.enc(1, -12, 100); s.enc(1, p, 100)
    s.btn(HOME, 200); s.btn(EDIT, 200); s.shot("t-" + NM[(t, p)], 1300)
finish(s, "m3")

# 4. GLOW: the theme on several screens
s = S(); s.btn(SEL, 400); s.btn(GLO, 200); s.enc(0, -30, 100); s.enc(0, 4, 100); s.enc(1, 4, 100); s.btn(HOME, 300)
s.shot("g-home", 1300); s.btn(EDIT, 300); s.shot("g-osc", 300); s.btn(ENV, 300); s.shot("g-env", 300); s.btn(LFO, 300); s.shot("g-lfo", 300)
s.btn(FX, 300); s.shot("g-fx", 300); s.btn(ARP, 300); s.shot("g-presets", 300); s.btn(SEQ, 300); s.shot("g-filter", 300)
finish(s, "m4")

# 5. TECH: the layout on its screens (the theme the 6th of the list)
s = S(); s.btn(SEL, 400); s.btn(GLO, 200); s.enc(0, -30, 100); s.enc(0, 4, 100); s.enc(1, 8, 100); s.btn(HOME, 300)
s.shot("k-home", 1300); s.btn(EDIT, 300); s.shot("k-osc", 300); s.btn(EDIT, 200); s.shot("k-oscb", 300); s.btn(ENV, 300); s.shot("k-env", 300)
s.btn(LFO, 300); s.shot("k-lfo", 300); s.btn(FX, 300); s.shot("k-fx", 300); s.btn(FX, 200); s.btn(FX, 200); s.shot("k-fx3", 300)
s.btn(SEQ, 300); s.shot("k-filter", 300); s.btn(ARP, 300); s.shot("k-presets", 300); s.btn(GLO, 300); s.shot("k-system", 300)
finish(s, "m5")

# 6. BRIGHTNESS: the same screen in the four steps
s = S(); s.btn(SEL, 400); s.btn(GLO, 200); s.enc(0, -30, 100); s.enc(0, 6, 100)
for lv, nm in ((0, "eco"), (1, "normal"), (2, "bright"), (3, "max")):
    s.enc(1, -5, 100); s.enc(1, lv, 100); s.btn(HOME, 200); s.shot("b-" + nm, 1300); s.btn(GLO, 200)
finish(s, "m6")
