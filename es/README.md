<p align="center"><img src="../docs/img/promo.png" alt="K-WASUB, sintetizador de graves moderno para el M-VAVE FM-1"></p>
<p align="center"><a href="https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/">https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/</a></p>

# K-WASUB · FM1 modern Bass firmware

**English** : [README](../README.md) · **Français** : [README](../fr/README.md) · **Español** : esta página

**Sintetizador de graves moderno para el M-VAVE FM-1**: DnB, dub, dubstep, techno. Wobble en vivo, reese, sub, 808, un EQ, un morph entre cuatro sonidos, efectos en las teclas. Gratuito y de código abierto (GPL-3.0). *Version 1.0.*

| | |
|---|---|
| 🎛 **Probarlo** (navegador) | [`emulator/index.html`](../emulator/index.html) |
| ⬇️ **Instalar** en el FM-1 | [`installer.html`](../installer.html) (Chrome o Edge, USB) · o `INSTALL-Windows.bat` / `INSTALL-Mac.command` / `INSTALL-Linux.sh` |
| 📖 **Manual** (en inglés o francés por ahora) | [`manual.html`](../manual.html) |
| 🏠 **Página de inicio** | [`index.html`](../index.html) (con GitHub Pages activo: <https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/>) |
| 🗺 **Especificaciones** | [`SPECIFICATIONS.md`](../SPECIFICATIONS.md): hecho, por hacer, ideas |
| 📜 Notas técnicas | [`docs/TECHNICAL-NOTES.md`](../docs/TECHNICAL-NOTES.md) |

## Funciones clave

1. **9 motores** por oscilador (ANALOG, **808**, CS, WAVETABLE, **FM 4 operadores**, **GROWL**, **ADDITIVE**, PHASE DIST, HARD SYNC), cada uno con un **FOLD** (CS: **RING**) detrás.
2. **Secuenciador de batería con condiciones y parameter locks** (también en el bajo: mantener un paso, girar un potenciómetro) y **automatización** (mantener REC durante la reproducción y girar cualquier potenciómetro; REC solo para borrar): 8 pistas de colores (kits 808, 909, dub techno, acústico), probabilidad y condiciones en cada paso, teclas negras para el instrumento, teclas blancas (pads) para sus pasos, OCT−/OCT+ para las páginas; REC en directo; salida sync para Pocket Operator y Volca.
3. **LFO learn**: mantén `LFO` y gira cualquier potenciómetro, el LFO 2 se asigna a ese ajuste en un gesto (con `OCT−`: LFO 1, con `OCT+`: LFO 3).
4. Modo **CLASSIC** o **SHIFT** (`OCT−` / `OCT+`) para ir más rápido, a elegir en las opciones.
5. **Ventanas SEL**: PERFORM, MORPH, FX LIVE, MACROS.
6. **Morph A/B**: mezcla dos sonidos en vivo.
7. **Tres LFO** (el tercero global: se queda al cambiar de sonido) y una **página de LFO** en vivo para remodelar tus graves wobble mientras tocas.
8. **SEQ BASS** (hasta 64 pasos, probabilidad, condiciones de disparo y duración de nota por paso, 30 presets, REC en directo), samples **OSC C** (ataques, texturas; inicio / fin recortados, más rápido o más lento, al revés, ping-pong), **DRUMS** (kits 808 / 909 / dub techno / acústico, 8 pistas de colores, presets de ritmo: techno, dub, dnb…), **ARP**, **MIDI**.
9. El sonido: motores, filtros, efectos, master, y **FX PADS**.
10. Visuales de osciladores animados, en vivo.
11. Un **EQ** visual.
12. **Temas** totalmente distintos, para adaptarse a tu forma de tocar.
13. **Brillo**, contraste, tipografías y tamaño.
14. **Idioma del firmware** (`SYSTEM › LANGUAGE`): English, Français o Español, inglés por defecto.

## Instalar

1. FM-1 por USB (cable de **datos**), otros programas MIDI cerrados.
2. Abre [`installer.html`](../installer.html) en Chrome o Edge → «Install K-WASUB».
3. Los paquetes están en [`install/`](../install/) (`k-wasub-X.fwsc`, los anteriores en `install/older/`, sumas de comprobación en `SHA256SUMS`).

Puedes volver a KAWA (`install/kawa-0.5.fwsc`) o al firmware de fábrica (M-UPGRADE) en cualquier momento; mantener `OCT−` al encender = rescate USB.

## Compilar

```sh
cd source
./build.sh --release 1.0.35          # -> build/k-wasub-1.0.35.fwsc
APP_VER=1.0.35 bash web/make_emulator.sh      # emulador
bash web/make_installer.sh                    # installer.html con el último paquete
bash tests/run_stress.sh                      # pruebas de carga (UBSan)
python3 tests/manual_shots.py                 # capturas del manual (docs/img)
```
Toolchain de JieLi y SDK AC79: ver `source/BUILDING.md` y `source/tools/get_toolchain.sh`.

## Apoyo

☕ [ko-fi.com/omnipotard](https://ko-fi.com/omnipotard)

## Créditos y licencia

GPL-3.0. K-WASUB nace de [KAWA](https://github.com/Guizmoh/Kawa-Tracker-Fm1) (Omnipotard / Leo Kuroshita, Hügelton Instruments), cuya plataforma FM-1 reutiliza (arranque, USB, audio, pantalla). Ver [`LICENSING.md`](../LICENSING.md). No afiliado a M-VAVE.
