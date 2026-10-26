/* SPDX-License-Identifier: GPL-3.0-only */
/* K-WASUB: drawing (as KAWA's): the screen is drawn in six bands of 240 x 40, each hashed and sent only if
 * it changed, two send buffers taking turns. Text: DejaVu Sans Bold in five sizes, 16 grey levels. */
#define BAND_H 40u
#define NBAND 6u
static uint16_t g_buf[240u * BAND_H] POOL;
static uint16_t g_txb[240u * BAND_H] POOL;
static int32_t g_y0;
static uint32_t g_hash[NBAND];
static uint8_t g_force = 1, g_tx;

/* the colours: six palettes for each theme (ksub_draw.c): its own, another, SYNTHWAVE, MINT, black and white, inverted */
enum { KC_BG, KC_PANEL, KC_LINE, KC_LIME, KC_LIMED, KC_CYAN, KC_WHITE, KC_GREY, KC_TRACK, KC_ORANGE, KC_WAVE, KC_INK, KC_MOD, KC_N };
#define C3(r, g, b) RGB(r, g, b)
static const uint16_t PALS[23][KC_N] = {
    /* CLASSIC: NEON, AMBER */
    {C3(11,18,20), C3(17,27,30), C3(40,56,60), C3(200,240,60), C3(30,40,20), C3(80,216,208), C3(236,242,242), C3(130,146,148), C3(36,52,56), C3(240,140,60), C3(200,240,60), C3(11,18,20), C3(170,140,250)},
    {C3(18,12,6), C3(30,20,10), C3(66,44,20), C3(255,170,40), C3(52,34,10), C3(255,214,140), C3(250,238,220), C3(170,140,110), C3(60,40,20), C3(255,90,60), C3(255,170,40), C3(18,12,6), C3(255,214,140)},
    /* STUDIO: STUDIO, OCEAN */
    {C3(10,14,16), C3(22,30,33), C3(44,58,62), C3(200,240,60), C3(30,40,20), C3(80,216,208), C3(240,244,244), C3(140,156,158), C3(44,58,62), C3(240,140,60), C3(200,240,60), C3(10,14,16), C3(170,140,250)},
    {C3(8,14,30), C3(16,26,50), C3(36,54,90), C3(80,200,255), C3(16,40,70), C3(255,120,200), C3(236,244,255), C3(130,150,180), C3(36,54,90), C3(255,170,60), C3(80,200,255), C3(8,14,30), C3(255,120,200)},
    /* PURE: PURE, PURE RED */
    {C3(28,28,32), C3(42,42,47), C3(62,62,70), C3(204,240,58), C3(50,50,58), C3(160,132,248), C3(238,238,242), C3(150,150,162), C3(60,60,68), C3(240,150,70), C3(160,132,248), C3(20,20,22), C3(160,132,248)},
    {C3(28,26,28), C3(44,40,42), C3(70,62,64), C3(255,90,70), C3(60,36,34), C3(255,190,120), C3(244,238,236), C3(160,150,150), C3(70,62,64), C3(255,200,60), C3(255,190,120), C3(24,20,20), C3(255,190,120)},
    /* RACK: RACK, MAGMA */
    {C3(8,10,12), C3(20,24,27), C3(40,46,50), C3(210,245,70), C3(32,42,16), C3(90,220,210), C3(250,250,250), C3(150,160,164), C3(40,46,50), C3(240,140,60), C3(90,220,210), C3(8,10,12), C3(175,145,255)},
    {C3(10,8,8), C3(26,18,16), C3(56,36,30), C3(255,120,40), C3(50,24,12), C3(255,214,80), C3(255,246,236), C3(170,140,120), C3(56,36,30), C3(255,60,60), C3(255,214,80), C3(10,8,8), C3(255,170,120)},
    /* for every theme: SYNTHWAVE, MINT */
    {C3(18,8,30), C3(32,16,52), C3(70,40,100), C3(255,70,200), C3(60,20,70), C3(80,230,255), C3(250,236,255), C3(170,140,200), C3(64,36,90), C3(255,160,60), C3(255,70,200), C3(18,8,30), C3(80,230,255)},
    {C3(8,20,16), C3(14,34,28), C3(34,70,58), C3(120,255,190), C3(20,60,44), C3(255,230,140), C3(230,255,244), C3(120,170,150), C3(30,64,52), C3(255,140,90), C3(120,255,190), C3(8,20,16), C3(255,230,140)},
    /* MONO: white on black (classic); INVERT: greys, dark on light, the cards a shade darker (as through a tint) */
    {C3(0,0,0), C3(16,16,16), C3(70,70,70), C3(255,255,255), C3(48,48,48), C3(200,200,200), C3(255,255,255), C3(140,140,140), C3(50,50,50), C3(255,255,255), C3(255,255,255), C3(0,0,0), C3(200,200,200)},
    {C3(206,209,212), C3(184,188,192), C3(156,160,165), C3(0,0,0), C3(160,164,170), C3(0,0,0), C3(0,0,0), C3(70,74,80), C3(166,170,175), C3(0,0,0), C3(0,0,0), C3(222,224,226), C3(70,74,90)},
    /* RED (the STUDIO look in red), ICE */
    {C3(14,8,9), C3(30,14,16), C3(66,30,34), C3(255,64,72), C3(62,14,18), C3(255,150,120), C3(248,236,236), C3(170,130,132), C3(58,26,30), C3(255,190,60), C3(255,64,72), C3(14,8,9), C3(255,140,170)},
    {C3(8,14,22), C3(16,26,40), C3(38,56,80), C3(150,220,255), C3(20,44,66), C3(220,240,255), C3(236,246,255), C3(130,156,180), C3(34,52,74), C3(255,180,90), C3(150,220,255), C3(8,14,22), C3(190,170,255)},
    /* FLUO: one fluorescent green on a deep black-green, the rest quiet (mint for the second, amber for warnings) */
    {C3(2,7,4), C3(8,18,11), C3(24,48,31), C3(57,255,20), C3(12,46,10), C3(150,255,200), C3(236,255,242), C3(112,150,126), C3(20,40,27), C3(255,214,64), C3(57,255,20), C3(2,7,4), C3(190,255,120)},
    /* GLOW (its own two): FLUO GREEN, TOXIC (a yellow-green); the panels deep, the accent bright: the gradients go from one to the other */
    {C3(1,6,3), C3(6,22,12), C3(20,62,34), C3(57,255,20), C3(10,70,16), C3(90,255,190), C3(240,255,244), C3(110,160,128), C3(16,44,26), C3(255,200,60), C3(57,255,20), C3(1,6,3), C3(0,230,180)},
    {C3(4,6,1), C3(16,22,4), C3(52,66,12), C3(198,255,0), C3(54,78,0), C3(120,240,255), C3(250,255,232), C3(150,165,110), C3(36,46,10), C3(255,150,40), C3(198,255,0), C3(4,6,1), C3(120,240,255)},
    /* for every theme too: PINK, GOLD */
    {C3(16,4,12), C3(34,10,26), C3(76,26,60), C3(255,60,170), C3(80,12,52), C3(120,230,255), C3(255,236,248), C3(180,130,160), C3(62,20,48), C3(255,190,60), C3(255,60,170), C3(16,4,12), C3(170,140,255)},
    {C3(12,9,2), C3(28,22,6), C3(70,56,16), C3(255,196,40), C3(72,52,8), C3(255,240,180), C3(255,250,236), C3(176,160,120), C3(56,44,14), C3(255,110,50), C3(255,196,40), C3(12,9,2), C3(255,140,90)},
    /* TECH (its own two): VOLT (fluo green, an ice white-cyan beside it), CYBER (electric cyan, magenta beside it) */
    {C3(2,5,6), C3(8,18,16), C3(22,50,44), C3(57,255,20), C3(8,56,20), C3(120,255,230), C3(240,255,250), C3(104,150,140), C3(16,38,34), C3(255,200,60), C3(57,255,20), C3(2,5,6), C3(120,255,230)},
    {C3(2,4,10), C3(8,14,30), C3(22,40,80), C3(0,225,255), C3(6,48,76), C3(255,70,200), C3(238,250,255), C3(104,136,170), C3(16,30,60), C3(255,190,60), C3(0,225,255), C3(2,4,10), C3(255,70,200)},
    /* for every theme: SKY (light: white cards on a pale blue, navy text, a clear blue accent), BLAZE (black, greys, fluo orange, the text white) */
    {C3(226,238,250), C3(252,253,255), C3(176,198,222), C3(18,108,210), C3(206,226,250), C3(0,150,196), C3(8,22,44), C3(70,92,118), C3(200,216,234), C3(226,104,16), C3(18,108,210), C3(255,255,255), C3(120,76,206)},
    {C3(0,0,0), C3(22,22,24), C3(72,72,76), C3(255,112,0), C3(70,30,0), C3(170,170,176), C3(255,255,255), C3(176,176,182), C3(46,46,50), C3(255,60,40), C3(255,128,0), C3(0,0,0), C3(255,176,64)},
};
static const char *const PAL_NAME[5][2] = {{"FLUO GREEN", "TOXIC"}, {"STUDIO", "OCEAN"}, {"PURE", "PURE RED"}, {"RACK", "MAGMA"}, {"VOLT", "CYBER"}};
static uint16_t kc[KC_N];
static uint8_t theme, theme_pal, g_rad;        /* (g_rad: a RAD palette, the gradient version of theme_pal) */
#define NPAL_BASE 13u                           /* the palettes: 0..12, then their RAD versions 13..25 */
#define PAL_SKY 11u
static uint16_t g_rtop, g_rbot, g_rcell;        /* RAD: the background's top and bottom, the cards' bottom */
static uint8_t g_wgrad, g_sky;                  /* (g_sky: SKY, office-like: square windows in relief, with a shadow) */                         /* 1: the oscillator's line yellow -> orange -> light red (SYNTHWAVE RAD) */
#define PAL_BW (theme_pal == 4u || theme_pal == 5u)   /* black and white, inverted: no colours of their own */
static uint16_t g_mix(uint16_t a, uint16_t b, uint32_t t);
static uint8_t g_con, g_bri = 3;                /* BRIGHTNESS: 0 ECO, 1 NORMAL, 2 BRIGHT, 3 MAX */
static uint32_t bri_ch(uint32_t v, uint32_t f, uint32_t max) { v = v * f >> 8; return v > max ? max : v; }
static uint16_t bri_px(uint16_t c, uint32_t f)  /* every channel x f / 256 (f > 256: brighter, to the channel's top) */
{
    return (uint16_t)(bri_ch(c >> 11, f, 31u) << 11 | bri_ch((c >> 5) & 63u, f, 63u) << 5 | bri_ch(c & 31u, f, 31u));
}
/* CONTRAST: 0 as drawn, 1 HIGH and 2 MAX: the background to black, the text to white */
static uint32_t con_ch(uint32_t v, uint32_t a, uint32_t b)   /* one channel (8 bits): a -> 0, b -> 255 (a > b: reversed) */
{
    if (a > b) return 255u - con_ch(255u - v, 255u - a, 255u - b);
    if (b <= a + 8u) return v;
    return v <= a ? 0u : v >= b ? 255u : (v - a) * 255u / (b - a);
}
static uint16_t con_px(uint16_t c, uint16_t bg, uint16_t wh)
{
    uint32_t r = con_ch((c >> 11) * 255u / 31u, (bg >> 11) * 255u / 31u, (wh >> 11) * 255u / 31u);
    uint32_t g = con_ch(((c >> 5) & 63u) * 255u / 63u, ((bg >> 5) & 63u) * 255u / 63u, ((wh >> 5) & 63u) * 255u / 63u);
    uint32_t b = con_ch((c & 31u) * 255u / 31u, (bg & 31u) * 255u / 31u, (wh & 31u) * 255u / 31u);
    return RGB(r, g, b);
}
static uint32_t lum8(uint16_t c) { return ((c >> 11) * 255u / 31u * 77u + ((c >> 5) & 63u) * 255u / 63u * 150u + (c & 31u) * 255u / 31u * 29u) >> 8; }
static void lum_gap(uint32_t k, uint32_t min)   /* a text colour too close to the background (in luminance): pushed to white or black, whichever is farther */
{
    uint32_t b = lum8(kc[KC_BG]), t = lum8(kc[k]);
    if ((t > b ? t - b : b - t) < min) kc[k] = b < 128u ? 0xFFFFu : 0x0000u;
}
static void theme_set(uint32_t t, uint32_t pal)
{
    uint32_t i, k;
    theme = (uint8_t)(t < 5u ? t : 0u);
    g_rad = (uint8_t)(pal >= NPAL_BASE && pal < 2u * NPAL_BASE);
    theme_pal = (uint8_t)(pal < NPAL_BASE ? pal : pal < 2u * NPAL_BASE ? pal - NPAL_BASE : 0u);
    k = theme_pal < 2u ? (theme == 0u ? 15u : theme < 4u ? theme * 2u : 19u) + theme_pal : theme_pal < 9u ? 6u + theme_pal : theme_pal < 11u ? 8u + theme_pal : 10u + theme_pal;   /* (rows: 4 themes x 2, 7 for all, GLOW's 2, 2 more for all, TECH's 2, SKY and BLAZE) */
    for (i = 0; i < KC_N; i++) kc[i] = g_con && theme_pal != PAL_SKY ? con_px(PALS[k][i], PALS[k][KC_BG], PALS[k][KC_WHITE]) : PALS[k][i];   /* (SKY keeps its pale blue) */
    g_rtop = g_mix(kc[KC_BG], kc[KC_LIME], 110); g_rbot = g_mix(kc[KC_BG], kc[KC_CYAN], 110); g_rcell = g_mix(kc[KC_BG], kc[KC_CYAN], 60);
    g_wgrad = 0;
    g_sky = theme_pal == PAL_SKY;
    if (g_rad && theme == 0u && theme_pal == 0u) {   /* CLASSIC GLOW, FLUO GREEN RAD: a deeper, bluer green into a night blue, the line yellow */
        g_rtop = RGB(10, 74, 66); g_rbot = RGB(3, 7, 30); g_rcell = RGB(4, 22, 40);
        kc[KC_WAVE] = RGB(255, 222, 40);
    } else if (g_rad && theme_pal == 2u) {      /* SYNTHWAVE RAD: violet into a very dark blue-violet, the line yellow to orange to light red */
        g_rtop = RGB(74, 22, 110); g_rbot = RGB(10, 6, 30); g_rcell = RGB(20, 10, 46);
        kc[KC_WAVE] = RGB(255, 140, 20); g_wgrad = 1;
    }
    if (g_con && theme_pal != PAL_SKY) {        /* (the cards stay apart from the background) */
        kc[KC_PANEL] = g_mix(kc[KC_PANEL], PALS[k][KC_PANEL], 128u);
    }
    lum_gap(KC_WHITE, 120u); lum_gap(KC_GREY, 70u); lum_gap(KC_LIME, 70u);   /* (the text always stands off its background) */
    if (g_bri < 3u) {                           /* ECO, NORMAL, BRIGHT: every channel scaled on its own; MAX: the colours as drawn */
        static const uint16_t F[3] = {104, 168, 218};
        for (i = 0; i < KC_N; i++) kc[i] = bri_px(kc[i], F[g_bri]);
    }
}
#define K_BG kc[KC_BG]
#define K_PANEL kc[KC_PANEL]
#define K_LINE kc[KC_LINE]
#define K_LIME kc[KC_LIME]
#define K_LIMED kc[KC_LIMED]
#define K_CYAN kc[KC_CYAN]
#define K_WHITE kc[KC_WHITE]
#define K_GREY kc[KC_GREY]
#define K_TRACK kc[KC_TRACK]
#define K_ORANGE kc[KC_ORANGE]
#define K_WAVE kc[KC_WAVE]
#define K_INK kc[KC_INK]
#define K_MOD kc[KC_MOD]

