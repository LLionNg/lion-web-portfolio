import fs from "fs";
import { PNG } from "pngjs";
import { encodeToKTX2 } from "ktx2-encoder";

const N = process.argv[2];
const pngBytes = fs.readFileSync(`project${N}_edited.png`);
const imageDecoder = async (buf) => {
  const p = PNG.sync.read(Buffer.from(buf));
  return { width: p.width, height: p.height, data: new Uint8Array(p.data) };
};
const out = await encodeToKTX2(new Uint8Array(pngBytes), {
  isUASTC: false, isKTX2File: true, isSetKTX2SRGBTransferFunc: true,
  isPerceptual: true, generateMipmap: false, isYFlip: false,
  qualityLevel: 220, compressionLevel: 4, imageDecoder,
});
fs.writeFileSync(`project${N}_new.ktx2`, Buffer.from(out));
console.log(`project${N}_new.ktx2`, out.length, "bytes");
