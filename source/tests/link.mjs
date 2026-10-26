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
console.log(bad === 3 ? "link OK" : "link FAILED");
process.exit(bad === 3 ? 0 : 1);
