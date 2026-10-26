/* SPDX-License-Identifier: GPL-3.0-only */
/* K-WASUB DATA: the link with the FM-1 (firmware: firmware/src/ksub_link.c), over Web MIDI SysEx, or with the
 * emulator (its WebAssembly). Frames: F0 7D 4B 57 cmd pack7(body) F7; the answer has cmd | 0x40.
 *   KWLink.connectMidi()        -> a transport on the FM-1 (asks for MIDI with SysEx)
 *   KWLink.emuTransport(x)      -> a transport on the emulator (x: the instance's exports)
 *   new KWLink.Session(t).hello() / .backup(onProgress) / .restore(blob, onProgress) */
(function (root) {
  "use strict";
  const HEAD = [0x7D, 0x4B, 0x57];
  const PORT_RE = /fm-1|felucca|ota|composite|sinco|usb-midi|k-wasub/i;
  let FR = false;
  const M = (en, fr) => (FR ? fr : en);
  const STATUS = () => [M("ok", "ok"), M("wrong size or place", "taille ou position fausse"), M("the data arrived damaged (CRC)", "les données sont arrivées abîmées (CRC)"),
    M("not a K-WASUB backup, or one from another firmware layout", "pas une sauvegarde K-WASUB, ou d'une autre organisation de firmware"),
    M("the FM-1 could not write its flash", "le FM-1 n'a pas pu écrire sa mémoire flash"), M("the FM-1 is busy, try again", "le FM-1 est occupé, réessaie")];

  function pack7(b) {
    const o = []; let acc = 0, nb = 0;
    for (const x of b) { acc |= x << nb; nb += 8; while (nb >= 7) { o.push(acc & 0x7F); acc >>>= 7; nb -= 7; } }
    if (nb) o.push(acc & 0x7F);
    return o;
  }
  function unpack7(b) {
    const o = []; let acc = 0, nb = 0;
    for (const x of b) { acc |= (x & 0x7F) << nb; nb += 7; if (nb >= 8) { o.push(acc & 0xFF); acc >>>= 8; nb -= 8; } }
    return new Uint8Array(o);
  }
  function crc16(b) {
    let c = 0;
    for (const x of b) { c ^= x << 8; for (let i = 0; i < 8; i++) c = c & 0x8000 ? ((c << 1) ^ 0x1021) & 0xFFFF : (c << 1) & 0xFFFF; }
    return c;
  }
  function frame(cmd, body) { return new Uint8Array([0xF0, ...HEAD, cmd, ...pack7(body || []), 0xF7]); }
  function parse(m) {   /* a whole F0..F7 message: {cmd, body} when it is ours */
    if (m.length < 6 || m[0] !== 0xF0 || m[1] !== HEAD[0] || m[2] !== HEAD[1] || m[3] !== HEAD[2] || m[m.length - 1] !== 0xF7) return null;
    return { cmd: m[4], body: unpack7(m.subarray(5, m.length - 1)) };
  }
  class LinkError extends Error {}
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  /* a transport: send(frame) and a queue of answers; ask() sends and waits for the answer to that command */
  class Transport {
    constructor() { this.q = []; this.waiter = null; }
    _rx(m) { const p = parse(m); if (!p) return; this.q.push(p); if (this.waiter) this.waiter(); }
    async ask(cmd, body, ms = 1500, tries = 3) {
      for (let t = 0; t < tries; t++) {
        this.q = [];
        await this.send(frame(cmd, body));
        const end = Date.now() + ms;
        while (Date.now() < end) {
          const i = this.q.findIndex(p => p.cmd === (cmd | 0x40));
          if (i >= 0) return this.q.splice(i, 1)[0].body;
          await new Promise(r => { this.waiter = r; setTimeout(r, 20); });
          this.waiter = null;
          if (this.poll) this.poll();
        }
      }
      throw new LinkError(M("the FM-1 does not answer (is K-WASUB 0.9.26 or later installed, the USB cable plugged in, no other program using its MIDI port?)", "le FM-1 ne répond pas (K-WASUB 0.9.26 ou plus installé ? câble USB branché ? aucun autre programme sur son port MIDI ?)"));
    }
    close() {}
  }

  async function connectMidi() {
    if (!(root.navigator && navigator.requestMIDIAccess)) throw new LinkError(M("this browser has no Web MIDI: use Chrome or Edge on a computer", "ce navigateur n'a pas Web MIDI : utilise Chrome ou Edge sur ordinateur"));
    let acc;
    try { acc = await navigator.requestMIDIAccess({ sysex: true }); }
    catch (e) { throw new LinkError(M("MIDI access refused: allow MIDI (with SysEx) for this page", "accès MIDI refusé : autorise le MIDI (avec SysEx) pour cette page")); }
    const ins = [...acc.inputs.values()].filter(p => PORT_RE.test(p.name || ""));
    const outs = [...acc.outputs.values()].filter(p => PORT_RE.test(p.name || ""));
    if (!ins.length || !outs.length) throw new LinkError(M("no FM-1 found: plug it in by USB, switched on, then try again", "aucun FM-1 trouvé : branche-le en USB, allumé, puis réessaie"));
    const t = new Transport(), inp = ins[0], out = outs[0];
    inp.onmidimessage = e => t._rx(e.data);
    await inp.open(); await out.open();
    await sleep(150);
    t.name = out.name;
    t.send = async f => out.send(f);
    t.close = () => { inp.onmidimessage = null; };
    return t;
  }
  function emuTransport(x) {   /* the emulator: the frame goes in through its memory, the answers come back at once */
    const t = new Transport();
    t.name = "emulator";
    t.send = async f => {
      const body = f.subarray(1, f.length - 1);
      new Uint8Array(x.memory.buffer, x.ksub_link_in(), body.length).set(body);
      x.ksub_link_frame(body.length);
      t.poll();
    };
    t.poll = () => {
      const n = x.ksub_link_take();
      if (!n) return;
      const b = new Uint8Array(x.memory.buffer, x.ksub_link_out(), n).slice();
      for (let s = 0; s < n;) { const e = b.indexOf(0xF7, s); if (e < 0) break; t._rx(b.subarray(s, e + 1)); s = e + 1; }
    };
    return t;
  }

  class Session {
    constructor(t) { this.t = t; }
    async hello() {
      const b = await this.t.ask(0x01, []);
      return { proto: b[0], size: b[1] | b[2] << 8, version: String.fromCharCode(...b.subarray(3)) };
    }
    async backup(progress) {
      const h = await this.hello(), blob = new Uint8Array(h.size);
      for (let off = 0; off < h.size;) {
        const n = Math.min(128, h.size - off);
        const r = await this.t.ask(0x02, [off & 0xFF, off >> 8, n]);
        if ((r[0] | r[1] << 8) !== off || r[2] !== n) throw new LinkError(M("the backup came back in the wrong order", "la sauvegarde est revenue dans le désordre"));
        blob.set(r.subarray(3, 3 + n), off);
        off += n;
        if (progress) progress(off / h.size);
      }
      if (String.fromCharCode(...blob.subarray(0, 4)) !== "KSB1") throw new LinkError(M("the FM-1 sent something that is not a backup", "le FM-1 a envoyé autre chose qu'une sauvegarde"));
      return { blob, version: h.version };
    }
    async restore(blob, progress) {
      if (String.fromCharCode(...blob.subarray(0, 4)) !== "KSB1") throw new LinkError(M("this file is not a K-WASUB backup (.kwsub)", "ce fichier n'est pas une sauvegarde K-WASUB (.kwsub)"));
      const h = await this.hello();
      if (h.size !== blob.length) throw new LinkError(M(`this backup (${blob.length} bytes) does not fit this firmware (${h.size}): install the version it was made with, restore, then update`, `cette sauvegarde (${blob.length} octets) ne correspond pas à ce firmware (${h.size}) : installe la version avec laquelle elle a été faite, recharge-la, puis mets à jour`));
      let st = (await this.t.ask(0x03, [blob.length & 0xFF, blob.length >> 8]))[0];
      if (st) throw new LinkError(STATUS()[st] || M("refused", "refusé"));
      for (let off = 0; off < blob.length;) {
        const n = Math.min(120, blob.length - off);
        const r = await this.t.ask(0x04, [off & 0xFF, off >> 8, n, ...blob.subarray(off, off + n)]);
        if (r[2]) throw new LinkError(STATUS()[r[2]] || M("refused", "refusé"));
        off += n;
        if (progress) progress(off / blob.length);
      }
      const c = crc16(blob);
      st = (await this.t.ask(0x05, [c & 0xFF, c >> 8], 6000, 1))[0];
      if (st) throw new LinkError(STATUS()[st] || M("refused", "refusé"));
      return true;
    }
  }
  /* the RESAMPLE recording as a WAV file (16 bit, mono, at its rate) */
  Session.prototype.recording = async function (progress) {
    const i = await this.t.ask(0x06, []);
    const len = (i[0] | i[1] << 8 | i[2] << 16 | i[3] << 24) >>> 0, rate = (i[4] | i[5] << 8 | i[6] << 16) >>> 0;
    if (!len) throw new LinkError(M("no recording on the FM-1 yet: EDIT, the OSC C SAMPLE view, RESAMPLE (or it is still recording)", "pas encore d'enregistrement sur le FM-1 : EDIT, la vue SAMPLE d'OSC C, RESAMPLE (ou il enregistre encore)"));
    const tab = new Int16Array(256);
    for (let k = 0; k < 256; k += 64) {
      const r = await this.t.ask(0x08, [k, 64]);
      for (let j = 0; j < r[1]; j++) tab[r[0] + j] = r[2 + 2 * j] | r[3 + 2 * j] << 8;
    }
    const mu = new Uint8Array(len);
    for (let off = 0; off < len;) {
      const n = Math.min(128, len - off);
      const r = await this.t.ask(0x07, [off & 0xFF, off >> 8, n]);
      if ((r[0] | r[1] << 8) !== off || r[2] !== n) throw new LinkError(M("the recording came back in the wrong order", "l'enregistrement est revenu dans le désordre"));
      mu.set(r.subarray(3, 3 + n), off);
      off += n;
      if (progress) progress(off / len);
    }
    return { wav: wav16(Int16Array.from(mu, b => tab[b]), rate), seconds: len / rate, rate };
  };
  function wav16(pcm, rate) {
    const b = new Uint8Array(44 + pcm.length * 2), v = new DataView(b.buffer);
    const s = (o, t) => { for (let k = 0; k < t.length; k++) b[o + k] = t.charCodeAt(k); };
    s(0, "RIFF"); v.setUint32(4, 36 + pcm.length * 2, true); s(8, "WAVEfmt "); v.setUint32(16, 16, true); v.setUint16(20, 1, true);
    v.setUint16(22, 1, true); v.setUint32(24, rate, true); v.setUint32(28, rate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true);
    s(36, "data"); v.setUint32(40, pcm.length * 2, true);
    for (let k = 0; k < pcm.length; k++) v.setInt16(44 + k * 2, pcm[k], true);
    return b;
  }
  const api = { wav16, setFrench: f => { FR = !!f; }, pack7, unpack7, crc16, frame, parse, Session, connectMidi, emuTransport, LinkError };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.KWLink = api;
})(typeof window !== "undefined" ? window : globalThis);
