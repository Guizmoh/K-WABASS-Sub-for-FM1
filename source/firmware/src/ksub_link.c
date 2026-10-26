/* SPDX-License-Identifier: GPL-3.0-only */
/* K-WASUB: the link with the web page (DATA): the backup of the sound design (the 32 user slots, SEQ BASS / ARP /
 * MACROS / CC / EQ / MORPH, the slots' rest) read out and written back, over the USB-MIDI SysEx the updater uses.
 *
 * Frames (between F0 and F7, every byte 7 bits): 7D 4B 57 cmd pack7(body)        (7D: non-commercial; "KW")
 * the answer:                                    7D 4B 57 cmd|40 pack7(body)
 *   01 HELLO                         -> proto, blob size (u16), the version (text)
 *   02 READ  off u16, n u8 (<= 128)  -> off u16, n, the bytes
 *   03 BEGIN size u16                -> status
 *   04 WRITE off u16, n u8, bytes    -> off u16, status
 *   05 COMMIT crc16 (u16)            -> status (sent once written: the flash work is done from the main loop)
 * status: 0 ok, 1 bad size / offset, 2 bad crc, 3 not a K-WASUB backup (or another layout), 4 flash failed, 5 busy
 * The blob: "KSB1", the sizes of the three parts (u16 each), then ustore, perf, uext. Little endian. */
#define LK_PROTO 1u
#define LK_HEAD 10u
#define LK_SIZE (LK_HEAD + sizeof ustore + sizeof perf + sizeof uext)
typedef char lk_fits[LK_SIZE < 65536u ? 1 : -1];
static uint8_t lk_stage[LK_SIZE], lk_out[2 + 3 + 1 + 160];
static uint32_t lk_got, lk_want;                /* staged bytes; the size BEGIN announced (0: no restore under way) */
static uint8_t lk_commit;                       /* 1: COMMIT asked, the main loop writes */
static uint16_t lk_commit_crc;

static uint32_t lk_crc16(const uint8_t *p, uint32_t n)   /* (poly 0x1021, init 0: as the updater's) */
{
    uint32_t c = 0, i;
    while (n--) {
        c ^= (uint32_t)*p++ << 8;
        for (i = 0; i < 8u; i++) c = c & 0x8000u ? (c << 1) ^ 0x1021u : c << 1;
        c &= 0xFFFFu;
    }
    return c;
}
static uint32_t lk_pack7(const uint8_t *in, uint32_t n, uint8_t *out)   /* 8 bits to 7, LSB first */
{
    uint32_t acc = 0, nb = 0, o = 0;
    while (n--) {
        acc |= (uint32_t)*in++ << nb;
        nb += 8u;
        while (nb >= 7u) { out[o++] = (uint8_t)(acc & 0x7Fu); acc >>= 7; nb -= 7u; }
    }
    if (nb) out[o++] = (uint8_t)(acc & 0x7Fu);
    return o;
}
static uint32_t lk_unpack7(const uint8_t *in, uint32_t n, uint8_t *out, uint32_t max)
{
    uint32_t acc = 0, nb = 0, o = 0;
    while (n--) {
        acc |= (uint32_t)(*in++ & 0x7Fu) << nb;
        nb += 7u;
        if (nb >= 8u) { if (o < max) out[o] = (uint8_t)acc; o++; acc >>= 8; nb -= 8u; }
    }
    return o;
}
static void lk_blob_read(uint32_t off, uint8_t *d, uint32_t n)   /* the backup as it is now, byte by byte */
{
    static const uint32_t S1 = sizeof ustore, S2 = sizeof perf, S3 = sizeof uext;
    uint32_t i;
    for (i = 0; i < n; i++, off++) {
        uint32_t o = off;
        uint8_t b;
        if (o < LK_HEAD) {
            const uint8_t H[LK_HEAD] = {'K', 'S', 'B', '1', (uint8_t)S1, (uint8_t)(S1 >> 8), (uint8_t)S2, (uint8_t)(S2 >> 8), (uint8_t)S3, (uint8_t)(S3 >> 8)};
            b = H[o];
        } else if ((o -= LK_HEAD) < S1) b = ((const uint8_t *)ustore)[o];
        else if ((o -= S1) < S2) b = ((const uint8_t *)&perf)[o];
        else if ((o -= S2) < S3) b = ((const uint8_t *)&uext)[o];
        else b = 0;
        d[i] = b;
    }
}

#if defined(KAWA_WASM)
static uint8_t w_link_out[4096];                /* the emulator: the answers wait here for the page */
static uint32_t w_link_n;
static void lk_wire(const uint8_t *p, uint32_t n) { if (w_link_n + n <= sizeof w_link_out) { memcpy(w_link_out + w_link_n, p, n); w_link_n += n; } }
#else
static void lk_wire(const uint8_t *p, uint32_t n) { (void)ota_wire_send(p, n); }
#endif
static void lk_send(uint32_t cmd, const uint8_t *body, uint32_t n)   /* n <= 136 */
{
    uint32_t w = 0;
    lk_out[w++] = 0xF0; lk_out[w++] = 0x7D; lk_out[w++] = 0x4B; lk_out[w++] = 0x57;
    lk_out[w++] = (uint8_t)(0x40u | cmd);
    w += lk_pack7(body, n, lk_out + w);
    lk_out[w++] = 0xF7;
    lk_wire(lk_out, w);
}
static void lk_status(uint32_t cmd, uint32_t st) { uint8_t b = (uint8_t)st; lk_send(cmd, &b, 1); }

