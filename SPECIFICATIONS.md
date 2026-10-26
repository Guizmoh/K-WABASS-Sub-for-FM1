# K-WASUB · Specifications

[English](SPECIFICATIONS.md) · [Français](fr/CAHIER-DES-CHARGES.md)

A modern bass synth for the M-VAVE FM-1 (JieLi AC79, two cores, no FPU). Last update: **0.9.58**.
This document says where the project stands: what is done, what has to be checked, what is left, and ideas to go further.

## 1. Vision

- **Who it is for**: people who make DnB, dub, dubstep, techno and want a bass that moves, playable with two hands on a pocket device.
- **Promise**: a wobble you shape live, deep and clean bass, a complete sound without plugins, a readable interface.
- **Principles**: simple to play, complete to tune; nothing blocks the audio; everything is free and open; every screen says what it does; no function is removed without saying so.

## 2. Done

### Sound
| Area | Detail | Version |
|---|---|---|
| Engines | 8 engines per oscillator (analog, super/reese, wavetable, FM, phase dist, wavefolder, sync, vocal); `SYSTEM › ENGINES` picks the first 4 (ESSENTIAL, default) or all 8 | ≤ 0.9, 0.9.19 |
| Oscillators | A + B (ADD, RING, X-MOD, SYNC), sub, noise, **OSC C sample** (18 sounds including 8 attacks, 9 textures; START / END cut, speed 25–400 % at the same pitch, forward / reverse / ping-pong, loop / once; 0.9.55) | 0.9.9-4 |
| Filter | 7 characters (LP24, LP12, BAND, HIGH, NOTCH, VOWEL, COMB), drive, mod by envelope, keyboard, velocity | ≤ 0.9 |
| Modulation | 3 envelopes, 2 LFOs locked to the tempo (round grid option), STEP FX (16 patterns), 4-slot matrix, 4 MACROS × 4 targets | ≤ 0.9 |
| Effects | Saturation, compressor + PUMP, bitcrush, chorus, phaser, delay (4 types), reverb (4 types), glue, sub boost, **4-band EQ** | 0.9.3 → 0.9.9-3 |
| Master | **DEEP BASS** (shelf +4 / +7 dB under 90 Hz), **always-on limiter**, **AUTO LEVEL** (normaliser) | 0.9.10 |
| Voices | Mono, legato, poly 4, glide with time | ≤ 0.9 |
| Presets | 51 factory sounds by style, 32 user slots, favourites, UNDO / REDO | ≤ 0.9 |
| SEQ / ARP / MIDI | SEQ BASS (16 patterns of up to 64 steps, probability, trig conditions and note length per step, 30 presets in 16/32/64, live REC; 0.9.53), **DRUMS** (808 / 909 / DUB TECHNO with its echo / ACOUSTIC (0.9.54), 8 coloured tracks, black keys = instrument, white keys = steps, OCT−/OCT+ = page, chance and conditions per step, 18 rhythm presets in 16/32/64, live REC; 0.9.53), **parameter locks** on the drums (LEVEL, TUNE, DECAY, TONE, RATCHET, ECHO: a step held + a knob) and SEQ BASS (CUTOFF, RESO, FILT ENV, DRIVE, WOB RATE, A SHAPE, SAMPLE START), recorded live with REC (0.9.57), ARP (5 modes), MIDI: learn, clock in/out, start/stop, program change; **SYNC OUT** for Pocket Operators / Volcas (a pulse every eighth on the left, 0.9.56); **USB audio** to a computer, a larger buffer for K-WASUB's long renders (0.9.56) | ≤ 0.9.8 |

### Playing and workflow
| Area | Detail | Version |
|---|---|---|
| Modes | CLASSIC (lists) and SHIFT (3 columns, OCT−/OCT+ = Shift); K1–K4 = the first 4 rows; knob acceleration | ≤ 0.9.7 |
| SEL windows | FX LIVE, MACROS, **MORPH X/Y**, **MORPH A/B** | 0.9.9-6 → 7 |
| **FX PADS** | Hold FX: white keys = wobble speed (4 8 16 24 32 48, 1/2, 1 bar), depth, shape; black = 4 stutters, tape stop, DJ filter, pump, saturation, phaser, crush | 0.9.10 |
| Long presses | OCT− UNDO, OCT+ REDO, SAVE UNDO/REDO, HOME A + B (0.9.52), REC PANIC, GLO CLASSIC/SHIFT, FX FX PADS, SEL A/B, PLAY HOLD, LFO/ENV quick assign, page = controlled random | 0.9.10 |
| Visual feedback | Value big with the old one, modulation bars, loading bar for long presses, scrolling destination list | ≤ 0.9.8 |
| Start | Screen with **the FM-1 seen from the front** (keys lit), no more question at every start | 0.9.10 |

