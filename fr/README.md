<p align="center"><img src="../docs/img/promo-fr.png" alt="K-WASUB, synthé de basses modernes pour le M-VAVE FM-1"></p>

# K-WASUB · FM1 modern Bass firmware

**English** : [README](../README.md) · **Français** : cette page · **Español** : [README](../es/README.md)

**Synthé de basses modernes pour le M-VAVE FM-1** : DnB, dub, dubstep, techno. Wobble en direct, reese, sub, 808, un EQ, un morph entre quatre sons, des effets sur les touches. Gratuit et libre (GPL-3.0). *Beta 0.9.*

| | |
|---|---|
| 🎛 **Essayer** (navigateur) | [`emulator/index.html`](../emulator/index.html?lang=fr)  |
| ⬇️ **Installer** sur le FM-1 | [`installer.html`](../installer.html) (Chrome ou Edge, USB) · ou `INSTALL-Windows.bat` / `INSTALL-Mac.command` / `INSTALL-Linux.sh` |
| 📖 **Manuel** illustré | [`manual.html`](manual.html) |
| 🏠 **Accueil** | [`index.html`](index.html) (si GitHub Pages est activé : <https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/>) |
| 🗺 **Cahier des charges** | [`CAHIER-DES-CHARGES.md`](CAHIER-DES-CHARGES.md) : fait, à faire, idées |
| 📜 Notes techniques | [`NOTES-TECHNIQUES.md`](NOTES-TECHNIQUES.md) |
| 🇪🇸 Espagnol | [`es/README.md`](../es/README.md) : le README en espagnol |

## Fonctions clés

1. **4 moteurs efficaces** pour des basses modernes, ou **8 moteurs** pour basses, pads et leads (`SYSTEM › ENGINES`).
2. **LFO learn** : `LFO` maintenu + n'importe quel potard, le LFO 2 se branche sur ce réglage en un geste.
3. Mode **CLASSIC** ou **SHIFT** (`OCT−` / `OCT+`) pour aller plus vite, au choix dans les options.
4. **Fenêtres SEL** : PERFORM, MORPH, FX LIVE, MACROS.
5. **Morph A/B** : fondu entre deux sons en direct.
6. Une **page LFO** en direct pour retravailler tes basses wobble en jouant.
7. **SEQ BASS** (jusqu'à 64 pas, probabilité, conditions de déclenchement et durée de note par pas, 30 presets, REC en direct), **DRUMS** (kits 808 / 909, 8 pistes colorées, presets de rythmes : techno, dub, dnb…), **ARP**, **MIDI**.
8. Le son : moteurs, filtres, effets, master, et **FX PADS**.
9. Visuels d'oscillateur animés, en direct.
10. Un **EQ** visuel.
11. Des **thèmes** complètement différents, pour s'adapter à ta façon de jouer.
12. **Luminosité**, contraste, polices et taille.
13. **Langue du firmware** (`SYSTEM › LANGUAGE`) : English, Français ou Español ; anglais par défaut.

## Installer

1. FM-1 en USB (câble **de données**), autres logiciels MIDI fermés.
2. Ouvrir [`installer.html`](../installer.html) dans Chrome ou Edge → « Installer K-WASUB ».
3. Les paquets sont dans [`install/`](../install/) (`k-wasub-X.fwsc`, anciens dans `install/older/`, sommes de contrôle dans `SHA256SUMS`).

Retour à KAWA (`install/kawa-0.5.fwsc`) ou au firmware officiel (M-UPGRADE) possible à tout moment ; `OCT−` maintenu à l'allumage = secours USB.

## Construire

```sh
cd source
./build.sh --release 0.9.53          # -> build/k-wasub-0.9.53.fwsc
APP_VER=0.9.53 bash web/make_emulator.sh      # émulateur
bash web/make_installer.sh                    # installer.html avec le dernier paquet
bash tests/run_stress.sh                      # tests de charge (UBSan)
python3 tests/manual_shots.py                 # captures du manuel (docs/img)
```
Toolchain JieLi et SDK AC79 : voir `source/BUILDING.md` et `source/tools/get_toolchain.sh`.

## Crédits et licence

☕ **Soutenir** : [ko-fi.com/omnipotard](https://ko-fi.com/omnipotard)

GPL-3.0. K-WASUB est né de [KAWA](https://github.com/Guizmoh/Kawa-Tracker-Fm1) (Omnipotard / Leo Kuroshita, Hügelton Instruments), dont il reprend la plate-forme du FM-1 (démarrage, USB, audio, écran). Voir [`LICENSING.md`](../LICENSING.md). Non affilié à M-VAVE.