/* the fonts: four families (SANS DejaVu Sans Bold, MONO IBM Plex Mono, HYPER Atkinson Hyperlegible Mono, PIXEL
 * Press Start 2P), five sizes */
static const ks_font_t *const FAMS[4][5] = {{&F_XS, &F_S, &F_M, &F_B, &F_L}, {&F_GXS, &F_GS, &F_GM, &F_GB, &F_GL},
                                           {&F_HXS, &F_HS, &F_HM, &F_HB, &F_HL}, {&F_PXS, &F_PS, &F_PM, &F_PB, &F_PL}};
static uint8_t g_bold;                          /* (HYPER is light: drawn twice, a pixel apart) */
static const ks_font_t *tf[5] = {&F_XS, &F_S, &F_M, &F_B, &F_L};
static const ks_font_t *const ZOOM[3][2] = {{&F_FZS, &F_FZM}, {&F_GZS, &F_GZM}, {&F_HZS, &F_HZM}};   /* LOUPE: S and M bigger */
static void font_set(uint32_t f, uint32_t zoom)   /* (SKY: always HYPER, the most readable, drawn a little thick) */
{
    uint32_t i;
    if (theme_pal == PAL_SKY) f = 2u;
    for (i = 0; i < 5u; i++) tf[i] = FAMS[f & 3u][i];
    if (zoom && (f & 3u) < 3u) { tf[1] = ZOOM[f & 3u][0]; tf[2] = ZOOM[f & 3u][1]; }
    g_bold = (f & 3u) == 2u;
}
#define T_XS tf[0]
#define T_S tf[1]
#define T_M tf[2]
#define T_B tf[3]
#define T_L tf[4]

