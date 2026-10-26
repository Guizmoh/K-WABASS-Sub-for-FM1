#!/usr/bin/env python3
"""The manual, short: manual.html (English) and fr/manual.html (French) from one text. A fixed table of contents on
   the left, a search box that hides the chapters that do not match. Run from the repo root:
   python3 source/tools/make_manual.py      (the pictures: source/tests/manual_shots.py -> docs/img)"""
from pathlib import Path

EXTRA_CSS = """.grid.sm{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}.grid.sm figcaption{font-size:.8rem}
ul.tight{margin:.4rem 0;padding-left:1.2rem}ul.tight li{margin:.15rem 0}
.layout{display:grid;grid-template-columns:230px 1fr;align-items:start;max-width:1280px;margin:0 auto}
.layout main{max-width:900px;margin:0;padding:30px 28px 80px}
aside.side{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:20px 16px;border-right:1px solid var(--rule)}
aside.side input[type=search]{width:100%;box-sizing:border-box;padding:9px 11px;border-radius:9px;border:1px solid var(--rule);
background:var(--panel2);color:var(--ink);font:.88rem var(--sans);margin-bottom:12px}
aside.side input[type=search]::placeholder{color:var(--mut)}
.side-toc{list-style:none;margin:0;padding:0;display:grid;gap:1px}
.side-toc a{display:block;padding:7px 10px;border-radius:7px;color:var(--mut);text-decoration:none;font-size:.9rem}
.side-toc a:hover{background:var(--panel2);color:var(--ink)}
.side-toc a.cur{background:var(--panel2);color:var(--lime)}
.side-toc li.nohit{display:none}
.chap.hide{display:none}
#noq{display:none;color:var(--mut);padding:30px 0}
@media(max-width:860px){.layout{display:block}aside.side{position:static;height:auto;border-right:0;border-bottom:1px solid var(--rule)}.layout main{max-width:none;margin:0 auto;padding:24px 18px 80px}}
"""
CSS = Path("source/web/manual.css.txt").read_text().replace("</style>", EXTRA_CSS + "</style>")
KOFI = "https://ko-fi.com/omnipotard"


def T(en, fr): return {"en": en, "fr": fr}


