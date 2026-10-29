import { Easing, interpolate, spring } from "remotion";
import timeline from "../data/timeline.json";

export const FPS = 30;
export const W = 1080;
export const H = 1920;

export type Word = { w: string; s: number; e: number; key: boolean };
export type Line = {
  id: string;
  scene: string;
  start: number;
  end: number;
  phrases: Word[][];
};

export const LINES = timeline.lines as Line[];
export const DURATION = timeline.duration;

const byId: Record<string, Line> = Object.fromEntries(
  LINES.map((l) => [l.id, l]),
);

/** Line by id (times in seconds on the voice track). */
export const L = (id: string): Line => byId[id];
/** Start time of phrase `i` of line `id`. */
export const PH = (id: string, i: number) => byId[id].phrases[i][0].s;

/** Spring from 0 to 1 starting at t0 (seconds). Bouncy by default. */
export const sp = (
  t: number,
  t0: number,
  damping = 11,
  stiffness = 150,
  mass = 0.8,
) =>
  t < t0
    ? 0
    : spring({
        frame: (t - t0) * FPS,
        fps: FPS,
        config: { damping, stiffness, mass },
      });

/** Spring with no overshoot. */
export const soft = (t: number, t0: number) => sp(t, t0, 200, 120, 1);

const OUT = Easing.bezier(0.16, 1, 0.3, 1);

/** 0..1 between a and b with an ease-out curve. */
export const ramp = (t: number, a: number, b: number, easing = OUT) =>
  interpolate(t, [a, b], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });

/** 1 inside [a, b], easing in and out over `f` seconds at the edges. */
export const win = (t: number, a: number, b: number, f = 0.25) =>
  Math.min(ramp(t, a, a + f), 1 - ramp(t, b - f, b));

export const clamp = (x: number, a = 0, b = 1) => Math.min(Math.max(x, a), b);
export const mix = (a: number, b: number, k: number) => a + (b - a) * k;

/** Mouth-flap amount when a word of the given line is being spoken. */
export const talking = (t: number, ...ids: string[]) => {
  for (const id of ids) {
    for (const ph of byId[id].phrases) {
      for (const w of ph) {
        if (t >= w.s && t <= w.e + 0.04) {
          return 0.35 + 0.65 * Math.abs(Math.sin(t * 17));
        }
      }
    }
  }
  return 0;
};

/** Deterministic pseudo-random in [0, 1). */
export const rand = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

// Scenes start a little before their first line so visuals lead the voice.
const LEAD = 0.45;
export type SceneSpan = { name: string; start: number; end: number };
export const SCENES: SceneSpan[] = (() => {
  const out: SceneSpan[] = [];
  for (const l of LINES) {
    if (!out.length || out[out.length - 1].name !== l.scene) {
      out.push({
        name: l.scene,
        start: out.length ? l.start - LEAD : 0,
        end: DURATION,
      });
    }
  }
  for (let i = 0; i < out.length - 1; i++) out[i].end = out[i + 1].start;
  return out;
})();
export const scene = (name: string) => SCENES.find((s) => s.name === name)!;

/** Start time of the nth word in a line matching `word` (punctuation ignored). */
export const WD = (id: string, word: string, nth = 0) => {
  const clean = (s: string) => s.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
  const target = clean(word);
  let n = 0;
  for (const ph of byId[id].phrases) {
    for (const w of ph) {
      if (clean(w.w) === target && n++ === nth) return w.s;
    }
  }
  throw new Error(`word ${word} not in ${id}`);
};
