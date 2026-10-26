<p align="center"><img src="docs/img/promo.png" alt="K-WASUB, a modern bass synth for the M-VAVE FM-1"></p>

# K-WASUB · FM1 modern Bass firmware

**English** · [Français](fr/README.md)

**A modern bass synth for the M-VAVE FM-1**: DnB, dub, dubstep, techno. Live wobble, reese, sub, 808, an EQ, a morph between four sounds, effects on the keys. Free and open source (GPL-3.0). *Beta.*

| | |
|---|---|
| 🎛 **Try it** (browser) | [`emulator/index.html`](emulator/index.html)  |
| ⬇️ **Install** on the FM-1 | [`installer.html`](installer.html) (Chrome or Edge, USB) · or `INSTALL-Windows.bat` / `INSTALL-Mac.command` / `INSTALL-Linux.sh` |
| 📖 **Manual** (illustrated) | [`manual.html`](manual.html) |
| 🏠 **Home page** | [`index.html`](index.html) (with GitHub Pages on: <https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/>) |
| 🗺 **Specifications** | [`SPECIFICATIONS.md`](SPECIFICATIONS.md): done, to do, ideas |
| 📜 Technical notes | [`docs/TECHNICAL-NOTES.md`](docs/TECHNICAL-NOTES.md) |
| 🇫🇷 French | [`fr/`](fr/): the home page, manual, specifications and notes in French |

## What it does

- **Play**: the 27 keys play the bass, `K1`–`K4` set the four settings that matter on each page.
- **Wobble**: hold `LFO` and turn a knob to wire LFO 2 to whatever that knob sets (LFO 1 if you prefer: `SYSTEM › LFO HELD = LFO`).
- **FX PADS**: hold `FX`; white keys change the wobble speed (4, 8, 16, 24, 32, 48), black keys play stutters, tape stop, DJ filter, saturation, phaser…
- **MORPH**: `SEL` ×2 = X/Y square (at first, the same sound in 4 variations), ×5 = A/B fade on the beat.
- **PERFORM** (`SEL`): 4 named macros, the morph and the pads on one screen.
- **Engines**: one firmware; `SYSTEM › ENGINES` picks ESSENTIAL (4 engines, the default) or ALL (8).
- **Sound**: multiband OTT, MONO BASS, a sub locked on OSC A, **RESAMPLE** (the output into OSC C, to replay, slow down, loop).
- **Presets**: tags (sub, reese, growl, wobble, pluck, 808, drone), instant change.
- **Two modes**: CLASSIC (lists) or SHIFT (3 columns, `OCT−` and `OCT+` as Shift); hold `GLO` to switch.
- **Looks**: 6 themes (CLASSIC GLOW and TECH with gradients), 19 palettes, 4 brightness levels.
- **Output**: DEEP BASS, limiter, AUTO LEVEL; if the FM-1 stops, `LAST STOP` says why.

## Install

1. FM-1 over USB (a **data** cable), other MIDI software closed.
2. Open [`installer.html`](installer.html) in Chrome or Edge → “Install K-WASUB”.
3. The packages are in [`install/`](install/) (`k-wasub-X.fwsc`, older ones in `install/older/`, checksums in `SHA256SUMS`).

You can go back to KAWA (`install/kawa-0.5.fwsc`) or to the stock firmware (M-UPGRADE) at any time; holding `OCT−` at power-on = USB rescue.

## Build

```sh
cd source
./build.sh --release 0.9.19          # -> build/k-wasub-0.9.19.fwsc
APP_VER=0.9.19 bash web/make_emulator.sh      # emulator
bash web/make_installer.sh                    # installer.html with the newest package
bash tests/run_stress.sh                      # load tests (UBSan)
python3 tests/manual_shots.py                 # the manual's screenshots (docs/img)
```
JieLi toolchain and AC79 SDK: see `source/BUILDING.md` and `source/tools/get_toolchain.sh`.

## Support

☕ [ko-fi.com/omnipotard](https://ko-fi.com/omnipotard)

## Credits and license

GPL-3.0. K-WASUB is born from [KAWA](https://github.com/Guizmoh/Kawa-Tracker-Fm1) (Omnipotard / Leo Kuroshita, Hügelton Instruments), whose FM-1 platform it reuses (boot, USB, audio, screen). See [`LICENSING.md`](LICENSING.md). Not affiliated with M-VAVE.