def build(L):
    fr = L == "fr"
    img = "../docs/img/" if fr else "docs/img/"
    t = lambda x: x[L] if isinstance(x, dict) else x

    def fig(name, cap): return f'<figure><img src="{img}{name}.png" alt=""><figcaption>{t(cap)}</figcaption></figure>'

    def grid(items, cls="grid sm"): return f'<div class="{cls}">' + "".join(fig(n, c) for n, c in items) + "</div>"

    def key(k): return f'<span class="key k">{k}</span>'

    nav = [("start", T("Start", "Démarrer")), ("panel", T("Buttons", "Boutons")), ("pages", T("Pages", "Pages")),
           ("sel", T("SEL · PERFORM", "SEL · PERFORM")), ("pads", "FX PADS"), ("seq", "SEQ · DRUMS"), ("looks", T("Themes", "Thèmes")),
           ("sound", T("Sound", "Son")), ("data", T("Data", "Données")), ("help", T("Help", "Aide"))]

    chaps = []  # (id, title, html) -- each becomes its own <section class="chap">, searched and listed in the TOC

    # 1 start
    inst = "../installer.html?lang=fr" if fr else "installer.html"
    chaps.append(("start", t(T("1 · Start", "1 · Démarrer")),
                  '<div class="card"><ol>' + t(T(
                      f'<li><b>Install</b>: <a href="{inst}">installer.html</a> in Chrome or Edge, FM-1 plugged in with a USB data cable. Without it: <code>INSTALL-*</code> scripts (Python 3).</li>'
                      '<li><b>First start</b>: CLASSIC (lists) or SHIFT (3 columns)? Asked once. Then the start picture waits for any button or key.</li>'
                      '<li><b>Play</b>: the keys; <kbd>PRESETS</kbd> changes the sound at once (<kbd>SAVE</kbd> held = UNDO). Each session starts at octave −1.</li>'
                      '<li><b>AUTOSAVE</b> keeps the sound you are making every minute; it comes back at the next start. <kbd>SAVE</kbd> keeps it for good in one of 32 slots.</li>',
                      f'<li><b>Installer</b> : <a href="{inst}">installer.html</a> dans Chrome ou Edge, FM-1 branché avec un câble USB de données. Sinon : les scripts <code>INSTALL-*</code> (Python 3).</li>'
                      '<li><b>Premier démarrage</b> : CLASSIC (listes) ou SHIFT (3 colonnes) ? Demandé une fois. Ensuite l’image de départ attend n’importe quel bouton ou touche.</li>'
                      '<li><b>Jouer</b> : les touches ; <kbd>PRESETS</kbd> change de son tout de suite (<kbd>SAVE</kbd> maintenu = UNDO). Chaque session démarre à l’octave −1.</li>'
                      '<li><b>AUTOSAVE</b> garde le son en cours toutes les minutes ; il revient au démarrage suivant. <kbd>SAVE</kbd> le garde pour de bon dans un des 32 emplacements.</li>'))
                  + '</ol></div>'))

    # 2 buttons
    rows = [("HOME", T("PLAY, LIVE MIX", "PLAY, LIVE MIX"), T("<b>A + B</b>: the two oscillators", "<b>A + B</b> : les deux oscillateurs")),
            ("EDIT", T("OSC A, B, SUB, A + B, OSC C (sample, resample)", "OSC A, B, SUB, A + B, OSC C (sample, resample)"), T("random of the page", "aléatoire de la page")),
            ("ENV", T("amp, filter, mod envelopes", "enveloppes ampli, filtre, mod"), T("+ knob: the mod envelope on it", "+ potard : l’enveloppe de mod dessus")),
            ("SEQ", T("filter, filter mod, SEQ BASS, DRUMS", "filtre, mod du filtre, SEQ BASS, DRUMS"), T("random of the page", "aléatoire de la page")),
            ("LFO", T("LFO 1 (wobble), LFO 2, STEP, matrix", "LFO 1 (wobble), LFO 2, STEP, matrice"), T("+ knob: LFO 2 on it · with OCT−: LFO 1", "+ potard : LFO 2 dessus · avec OCT− : LFO 1")),
            ("FX", T("SAT, OTT, COMP, EQ, DELAY, VERB, CHORUS, PHASER, CRUSH, MASTER", "SAT, OTT, COMP, EQ, DELAY, VERB, CHORUS, PHASER, CRUSH, MASTER"), T("<b>FX PADS</b>", "<b>FX PADS</b>")),
            ("ARP", T("presets A / B, SAVE, ARP", "presets A / B, SAVE, ARP"), T("random of the page", "aléatoire de la page")),
            ("GLO", T("SYSTEM, MIDI", "SYSTEM, MIDI"), T("CLASSIC ↔ SHIFT", "CLASSIC ↔ SHIFT")),
            ("SEL", T("PERFORM → MORPH X/Y → FX LIVE → MACROS → MORPH A/B", "PERFORM → MORPH X/Y → FX LIVE → MACROS → MORPH A/B"), T("hear the saved sound (compare)", "écouter le son enregistré (comparer)")),
            ("SAVE", T("save", "enregistrer"), T("+ OCT− UNDO / OCT+ REDO (16 steps); on presets: favourite", "+ OCT− UNDO / OCT+ REDO (16 pas) ; sur les presets : favori")),
            ("PLAY", T("SEQ start / stop", "SEQ marche / arrêt"), T("HOLD: the keys stay on", "HOLD : les touches restent tenues")),
            ("REC", T("tap tempo · on SEQ: step record", "tap tempo · sur SEQ : enregistrement des pas"), T("<b>PANIC</b>", "<b>PANIC</b>")),
            ("OCT− OCT+", T("octave", "octave"), T("UNDO / REDO · with a knob: SHIFT", "UNDO / REDO · avec un potard : SHIFT"))]
    chaps.append(("panel", t(T("2 · The buttons", "2 · Les boutons")),
                  f'<table><tr><th></th><th>{t(T("Press", "Appui"))}</th><th>{t(T("Hold (a bar fills)", "Maintien (une barre se remplit)"))}</th></tr>'
                  + "".join(f'<tr><td>{" ".join(key(k) for k in b.split())}</td><td>{t(p)}</td><td>{t(h)}</td></tr>' for b, p, h in rows) + "</table>"
                  + f'<p>{t(T("Pressing a page button again shows its next view. <kbd>SELECT</kbd> a row, <kbd>ALGO</kbd> its value. <kbd>KNOB ACCEL</kbd> (SYSTEM): OFF, ON, FAST, ULTRA.", "Rappuyer sur un bouton de page montre sa vue suivante. <kbd>SELECT</kbd> une ligne, <kbd>ALGO</kbd> sa valeur. <kbd>KNOB ACCEL</kbd> (SYSTEM) : OFF, ON, FAST, ULTRA."))}</p>'))

    # 3 pages -- one picture (HOME); every view listed as text, grouped by the button that opens it (complete, not a
    # sample: FX alone has 10 views, showing a thumbnail of each would not fit a short manual)
    pages = [("HOME", T("CURRENT PATCH, LIVE MIX", "CURRENT PATCH, LIVE MIX")),
             ("EDIT", T("OSCILLATOR A, OSCILLATOR B, SUB + NOISE, COMBINE A + B, OSCILLATOR C · SAMPLE", "OSCILLATEUR A, OSCILLATEUR B, SUB + BRUIT, COMBINER A + B, OSCILLATEUR C · SAMPLE")),
             ("ENV", T("AMP ENVELOPE, FILTER ENVELOPE, MOD ENVELOPE", "ENVELOPPE AMPLI, ENVELOPPE FILTRE, ENVELOPPE MOD")),
             ("SEQ", T("FILTER / COLOUR, FILTER MOD, SEQ BASS, DRUMS", "FILTRE / COULEUR, MOD DU FILTRE, SEQ BASS, DRUMS")),
             ("LFO", T("LFO 1 · WOBBLE, LFO 2 · MOTION, STEP FX, MOD MATRIX", "LFO 1 · WOBBLE, LFO 2 · MOUVEMENT, STEP FX, MATRICE DE MOD")),
             ("FX", T("SATURATION, MULTIBAND (OTT), COMPRESSOR, EQ, DELAY, REVERB, CHORUS, PHASER, CRUSH, MASTER", "SATURATION, MULTIBANDE (OTT), COMPRESSEUR, EQ, DELAY, REVERB, CHORUS, PHASER, CRUSH, MASTER")),
             ("ARP", T("PRESET BANK A, PRESET BANK B, SAVE PATCH, ARPEGGIATOR", "BANQUE DE PRESETS A, BANQUE DE PRESETS B, ENREGISTRER LE PATCH, ARPEGIATEUR")),
             ("GLO", T("GLOBAL SETUP, MIDI", "REGLAGES GENERAUX, MIDI"))]
    chaps.append(("pages", t(T("3 · The pages", "3 · Les pages")),
                  '<div class="row">' + fig("p-home", T("HOME, the first view", "HOME, la première vue"))
                  + '<div><ul class="tight">' + "".join(f'<li>{key(b)} {t(v)}</li>' for b, v in pages) + '</ul></div></div>'
                  + '<ul class="tight">' + t(T(
                      '<li><b>EQ</b>: SELECT a band; K1 FREQ, K2 GAIN, K3 Q, K4 SHAPE.</li>'
                      '<li><b>OSC C · SAMPLE</b>: 18 sounds (808, kick, snare, vox, reese, growl, pluck, bell, metal, brass; attacks PICK, MALLET, CHIFF, HAMMER, ZAP, SLAP, CLICK, SCRATCH) and 9 textures (vinyl, tape hiss, rain, wind, data, SHIMMER, DARK PAD, BUBBLES, MACHINE). K3 <b>START</b> and K4 <b>END</b> cut the beginning and the end (the cut parts dim on the picture); <b>SPEED</b> 25 %–400 %, the pitch kept (right: slower, left: faster); <b>DIR</b> FORWARD, REVERSE or PING-PONG; PLAY AUTO / LOOP / ONCE.</li>''<li><b>RESAMPLE</b> (OSC C): records 2–4 s of the output, OSC C plays it back (loop, speed, keys). Kept until power-off.</li>'
                      '<li>Almost anything is a <b>destination</b> (LFOs, matrix, quick assign), MORPH X / Y / A-B and A/B MIX included.</li>',
                      '<li><b>EQ</b> : SELECT une bande ; K1 FREQ, K2 GAIN, K3 Q, K4 SHAPE.</li>'
                      '<li><b>OSC C · SAMPLE</b> : 18 sons (808, kick, snare, voix, reese, growl, pluck, cloche, métal, cuivre ; attaques PICK, MALLET, CHIFF, HAMMER, ZAP, SLAP, CLICK, SCRATCH) et 9 textures (vinyle, souffle de bande, pluie, vent, data, SHIMMER, DARK PAD, BUBBLES, MACHINE). K3 <b>START</b> et K4 <b>END</b> coupent le début et la fin (les parties coupées s’assombrissent sur l’image) ; <b>SPEED</b> de 25 % à 400 %, à hauteur égale (à droite : plus lent, à gauche : plus rapide) ; <b>DIR</b> FORWARD, REVERSE ou PING-PONG ; PLAY AUTO / LOOP / ONCE.</li>''<li><b>RESAMPLE</b> (OSC C) : enregistre 2 à 4 s de la sortie, OSC C la rejoue (boucle, vitesse, touches). Gardé jusqu’à l’extinction.</li>'
                      '<li>Presque tout peut être une <b>destination</b> (LFO, matrice, assignation rapide), y compris MORPH X / Y / A-B et A/B MIX.</li>')) + '</ul>'))

    # 4 SEL -- one picture (MORPH X/Y, the one that needs a picture: a point dragged in a square); the rest as text
    chaps.append(("sel", t(T("4 · SEL: live windows", "4 · SEL : les fenêtres de jeu")),
                  '<div class="row">' + fig("w-morph-xy", T("MORPH X/Y: 4 versions of the sound in the corners, a point blends them", "MORPH X/Y : 4 versions du son dans les coins, un point les mélange"))
                  + '<div><ul class="tight">' + t(T(
                      '<li><b>PERFORM</b>: K1–K4 the 4 macros, SELECT / ALGO the morph.</li>'
                      '<li><b>MORPH X/Y</b>: SELECT / ALGO move the point (an LFO can too); the four corners are A, B, C, D.</li>'
                      '<li><b>FX LIVE</b>: DJ filter, pump, stutter, tape stop, resonance, live, not stored.</li>'
                      '<li><b>MACROS</b>: 4 named knobs, each wired to up to 4 destinations.</li>'
                      '<li><b>MORPH A/B</b>: PLAY makes the trip between two sounds on the beat.</li>',
                      '<li><b>PERFORM</b> : K1–K4 les 4 macros, SELECT / ALGO le morph.</li>'
                      '<li><b>MORPH X/Y</b> : SELECT / ALGO déplacent le point (un LFO aussi) ; les quatre coins sont A, B, C, D.</li>'
                      '<li><b>FX LIVE</b> : filtre DJ, pump, stutter, tape stop, résonance, en direct, non enregistrés.</li>'
                      '<li><b>MACROS</b> : 4 potards nommés, chacun branché sur jusqu’à 4 destinations.</li>'
                      '<li><b>MORPH A/B</b> : PLAY fait le trajet entre deux sons en rythme.</li>')) + '</ul></div></div>'
                  + f'<p>{t(T("In PERFORM, <kbd>OCT+</kbd> held turns the keys into FX PADS. A page button closes a window.", "Dans PERFORM, <kbd>OCT+</kbd> maintenu transforme les touches en FX PADS. Un bouton de page ferme une fenêtre."))}</p>'))

    # 5 pads -- the keybed heat-map: genuinely clearer as a picture than as more rows of text
    chaps.append(("pads", f'5 · FX PADS ({t(T("FX held", "FX maintenu"))})',
                  f'<div class="row">{fig("w-pads", "FX PADS")}<div><table>'
                  + t(T('<tr><td>White 1–8</td><td>wobble speed</td></tr><tr><td>White 9–16</td><td>wobble depth, shape</td></tr>'
                        '<tr><td>Black 1–4</td><td>stutter (held)</td></tr><tr><td>Black 5–11</td><td>tape stop, DJ filters, pump, saturate, phaser, crush</td></tr>',
                        '<tr><td>Blanches 1–8</td><td>vitesse du wobble</td></tr><tr><td>Blanches 9–16</td><td>profondeur, forme du wobble</td></tr>'
                        '<tr><td>Noires 1–4</td><td>stutter (tenu)</td></tr><tr><td>Noires 5–11</td><td>tape stop, filtres DJ, pump, saturation, phaser, crush</td></tr>'))
                  + f'</table><p>{t(T("K1 CUTOFF · K2 RESONANCE · K3 FILTER TYPE · K4 MORPH A/B · <b>ALGO: QUANTIZE</b> (OFF to 1/64): a key waits for the next division, so it lands on time.", "K1 CUTOFF · K2 RÉSONANCE · K3 TYPE DE FILTRE · K4 MORPH A/B · <b>ALGO : QUANTISATION</b> (OFF à 1/64) : une touche attend la prochaine division, elle tombe en rythme."))}</p></div></div>'))

    # 6 sequencers -- the drums' grid and the keys that fill it
    chaps.append(("seq", t(T("6 · SEQ BASS and DRUMS", "6 · SEQ BASS et DRUMS")),
                  grid([("d-drums", "DRUMS · TECHNO"), ("d-lock", "PARAMETER LOCK"), ("d-drums-dub", T("DUB TECHNO kit", "kit DUB TECHNO")), ("d-seq", "SEQ BASS"), ("v-sample-cut", T("OSC C: START / END", "OSC C : START / END"))])
                  + t(T('<p><b>PLAY</b> starts both sequencers (SEQ BASS and DRUMS) on the tempo; <b>REC</b> on their views records: stopped, step by step; playing, live. '
                        'DRUMS is the 4th view of SEQ (press SEQ until it shows).</p>'
                        '<table><tr><td>Black keys 1–8</td><td>choose the instrument and play it (REC + PLAY: record it now)</td></tr>'
                        '<tr><td>Black key 9 · 10</td><td>mute the instrument · clear its track</td></tr>'
                        '<tr><td>White keys 1–16</td><td>its steps on the page shown (on / off)</td></tr>'
                        '<tr><td>OCT− · OCT+</td><td>previous · next page of 16 steps (32 and 64-step patterns)</td></tr>'
                        '<tr><td>K1–K4</td><td>LEVEL, TUNE, DECAY, TONE of the instrument</td></tr>'
                        '<tr><td>A white key held + K1–K4 · ALGO · SELECT</td><td><b>parameter lock</b> on that step: its own LEVEL, TUNE, DECAY, TONE · RATCHET (2–4 hits) · ECHO (DUB TECHNO); a white corner marks it. Held + black 10: its locks cleared. Let go untouched: the step goes off</td></tr>'
                        '<tr><td>SELECT · ALGO</td><td>a row, its value: STEP, HIT (on / accent), PROB (chance), COND, PAT (8 patterns), PRESET, STEPS, KIT, VOL, PLAYS, SWING</td></tr></table>'
                        '<p><b>Colours</b>: kick red, snare green, clap pink, closed hat yellow, open hat orange, tom blue, perc violet, cymbal cyan (shades of white with the BLACK / WHITE palette). '
                        'A dot on a step: it has a chance or a condition. The white column is the step playing.</p>'
                        '<p><b>Conditions</b> (per step, SEQ BASS too): 1/2, 2/2, 1/4…4/4 (that time round), START / NOT START (the first time round), IF BEFORE (the step before played), IF AFTER (the next one plays). '
                        '<b>Kits</b>: 808, 909, DUB TECHNO (deep kick, chord stab on PERC, its own dub echo), ACOUSTIC (beater kick, snare wires, toms, conga, ride). '
                        '<b>Presets</b>: 18 rhythms (TECHNO, HOUSE, DUB, DNB, JUNGLE, DUBSTEP, BREAKBEAT, UK GARAGE, ELECTRO, MINIMAL, HALFTIME, TRAP, ROLLING HATS, FOUR FLOOR, DUB TECHNO, ROCK, FUNK, JAZZ RIDE) in 16, 32 and 64 steps; MY PATTERN brings yours back. '
                        '<b>PLAYS</b>: bass + drums, drums only, bass only.</p>'
                        '<p><b>SEQ BASS</b>: per step a note, a NOTE LEN (1/8 step to 64 steps, or HOLD), a type (accent, slide), a chance and a condition; 30 basslines in 16, 32, 64 steps. <b>Parameter locks</b>: the rows P-LOCK (CUTOFF, RESO, FILT ENV, DRIVE, WOB RATE, A SHAPE, SMP START) and LOCK VALUE give the cursor\'s step its own value (OFF below the range); a cyan corner marks it. <b>REC while it plays</b>: turning one of these settings, in any view, locks it on the step playing, for the bass, and K1–K4 on the drums.</p>'
                        '<p><b>Sync</b>: SYSTEM › MIDI › SYNC OUT = PO / VOLCA puts a pulse every eighth note on the left output while it plays, the sound in mono on the right: '
                        'a stereo-to-two-mono cable to a Pocket Operator (SY mode that follows) or a Volca\'s SYNC IN. MIDI clock in / out is in the same view.</p>',
                        '<p><b>PLAY</b> lance les deux séquenceurs (SEQ BASS et DRUMS) sur le tempo ; <b>REC</b> sur leurs vues enregistre : à l’arrêt pas à pas, en lecture en direct. '
                        'DRUMS est la 4e vue de SEQ (appuyer sur SEQ jusqu’à la voir).</p>'
                        '<table><tr><td>Noires 1–8</td><td>choisir l’instrument et le jouer (REC + PLAY : l’enregistrer à l’instant)</td></tr>'
                        '<tr><td>Noire 9 · 10</td><td>couper l’instrument · effacer sa piste</td></tr>'
                        '<tr><td>Blanches 1–16</td><td>ses pas sur la page affichée (on / off)</td></tr>'
                        '<tr><td>OCT− · OCT+</td><td>page de 16 pas précédente · suivante (patterns de 32 et 64 pas)</td></tr>'
                        '<tr><td>K1–K4</td><td>LEVEL, TUNE, DECAY, TONE de l’instrument</td></tr>'
                        '<tr><td>Blanche maintenue + K1–K4 · ALGO · SELECT</td><td><b>parameter lock</b> sur ce pas : ses propres LEVEL, TUNE, DECAY, TONE · RATCHET (2 à 4 coups) · ECHO (DUB TECHNO) ; un coin blanc le marque. Maintenue + noire 10 : ses verrous effacés. Relâchée sans rien tourner : le pas s’éteint</td></tr>'
                        '<tr><td>SELECT · ALGO</td><td>une ligne, sa valeur : STEP, HIT (on / accent), PROB (chance), COND, PAT (8 patterns), PRESET, STEPS, KIT, VOL, PLAYS, SWING</td></tr></table>'
                        '<p><b>Couleurs</b> : kick rouge, snare vert, clap rose, charley fermé jaune, charley ouvert orange, tom bleu, percu violet, cymbale cyan (nuances de blanc avec la palette BLACK / WHITE). '
                        'Un point sur un pas : il a une chance ou une condition. La colonne blanche est le pas joué.</p>'
                        '<p><b>Conditions</b> (par pas, SEQ BASS aussi) : 1/2, 2/2, 1/4…4/4 (ce tour-là), START / NOT START (le premier tour), IF BEFORE (le pas d’avant a joué), IF AFTER (le suivant joue). '
                        '<b>Kits</b> : 808, 909, DUB TECHNO (kick profond, accord sur PERC, son propre écho dub), ACOUSTIC (kick à batte, caisse claire à timbre, toms, conga, ride). '
                        '<b>Presets</b> : 18 rythmes (TECHNO, HOUSE, DUB, DNB, JUNGLE, DUBSTEP, BREAKBEAT, UK GARAGE, ELECTRO, MINIMAL, HALFTIME, TRAP, ROLLING HATS, FOUR FLOOR, DUB TECHNO, ROCK, FUNK, JAZZ RIDE) en 16, 32 et 64 pas ; MY PATTERN ramène le tien. '
                        '<b>PLAYS</b> : basse + batterie, batterie seule, basse seule.</p>'
                        '<p><b>SEQ BASS</b> : par pas une note, une NOTE LEN (1/8 de pas à 64 pas, ou HOLD), un type (accent, slide), une chance et une condition ; 30 lignes de basse en 16, 32, 64 pas. <b>Parameter locks</b> : les lignes P-LOCK (CUTOFF, RESO, FILT ENV, DRIVE, WOB RATE, A SHAPE, SMP START) et LOCK VALUE donnent au pas du curseur sa propre valeur (OFF sous la plage) ; un coin cyan le marque. <b>REC pendant la lecture</b> : tourner un de ces réglages, dans n’importe quelle vue, le verrouille sur le pas joué pour la basse, et K1–K4 sur la batterie.</p>'
                        '<p><b>Synchro</b> : SYSTEM › MIDI › SYNC OUT = PO / VOLCA met une impulsion par croche sur la sortie gauche pendant la lecture, le son en mono à droite : '
                        'un câble stéréo vers deux mono jusqu’à un Pocket Operator (mode SY qui suit) ou le SYNC IN d’une Volca. L’horloge MIDI in / out est dans la même vue.</p>'))))

    # 6 looks -- pictures are the point here (what a palette looks like cannot be said in words): kept
    chaps.append(("looks", t(T("7 · Themes, palettes, fonts", "7 · Thèmes, palettes, polices")),
                  f'<p>{t(T("SYSTEM › THEME, PALETTE (13, then their RAD gradient versions), FONT (9; OUTFIT by default), LOUPE (on by default), BRIGHTNESS. Two modes: CLASSIC (lists) and SHIFT (3 columns, OCT− / OCT+ held for the middle and right ones).", "SYSTEM › THEME, PALETTE (13, puis leurs versions dégradé RAD), FONT (9 ; OUTFIT par défaut), LOUPE (active par défaut), BRIGHTNESS. Deux modes : CLASSIC (listes) et SHIFT (3 colonnes, OCT− / OCT+ maintenus pour celles du milieu et de droite)."))}</p>'
                  + grid([("t-glow-green", "CLASSIC GLOW"), ("t-studio", "STUDIO"), ("t-pure", "PURE"), ("t-rack", "RACK"), ("t-tech-volt", "TECH"),
                          ("rb-osc", "RIBBON"), ("rbc-osc", "RIBBON CLASSIC"), ("s-osc", "SHIFT")])
                  + grid([("t-red", "RED"), ("t-gold", "GOLD"), ("t-synthwave", "SYNTHWAVE"), ("t-fluo", "FLUO"), ("t-pink", "PINK"), ("t-ice", "ICE"),
                          ("t-mint", "MINT"), ("t-blackwhite", "BLACK / WHITE"), ("t-inverted", "INVERTED"), ("t-sky", "SKY"), ("t-blaze", "BLAZE"),
                          ("t-ribbon-ice", "ICE NEON"), ("t-rad-red", "RED RAD"), ("t-rad-synthwave", "SYNTHWAVE RAD"), ("t-rad-glow-green", "FLUO GREEN RAD"), ("t-rad-sky", "SKY RAD")])))

    # 7 sound
    chaps.append(("sound", t(T("8 · The sound", "8 · Le son")),
                  '<ul class="tight">' + t(T(
                      '<li><b>Engines</b>: ANALOG, SUPER / REESE, WAVE, FM (ESSENTIAL) + PHASE, FOLD, SYNC, VOCAL (SYSTEM › ENGINES › ALL). A and B: add, ring, X-mod, sync.</li>'
                      '<li><b>Filter</b>: LP 24, LP 12, BAND, HIGH, NOTCH, VOWEL, COMB.</li>'
                      '<li><b>Low end</b>: MONO BASS (mono under 120 Hz), SUB LOCK (sub in phase with OSC A), DEEP BASS (+4 / +7 dB under 90 Hz), OTT.</li>'
                      '<li><b>Output</b>: AUTO LEVEL (same loudness for every sound), limiter always on, MASTER volume last.</li>'
                      '<li><b>Presets</b>: 51 factory sounds (with tags: SUB, REESE, GROWL, WOBBLE, PLUCK, 808, DRONE), 32 of yours.</li>'
                      '<li><b>SEQ BASS</b>: 16 patterns of up to 64 steps (LENGTH 16, 32, 64…), each step with a <b>PROBABILITY</b> (%) and a <b>TRIG CONDITION</b>: 1/2, 2/2, 1/4…4/4 (that time round), START / NOT START (the first time round), IF BEFORE (the step before played), IF AFTER (the step after plays). A white dot marks such steps, the marks top right the page of 16 shown. Each step also has a <b>NOTE LEN</b> (1/8 step to 64 steps, or HOLD: continuous notes and drones). <b>PRESET</b>: 30 basslines (DNB ROLL, DUB STEPPA, ACID, DRONE, SUSTAIN, WOBBLE HALF…), each in 16, 32 and 64 steps; MY PATTERN brings yours back. <b>REC</b>: stopped, the keys write step by step; playing, they record live (the time held sets NOTE LEN).</li><li><b>DRUMS</b> (SEQ, 4th view): 8 tracks, 4 kits (808, 909, <b>DUB TECHNO</b>: deep kick, noisy hats, a minor chord stab on PERC and a dub echo; <b>ACOUSTIC</b>: beater kick, snare wires, toms, conga, ride), one colour each (kick red, snare green, clap pink, closed hat yellow, open hat orange, tom blue, perc violet, cymbal cyan). <b>Black keys</b> choose the instrument (and play it), the 9th mutes it, the 10th clears it; <b>white keys</b> = the 16 steps of the page; <b>OCT− / OCT+</b> = previous / next page. LVL, TUNE, DEC, TONE per track; per step HIT (accent), PROB (chance) and COND (conditions). PRESET: TECHNO, HOUSE, DUB, DNB, JUNGLE, DUBSTEP, BREAKBEAT, UK GARAGE, ELECTRO, MINIMAL, HALFTIME, TRAP, DUB TECHNO, ROCK, FUNK, JAZZ RIDE… in 16 / 32 / 64 steps (fills; toms on ACOUSTIC). PLAYS: bass + drums, drums only or bass only. <b>REC</b> while playing: the black keys record live. <b>ARP</b>: 5 modes. <b>MIDI</b>: learn, clock in / out, program change.</li>'
                      '<li><b>LANGUAGE</b> (SYSTEM): English, Français or Español translate the view titles at the top of every screen; English by default.</li>',
                      '<li><b>Moteurs</b> : ANALOG, SUPER / REESE, WAVE, FM (ESSENTIAL) + PHASE, FOLD, SYNC, VOCAL (SYSTEM › ENGINES › ALL). A et B : addition, ring, X-mod, sync.</li>'
                      '<li><b>Filtre</b> : LP 24, LP 12, BAND, HIGH, NOTCH, VOWEL, COMB.</li>'
                      '<li><b>Grave</b> : MONO BASS (mono sous 120 Hz), SUB LOCK (sub en phase avec OSC A), DEEP BASS (+4 / +7 dB sous 90 Hz), OTT.</li>'
                      '<li><b>Sortie</b> : AUTO LEVEL (même volume pour tous les sons), limiteur toujours actif, volume MASTER en dernier.</li>'
                      '<li><b>Presets</b> : 51 sons d’usine (avec tags : SUB, REESE, GROWL, WOBBLE, PLUCK, 808, DRONE), 32 à toi.</li>'
                      '<li><b>SEQ BASS</b> : 16 patterns jusqu\'à 64 pas (LENGTH 16, 32, 64…), chaque pas avec une <b>PROBABILITY</b> (%) et une <b>TRIG CONDITION</b> : 1/2, 2/2, 1/4…4/4 (ce tour-là), START / NOT START (le premier tour), IF BEFORE (le pas d\'avant a joué), IF AFTER (le pas d\'après joue). Un point blanc marque ces pas, les repères en haut à droite la page de 16 affichée. Chaque pas a aussi une <b>NOTE LEN</b> (1/8 de pas à 64 pas, ou HOLD : notes continues et drones). <b>PRESET</b> : 30 lignes de basse (DNB ROLL, DUB STEPPA, ACID, DRONE, SUSTAIN, WOBBLE HALF…), chacune en 16, 32 et 64 pas ; MY PATTERN ramène le tien. <b>REC</b> : à l’arrêt, les touches écrivent pas à pas ; en lecture, elles enregistrent en direct (la durée d’appui donne NOTE LEN).</li><li><b>DRUMS</b> (SEQ, 4e vue) : 8 pistes, 4 kits (808, 909, <b>DUB TECHNO</b> : kick profond, charleys bruités, accord mineur sur PERC et écho dub ; <b>ACOUSTIC</b> : kick à batte, caisse claire à timbre, toms, conga, ride), une couleur chacune (kick rouge, snare vert, clap rose, charley fermé jaune, charley ouvert orange, tom bleu, percu violet, cymbale cyan). <b>Touches noires</b> : choisir l’instrument (et le jouer), la 9e le coupe, la 10e l’efface ; <b>touches blanches</b> = les 16 pas de la page ; <b>OCT− / OCT+</b> = page précédente / suivante. LVL, TUNE, DEC, TONE par piste ; par pas HIT (accent), PROB (chance) et COND (conditions). PRESET : TECHNO, HOUSE, DUB, DNB, JUNGLE, DUBSTEP, BREAKBEAT, UK GARAGE, ELECTRO, MINIMAL, HALFTIME, TRAP, DUB TECHNO, ROCK, FUNK, JAZZ RIDE… en 16 / 32 / 64 pas (avec breaks ; aux toms sur ACOUSTIC). PLAYS : basse + batterie, batterie seule ou basse seule. <b>REC</b> en lecture : les touches noires enregistrent en direct. <b>ARP</b> : 5 modes. <b>MIDI</b> : learn, horloge in / out, program change.</li>'
                      '<li><b>LANGUAGE</b> (SYSTEM) : English, Français ou Español traduisent les titres de vue en haut de chaque écran ; anglais par défaut.</li>')) + '</ul>'))

    # 8 data
    data = "../data.html?lang=fr" if fr else "data.html"
    chaps.append(("data", t(T("9 · Data page (USB)", "9 · Page Données (USB)")),
                  '<p>' + t(T(
                      f'<a href="{data}"><b>Data</b></a> (Chrome / Edge): back up and restore your sounds (<code>.kwsub</code>), save a RESAMPLE recording as WAV, send a sound file of yours to OSC C (until power-off).',
                      f'<a href="{data}"><b>Données</b></a> (Chrome / Edge) : sauvegarder et recharger tes sons (<code>.kwsub</code>), enregistrer un RESAMPLE en WAV, envoyer un fichier son à toi vers OSC C (jusqu’à l’extinction).')) + '</p>'))

    # 9 help
    chaps.append(("help", t(T("10 · Help", "10 · Aide")),
                  '<div class="card warn">' + t(T(
                      '<b>It switched off or restarted?</b> The reason shows at the next start (<code>LAST STOP</code>): WATCHDOG = overloaded, LOW VOLTAGE = power (battery, cable), CRASH + address = send it to me. '
                      '<b>No sound?</b> Check MASTER. <b>Stuck notes?</b> REC held (PANIC). <b>Rescue:</b> OCT− held at power-on, the installer always works.',
                      '<b>Il s’est éteint ou a redémarré ?</b> La cause s’affiche au démarrage suivant (<code>LAST STOP</code>) : WATCHDOG = surchargé, LOW VOLTAGE = alimentation (batterie, câble), CRASH + adresse = envoie-la-moi. '
                      '<b>Pas de son ?</b> Vérifie MASTER. <b>Notes bloquées ?</b> REC maintenu (PANIC). <b>Secours :</b> OCT− maintenu à l’allumage, l’installateur marche toujours.')) + '</div>'))

    o = [f'<!doctype html>\n<!-- SPDX-License-Identifier: GPL-3.0-only -- K-WASUB: the manual, generated by source/tools/make_manual.py -->\n'
         f'<html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
         f'<title>K-WASUB · {t(T("Manual", "Manuel"))}</title>\n'
         f'<meta name="description" content="{t(T("The K-WASUB manual, short: the buttons, the pages, the live tools, the themes, the sound. A table of contents and a search box on the left.", "Le manuel de K-WASUB, en bref : les boutons, les pages, le jeu en direct, les thèmes, le son. Une table des matières et une recherche à gauche."))}">\n{CSS}</head><body>',
         f'<header class="top"><a class="logo" href="index.html">K-WA<b>SUB</b></a>\n<nav style="margin-left:auto;display:flex;gap:14px;align-items:center">' +
         f'<a href="{KOFI}" target="_blank" rel="noopener" style="color:#f08c3c;font-weight:700">☕ {t(T("Donate", "Don"))}</a>' +
         ('<a href="../manual.html" hreflang="en">EN</a><b style="color:var(--lime);font-size:.86rem">FR</b>' if fr else
          '<b style="color:var(--lime);font-size:.86rem">EN</b><a href="fr/manual.html" hreflang="fr">FR</a>') + '</nav></header>\n'
         '<div class="layout">'
         f'<aside class="side"><input type="search" id="q" placeholder="{t(T("Search the manual…", "Chercher dans le manuel…"))}" aria-label="{t(T("Search", "Recherche"))}">'
         '<ul class="side-toc" id="toc">' + "".join(f'<li><a href="#{a}">{t(n)}</a></li>' for a, n in nav) + '</ul></aside>'
         '<main>']
    o.append(f'<section class="hero"><h1>{t(T("The <em>K-WASUB</em> manual", "Le manuel de <em>K-WASUB</em>"))}</h1>'
             f'<p class="lead">{t(T("A modern bass synth for the M-VAVE FM-1. The 27 keys play, K1–K4 set what the screen shows (written at the bottom), the buttons open the pages. Short on purpose: what you see on the screen is not explained again.", "Un synthé de basses modernes pour le M-VAVE FM-1. Les 27 touches jouent, K1–K4 règlent ce que montre l’écran (écrit en bas), les boutons ouvrent les pages. Court exprès : ce qui se voit à l’écran n’est pas réexpliqué."))}</p>'
             f'<img src="{img}{"promo-fr" if fr else "promo"}.png" alt="K-WASUB"></section>')
    dbar = f'<div class="dbar"><span>{t(T("K-WASUB is free. If it helps your sounds, a coffee keeps it going.", "K-WASUB est gratuit. S’il t’aide pour tes sons, un café le fait avancer."))}</span><a href="{KOFI}" target="_blank" rel="noopener">{t(T("Donate on Ko-fi", "Faire un don sur Ko-fi"))}</a></div>'
    o.append(dbar)
    o.append('<ul class="feat">' + t(T(
        "<li><b>4 or 8 engines</b>, two oscillators, a sub, a sample / resample oscillator</li><li><b>LFO learn</b>: hold LFO, turn a knob</li>"
        "<li><b>FX PADS</b> with quantize, <b>PERFORM</b>, <b>MORPH</b> X/Y and A/B</li><li><b>SEQ BASS</b>, ARP, MIDI</li>"
        "<li>Deep, tight low end: OTT, MONO BASS, SUB LOCK, auto level</li><li><b>7 themes</b>, 26 palettes, 9 fonts</li>",
        "<li><b>4 ou 8 moteurs</b>, deux oscillateurs, un sub, un oscillateur sample / resample</li><li><b>LFO learn</b> : LFO maintenu, tourner un potard</li>"
        "<li><b>FX PADS</b> avec quantisation, <b>PERFORM</b>, <b>MORPH</b> X/Y et A/B</li><li><b>SEQ BASS</b>, ARP, MIDI</li>"
        "<li>Un grave profond et propre : OTT, MONO BASS, SUB LOCK, auto level</li><li><b>7 thèmes</b>, 26 palettes, 9 polices</li>")) + '</ul>'
             + f'<p class="more">{t(T("<b>And more is coming.</b> Tell me what would help you most; a donation, even small, helps enormously.", "<b>Et d’autres choses arrivent.</b> Dis-moi ce qui t’aiderait le plus ; un don, même petit, aide énormément."))}</p>')

    for a, title, html in chaps:
        o.append(f'<section class="chap" id="{a}"><h2>{title}</h2>{html}</section>')

    o.append(f'<p id="noq">{t(T("Nothing matches that search.", "Rien ne correspond à cette recherche."))}</p>')
    o.append(dbar)
    spec = "CAHIER-DES-CHARGES.md" if fr else "SPECIFICATIONS.md"
    o.append(f'<footer>{t(T("K-WASUB is free software (GPL-3.0), born from", "K-WASUB est un logiciel libre (GPL-3.0), né de"))} <a href="https://github.com/Guizmoh/Kawa-Tracker-Fm1">KAWA</a> (Omnipotard / Leo Kuroshita, Hügelton Instruments). '
             f'{t(T("Beta 0.9: not yet tried on every FM-1.", "Bêta 0.9 : pas encore essayé sur tous les FM-1."))} <a href="index.html">← {t(T("Home", "Accueil"))}</a> · <a href="{spec}">{t(T("Specifications", "Cahier des charges"))}</a></footer>')
    o.append('</main></div>')
    o.append(f'<a class="fab" href="{KOFI}" target="_blank" rel="noopener">☕ {t(T("Support K-WASUB", "Soutenir K-WASUB"))}</a>')
    o.append('''<script>
(function(){
  var q=document.getElementById("q"), toc=document.getElementById("toc"), noq=document.getElementById("noq");
  var chaps=[].slice.call(document.querySelectorAll(".chap"));
  var items=[].slice.call(toc.querySelectorAll("li"));
  q.addEventListener("input",function(){
    var v=q.value.trim().toLowerCase(), any=false;
    chaps.forEach(function(c){
      var hit=!v||c.textContent.toLowerCase().indexOf(v)>-1;
      c.classList.toggle("hide",!hit); if(hit)any=true;
    });
    items.forEach(function(li){
      var a=li.querySelector("a"), c=document.getElementById(a.getAttribute("href").slice(1));
      li.classList.toggle("nohit",!(!v||(c&&c.textContent.toLowerCase().indexOf(v)>-1)));
    });
    noq.style.display=(v&&!any)?"":"none";
  });
  if("IntersectionObserver" in window){
    var links={}; toc.querySelectorAll("a").forEach(function(a){links[a.getAttribute("href").slice(1)]=a;});
    var obs=new IntersectionObserver(function(es){
      es.forEach(function(e){var a=links[e.target.id]; if(a)a.classList.toggle("cur",e.isIntersecting);});
    },{rootMargin:"-10% 0px -70% 0px"});
    chaps.forEach(function(c){obs.observe(c);});
  }
})();
</script>''')
    o.append('</body></html>\n')
    return "\n".join(o)


Path("manual.html").write_text(build("en"))
Path("fr/manual.html").write_text(build("fr"))
print("manual.html", len(build("en")), "B; fr/manual.html", len(build("fr")), "B")