static int app_sysex(const uint8_t *p, uint32_t n)
{
    uint8_t b[160];
    uint32_t d;
    if (n < 4u || p[0] != 0x7Du || p[1] != 0x4Bu || p[2] != 0x57u) return 0;   /* not ours: the updater's */
    d = lk_unpack7(p + 4, n - 4u, b, sizeof b);
    if (d > sizeof b) return 1;
    switch (p[3]) {
    case 0x01: {                                /* HELLO */
        uint8_t r[40];
        uint32_t k = 0, i;
        const char *v = APP_VER;
        r[k++] = LK_PROTO; r[k++] = (uint8_t)LK_SIZE; r[k++] = (uint8_t)(LK_SIZE >> 8);
        for (i = 0; v[i] && k < sizeof r; i++) r[k++] = (uint8_t)v[i];
        lk_send(0x01, r, k);
        break;
    }
    case 0x02: {                                /* READ */
        uint8_t r[3 + 128];
        uint32_t off = d >= 3u ? (uint32_t)b[0] | (uint32_t)b[1] << 8 : 0xFFFFu, m = d >= 3u ? b[2] : 0u;
        if (m > 128u) m = 128u;
        if (off >= LK_SIZE) m = 0;
        else if (off + m > LK_SIZE) m = LK_SIZE - off;
        r[0] = (uint8_t)off; r[1] = (uint8_t)(off >> 8); r[2] = (uint8_t)m;
        lk_blob_read(off, r + 3, m);
        lk_send(0x02, r, 3u + m);
        break;
    }
    case 0x03: {                                /* BEGIN */
        uint32_t sz = d >= 2u ? (uint32_t)b[0] | (uint32_t)b[1] << 8 : 0u;
        if (lk_commit) { lk_status(0x03, 5); break; }
        if (sz != LK_SIZE) { lk_want = 0; lk_status(0x03, 3); break; }
        lk_want = sz; lk_got = 0;
        lk_status(0x03, 0);
        break;
    }
    case 0x04: {                                /* WRITE */
        uint8_t r[3];
        uint32_t off = d >= 3u ? (uint32_t)b[0] | (uint32_t)b[1] << 8 : 0xFFFFu, m = d >= 3u ? b[2] : 0u;
        r[0] = (uint8_t)off; r[1] = (uint8_t)(off >> 8); r[2] = 0;
        if (!lk_want || lk_commit || d < 3u + m || off + m > lk_want) r[2] = 1;
        else {
            memcpy(lk_stage + off, b + 3, m);
            if (off + m > lk_got) lk_got = off + m;
        }
        lk_send(0x04, r, 3);
        break;
    }
    case 0x05:                                  /* COMMIT: checked here, written by the main loop (link_service) */
        if (!lk_want || lk_got != lk_want || d < 2u) { lk_status(0x05, 1); break; }
        lk_commit_crc = (uint16_t)(b[0] | b[1] << 8);
        lk_commit = 1;
        break;
    default:
        break;
    }
    return 1;
}

static void link_service(void)                  /* the main loop: a restore asked for, written to the flash */
{
    uint32_t st = 0;
    if (!lk_commit) return;
    if (lk_crc16(lk_stage, lk_want) != lk_commit_crc) st = 2;
    else {
        uint8_t h[LK_HEAD];
        uint32_t i;
        lk_blob_read(0, h, LK_HEAD);
        for (i = 0; i < LK_HEAD; i++) if (h[i] != lk_stage[i]) st = 3;   /* ("KSB1" and this firmware's sizes) */
    }
    if (!st) {
        memcpy(ustore, lk_stage + LK_HEAD, sizeof ustore);
        memcpy(&perf, lk_stage + LK_HEAD + sizeof ustore, sizeof perf);
        memcpy(&uext, lk_stage + LK_HEAD + sizeof ustore + sizeof perf, sizeof uext);
        store_fixup();
        if (store_save() || perf_save()) st = 4;
        perf_dirty = 0;
        toast(st ? "RESTORE FAILED" : "BACKUP RESTORED");
        g_force = 1;
    }
    lk_commit = 0; lk_want = 0; lk_got = 0;
    lk_status(0x05, st);
}

#if defined(KAWA_WASM)
static uint8_t w_link_in[640];                  /* the page writes one frame here (the bytes between F0 and F7) */
WASM_EXPORT("ksub_link_in") uint8_t *ksub_link_in(void) { return w_link_in; }
WASM_EXPORT("ksub_link_frame") void ksub_link_frame(uint32_t n) { if (n <= sizeof w_link_in) app_sysex(w_link_in, n); link_service(); }
WASM_EXPORT("ksub_link_out") uint8_t *ksub_link_out(void) { return w_link_out; }
WASM_EXPORT("ksub_link_take") uint32_t ksub_link_take(void) { uint32_t n = w_link_n; w_link_n = 0; return n; }   /* (read the bytes before the next frame) */
#endif
