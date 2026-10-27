# K-WASUB · Technical notes

For the user guide see the [manual](../manual.html). These notes are for people who build, test or modify the firmware.
(Version française : [`fr/NOTES-TECHNIQUES.md`](../fr/NOTES-TECHNIQUES.md).)

## The machine

M-VAVE FM-1: JieLi AC79, two cores, no FPU, code run in place from flash. Rules the code follows:
- integers only (Q15 / Q24 fixed point); no 64-bit division (64-bit multiplication is fine);
- the audio interrupt runs every 256 frames (5.8 ms) and must stay short;
- a flash write stops the sound for a few tens of ms, so settings are written 2 s after the last change and only in silence; core 1 then waits in a RAM loop;
- memory: RAM about 54 KB of 96, pool 330 KB of 344 (the RESAMPLE buffer is 44 KB of it), image about 500 KB of 581.

## Two cores: off since 0.9.52

The AC79 is a two-core chip, and the code to split the voices onto a second core still lives in `ksub_dsp.c`
(`#if KS_DUAL`), but `KS_DUAL` is 0: a crash report pointed at the second core, and `SYSTEM › AUDIO CORES`
is gone (there is nothing left to switch). The notes below describe that code as it stood, kept because the
fallback / safeguard logic it used (core 1 silent, too slow, a flash write) still shapes `voices_render`'s single-core path.

- **core 1**: the voices (oscillators, filter, envelopes, LFOs, matrix) of the next block, into `vbus`;
- **core 0**: the audio interrupt, the effects of the current block, the screen, buttons, MIDI and USB.

There is one block of latency (5.8 ms). The start of core 1 follows the JieLi SDK sequence (`EnableOtherCpu`, `cpu1_start`; see `source/firmware/hal/fm1_cpu1.h`) with safeguards:
- if core 1 does not answer, everything runs on core 0 (same sound);
- if core 1 cannot keep up (6 late or cut blocks out of the last 32, about 0.2 s), core 0 takes the voices back, `CORE 1 TOO SLOW: 1 CORE` shows; for this session only (0.9.52: the next start tries two cores again);
- if the FM-1 crashes (crash, watchdog, low voltage) within 10 s of a two-core start, the next start uses one core; `SYSTEM › AUDIO CORES` lets you try again (0.9.52: a power off or a restart asked for no longer counts);
- `SYSTEM › AUDIO CORES` says why two cores do not run: `AT NEXT START`, `CORE 1 SILENT` (it did not answer at the start), `STOPPED: TOO SLOW`, `STOPPED: FLASH` (it did not wait for a flash write), `SAFE (CRASH)`; the start screen too;
- before an update, UBOOT mode or a crash, core 1 is put back in reset.

## Load and stability

- **Governor**: a block over 70 % twice in a row (or over 92 % once) thins the sound out one step: 1 reverb and chorus off, 2 two voices and 3 saws per SUPER, 3 one voice and 2 saws. Two seconds under 45 % brings a step back. `CPU LOAD` shows `· -1`, `-2` or `-3`.
- **Audio budget**: the effects' time is measured every block, and the voices get what is left of 80 % of the block (at least a quarter); core 0's wait for core 1 is capped at half a block. Without this, a heavy effect chain could starve the main loop, the watchdog (about 8 s, fed from the main loop) would fire, and the FM-1 would restart (it looked like switching off).
- **LAST STOP**: the reset source (`fm1_boot.p3_rst`: power-on, low voltage, watchdog, long press, 1.2 V, soft) and a crash mark kept in `.noinit` (address of the fault) are read at start-up, shown in orange on the start screen and in `SYSTEM`.
- **Output stage** (core 0, end of `fx_render`): optional multiband (3 bands, one-pole splits at 120 Hz and 2.5 kHz, block-rate gains), mono bass (two one-pole low-passes, 60–200 Hz), DEEP BASS shelf (about 90 Hz), glue gain, DC removal, AUTO LEVEL (block-rate gain toward a mean level of 8000, x0.5 .. x2.5, up in about 3 s, down in about 0.7 s, still below a mean of 600), master volume, limiter (instant attack under a 29000 ceiling, about 50 ms release), soft clip.