### Added in 0.9.11
| Area | Detail |
|---|---|
| Sound | **MULTIBAND / OTT** 3 bands (per sound); adjustable **MONO BASS** (60–200 Hz); **SUB LOCK** (sub = OSC A lower, in phase) |
| Resample | The output for 2 to 4 s (11 kHz, mu-law, RAM) into OSC C, then loop / once / speed / keyboard |
| Live | **PERFORM** window: 4 named macros, X/Y morph, wobble, pads on OCT+ held; MORPH X/Y: the same sound in the 4 corners (as is, cutoff ¼ res ¾, wobble 1/8, wobble 1/16) |
| Presets | **Tags** (SUB, REESE, GROWL, WOBBLE, PLUCK, 808, DRONE) read from the settings, filter on K4; instant preset change (no question), only on HOME and PRESETS |
| Navigation | Each button opens the first view of its page; views and rows reordered by importance (EDIT, FX, SYSTEM, SEL, SHIFT FX); K1–K4 hints at the bottom of every screen (short form when needed); CLASSIC/SHIFT asked on the first start only |
| Theme | **FLUO** palette (fluo green on black) |

### Added in 0.9.12 – 0.9.13 and after
| Area | Detail |
|---|---|
| Themes | **CLASSIC GLOW** (gradients, fluo green; 0.9.12) and **TECH** (the picture on almost the whole page, four tiles, gradients running in different directions; 0.9.13) |
| Palettes | PINK, GOLD for every theme; VOLT and CYBER for TECH: 19 in all |
| Brightness | **BRIGHTNESS** ECO / NORMAL / BRIGHT / MAX (0.9.13): MAX = every colour at its top, pure white, panel at 255 |
| Languages | Everything is in English by default; the home page, manual, README, specifications and notes also exist in French under `fr/`; the emulator and the installer switch with `?lang=fr` |

### Interface
7 themes, 13 palettes + RAD gradient versions (INVERTED grey, RED, ICE, FLUO, PINK, GOLD…), 9 fonts, LOUPE, contrast fixed on MAX (DEEP BLACK), visuals everywhere (waves, envelopes with a dot, wavetable, FM operators, EQ…).

### Stability and tooling
Load governor; measured audio budget for the effects (the watchdog no longer sees the audio block); fallback to one core; **LAST STOP** (watchdog, low voltage, crash + address); automatic load tests (UBSan, A and B); web emulator A and B; one-page installer; standalone build.

## 3. To check on a real FM-1

Nothing has been tried on the device since 0.9.9-4. To look at first:

1. **Two-core mode**: is there sound? `SYSTEM › CPU LOAD` while playing WIDE REESE in POLY with effects?
2. **Switch-offs**: if the FM-1 still switches off, note `LAST STOP` at restart (and the address if CRASH).
3. **Brightness and contrast**: MAX clearly brighter than NORMAL? HIGH and MAX blacks really black? MAX too dark?
4. **Bass**: DEEP BASS (DEEP / MAX) on speakers or headphones; OTT at full stays clean?; AUTO LEVEL too slow / too pumping?
5. **FX PADS, MORPH, long presses**: is the timing (1 s for OCT−/OCT+) comfortable? accidental triggers in SHIFT?
6. **Screen**: smoothness of the gradients (TECH, CLASSIC GLOW, MORPH X/Y); banding?
7. **RESAMPLE**: does it record and play back as in the emulator?

## 4. Still to do

| Priority | Topic | Notes |
|---|---|---|
| High | Feedback from the first try on the FM-1 | fix whatever comes out of the test (cores, load, screen) |
| High | **Photo of the KAWA seen from the front** for the start screen | today drawn in code; a photo costs about 60 to 115 KB of flash |
| Medium | Turn on GitHub Pages (Settings › Pages › main / root) | so the home page, emulator and manual are online |
| Medium | Screen regression tests (compared screenshots) | `source/tests/manual_shots.py` is the base |
| Low | Demo B presets for the new functions (MORPH, PADS) | |

## 5. Ideas to go further