static int g_vis(int32_t y, int32_t h) { return y < g_y0 + (int32_t)BAND_H && y + h > g_y0; }
static uint16_t g_mix(uint16_t a, uint16_t b, uint32_t t)   /* a .. b, t = 0..256 */
{
    uint32_t ar = a >> 11, ag = (a >> 5) & 63u, ab = a & 31u, br = b >> 11, bg = (b >> 5) & 63u, bb = b & 31u;
    ar = (ar * (256u - t) + br * t) >> 8;
    ag = (ag * (256u - t) + bg * t) >> 8;
    ab = (ab * (256u - t) + bb * t) >> 8;
    return (uint16_t)(ar << 11 | ag << 5 | ab);
}
static void g_rect(int32_t x, int32_t y, int32_t w, int32_t h, uint16_t c)
{
    int32_t x1 = x + w, y1 = y + h, i;
    if (x < 0) x = 0;
    if (x1 > 240) x1 = 240;
    if (y < g_y0) y = g_y0;
    if (y1 > g_y0 + (int32_t)BAND_H) y1 = g_y0 + (int32_t)BAND_H;
    for (; y < y1; y++) {
        uint16_t *p = &g_buf[(uint32_t)(y - g_y0) * 240u];
        for (i = x; i < x1; i++) p[i] = c;
    }
}
static void g_px(int32_t x, int32_t y, uint16_t c)
{
    y -= g_y0;
    if ((uint32_t)x < 240u && (uint32_t)y < BAND_H) g_buf[(uint32_t)y * 240u + (uint32_t)x] = c;
}
static void g_pxa(int32_t x, int32_t y, uint16_t c, uint32_t t)   /* a pixel blended in (t 0..256) */
{
    y -= g_y0;
    if ((uint32_t)x < 240u && (uint32_t)y < BAND_H) {
        uint16_t *p = &g_buf[(uint32_t)y * 240u + (uint32_t)x];
        *p = g_mix(*p, c, t);
    }
}
static void g_box(int32_t x, int32_t y, int32_t w, int32_t h, uint16_t fill, uint16_t edge)   /* rounded, 1 px edge */
{
    if (g_sky && w >= 8 && h >= 8) {            /* SKY: square, a shadow below and right, lit from the top (a bevel), a light gradient */
        int32_t j;
        uint16_t sh = g_mix(kc[KC_BG], RGB(20, 50, 100), 70), hi = g_mix(fill, 0xFFFFu, 150), lo = g_mix(fill, RGB(40, 80, 140), 40);
        if (!g_vis(y, h + 2)) return;
        g_rect(x + 2, y + h, w, 2, sh);
        g_rect(x + w, y + 2, 2, h - 2, sh);
        g_rect(x, y, w, h, edge);
        for (j = 1; j < h - 1; j++) g_rect(x + 1, y + j, w - 2, 1, g_mix(hi, lo, (uint32_t)(j * 256 / h)));
        g_rect(x + 1, y + 1, w - 2, 1, 0xFFFFu);   /* (the bevel: a white top edge, a darker bottom one) */
        g_rect(x + 1, y + h - 2, w - 2, 1, g_mix(edge, fill, 90));
        return;
    }
    if (!g_vis(y, h)) return;
    g_rect(x + 1, y, w - 2, h, edge);
    g_rect(x, y + 1, w, h - 2, edge);
    g_rect(x + 1, y + 1, w - 2, h - 2, fill);
    g_px(x + 1, y + 1, edge);
    g_px(x + w - 2, y + 1, edge);
    g_px(x + 1, y + h - 2, edge);
    g_px(x + w - 2, y + h - 2, edge);
}
/* a setting's bar: the part up to the knob a little softer, the knob's place a sharp line, a light fade on each side */
static void g_hgrad(int32_t x, int32_t y, int32_t w, int32_t h, uint16_t c0, uint16_t c1)   /* left c0 .. right c1 */
{
    int32_t i;
    if (w <= 0 || !g_vis(y, h)) return;
    for (i = 0; i < w; i++) g_rect(x + i, y, 1, h, g_mix(c0, c1, (uint32_t)(i * 256 / w)));
}
static void g_vgrad(int32_t x, int32_t y, int32_t w, int32_t h, uint16_t c0, uint16_t c1)   /* top c0 .. bottom c1 (this band only) */
{
    int32_t j = y > g_y0 ? y : g_y0, e = y + h < g_y0 + (int32_t)BAND_H ? y + h : g_y0 + (int32_t)BAND_H;
    for (; j < e; j++) g_rect(x, j, w, 1, g_mix(c0, c1, (uint32_t)((j - y) * 256 / h)));
}
static void g_vbar(int32_t x, int32_t y, int32_t w, int32_t h, uint32_t frac, uint16_t c)   /* frac 0..256 */
{
    int32_t f = (int32_t)((uint32_t)(w - 2) * frac >> 8), i;
    uint16_t soft = g_mix(K_TRACK, c, 150);
    if (!g_vis(y, h)) return;
    g_rect(x, y, w, h, K_TRACK);
    if (f > 0) g_rect(x, y, f, h, soft);
    for (i = 1; i <= 6; i++) {
        uint32_t t = 256u - (uint32_t)i * 34u;
        if (f - i >= 0) g_rect(x + f - i, y, 1, h, g_mix(soft, c, t));
        if (f + 1 + i < w) g_rect(x + f + 1 + i, y, 1, h, g_mix(K_TRACK, c, t * 3u / 4u));
    }
    g_rect(x + f, y, 2, h, c);
    if (h > 3) { g_px(x, y, K_BG); g_px(x, y + h - 1, K_BG); g_px(x + w - 1, y, K_BG); g_px(x + w - 1, y + h - 1, K_BG); }
}
static void g_bar(int32_t x, int32_t y, int32_t w, int32_t h, uint32_t frac, uint16_t c)   /* frac 0..256 */
{
    int32_t f = (int32_t)((uint32_t)w * frac >> 8);
    if (!g_vis(y, h)) return;
    g_rect(x, y, w, h, K_TRACK);
    if (f > 0) g_rect(x, y, f, h, c);
    if (h > 3) {                                /* rounded ends */
        g_px(x, y, K_BG); g_px(x, y + h - 1, K_BG); g_px(x + w - 1, y, K_BG); g_px(x + w - 1, y + h - 1, K_BG);
    }
}
static void g_line(int32_t x0, int32_t y0, int32_t x1, int32_t y1, uint16_t c)   /* (anti-aliased in y) */
{
    int32_t dx = x1 - x0, dy = y1 - y0, n = (dx < 0 ? -dx : dx) > (dy < 0 ? -dy : dy) ? (dx < 0 ? -dx : dx) : (dy < 0 ? -dy : dy), i;
    if (!n) { g_px(x0, y0, c); return; }
    if ((y0 < g_y0 - 1 && y1 < g_y0 - 1) || (y0 > g_y0 + (int32_t)BAND_H && y1 > g_y0 + (int32_t)BAND_H)) return;
    for (i = 0; i <= n; i++) {
        int32_t x = x0 + dx * i / n, y8 = (y0 << 8) + (dy << 8) * i / n, fy = y8 & 255;
        g_pxa(x, y8 >> 8, c, 256u - (uint32_t)fy);
        g_pxa(x, (y8 >> 8) + 1, c, (uint32_t)fy);
    }
}