## Patches and storage

- A patch has 138 parameters (`NP`, 0.9.55: OSC C's `SM_START`, `SM_END`, `SM_DIR`), 140 at most (`NP_MAX`). A user slot keeps `NP_STORE` = 112 bytes in the first flash sector and the rest in `uext` (28 bytes a slot) in the second sector, at `UX_AT` (0x400), after `perf` (SEQ BASS, ARP, MACROS, MIDI CC map, EQ, MORPH choices). Static asserts keep `perf` under `UX_AT` and `uext` inside the sector.
- `UX_MAGIC` marks the layout (0x58: 16 bytes a slot, 0x59: 20, 0x5A: 28); `ux_migrate` converts older ones and gives new parameters their defaults.
- The 48 steps past 16 of each SEQ BASS pattern (`sqx`) take the third sector; the DRUMS (`dk`: 8 patterns of up to 64 steps, the kit, the track sounds) the fourth and fifth (0x9A000–0x9BFFF, `STORE_HI` 0x9C000), with a magic and a sum (`dk_mark`). A step's `cond` byte: the trig condition in its low nibble, the note length (`SQ_GL`, 0 = half a step as before, 15 = HOLD) in its high nibble. A drum step's chance (`DK_PROB`) is the high nibble of `pc`, its condition the low one. The drums are synthesised (`dk_start` / `dk_voice`, no samples; four kits, `DK_TMIN` / `DK_TRIM` per kit; DUB TECHNO sends snare, clap, toms, chord and open hats (`DK_SEND`) to its own echo, `dk_echo`: a dotted eighth at 11 kHz in a 6144-sample buffer, low-passed and fading) and mixed after AUTO LEVEL, before MASTER and the limiter; hits are placed at the 16-sample chunk (`sq_at`) where the step falls.
- PARAMETER LOCKS (0.9.57): one list `pl` of 512 `{pat, step, tp, v}` (pat: a drum pattern 0..7 or `PL_BASS` | the SEQ BASS pattern; tp: the track << 4 | what), on the store's 6th sector (`STORE_HI` 0x9D000), in the data-link backup after dk (a backup without it, 2052 bytes shorter, still restores). The sound reads it when a step plays: `dk_step_on` fills `dk_lkm` / `dk_lkv` for the tracks hitting (`dk_start` takes them instead of `dk.prm`; RATCHET re-triggers 1..4 times through the step, `dk_rn` / `dk_rc`; ECHO replaces `DK_SEND`), `seq_step_on` fills `sq_lkm` / `sq_lkv` for the note, which `LKB()` puts in place of `F_CUT`, `F_RES`, `F_ENV`, `F_DRV`, LFO 1's `L1_DIV`, `A_P1` and `SM_START` until the next note. REC stays on in every view while it plays; a SEQ BASS setting turned then is locked on `sq_now_step()` instead of changing the patch.
- AUTOMATION (0.9.59): in the same list `pl`, pat `PL_AUTO` | the SEQ BASS pattern, tp a patch parameter (0..137). REC held while it plays (its hold action is then none, no PANIC): a knob records the setting it moves on `sq_now_step()` (`aut_turn`); the main loop (`aut_play`) writes the step's values into `patch` when SEQ BASS moves to it, keeping each touched setting's own value (`aut_base`, also updated by a hand turn) and putting it back at STOP. REC held alone 400 ms: `aut_erasing`, the steps passed lose their automation.
- USB audio (`usb.c`, UAC1, from Felucca / SLOOP / KAWA): the ring is fed once a render ends while TIMER5 keeps sending a packet a ms, so its low point is the fill at render start minus a whole render. K-WASUB's renders are long, so 0.9.56 holds the fill at 272..330 frames (48 kHz: 296..359) in a 1024-frame ring instead of KAWA's 80..128 in 512 (~7 ms more latency).
- SYNC OUT (`set.sync`, `ks_sync`): while the sequencers play, a 2.5 ms pulse at each eighth of `ks_beats` on the left (amplitude raised against the MASTER knob, which the platform applies after), the sound in mono on the right: Pocket Operator / Volca sync, 2 pulses a beat.
- Settings (`set`) are one sector with a CRC; fields are only ever appended, and older saves load with the new fields at their defaults (see the `LEN` list in `app_init`).
- Item ids are `uint8_t` (`I_L1RATE` = 140 …, 136 before 0.9.55); static asserts keep them under 255 (`ids_fit`) and the patch under them (`np_fits`). MIDI LEARN stores item ids: a CC map saved before 0.9.55 (`cc_magic` 0x43) has its ids from 136 moved up 4 when loaded (0x44).
- OSC C's samples: SAMPLE keeps 16 for RESAMPLE; the samples added in 0.9.55 are 17–28 (`sm_desc`), the knob steps through them in order with RESAMPLE last. A voice reads its sample between START and END in either direction (`sm_adv`); at any SPEED but 100 % two grains read at the pitch while the play moves slower or faster (up to 4x).
- Destinations are stored in patches: append only (`D_MORPHX/Y/MORPH` come after the phaser's).

## Sample layer

OSC C plays 8-bit mu-law sounds from flash (`KS_SMP`, 10 sounds at 22.05 kHz and 5 textures at 11.025 kHz, all generated by `source/tools/gen_ksub.py`). Sample 16 is **RESAMPLE**: the final output, 4 samples averaged, mu-law encoded by a search in `KS_MULAW`, into a 44 100-byte RAM buffer (4 s at 11.025 kHz), played back with the same speed / grain code. It is lost at power-off.

## Data link (backup, WAV, samples)

`firmware/src/ksub_link.c` answers SysEx frames on the updater's USB-MIDI port: `F0 7D 4B 57 cmd pack7(body) F7` (answer: `cmd | 0x40`). HELLO, READ / BEGIN / WRITE / COMMIT for the backup (`KSB1` + the sizes of the user slots, the performance block and the slots' extension, then the three; CRC16 checked, written to the flash from the main loop), RS INFO / RS READ / MULAW for the RESAMPLE recording (µ-law, 11 025 Hz), SMP BEGIN / WRITE / DONE for a sample into the same RAM (OSC C plays it until power-off). `web/kwlink.js` is the host side (Web MIDI, or the emulator's exports `ksub_link_*`); `data.html` is the page.

## Build

```sh
cd source
./build.sh --release 1.0.17                 # build/k-wasub-1.0.17.fwsc   (X.Y, X.Y.Z or X.Y.Z-suffix; identity FM-1_97Y for 0.Y, FM-1_98Y for 1.Y)
APP_VER=1.0.17 bash web/make_emulator.sh    # ../emulator/index.html  
bash web/make_installer.sh                  # ../installer.html with the newest install/k-wasub-*.fwsc
sh web/make_data.sh                         # ../data.html (backup, WAV export, samples) with web/kwlink.js
node tests/link.mjs                         # the Data link against the emulator
bash tests/run_stress.sh                    # 13 000 parameter runs under UBSan
python3 tests/manual_shots.py               # every screen of the manual -> docs/img
python3 tools/make_manual.py                # (from the repo root) manual.html and fr/manual.html, short, from one text
```
Toolchain and SDK: see [`source/BUILDING.md`](../source/BUILDING.md). The build checks the memory map, that no register address appears outside `hal/`, and that the package fits the loader's limits.

## Tests

`tests/run_stress.sh` renders random settings of every parameter (and the new master stages) under UBSan and fails on any integer overflow or late block. `tests/levels.mjs` plays every factory preset and prints peak, RMS, clipping and DC. `tests/shots.mjs` drives the emulator with a script (`btn`, `down`, `up`, `on`, `off`, `enc`, `midi`, `shot`) and writes screens and a WAV.
