<p align="center"><img src="../docs/img/promo.png" alt="K-WASUB, sintetizador de graves moderno para el M-VAVE FM-1"></p>

# K-WASUB · FM1 modern Bass firmware

**English** : [README](../README.md) · **Français** : [README](../fr/README.md) · **Español** : esta página

**Sintetizador de graves moderno para el M-VAVE FM-1**: DnB, dub, dubstep, techno. Wobble en vivo, reese, sub, 808, un EQ, un morph entre cuatro sonidos, efectos en las teclas. Gratuito y de código abierto (GPL-3.0). *Beta 0.9.*

| | |
|---|---|
| 🎛 **Probarlo** (navegador) | [`emulator/index.html`](../emulator/index.html) |
| ⬇️ **Instalar** en el FM-1 | [`installer.html`](../installer.html) (Chrome o Edge, USB) · o `INSTALL-Windows.bat` / `INSTALL-Mac.command` / `INSTALL-Linux.sh` |
| 📖 **Manual** (en inglés o francés por ahora) | [`manual.html`](../manual.html) |
| 🏠 **Página de inicio** | [`index.html`](../index.html) (con GitHub Pages activo: <https://guizmoh.github.io/K-WASUB_Firmware_for_FM1/>) |
| 🗺 **Especificaciones** | [`SPECIFICATIONS.md`](../SPECIFICATIONS.md): hecho, por hacer, ideas |
| 📜 Notas técnicas | [`docs/TECHNICAL-NOTES.md`](../docs/TECHNICAL-NOTES.md) |

## Funciones clave

1. **4 motores eficientes** para graves modernos, o **8 motores** para bajo, pads y leads (`SYSTEM › ENGINES`).
2. **LFO learn**: mantén `LFO` y gira cualquier potenciómetro, el LFO 2 se asigna a ese ajuste en un gesto.
3. Modo **CLASSIC** o **SHIFT** (`OCT−` / `OCT+`) para ir más rápido, a elegir en las opciones.
4. **Ventanas SEL**: PERFORM, MORPH, FX LIVE, MACROS.
5. **Morph A/B**: mezcla dos sonidos en vivo.
6. Una **página de LFO** en vivo para remodelar tus graves wobble mientras tocas.
7. **SEQ BASS** (hasta 64 pasos, probabilidad y condiciones de disparo por paso), **ARP**, **MIDI**.
8. El sonido: motores, filtros, efectos, master, y **FX PADS**.
9. Visuales de osciladores animados, en vivo.
10. Un **EQ** visual.
11. **Temas** totalmente distintos, para adaptarse a tu forma de tocar.
12. **Brillo**, contraste, tipografías y tamaño.
13. **Idioma del firmware** (`SYSTEM › LANGUAGE`): English, Français o Español, inglés por defecto.

## Instalar

1. FM-1 por USB (cable de **datos**), otros programas MIDI cerrados.
2. Abre [`installer.html`](../installer.html) en Chrome o Edge → «Install K-WASUB».
3. Los paquetes están en [`install/`](../install/) (`k-wasub-X.fwsc`, los anteriores en `install/older/`, sumas de comprobación en `SHA256SUMS`).

Puedes volver a KAWA (`install/kawa-0.5.fwsc`) o al firmware de fábrica (M-UPGRADE) en cualquier momento; mantener `OCT−` al encender = rescate USB.

## Compilar

```sh
cd source
./build.sh --release 0.9.50          # -> build/k-wasub-0.9.50.fwsc
APP_VER=0.9.50 bash web/make_emulator.sh      # emulador
bash web/make_installer.sh                    # installer.html con el último paquete
bash tests/run_stress.sh                      # pruebas de carga (UBSan)
python3 tests/manual_shots.py                 # capturas del manual (docs/img)
```
Toolchain de JieLi y SDK AC79: ver `source/BUILDING.md` y `source/tools/get_toolchain.sh`.

## Apoyo

☕ [ko-fi.com/omnipotard](https://ko-fi.com/omnipotard)

## Créditos y licencia

GPL-3.0. K-WASUB nace de [KAWA](https://github.com/Guizmoh/Kawa-Tracker-Fm1) (Omnipotard / Leo Kuroshita, Hügelton Instruments), cuya plataforma FM-1 reutiliza (arranque, USB, audio, pantalla). Ver [`LICENSING.md`](../LICENSING.md). No afiliado a M-VAVE.