static int32_t g_text(const ks_font_t *f, int32_t x, int32_t y, const char *s, uint16_t c)
{
    int vis = g_vis(y, f->h);
    for (; *s; s++) {
        uint32_t ch = (uint8_t)*s, w, bpr, gx, gy;
        const uint8_t *d;
        if (ch == 0xB7) ch = f->last;           /* the middle dot */
        if (ch >= 'a' && ch <= 'z' && f->last < 'a') ch -= 32u;
        if (ch < f->first || ch > f->last) ch = '?';
        w = f->adv[ch - f->first];
        if (vis) {
            bpr = (w + 1u) / 2u;
            d = f->data + f->off[ch - f->first];
            for (gy = 0; gy < f->h; gy++) {
                int32_t py = y + (int32_t)gy - g_y0;
                uint16_t *row;
                if ((uint32_t)py >= BAND_H) continue;
                row = &g_buf[(uint32_t)py * 240u];
                for (gx = 0; gx < w; gx++) {
                    uint32_t v = d[gy * bpr + gx / 2u];
                    int32_t px = x + (int32_t)gx;
                    v = (gx & 1u) ? (v & 15u) : (v >> 4);
                    if (v && (uint32_t)px < 240u) row[px] = v >= 15u ? c : g_mix(row[px], c, v * 17u);
                    if (v && g_bold && (uint32_t)(px + 1) < 240u) row[px + 1] = v >= 15u ? c : g_mix(row[px + 1], c, v * 17u);
                }
            }
        }
        x += (int32_t)w;
    }
    return x;
}
static int32_t g_text_w(const ks_font_t *f, const char *s)
{
    int32_t w = 0;
    for (; *s; s++) {
        uint32_t ch = (uint8_t)*s;
        if (ch == 0xB7) ch = f->last;
        if (ch >= 'a' && ch <= 'z' && f->last < 'a') ch -= 32u;
        if (ch < f->first || ch > f->last) ch = '?';
        w += f->adv[ch - f->first];
    }
    return w;
}
static void g_text_r(const ks_font_t *f, int32_t xr, int32_t y, const char *s, uint16_t c) { g_text(f, xr - g_text_w(f, s), y, s, c); }
static void g_text_c(const ks_font_t *f, int32_t xc, int32_t y, const char *s, uint16_t c) { g_text(f, xc - g_text_w(f, s) / 2, y, s, c); }

