<p align="center"><img src="docs/img/promo.png" alt="K-WASUB, a modern bass synth for the M-VAVE FM-1"></p>

# K-WASUB · FM1 modern Bass firmware

**English** · [Français](fr/README.md) · [Español](es/README.md)

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
| 🇪🇸 Spanish | [`es/README.md`](es/README.md): the README in Spanish |

## Key features

1. **4 efficient engines** for modern basses, or **8 engines** for bass, pads & leads (`SYSTEM › ENGINES`).
2. **LFO learn**: hold `LFO` and turn any knob, LFO 2 is assigned to that setting in one gesture.
3. **CLASSIC** or **SHIFT** mode (`OCT−` / `OCT+`) for a faster workflow, chosen in the options.
4. **SEL windows**: PERFORM, MORPH, FX LIVE, MACROS.
5. **A/B morph**: blend two sounds live.
6. A live **LFO page** to reshape your wobble basses while you play.
7. **SEQ BASS**, **ARP**, **MIDI**.
8. The sound: engines, filters, effects, master, and **FX PADS**.
9. Animated oscillator visuals, live.
10. A visual **EQ**.
11. Totally different **themes**, to fit the way you work.
12. **Brightness**, contrast, fonts and size.
13. **Firmware language** (`SYSTEM › LANGUAGE`): English, Français or Español; English by default.

## Install

1. FM-1 over USB (a **data** cable), other MIDI software closed.
2. Open [`installer.html`](installer.html) in Chrome or Edge → “Install K-WASUB”.
3. The packages are in [`install/`](install/) (`k-wasub-X.fwsc`, older ones in `install/older/`, checksums in `SHA256SUMS`).

You can go back to KAWA (`install/kawa-0.5.fwsc`) or to the stock firmware (M-UPGRADE) at any time; holding `OCT−` at power-on = USB rescue.

## Build

```sh
cd source
./build.sh --release 0.9.46          # -> build/k-wasub-0.9.46.fwsc
APP_VER=0.9.46 bash web/make_emulator.sh      # emulator
bash web/make_installer.sh                    # installer.html with the newest package
bash tests/run_stress.sh                      # load tests (UBSan)
python3 tests/manual_shots.py                 # the manual's screenshots (docs/img)
```
JieLi toolchain and AC79 SDK: see `source/BUILDING.md` and `source/tools/get_toolchain.sh`.

## Support

☕ [ko-fi.com/omnipotard](https://ko-fi.com/omnipotard)

## Credits and license

GPL-3.0. K-WASUB is born from [KAWA](https://github.com/Guizmoh/Kawa-Tracker-Fm1) (Omnipotard / Leo Kuroshita, Hügelton Instruments), whose FM-1 platform it reuses (boot, USB, audio, screen). See [`LICENSING.md`](LICENSING.md). Not affiliated with M-VAVE.
