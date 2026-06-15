import fs from "fs";
import { PNG } from "pngjs";
import { encodeToKTX2 } from "ktx2-encoder";

const pngBytes = fs.readFileSync("project2_edited.png");

// Node requires an imageDecoder: PNG bytes -> {width,height,data:RGBA}
const imageDecoder = async (buf) => {
  const p = PNG.sync.read(Buffer.from(buf));
  return { width: p.width, height: p.height, data: new Uint8Array(p.data) };
};

// Match the original project2.ktx2: ETC1S / BasisLZ, sRGB, no mipmaps, 1024x1024
const out = await encodeToKTX2(new Uint8Array(pngBytes), {
  isUASTC: false,                    // ETC1S (not UASTC)
  isKTX2File: true,                  // .ktx2 container
  isSetKTX2SRGBTransferFunc: true,   // sRGB transfer in DFD
  isPerceptual: true,                // input is sRGB color data
  generateMipmap: false,             // original has 1 level
  isYFlip: false,                    // test orientation; flip if upside-down in app
  qualityLevel: 220,                 // ETC1S quality (1-255)
  compressionLevel: 4,               // encoder effort (0-6)
  imageDecoder,
});

fs.writeFileSync("project2_new.ktx2", Buffer.from(out));
console.log("wrote project2_new.ktx2:", out.length, "bytes");