static char *str_cat(char *p, const char *s) { while (*s) *p++ = *s++; *p = 0; return p; }
static const ks_font_t *g_fit(const ks_font_t *f, const char *t, int32_t w)   /* f, or the next size down that fits w */
{
    int32_t i;
    for (i = 4; i > 0 && tf[i] != f; i--) {}
    while (i > 0 && g_text_w(tf[i], t) > w) i--;
    return tf[i];
}
static char *fmt_u(char *p, uint32_t v, uint32_t digits)
{
    char t[12];
    uint32_t n = 0;
    do { t[n++] = (char)('0' + v % 10u); v /= 10u; } while (v || n < digits);
    while (n) *p++ = t[--n];
    *p = 0;
    return p;
}
static char *fmt_s(char *p, int32_t v)          /* with its sign */
{
    *p++ = v < 0 ? '-' : '+';
    return fmt_u(p, (uint32_t)(v < 0 ? -v : v), 0);
}

/* one frame: draw() for each band, send what changed; poll in between (USB) */
static void g_frame_send(void (*draw)(void))
{
    uint32_t b;
    for (b = 0; b < NBAND; b++) {
        uint32_t h = 2166136261u, i, *w = (uint32_t *)g_buf;
        uint16_t *tx;
        g_y0 = (int32_t)(b * BAND_H);
        draw();
        for (i = 0; i < 240u * BAND_H / 2u; i++) h = (h ^ w[i]) * 16777619u;
        if (h == g_hash[b] && !g_force) { platform_poll(); continue; }
        g_hash[b] = h;
        tx = g_tx ? g_txb : cv_px;
        g_tx ^= 1u;
        for (i = 0; i < 240u * BAND_H; i++) { uint16_t c = g_buf[i]; tx[i] = (uint16_t)(c >> 8 | c << 8); }
        lcd_blit(0, b * BAND_H, 240, BAND_H, tx);
        platform_poll();
    }
    g_force = 0;
}