### Playing live: more reactive, more addictive
- **Custom PADS**: choose which effect goes on each black key, remember 4 pad sets (one per style).
- **Scene pads**: one key recalls a preset + a morph (drop, break, build) on the beat.
- **Build / drop**: one gesture (hold REC) that raises everything (filter, resonance, stutter, reverb) and releases on the downbeat.
- **Wobble tap**: tap the wobble's rhythm on a key, the LFO locks to it (like TAP tempo).
- **Record movements**: 4 to 8 bars of gestures (knobs, pads) replayed in a loop, with overdub.
- **A visual that dances**: the morph dot leaves a trail, the wave pulses with the kick, colour by style.
- **Performance mode**: one screen with only the 4 macros in big, the morph and the pads, nothing else.
- **Gesture lock**: both OCT buttons together lock the knobs (no wrong move on stage).
- **Velocity / pressure playing**: the keys also drive the filter or the morph if the keyboard sends pressure.

### More sound
- **Mono-bass assistant** (done in 0.9.11: MONO BASS): next, a crossover that follows the note.
- **Smart sub oscillator** (done: SUB LOCK).
- **Multiband distortion** (low / mid / high apart), giving wide basses without losing the sub.
- **Animated formant / vowel** driven by the LFO (the classic dubstep “yoi”), with a vowel library.
- **Longer resample**, with several slots, and saving to flash.
- **More samples and wavetables** (growl, screech, varied 808s), including a bank installable on its own.
- **Oversampling** on the saturation and the wavefolder (less aliasing) if the CPU allows.
- **Presets**: one set per sub-genre (liquid, neuro, jump-up, minimal dub techno…), with a tag and a search by style.

### Stability and performance
- **Continuous measurement** of every effect's time, with an “economy mode” that switches off the heaviest effects by itself.
- **Crash log** (the last 3 `LAST STOP` kept) readable in SYSTEM.
- **Start-up self-test** (voltage, flash, second core) with a clear message.
- **Safe saving**: two-step flash writes (no loss if power is cut while saving), export / import of patches over SysEx.
- **Tests on the device**: a 30-minute “burn-in” script (notes + morph + pads) with a load report.

### Interface and getting started
- **Built-in help**: one help screen per page (one key, a short text + a drawing).
- **Guided tour** at the first start (4 screens: play, wobble, FX PADS, record).
- **Preset search** by style with the knobs.
- **Custom themes**: choose accent and background colours, remembered.
- **Accessibility**: readable small font (done), contrast, text size, colour-blind friendly palettes (tested).
- **Manual and emulator**: “try this preset” links from the manual, sharing a patch by link.

### Community and project
- A community **preset bank**, installable from the page.
- A **download / version counter** on the home page, automatic changelog.
- **More translations**: ES, then others.
- A **contribution guide** (build, tests, screenshots) and sorted **issues** (bug / idea / sound).

## 6. Technical constraints (to keep in mind)

- Integers only, no 64-bit division (the processor has no FPU); the audio interrupt must stay short (256-sample blocks, 5.8 ms).
- RAM 78 KB of 96, pool 342 KB of 344, image 554 KB of 581 (0.9.55): the flash is nearly full; little room is left for samples.
- Patches have 140 parameters at most; user patches keep 112 bytes in the first sector and the rest in the second. Item ids fit in one byte (static assert).
- A flash write stops the sound for a few tens of ms (so only in silence); core 1 then waits in RAM.
- Any change of the save format must stay readable by older saves (fields added at the end).

## 7. Decisions to take together

1. A photo file of the KAWA seen from the front, to replace the start-screen drawing?
2. Names: K-WASUB everywhere (done in the firmware, the pages and the packages); the repository is **K-WASUB_Firmware_for_FM1**.
3. Next priority: **animated LFO shapes (drawn)**, **custom PADS**, **scenes**, **wobble tap**.

## 8. What Pure SUB and Serum do that would be worth adding here

Ranked by **value for a bass** and **cost on the FM-1** (CPU, RAM, a screen with a few buttons and 4 knobs). Pure SUB's functions are given from its general reputation; check before borrowing details.

