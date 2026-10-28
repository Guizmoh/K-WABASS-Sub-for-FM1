<p align="center"><img src="../docs/img/promo-fr.png" alt="K-WASUB, synthé de basses modernes pour le M-VAVE FM-1"></p>
<p align="center"><a href="https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/">https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/</a></p>

# K-WASUB · FM1 modern Bass firmware

**English** : [README](../README.md) · **Français** : cette page · **Español** : [README](../es/README.md)

**Synthé de basses modernes pour le M-VAVE FM-1** : DnB, dub, dubstep, techno. Wobble en direct, reese, sub, 808, un EQ, un morph entre quatre sons, des effets sur les touches. Gratuit et libre (GPL-3.0). *Version 1.0.45 **BÊTA** : testée dans l'émulateur et par des tests automatiques, pas encore sur tous les FM-1 ; dis-moi ce que tu vois (onglet Issues).*

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

1. **9 moteurs** par oscillateur (ANALOG, **808**, CS, WAVETABLE, **FM 4 opérateurs**, **GROWL**, **ADDITIVE**, PHASE DIST, HARD SYNC), chacun avec un 4e réglage : **FOLD** (CS : **RING**, 808 : **CLICK**, FM : **ALGO**, 8 façons de brancher les opérateurs).
2. **Séquenceur de batterie avec conditions & parameter locks** (sur la basse aussi : maintenir un pas, tourner un potard) et **automation** (maintenir REC pendant la lecture et tourner n'importe quel potard ; REC maintenu seul pour effacer) : 8 pistes colorées (kits 808, 909, dub techno, acoustique), chance et conditions sur chaque pas, touches noires pour l'instrument, touches blanches (pads) pour ses pas, OCT−/OCT+ pour les pages ; REC en direct ; sortie sync pour Pocket Operator et Volca.
3. **LFO learn** : `LFO` maintenu + n'importe quel potard, le LFO 2 se branche sur ce réglage en un geste (avec `OCT−` : LFO 1, avec `OCT+` : LFO 3).
4. Mode **CLASSIC** ou **SHIFT** (`OCT−` / `OCT+`) pour aller plus vite, au choix dans les options.
5. **Fenêtres SEL** : PERFORM, MORPH, FX LIVE, MACROS.
6. **Morph A/B** : fondu entre deux sons en direct.
7. **Trois LFO** (le troisième global : il reste quand tu changes de son) et une **page LFO** en direct pour retravailler tes basses wobble en jouant.
8. **SEQ BASS** (jusqu'à 64 pas, probabilité, conditions de déclenchement et durée de note par pas, 30 presets, REC en direct), samples **OSC C** (attaques, textures ; début / fin coupés, plus rapide ou plus lent, inversé, ping-pong), **DRUMS** (kits 808 / 909 / dub techno / acoustique, 8 pistes colorées, presets de rythmes : techno, dub, dnb…), **ARP**, **MIDI**.
9. Le son : moteurs, filtres, effets, master, et **FX PADS**.
10. Visuels d'oscillateur animés, en direct.
11. Un **EQ** visuel.
12. Des **thèmes** complètement différents, pour s'adapter à ta façon de jouer.
13. **Luminosité**, contraste, polices et taille.
14. **Langue du firmware** (`SYSTEM › LANGUAGE`) : English, Français ou Español ; anglais par défaut.

## Installer

1. FM-1 en USB (câble **de données**), autres logiciels MIDI fermés.
2. Ouvrir [`installer.html`](../installer.html) dans Chrome ou Edge → « Installer K-WASUB ».
3. Les paquets sont dans [`install/`](../install/) (`k-wasub-X.fwsc`, anciens dans `install/older/`, sommes de contrôle dans `SHA256SUMS`).

Retour à KAWA (`install/kawa-0.5.fwsc`) ou au firmware officiel (M-UPGRADE) possible à tout moment ; `OCT−` maintenu à l'allumage = secours USB.

## Construire

```sh
cd source
./build.sh --release 1.0.45          # -> build/k-wasub-1.0.45.fwsc
APP_VER=1.0.45 bash web/make_emulator.sh      # émulateur
bash web/make_installer.sh                    # installer.html avec le dernier paquet
bash tests/run_stress.sh                      # tests de charge (UBSan)
python3 tests/manual_shots.py                 # captures du manuel (docs/img)
```
Toolchain JieLi et SDK AC79 : voir `source/BUILDING.md` et `source/tools/get_toolchain.sh`.

## Crédits et licence

☕ **Soutenir** : [ko-fi.com/omnipotard](https://ko-fi.com/omnipotard)

GPL-3.0. K-WASUB est né de [KAWA](https://github.com/Guizmoh/Kawa-Tracker-Fm1) (Omnipotard / Leo Kuroshita, Hügelton Instruments), dont il reprend la plate-forme du FM-1 (démarrage, USB, audio, écran). Voir [`LICENSING.md`](../LICENSING.md). Non affilié à M-VAVE.
