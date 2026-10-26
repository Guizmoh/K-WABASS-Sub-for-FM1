// The DATA link against the emulator: backup, change, restore, compare; and the refusals.
import fs from "fs";
import { createRequire } from "module";
const KW = createRequire(import.meta.url)("../web/kwlink.js");
const wasm = fs.readFileSync(new URL("../build/web/ksub.wasm", import.meta.url));
const { instance } = await WebAssembly.instantiate(wasm, {});
const x = instance.exports;
x.ksub_init();
for (let i = 0; i < 50; i++) x.ksub_step();
const s = new KW.Session(KW.emuTransport(x));
const h = await s.hello();
console.log("hello", h);
const a = await s.backup();
console.log("backup", a.blob.length, "B, starts", String.fromCharCode(...a.blob.subarray(0, 4)));
// a slot of our own in the copy: name and a magic that the firmware's check must reject or keep
const b = a.blob.slice(); b[10 + 2] = 0x41;   // (slot 0 name: not valid without its sum: the fixup clears it)
await s.restore(a.blob);
const c = await s.backup();
console.log("restore + backup again equal:", Buffer.compare(Buffer.from(a.blob), Buffer.from(c.blob)) === 0);
let bad = 0;
try { await s.restore(a.blob.slice(0, 100)); } catch (e) { bad++; console.log("short file refused:", e.message.slice(0, 60)); }
const d = a.blob.slice(); d[0] = 0x58;
try { await s.restore(d); } catch (e) { bad++; console.log("bad header refused:", e.message.slice(0, 60)); }
// a CRC error: write the right size, then a wrong COMMIT crc
const t = s.t;
await t.ask(0x03, [a.blob.length & 0xFF, a.blob.length >> 8]);
for (let off = 0; off < a.blob.length; off += 120) { const n = Math.min(120, a.blob.length - off); await t.ask(0x04, [off & 0xFF, off >> 8, n, ...a.blob.subarray(off, off + n)]); }
const st = (await t.ask(0x05, [1, 2]))[0];
console.log("bad crc status", st, st === 2 ? "(refused)" : "(WRONG)");
if (st === 2) bad++;
// the RESAMPLE recording: none yet, then one made as the manual's picture does (EDIT x5: the sample view, a key held, RESAMPLE on)
try { await s.recording(); } catch (e) { bad++; console.log("no recording yet:", e.message.slice(0, 50)); }
let ms = 0;
const run = until => { while (ms < until) { x.ksub_audio(); x.ksub_step(); x.ksub_step(); ms += 256 / 44.1; } };
const btn = id => { x.ksub_button(id, 1); x.ksub_step(); x.ksub_button(id, 0); };
run(3000); btn(8); run(3300); btn(3); run(3700);     // (the start screen: a touch; then the question: CLASSIC)
for (let i = 0; i < 5; i++) { btn(6); run(ms + 150); }
x.ksub_keys(1 << 12); run(ms + 200); x.ksub_turn(0, 4); run(ms + 150); x.ksub_turn(1, 1); run(ms + 5000); x.ksub_keys(0); run(ms + 300);
const r = await s.recording();
const pcm = new Int16Array(r.wav.buffer.slice(44));
let peak = 0; for (const v of pcm) peak = Math.max(peak, Math.abs(v));
console.log("recording", r.seconds.toFixed(2), "s at", r.rate, "Hz, wav", r.wav.length, "B, peak", peak);
fs.writeFileSync("build/rs.wav", r.wav);
if (r.seconds >= 2 && peak > 500) bad++;
// a sample of ours: a 110 Hz saw, 1.5 s; sent, then read back as the recording (the same memory)
const N = 16538, saw = new Int16Array(N);
for (let i = 0; i < N; i++) saw[i] = Math.round(((i * 110 / 11025) % 1 * 2 - 1) * 26000);
const sent = await s.sendSample(saw);
run(ms + 100);
const back = await s.recording();
const pb = new Int16Array(back.wav.buffer.slice(44));
let err = 0; for (let i = 0; i < N; i++) err = Math.max(err, Math.abs(pb[i] - saw[i]));
console.log("sample sent", sent, "bytes, read back", pb.length, "samples, max error", err);
if (pb.length === N && err < 2000) bad++;
console.log(bad === 6 ? "link OK" : "link FAILED");
process.exit(bad === 6 ? 0 : 1);