| # | Function | From | Value | Cost | Remark |
|---|---|---|---|---|---|
| 1 | **Drag-and-drop-like mod matrix** (assign with one gesture, see the range on every setting) | Serum, Pure SUB | very high | low | already: LFO held + knob, violet bars. Left: ENV/VEL/MACRO sources, several amounts per knob, a view of assignments per page |
| 2 | **Drawn envelope and LFO curves** (free shape, 8 points) | Serum | high | medium | a 16-point “custom” LFO locked to the tempo: the signature wobble |
| 3 | **Wavetable warp modes** (bend, sync, mirror, PWM, FM from B) | Serum | high | medium | adds to WARP: a truly “living table” with a modulatable position |
| 4 | **Unison with blend, stereo and detune** per engine | Serum | high | medium | SUPER has part of it; add stereo spread and blend |
| 5 | **Multiband / OTT** (3-band compression, very “bass music”) | Serum (FX) | very high | medium | **done in 0.9.11** |
| 6 | **Clean sub and “mono bass”** (sub in phase, mono under a frequency) | Pure SUB | very high | low | **done in 0.9.11** |
| 7 | **Several saturation / distortion types**, in series or in parallel | Serum, Pure SUB | high | low | 4 types; add parallel (dry/wet) and a “tape” type |
| 8 | **More filters** (formant, comb, phaser, flanger as filters) | Serum | medium | low | VOWEL and COMB exist; add more curves and an adjustable slope |
| 9 | **Voices: mono / legato / glide / portamento per note** | Serum, Pure SUB | medium | low | glide done; add “glide in legato only” and a per-note time from the SEQ |
| 10 | **Named macros + performance page** | Serum, Pure SUB | high | low | **done in 0.9.11** (PERFORM) |
| 11 | **Preset browser with tags and search** | Serum | high | low | **done in 0.9.11** (tags on K4) |
| 12 | **Resample** (record the output into an oscillator) | Serum, DnB practice | very high | medium | **done in 0.9.11** |
| 13 | **Noise oscillator and textures** | Serum | medium | low | 5 textures already; add filtered, pitchable noise |
| 14 | **Visualisers (spectrum, waveform)** | Serum | medium | medium | 16-band spectrum on the FX page or the master |
| 15 | **MPE / full aftertouch** | Serum | low here | medium | only if an external controller justifies it |

**Next**: 2 (drawn LFO), 3 (wavetable modes), 4 (stereo unison), 7 (parallel saturation).

## 9. The most effective optimisations

### Workflow (what changes when you play)
1. **Performance page**: one page with 4 macros, the morph and the pads, no navigating during a song (**done**: PERFORM).
2. **Scenes**: one press recalls a preset + a morph + a wobble speed. A drop in one key.
3. **Wobble tap**: tapping the rhythm sets the division.
4. **Copy / paste a setting or a page** (hold a row, paste it on another) and **INIT** (start again from a neutral sound).
5. **The most used settings always first** (K1–K4) and a “FAVOURITES” page made of your 12 favourite settings.
6. **Fewer steps for common gestures**: A/B of presets on two keys, “lock the knobs” (OCT− + OCT+ held).
7. **Built-in help**: pressing a button twice shows one line saying what it does.
8. **Tutorial at the first start** (4 screens, skippable).

### Program (what changes in the firmware)
1. **Modulation at block rate** for everything that is not audible per sample (already done for the effects): generalise to slow LFOs and macros.
2. **Tables instead of calculation**: saturation curves, sine, wavefold, envelopes as Q15 tables (faster, more stable).
3. **Finer split of the two cores**: move chorus / phaser / delay to core 1 when it has room, measure each stage's real time and balance by itself.
4. **Smart voice stealing** and **economy mode**: switch off the least audible effects first when the load rises (today: reverb and chorus, then the voices).
5. **Draw the screen by changed zones** (already by 40 px bands): add a small cache of the fixed elements (grids, titles) to lighten the busiest pages (MORPH X/Y).
6. **Flash**: group the writes, limit erase cycles (settings 2 s after the last change, done), circular crash log.
7. **Tests**: compared screenshots to spot broken screens (like the ARP title), load test extended to FX PADS / MORPH / limiter, a 30-minute burn-in on the device.
8. **Measurement**: show in SYSTEM the maximum load over the last 10 seconds (not only the instant one) so you can tune without guessing.

## 10. Versions

- **0.9.19**: one firmware. The separate versions A (4 engines) and B (8 engines) are merged: `SYSTEM › ENGINES` picks **ESSENTIAL** (the first four: ANALOG, SUPER/REESE, WAVE, FM; the default) or **ALL** (eight). A sound keeps its own engine either way, and the factory presets use all eight.
