# K-WASUB · Notes techniques

Pour le guide d'utilisation, voir le [manuel](manual.html). Ces notes sont pour celles et ceux qui construisent, testent ou modifient le firmware.
(English version: [`docs/TECHNICAL-NOTES.md`](../docs/TECHNICAL-NOTES.md).)

## La machine

M-VAVE FM-1 : JieLi AC79, deux cœurs, pas de FPU, code exécuté depuis la flash. Règles suivies :
- uniquement des entiers (virgule fixe Q15 / Q24) ; pas de division 64 bits (la multiplication 64 bits est permise) ;
- l'interruption audio tourne tous les 256 échantillons (5,8 ms) et doit rester courte ;
- une écriture en flash arrête le son quelques dizaines de ms : les réglages sont écrits 2 s après le dernier changement, et seulement en silence ; le cœur 1 attend alors dans une boucle en RAM ;
- mémoire : RAM environ 54 Ko sur 96, pool 330 Ko sur 344 (dont 44 Ko pour le tampon RESAMPLE), image environ 500 Ko sur 581.

## Deux cœurs : désactivés depuis la 0.9.52

L'AC79 est une puce à deux cœurs, et le code qui répartit les voix sur un second cœur vit toujours dans
`ksub_dsp.c` (`#if KS_DUAL`), mais `KS_DUAL` vaut 0 : un rapport de plantage pointait vers le second cœur,
et `SYSTEM › AUDIO CORES` a disparu (il n'y a plus rien à choisir). Les notes ci-dessous décrivent ce code
tel qu'il était, gardées parce que la logique de repli / sécurité qu'il utilisait (cœur 1 silencieux, trop
lent, une écriture flash) façonne toujours le chemin à un seul cœur de `voices_render`.

- **cœur 1** : les voix (oscillateurs, filtre, enveloppes, LFO, matrice) du bloc suivant, dans `vbus` ;
- **cœur 0** : l'interruption audio, les effets du bloc en cours, l'écran, les boutons, le MIDI et l'USB.

Il y a un bloc de latence (5,8 ms). Le démarrage du cœur 1 suit la séquence du SDK JieLi (`EnableOtherCpu`, `cpu1_start`, voir `source/firmware/hal/fm1_cpu1.h`), avec des sécurités :
- si le cœur 1 ne répond pas, tout tourne sur le cœur 0 (même son) ;
- s'il ne suit pas (6 blocs en retard ou coupés sur les 32 derniers, environ 0,2 s), le cœur 0 reprend les voix, `CORE 1 TOO SLOW: 1 CORE` s'affiche ; pour cette session seulement (0.9.52 : le démarrage suivant réessaie deux cœurs) ;
- si le FM-1 plante (crash, watchdog, tension basse) dans les 10 s d'un démarrage à deux cœurs, le démarrage suivant se fait sur un seul cœur ; `SYSTEM › AUDIO CORES` permet de réessayer (0.9.52 : une extinction ou un redémarrage voulu ne compte plus) ;
- `SYSTEM › AUDIO CORES` dit pourquoi les deux cœurs ne tournent pas : `AT NEXT START`, `CORE 1 SILENT` (pas de réponse au démarrage), `STOPPED: TOO SLOW`, `STOPPED: FLASH` (il n'a pas attendu une écriture flash), `SAFE (CRASH)` ; l'écran de démarrage aussi ;
- avant une mise à jour, le mode UBOOT ou un plantage, le cœur 1 est remis en reset.

## Charge et stabilité

- **Gouverneur** : un bloc au-dessus de 70 % deux fois de suite (ou au-dessus de 92 % une fois) allège le son d'un cran : 1 reverb et chorus coupés, 2 deux voix et 3 dents de scie par SUPER, 3 une voix et 2 dents de scie. Deux secondes sous 45 % ramènent d'un cran. `CPU LOAD` affiche `· -1`, `-2` ou `-3`.
- **Budget audio** : le temps des effets est mesuré à chaque bloc, et les voix reçoivent ce qui reste de 80 % du bloc (au moins un quart) ; l'attente du cœur 0 sur le cœur 1 est limitée à un demi-bloc. Sans cela, une chaîne d'effets lourde pouvait affamer la boucle principale, le chien de garde (environ 8 s, nourri par la boucle principale) se déclenchait et le FM-1 redémarrait (on aurait dit qu'il s'éteignait).
- **LAST STOP** : la source du reset (`fm1_boot.p3_rst` : mise sous tension, tension basse, watchdog, appui long, 1,2 V, soft) et une marque de plantage gardée en `.noinit` (adresse de la faute) sont lues au démarrage, affichées en orange sur l'écran de démarrage et dans `SYSTEM`.
- **Étage de sortie** (cœur 0, fin de `fx_render`) : multibande optionnel (3 bandes, coupures à un pôle à 120 Hz et 2,5 kHz, gains au rythme du bloc), mono bass (deux passe-bas à un pôle, 60–200 Hz), shelf DEEP BASS (environ 90 Hz), gain glue, retrait du continu, AUTO LEVEL (gain au rythme du bloc vers un niveau moyen de 8000, x0,5 .. x2,5, monte en 3 s environ, descend en 0,7 s environ, immobile sous une moyenne de 600), volume master, limiteur (attaque immédiate sous un plafond de 29000, relâchement d'environ 50 ms), écrêtage doux.

## Patchs et stockage

- Un patch a 138 paramètres (`NP`, 0.9.55 : `SM_START`, `SM_END`, `SM_DIR` d'OSC C), 140 au maximum (`NP_MAX`). Un emplacement utilisateur garde `NP_STORE` = 112 octets dans le premier secteur de flash et le reste dans `uext` (28 octets par emplacement) dans le second secteur, à `UX_AT` (0x400), après `perf` (SEQ BASS, ARP, MACROS, table des CC MIDI, EQ, choix du MORPH). Des static asserts gardent `perf` sous `UX_AT` et `uext` dans le secteur.
- `UX_MAGIC` marque la disposition (0x58 : 16 octets par emplacement, 0x59 : 20, 0x5A : 28) ; `ux_migrate` convertit les anciennes et donne aux nouveaux paramètres leur valeur par défaut.
- Les 48 pas au-delà de 16 de chaque pattern SEQ BASS (`sqx`) occupent le troisième secteur ; la batterie DRUMS (`dk` : 8 patterns jusqu'à 64 pas, le kit, les sons des pistes) les quatrième et cinquième (0x9A000–0x9BFFF, `STORE_HI` 0x9C000), avec un magic et une somme (`dk_mark`). L'octet `cond` d'un pas : la condition dans le quartet bas, la durée de note (`SQ_GL`, 0 = demi-pas comme avant, 15 = HOLD) dans le quartet haut. La chance d'un pas de batterie (`DK_PROB`) est le quartet haut de `pc`, sa condition le bas. La batterie est synthétisée (`dk_start` / `dk_voice`, sans échantillons ; quatre kits, `DK_TMIN` / `DK_TRIM` par kit ; DUB TECHNO envoie caisse claire, clap, toms, accord et charley ouvert (`DK_SEND`) dans son propre écho, `dk_echo` : une croche pointée à 11 kHz dans un tampon de 6144 échantillons, filtrée et qui s'éteint) et mixée après AUTO LEVEL, avant MASTER et le limiteur ; les coups tombent sur le bloc de 16 échantillons (`sq_at`) du pas.
- PARAMETER LOCKS (0.9.57) : une liste `pl` de 512 `{pat, step, tp, v}` (pat : un pattern de batterie 0..7 ou `PL_BASS` | le pattern SEQ BASS ; tp : la piste << 4 | quoi), sur le 6e secteur du store (`STORE_HI` 0x9D000), dans la sauvegarde USB après dk (une sauvegarde sans elle, plus courte de 2052 octets, se recharge encore). Le son la lit quand un pas joue : `dk_step_on` remplit `dk_lkm` / `dk_lkv` pour les pistes qui frappent (`dk_start` les prend à la place de `dk.prm` ; RATCHET relance 1 à 4 fois dans le pas, `dk_rn` / `dk_rc` ; ECHO remplace `DK_SEND`), `seq_step_on` remplit `sq_lkm` / `sq_lkv` pour la note, que `LKB()` met à la place de `F_CUT`, `F_RES`, `F_ENV`, `F_DRV`, `L1_DIV` du LFO 1, `A_P1` et `SM_START` jusqu'à la note suivante. REC reste actif dans toutes les vues pendant la lecture ; un réglage SEQ BASS tourné alors est verrouillé sur `sq_now_step()` au lieu de changer le patch.
- AUTOMATION (0.9.59) : dans la même liste `pl`, pat `PL_AUTO` | le pattern SEQ BASS, tp un paramètre du patch (0..137). REC maintenu pendant la lecture (son action longue est alors nulle, pas de PANIC) : un potard enregistre le réglage qu'il bouge sur `sq_now_step()` (`aut_turn`) ; la boucle principale (`aut_play`) écrit les valeurs du pas dans `patch` quand SEQ BASS y arrive, en gardant la valeur propre de chaque réglage touché (`aut_base`, mise à jour aussi par un réglage à la main) et la remet au STOP. REC maintenu seul 400 ms : `aut_erasing`, les pas traversés perdent leur automation.
- Audio USB (`usb.c`, UAC1, de Felucca / SLOOP / KAWA) : l'anneau est rempli à la fin d'un rendu pendant que TIMER5 envoie un paquet par ms, donc son point bas est le remplissage au début du rendu moins un rendu entier. Les rendus de K-WASUB sont longs : la 0.9.56 tient le remplissage entre 272 et 330 trames (48 kHz : 296..359) dans un anneau de 1024 au lieu de 80..128 dans 512 pour KAWA (~7 ms de latence en plus).
- SYNC OUT (`set.sync`, `ks_sync`) : pendant la lecture, une impulsion de 2,5 ms à chaque croche de `ks_beats` à gauche (amplitude relevée contre le potard MASTER, appliqué après par la plateforme), le son en mono à droite : synchro Pocket Operator / Volca, 2 impulsions par temps.
- Les réglages (`set`) tiennent dans un secteur avec un CRC ; on n'ajoute des champs qu'à la fin, et les anciennes sauvegardes se chargent avec les nouveaux champs à leur défaut (voir la liste `LEN` dans `app_init`).
- Les identifiants d'items sont des `uint8_t` (`I_L1RATE` = 140 …, 136 avant la 0.9.55) ; des static asserts les gardent sous 255 (`ids_fit`) et le patch en dessous (`np_fits`). MIDI LEARN stocke des identifiants d'items : une table de CC enregistrée avant la 0.9.55 (`cc_magic` 0x43) voit ses identifiants à partir de 136 décalés de 4 au chargement (0x44).
- Les samples d'OSC C : SAMPLE garde 16 pour RESAMPLE ; les samples ajoutés en 0.9.55 sont 17–28 (`sm_desc`), le potard les parcourt dans l'ordre avec RESAMPLE en dernier. Une voix lit son sample entre START et END dans un sens ou l'autre (`sm_adv`) ; à toute SPEED autre que 100 %, deux grains lisent à la hauteur pendant que la lecture avance plus lentement ou plus vite (jusqu'à 4x).
- Les destinations sont enregistrées dans les patchs : on n'ajoute qu'à la fin (`D_MORPHX/Y/MORPH` viennent après celles du phaser).

## Couche sample

OSC C joue des sons µ-law 8 bits depuis la flash (`KS_SMP`, 10 sons à 22,05 kHz et 5 textures à 11,025 kHz, tous générés par `source/tools/gen_ksub.py`). Le sample 16 est **RESAMPLE** : la sortie finale, 4 échantillons moyennés, encodée en µ-law par recherche dans `KS_MULAW`, dans un tampon RAM de 44 100 octets (4 s à 11,025 kHz), rejoué avec le même code de vitesse / grains. Il est perdu à l'extinction.

## Lien Données (sauvegarde, WAV, samples)

`firmware/src/ksub_link.c` répond à des trames SysEx sur le port USB-MIDI de l'installateur : `F0 7D 4B 57 cmd pack7(corps) F7` (réponse : `cmd | 0x40`). HELLO, READ / BEGIN / WRITE / COMMIT pour la sauvegarde (`KSB1` + les tailles des emplacements, du bloc performance et de l'extension, puis les trois ; CRC16 vérifié, écrit en flash depuis la boucle principale), RS INFO / RS READ / MULAW pour l'enregistrement RESAMPLE (µ-law, 11 025 Hz), SMP BEGIN / WRITE / DONE pour un sample dans la même RAM (OSC C le joue jusqu'à l'extinction). `web/kwlink.js` est le côté ordinateur (Web MIDI, ou les exports `ksub_link_*` de l'émulateur) ; `data.html` est la page.

## Construire

```sh
cd source
./build.sh --release 1.0.43                 # build/k-wasub-1.0.43.fwsc   (X.Y, X.Y.Z ou X.Y.Z-suffixe ; identité FM-1_97Y pour 0.Y, FM-1_1990 pour 1.Y (depuis 1.0.43))
APP_VER=1.0.43 bash web/make_emulator.sh    # ../emulator/index.html  
sh web/make_data.sh                         # ../data.html (sauvegarde, export WAV, samples)
node tests/link.mjs                         # le lien Données contre l'émulateur
bash web/make_installer.sh                  # ../installer.html avec le dernier install/k-wasub-*.fwsc
bash tests/run_stress.sh                    # 13 000 essais de réglages sous UBSan
python3 tests/manual_shots.py               # tous les écrans du manuel -> docs/img
```
Toolchain et SDK : voir [`source/BUILDING.md`](../source/BUILDING.md). La construction vérifie la carte mémoire, qu'aucune adresse de registre n'apparaît hors de `hal/`, et que le paquet tient dans les limites du chargeur.

## Tests

`tests/run_stress.sh` fait jouer des réglages aléatoires de chaque paramètre (et des nouveaux étages master) sous UBSan et échoue au moindre débordement d'entier ou bloc en retard. `tests/levels.mjs` joue chaque preset d'usine et affiche crête, RMS, écrêtage et continu. `tests/shots.mjs` pilote l'émulateur par un script (`btn`, `down`, `up`, `on`, `off`, `enc`, `midi`, `shot`) et écrit des écrans et un WAV.
