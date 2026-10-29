// Render a few frames as PNGs for a quick visual check.
// Usage: node scripts/stills.mjs <outDir> <sec1,sec2,...>
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";

const [outDir, list] = process.argv.slice(2);
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), enableCaching: true });
const browserExecutable = "/opt/pw-browsers/chromium";
const composition = await selectComposition({ serveUrl, id: "ThuongCon", browserExecutable });
for (const s of list.split(",").map(Number)) {
  const frame = Math.min(composition.durationInFrames - 1, Math.round(s * composition.fps));
  await renderStill({ composition, serveUrl, frame, output: path.join(outDir, `s_${s.toFixed(2).padStart(6, "0")}.png`), browserExecutable });
  console.log("frame", s);
}
