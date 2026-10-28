# K-WASUB · Cahier des charges

[English](../SPECIFICATIONS.md) · **Français**

Synthé de basses modernes pour le M-VAVE FM-1 (JieLi AC79, deux cœurs, sans FPU). Dernière mise à jour : **1.0.44 (BÊTA)**, testée dans l’émulateur et par des tests automatiques, pas encore sur tous les FM-1 (le détail des versions récentes est dans SPECIFICATIONS.md).
Ce document dit où en est le projet : ce qui est fait, ce qui est à vérifier, ce qui reste, et des idées pour aller plus loin.

## 1. Vision

- **Pour qui** : celles et ceux qui font de la DnB, du dub, du dubstep, de la techno et veulent une basse qui bouge, jouable à deux mains sur un appareil de poche.
- **Promesse** : un wobble qu'on module en direct, des basses profondes et propres, un son complet sans plugin, une interface lisible.
- **Principes** : simple à jouer, complet à régler ; rien ne bloque l'audio ; tout est gratuit et libre ; chaque écran dit ce qu'il fait ; on ne retire pas une fonction sans le dire.

## 2. Fait

### Son
| Domaine | Détail | Version |
|---|---|---|
| Moteurs | 9 moteurs par oscillateur (analog, 808 / kick bass (1.0.27), CS, wavetable, FM 4 opérateurs à 8 algorithmes (1.0.28), GROWL et ADDITIVE (1.0.29), phase dist, hard sync), chacun avec un 4e réglage (FOLD ; CS : RING, 808 : CLICK, FM : ALGO, GROWL : TYPE, ADDITIVE : REGISTER) ; SUPER, WAVEFOLDER et VOCAL retirés en 1.0.26 | 1.0.26 |
| Oscillateurs | A + B (ADD, RING, X-MOD, SYNC), sub, bruit, **OSC C sample** (10 sons, 5 textures, boucle / une fois, vitesse) | 0.9.9-4 |
| Filtre | 7 caractères (LP24, LP12, BAND, HIGH, NOTCH, VOWEL, COMB), drive, mod par enveloppe, clavier, vélocité | ≤ 0.9 |
| Modulation | 3 enveloppes, 3 LFO calés sur le tempo (le 3e global, quel que soit le patch) (grille ronde en option), STEP FX (16 motifs), matrice 4 slots, 4 MACROS × 4 cibles | ≤ 0.9 |
| Effets | Saturation, compresseur + PUMP, bitcrush, chorus, phaser, delay (4 types), reverb (4 types), glue, sub boost, **EQ 4 bandes** | 0.9.3 → 0.9.9-3 |
| Master | **DEEP BASS** (shelf +4 / +7 dB sous 90 Hz), **limiteur toujours actif**, **AUTO LEVEL** (normaliseur) | 0.9.10 |
| Voix | Mono, legato, poly 4, glide avec durée | ≤ 0.9 |
| Presets | 96 sons d'usine par style, 32 emplacements utilisateur, favoris, UNDO / REDO | ≤ 0.9 |
| SEQ / ARP / MIDI | SEQ BASS (16 patterns jusqu'à 64 pas, probabilité et conditions de déclenchement par pas, 0.9.47), ARP (5 modes), MIDI : learn, clock in/out, start/stop, program change | ≤ 0.9.8 |

### Jeu et workflow
| Domaine | Détail | Version |
|---|---|---|
| Modes | CLASSIC (listes) et SHIFT (3 colonnes, OCT−/OCT+ = Shift) ; K1–K4 = les 4 premières lignes ; accélération des potards | ≤ 0.9.7 |
| Fenêtres SEL | FX LIVE, MACROS, **MORPH X/Y**, **MORPH A/B** | 0.9.9-6 → 7 |
| **FX PADS** | FX maintenu : touches blanches = vitesse du wobble (4 8 16 24 32 48, 1/2, 1 bar), profondeur, forme ; noires = 4 stutters, tape stop, DJ filter, pump, saturation, phaser, crush | 0.9.10 |
| Appuis longs | OCT− UNDO, OCT+ REDO, SAVE UNDO/REDO, HOME PANIC, GLO CLASSIC/SHIFT, FX FX PADS, SEL A/B, PLAY HOLD, LFO/ENV assignation rapide, page = aléatoire contrôlé | 0.9.10 |
| Retours visuels | Valeur en grand avec l'ancienne, barres de modulation, barre de chargement des appuis longs, liste de destinations déroulante | ≤ 0.9.8 |
| Démarrage | Écran avec **le FM-1 de face** (touches allumées), plus de question à chaque démarrage | 0.9.10 |

### Ajouté en 0.9.11
| Domaine | Détail |
|---|---|
| Son | **MULTIBAND / OTT** 3 bandes (par son) ; **MONO BASS** réglable (60–200 Hz) ; **SUB LOCK** (sub = OSC A plus bas, en phase) |
| Resample | La sortie 2 à 4 s (11 kHz, µ-law, RAM) dans OSC C, puis boucle / once / speed / clavier |
| Live | Fenêtre **PERFORM** : 4 macros nommées, morph X/Y, wobble, pads sur OCT+ maintenu ; MORPH X/Y : même son aux 4 coins (tel quel, cutoff ¼ res ¾, wobble 1/8, wobble 1/16) |
| Presets | **Tags** (SUB, REESE, GROWL, WOBBLE, PLUCK, 808, DRONE) déduits des réglages, filtre sur K4 ; changement de preset immédiat (sans question), seulement sur HOME et PRESETS |
| Navigation | Chaque bouton ouvre la première vue de sa page ; vues et lignes réordonnées par importance (EDIT, FX, SYSTEM, SEL, SHIFT FX) ; aides K1–K4 au bas de chaque écran (forme courte si besoin) ; CLASSIC/SHIFT demandé au premier lancement seulement |
| Thème | Palette **FLUO** (vert fluo sur noir) |

### Langues (0.9.13 et après)
Tout est en anglais par défaut ; l'accueil, le manuel, le README, le cahier des charges et les notes existent aussi en français dans `fr/` ; l'émulateur et l'installateur basculent avec `?lang=fr`.

### Interface
6 thèmes dont **CLASSIC GLOW** (dégradés, vert fluo, 0.9.12) et **TECH** (image sur presque toute la page, 0.9.13), **BRIGHTNESS** ECO / NORMAL / BRIGHT / MAX (0.9.13), 19 palettes (dont INVERTED gris, RED, ICE, FLUO, PINK, GOLD), 4 polices, LOUPE, **CONTRAST** HIGH / MAX, visuels partout (ondes, enveloppes avec point, wavetable, opérateurs FM, EQ…).

### Stabilité et outillage
Gouverneur de charge ; budget audio mesuré pour les effets (le watchdog ne voit plus l'audio bloquer) ; repli sur un cœur ; **LAST STOP** (watchdog, tension basse, plantage + adresse) ; tests de charge automatiques (UBSan, A et B) ; émulateur web A et B ; installateur en une page ; build autonome.

## 3. À vérifier sur un vrai FM-1

Rien n'a encore été essayé sur l'appareil depuis 0.9.9-4. À regarder en premier :

1. **Mode 2 cœurs** : du son ? `SYSTEM › CPU LOAD` en jouant WIDE REESE en POLY avec effets ?
2. **Extinctions** : si le FM-1 s'éteint encore, noter `LAST STOP` au redémarrage (et l'adresse si CRASH).
3. **Contraste** HIGH et MAX : noirs vraiment noirs ? MAX trop sombre ?
4. **Basses** : DEEP BASS (DEEP / MAX) sur les haut-parleurs ou le casque ; AUTO LEVEL trop lent / trop pompant ?
5. **FX PADS, MORPH, appuis longs** : timing (1 s pour OCT−/OCT+) confortable ? déclenchements par erreur en SHIFT ?
6. **Écran** : fluidité du dégradé MORPH X/Y.

## 4. Reste à faire

| Priorité | Sujet | Notes |
|---|---|---|
| Haute | Retours du premier essai sur FM-1 | corriger ce qui sort du test (cœurs, charge, écran) |
| Haute | **Photo du KAWA de face** pour l'écran de démarrage | aujourd'hui dessiné en code ; une photo coûte ~60 à 115 Ko de flash |
| Moyenne | Activer GitHub Pages (Settings › Pages › main / root) | pour que l'accueil, l'émulateur et le manuel soient en ligne |
| Moyenne | Tests de non-régression des écrans (captures comparées) | `source/tests/manual_shots.py` en est la base |
| Basse | Presets B de démonstration pour les nouvelles fonctions (MORPH, PADS) | |

## 5. Propositions pour aller plus loin

### Un jeu en live plus réactif, plus addictif
- **PADS personnalisables** : choisir quel effet va sur chaque touche noire, mémoriser 4 jeux de pads (un par style).
- **Pads « scènes »** : une touche rappelle un preset + un morph (drop, break, build) sur le tempo.
- **Build / drop** : un geste (maintenir REC) qui monte tout (filtre, résonance, stutter, reverb) et relâche sur le temps fort.
- **Wobble « tap »** : taper le rythme du wobble sur une touche, le LFO s'y cale (comme le TAP tempo).
- **Enregistrer les mouvements** : 4 à 8 mesures de gestes (potards, pads) rejouées en boucle, avec overdub.
- **Visuel qui danse** : le point du morph laisse une traînée, l'onde pulse avec le kick, couleur selon le style.
- **Mode « performance »** : un écran avec uniquement les 4 macros en gros, le morph et les pads, rien d'autre.
- **Verrouillage de gestes** : les deux boutons OCT en même temps verrouillent les potards (pas de fausse manœuvre sur scène).
- **Jeu à la vélocité / pression** : les touches pilotent aussi le filtre ou le morph si le clavier envoie la pression.

### Plus de son
- **Mono-bass assistant** : bascule automatique en mono sous une fréquence réglable, pour la clarté du sub.
- **Oscillateur de sub intelligent** : sub qui suit la note en phase avec A, pour éviter les annulations.
- **Distorsion multibande** (low / mid / high séparés), qui donne des basses larges sans perdre le sub.
- **Formant / vowel animé** par le LFO (le « yoi » classique du dubstep) avec bibliothèque de voyelles.
- **Resample** : enregistrer 2 à 4 secondes de la sortie dans OSC C, puis le rejouer, le ralentir, le boucler (la « resample bass » de la DnB).
- **Plus de samples et de wavetables** (growl, screech, 808 variés), dont une banque installable à part.
- **Oversampling** sur la saturation et le wavefolder (moins d'aliasing) si le CPU le permet.
- **Presets** : un jeu par sous-genre (liquid, neuro, jump-up, minimal dub techno…), avec un tag et une recherche par style.

### Stabilité et performances
- **Mesure continue** du temps de chaque effet, avec un « mode économie » qui coupe seul les effets les plus lourds.
- **Journal de plantage** (3 derniers `LAST STOP` conservés) lisible dans SYSTEM.
- **Auto-test au démarrage** (tension, flash, deuxième cœur) avec un message clair.
- **Sauvegarde sûre** : écritures flash en deux temps (pas de perte si on coupe pendant l'enregistrement), export / import des patchs en SysEx.
- **Tests sur appareil** : script de « burn-in » 30 minutes (notes + morph + pads) avec rapport de charge.

### Interface et prise en main
- **Mode d'emploi intégré** : un écran d'aide par page (une touche, un texte court + un dessin).
- **Visite guidée** au premier démarrage (4 écrans : jouer, wobble, FX PADS, enregistrer).
- **Recherche de preset** par style avec les potards.
- **Thèmes personnalisés** : choisir couleur d'accent et fond, mémorisés.
- **Accessibilité** : police lisible en petit (déjà), contraste, taille du texte, daltonisme (palettes testées).
- **Manuel et émulateur** : liens « essayer ce preset » depuis le manuel, partage d'un patch par lien.

### Communauté et projet
- **Banque de presets** de la communauté, installables depuis la page.
- **Compteur de téléchargements / version** sur l'accueil, journal des changements automatique.
- **Traductions** : EN, ES, puis d'autres.
- **Guide de contribution** (build, tests, captures) et **tickets** classés (bug / idée / son).

## 6. Contraintes techniques (à garder en tête)

- Entiers seulement, pas de division 64 bits (le processeur n'a pas de FPU) ; l'interruption audio doit rester courte (bloc de 256 échantillons, 5,8 ms).
- RAM 53 Ko sur 96, pool 286 Ko sur 344, image 489 Ko sur 581 : il reste de la marge, mais pas pour de gros samples.
- Les patchs ont 130 paramètres (132 max) ; les patchs utilisateur gardent 112 octets dans le premier secteur et le reste dans le second. Les identifiants d'items tiennent dans un octet (static assert).
- Une écriture flash arrête le son quelques dizaines de ms (donc seulement en silence) ; le cœur 1 attend alors en RAM.
- Tout changement de format de sauvegarde doit rester lisible par les anciennes sauvegardes (champs ajoutés à la fin).

## 7. Décisions à prendre ensemble

1. Une photo du KAWA de face (fichier image) pour remplacer le dessin de l'écran de démarrage ?
2. Les noms : K-WASUB partout (déjà fait dans le firmware, les pages et les paquets) ; le dépôt s'appelle **K-WASUB_Firmware_for_FM1**.
3. Priorité suivante : **LFO dessiné**, **PADS personnalisables**, **scènes**, **wobble tap**.

## 8. Ce que Pure SUB et Serum ont de plus important, et qui ferait une plus-value ici

Classé par **valeur pour une basse** et **coût sur le FM-1** (CPU, RAM, écran à 5 boutons et 4 potards). Les noms des fonctions de Pure SUB sont donnés d'après leur réputation générale ; à vérifier avant de s'en inspirer au détail.

| # | Fonction | Vient de | Valeur | Coût | Remarque |
|---|---|---|---|---|---|
| 1 | **Mod matrix en glisser-déposer** (assigner d'un geste, voir la plage sur chaque réglage) | Serum, Pure SUB | très haute | faible | déjà : LFO maintenu + potard, barres violettes. Reste : source ENV/VEL/MACRO, plusieurs amounts par potard, visuel des assignations par page |
| 2 | **Courbes d'enveloppe et de LFO dessinées** (forme libre, 8 points) | Serum | haute | moyen | LFO « custom » de 16 points, calé sur le tempo : le wobble signature |
| 3 | **Modes de déformation de wavetable** (bend, sync, mirror, PWM, FM depuis B) | Serum | haute | moyen | s'ajoute à WARP : une vraie « table vivante » avec position modulable |
| 4 | **Unison avec blend, stéréo et détune** par moteur | Serum | haute | moyen | SUPER l'a en partie ; ajouter spread stéréo et blend |
| 5 | **Multibande / OTT** (compression 3 bandes, très « bass music ») | Serum (FX) | très haute | moyen | 3 bandes + sortie mono sous 120 Hz : grosse plus-value sur le son final |
| 6 | **Sub propre et « mono bass »** (sub en phase, mono sous une fréquence) | Pure SUB | très haute | faible | mono-bass automatique + sub qui suit la phase d'A |
| 7 | **Saturation / distorsion multi-types**, en série ou en parallèle | Serum, Pure SUB | haute | faible | 4 types ; ajouter parallèle (dry/wet) et un type « tape » |
| 8 | **Filtres supplémentaires** (formant, comb, phaser, flanger comme filtres) | Serum | moyenne | faible | VOWEL et COMB existent ; ajouter courbes plus nombreuses et une pente réglable |
| 9 | **Voix : mono / legato / glide / portamento par note** | Serum, Pure SUB | moyenne | faible | glide fait ; ajouter « glide en legato seulement » et durée par note du SEQ |
| 10 | **Macros nommées + page performance** | Serum, Pure SUB | haute | faible | MACROS existent ; leur donner un nom, un écran performance (4 macros + morph + pads) |
| 11 | **Navigateur de presets avec tags et recherche** | Serum | haute | faible | style existe ; ajouter tags (sub, reese, growl, pluck), recherche, « similaires » |
| 12 | **Resample** (enregistrer la sortie dans un oscillateur) | Serum (resample), pratique DnB | très haute | moyen | OSC C pourrait recevoir 2 à 4 s de sa propre sortie |
| 13 | **Oscillateur de bruit et textures** | Serum | moyenne | faible | 5 textures déjà ; ajouter bruit filtré, pitchable |
| 14 | **Visualiseurs (spectre, forme d'onde)** | Serum | moyenne | moyen | spectre 16 bandes sur la page FX ou le master |
| 15 | **MPE / aftertouch complet** | Serum | basse ici | moyen | seulement si un contrôleur externe le justifie |

**Faits en 0.9.11** : 6 (mono-bass, sub verrouillé), 5 (OTT 3 bandes), 10 (page PERFORM), 12 (resample), 11 (tags). **Suivant** : 2 (LFO dessiné), 3 (modes de wavetable), 4 (unison stéréo), 7 (saturation parallèle).

## 9. Les optimisations les plus efficaces

### Workflow (ce que ça change quand on joue)
1. **Page performance** : une seule page avec 4 macros, le morph et les pads. On ne navigue plus pendant un morceau. (Gain : très grand, coût : faible.)
2. **Scènes** : un appui rappelle un preset + un morph + une vitesse de wobble. Un drop en une touche.
3. **Wobble tap** : taper le rythme sur une touche calcule la division.
4. **Copier / coller un réglage ou une page** (maintenir une ligne, la coller sur une autre) et **INIT** (repartir d'un son neutre).
5. **Réglages les plus utilisés toujours en premier** (K1–K4) et une page « FAVORIS » faite de tes 12 réglages préférés.
6. **Moins de pas pour les gestes courants** : A/B des presets sur deux touches, « verrouiller les potards » (OCT− + OCT+ longtemps).
7. **Aide intégrée** : appuyer deux fois sur un bouton affiche une ligne qui dit ce qu'il fait.
8. **Tutoriel au premier démarrage** (4 écrans, sautable).

### Programme (ce que ça change dans le firmware)
1. **Modulation à la cadence du bloc** pour tout ce qui n'est pas audible à l'échantillon (déjà fait pour les effets) : généraliser aux LFO lents et aux macros.
2. **Tables plutôt que calculs** : courbes de saturation, sinus, wavefold, enveloppes en tables Q15 (plus rapide, plus stable).
3. **Répartition fine des deux cœurs** : déplacer chorus / phaser / delay sur le cœur 1 quand il a de la marge, mesurer le temps réel de chaque étage et équilibrer tout seul.
4. **Vol de voix intelligent** et **mode économie** : couper d'abord les effets les moins audibles quand la charge monte (aujourd'hui : reverb et chorus, puis les voix).
5. **Dessin de l'écran par zones modifiées** (déjà par bandes de 40 px) : ajouter un petit cache des éléments fixes (grilles, titres) pour réduire la charge des pages chargées (MORPH X/Y).
6. **Flash** : regrouper les écritures, limiter les cycles d'effacement (réglages 2 s après le dernier changement, déjà fait), journal de plantage circulaire.
7. **Tests** : captures comparées (`source/tests/manual_shots.py`) pour repérer les écrans cassés (comme le titre ARP), test de charge étendu à FX PADS / MORPH / limiteur, burn-in de 30 minutes sur l'appareil.
8. **Mesure** : afficher dans SYSTEM la charge maximale des 10 dernières secondes (pas seulement l'instant) pour régler sans deviner.
