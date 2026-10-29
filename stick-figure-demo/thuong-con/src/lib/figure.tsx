import React from "react";

export const INK = "#23203b";

// Angles in degrees: 0 points straight down, positive swings toward the way
// the figure faces. dy pushes the hip down (crouch / sit) or up (jump, < 0).
export type Pose = {
  x: number;
  dy: number;
  lean: number;
  lt: number;
  lk: number;
  rt: number;
  rk: number;
  la: number;
  le: number;
  ra: number;
  re: number;
};

export const P = (x: number, o: Partial<Pose> = {}): Pose => ({
  x,
  dy: 0,
  lean: 0,
  lt: 9,
  lk: 4,
  rt: -9,
  rk: 4,
  la: -12,
  le: 8,
  ra: 12,
  re: 8,
  ...o,
});

type Arms = Pick<Pose, "la" | "le" | "ra" | "re">;
const GESTURES: Record<string, Arms> = {
  rest: { la: -12, le: 8, ra: 12, re: 8 },
  akimbo: { la: -40, le: 95, ra: 40, re: -95 },
  point: { la: -15, le: 10, ra: 95, re: -5 },
  stop: { la: -15, le: 10, ra: 120, re: -50 },
  chest: { la: -12, le: 8, ra: 30, re: -160 },
  hold: { la: -12, le: 8, ra: 38, re: 4 },
  holdBoth: { la: -38, le: -4, ra: 38, re: 4 },
  open: { la: -55, le: -30, ra: 65, re: -40 },
  up: { la: -150, le: -15, ra: 150, re: 15 },
  reach: { la: -12, le: 8, ra: 155, re: 5 },
  balance: { la: -95, le: 0, ra: 95, re: 0 },
  phone: { la: 60, le: 70, ra: 55, re: 80 },
  dig: { la: 60, le: -10, ra: 70, re: -15 },
  splash: { la: 120, le: -230, ra: 125, re: -240 },
  hug: { la: 95, le: 30, ra: 100, re: 25 },
  sad: { la: -6, le: 4, ra: 6, re: 4 },
  scratch: { la: -12, le: 8, ra: 150, re: -300 },
  wave: { la: -12, le: 8, ra: 140, re: 20 },
  ears: { la: -150, le: 300, ra: 150, re: -300 },
  visor: { la: -12, le: 8, ra: 150, re: -255 },
  clap: { la: 70, le: 40, ra: 75, re: 35 },
};

export const gesture = (p: Pose, name: string, t = 0, wiggle = 0): Pose => {
  const g = GESTURES[name];
  const q = { ...p, ...g };
  if (wiggle) {
    q.ra += wiggle * Math.sin(t * 9);
    q.la -= wiggle * 0.6 * Math.sin(t * 7 + 1);
    if (name === "wave") q.re = 20 + 28 * Math.sin(t * 13);
  }
  return q;
};

export const blend = (a: Pose, b: Pose, k: number): Pose => {
  const s = k * k * (3 - 2 * k);
  const out = { ...a };
  (Object.keys(a) as (keyof Pose)[]).forEach((key) => {
    out[key] = a[key] + (b[key] - a[key]) * s;
  });
  return out;
};

export const idle = (t: number, x: number, o: Partial<Pose> = {}) =>
  P(x, { dy: 3 * Math.sin(t * 4.5), ...o });

export const walkCycle = (t: number, x: number, run = false): Pose => {
  const p = t * 2 * Math.PI * (run ? 1.7 : 1.25);
  const s = Math.sin(p);
  const c = Math.cos(p);
  const [amp, knee, arm] = run ? [38, 55, 45] : [24, 32, 26];
  return P(x, {
    dy: -Math.abs(s) * (run ? 14 : 6),
    lean: run ? 12 : 3,
    lt: amp * s,
    lk: 10 + knee * Math.max(0, -c),
    rt: -amp * s,
    rk: 10 + knee * Math.max(0, c),
    la: -arm * s,
    le: run ? 70 : 15,
    ra: arm * s,
    re: run ? 70 : 15,
  });
};

/** Walk (or run) from x0 to x1 between t0 and t1. */
export const move = (
  t: number,
  x0: number,
  x1: number,
  t0: number,
  t1: number,
  run = false,
) => {
  const facing = x1 >= x0 ? 1 : -1;
  if (t <= t0) return { pose: idle(t, x0), facing };
  if (t >= t1) return { pose: idle(t, x1), facing };
  const k = (t - t0) / (t1 - t0);
  const e = 0.5 - 0.5 * Math.cos(k * Math.PI);
  return { pose: walkCycle(t, x0 + (x1 - x0) * e, run), facing };
};

/** Repeated happy hops with arms up. */
export const hop = (t: number, x: number, period = 0.7, height = 120) => {
  const a = (((t % period) + period) % period) / period;
  const p = idle(t, x);
  if (a < 0.2) {
    const c = Math.sin((a / 0.2) * (Math.PI / 2));
    return {
      ...p,
      dy: 40 * c,
      lt: 10 + 25 * c,
      lk: 4 + 55 * c,
      rt: -10 + 25 * c,
      rk: 4 + 55 * c,
      la: -40,
      le: 20,
      ra: 40,
      re: -20,
    };
  }
  const k = (a - 0.2) / 0.8;
  return {
    ...p,
    dy: -height * 4 * k * (1 - k),
    lt: 25,
    lk: 45,
    rt: 5,
    rk: 45,
    la: -150,
    le: -15,
    ra: 150,
    re: 15,
  };
};

export const crouch = (p: Pose, amount = 1): Pose => ({
  ...p,
  dy: p.dy + 95 * amount,
  lean: p.lean + 18 * amount,
  lt: 70 * amount + p.lt * (1 - amount),
  lk: 120 * amount + p.lk * (1 - amount),
  rt: 60 * amount + p.rt * (1 - amount),
  rk: 115 * amount + p.rk * (1 - amount),
});

export const sit = (p: Pose): Pose => ({
  ...p,
  dy: p.dy + 120,
  lean: -2,
  lt: 82,
  lk: 82,
  rt: 76,
  rk: 76,
});

export type Char = {
  k: number;
  hair: "bun" | "short" | "tuft" | "pigtails";
  shirt: string;
  skirt?: string;
  hairColor?: string;
};

export const MOM: Char = { k: 1, hair: "bun", shirt: "#f27a9a", skirt: "#f27a9a" };
export const DAD: Char = { k: 1.04, hair: "short", shirt: "#2fa6a0" };
export const KID1: Char = { k: 0.62, hair: "tuft", shirt: "#4f86f7" };
export const KID2: Char = {
  k: 0.62,
  hair: "pigtails",
  shirt: "#ff9a2e",
  skirt: "#ff9a2e",
};

export type Face =
  | "happy"
  | "joy"
  | "sad"
  | "worried"
  | "surprised"
  | "bored"
  | "focus";

type Pt = [number, number];

export const joints = (p: Pose, ch: Char, facing = 1, ground = 1300) => {
  const k = ch.k;
  const T = 135 * k;
  const S = 135 * k;
  const TO = 230 * k;
  const N = 25 * k;
  const HD = 58 * k;
  const U = 115 * k;
  const F = 105 * k;
  const vec = (o: Pt, ang: number, len: number): Pt => {
    const r = (ang * Math.PI) / 180;
    return [o[0] + facing * Math.sin(r) * len, o[1] + Math.cos(r) * len];
  };
  const hip: Pt = [p.x, ground - (T + S - 12 * k) + p.dy * k];
  const sh = vec(hip, 180 - p.lean, TO);
  const neck = vec(sh, 180 - p.lean, N);
  const head = vec(neck, 180 - p.lean, HD);
  const lknee = vec(hip, p.lt, T);
  const lfoot0 = vec(lknee, p.lt - p.lk, S);
  const rknee = vec(hip, p.rt, T);
  const rfoot0 = vec(rknee, p.rt - p.rk, S);
  const lfoot: Pt = [lfoot0[0], Math.min(lfoot0[1], ground)];
  const rfoot: Pt = [rfoot0[0], Math.min(rfoot0[1], ground)];
  const lelbow = vec(sh, p.la, U);
  const lhand = vec(lelbow, p.la + p.le, F);
  const relbow = vec(sh, p.ra, U);
  const rhand = vec(relbow, p.ra + p.re, F);
  return { hip, sh, neck, head, r: HD, lknee, lfoot, rknee, rfoot, lelbow, lhand, relbow, rhand, vec };
};

const pts = (...p: Pt[]) => p.map((q) => `${q[0].toFixed(1)},${q[1].toFixed(1)}`).join(" ");

export const Shadow: React.FC<{ x: number; k?: number; ground?: number; air?: number }> = ({
  x,
  k = 1,
  ground = 1300,
  air = 0,
}) => (
  <ellipse
    cx={x}
    cy={ground}
    rx={(95 - 40 * Math.min(1, air)) * k}
    ry={11 * k}
    fill="rgba(0,0,0,0.13)"
  />
);

export const Figure: React.FC<{
  p: Pose;
  ch: Char;
  facing?: number;
  face?: Face;
  talk?: number;
  t?: number;
  ground?: number;
  shadow?: boolean;
}> = ({ p, ch, facing = 1, face = "happy", talk = 0, t = 0, ground = 1300, shadow = true }) => {
  const j = joints(p, ch, facing, ground);
  const k = ch.k;
  const lw = 16 * k;
  const [cx, cy] = j.head;
  const r = j.r;
  const hairColor = ch.hairColor ?? "#3d2b26";
  const fx = facing * 13 * k;
  const ey = cy - 6 * k;
  const eyes: Pt[] = [
    [cx + fx - 16 * k, ey],
    [cx + fx + 17 * k, ey],
  ];
  const mx = cx + fx;
  const my = cy + 22 * k;
  const blink = Math.abs(Math.sin(t * 0.9 + p.x)) > 0.995;
  const torsoTop = j.vec(j.hip, 180 - p.lean, 200 * k);
  const torsoBot = j.vec(j.hip, 180 - p.lean, 12 * k);
  const skirtTop = j.vec(j.hip, 180 - p.lean, 40 * k);
  const air = Math.max(0, -p.dy) / 150;

  const limb = (a: Pt, b: Pt, c: Pt) => (
    <polyline
      points={pts(a, b, c)}
      fill="none"
      stroke={INK}
      strokeWidth={lw}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  );
  const chordTop = (rr: number, y: number) => {
    const half = Math.sqrt(Math.max(0, rr * rr - (y - cy) * (y - cy)));
    return `M ${cx - half} ${y} A ${rr} ${rr} 0 0 1 ${cx + half} ${y} Z`;
  };

  return (
    <g>
      {shadow ? <Shadow x={p.x} k={k} ground={ground} air={air} /> : null}
      {ch.hair === "bun" ? (
        <circle cx={cx - facing * 30 * k} cy={cy - r * 0.95} r={26 * k} fill={hairColor} />
      ) : null}
      {ch.hair === "pigtails" ? (
        <>
          <circle cx={cx - r * 1.02} cy={cy - r * 0.35} r={20 * k} fill={hairColor} />
          <circle cx={cx + r * 1.02} cy={cy - r * 0.35} r={20 * k} fill={hairColor} />
        </>
      ) : null}
      {limb(j.hip, j.lknee, j.lfoot)}
      {limb(j.hip, j.rknee, j.rfoot)}
      <line
        x1={torsoBot[0]}
        y1={torsoBot[1]}
        x2={torsoTop[0]}
        y2={torsoTop[1]}
        stroke={ch.shirt}
        strokeWidth={52 * k}
        strokeLinecap="round"
      />
      {ch.skirt ? (
        <polygon
          points={pts(
            [skirtTop[0] - 24 * k, skirtTop[1]],
            [skirtTop[0] + 24 * k, skirtTop[1]],
            [j.hip[0] + 58 * k, j.hip[1] + 70 * k],
            [j.hip[0] - 58 * k, j.hip[1] + 70 * k],
          )}
          fill={ch.skirt}
          stroke={ch.skirt}
          strokeWidth={8 * k}
          strokeLinejoin="round"
        />
      ) : null}
      {limb(j.sh, j.lelbow, j.lhand)}
      {limb(j.sh, j.relbow, j.rhand)}
      <line x1={j.sh[0]} y1={j.sh[1]} x2={j.neck[0]} y2={j.neck[1]} stroke={INK} strokeWidth={lw} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={r} fill="#ffe4cf" stroke={INK} strokeWidth={lw} />
      {ch.hair === "short" || ch.hair === "bun" || ch.hair === "pigtails" ? (
        <path d={chordTop(r + lw * 0.3, cy - r * 0.35)} fill={hairColor} />
      ) : null}
      {ch.hair === "tuft"
        ? [-14, 0, 14].map((dx) => (
            <line
              key={dx}
              x1={cx + dx * k}
              y1={cy - r}
              x2={cx + dx * k * 1.8 + facing * 6}
              y2={cy - r - 24 * k}
              stroke={INK}
              strokeWidth={9 * k}
              strokeLinecap="round"
            />
          ))
        : null}
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={INK} strokeWidth={lw} />
      {/* eyes */}
      {eyes.map(([ex, eyy], i) =>
        blink || face === "joy" ? (
          <path
            key={i}
            d={`M ${ex - 9 * k} ${eyy + 2 * k} Q ${ex} ${eyy - 9 * k} ${ex + 9 * k} ${eyy + 2 * k}`}
            stroke={INK}
            strokeWidth={5 * k}
            fill="none"
            strokeLinecap="round"
          />
        ) : (
          <g key={i}>
            <ellipse cx={ex} cy={eyy} rx={7 * k} ry={(face === "surprised" ? 10 : 8.5) * k} fill={INK} />
            <circle cx={ex + 2.5 * k} cy={eyy - 3 * k} r={2.3 * k} fill="#fff" />
          </g>
        ),
      )}
      {/* brows */}
      {face === "sad" || face === "worried"
        ? eyes.map(([ex, eyy], i) => {
            const s = i === 0 ? 1 : -1;
            return (
              <line
                key={i}
                x1={ex - 11 * k}
                y1={eyy - 18 * k - s * 5 * k}
                x2={ex + 11 * k}
                y2={eyy - 18 * k + s * 5 * k}
                stroke={INK}
                strokeWidth={5 * k}
                strokeLinecap="round"
              />
            );
          })
        : null}
      {face === "bored"
        ? eyes.map(([ex, eyy], i) => (
            <line key={i} x1={ex - 9 * k} y1={eyy - 4 * k} x2={ex + 9 * k} y2={eyy - 4 * k} stroke="#ffe4cf" strokeWidth={7 * k} />
          ))
        : null}
      {/* mouth */}
      {talk > 0.15 || face === "surprised" ? (
        <ellipse
          cx={mx}
          cy={my}
          rx={11 * k}
          ry={(4 + 10 * Math.max(talk, face === "surprised" ? 0.6 : 0)) * k}
          fill="#8a2f3f"
        />
      ) : face === "sad" || face === "worried" || face === "bored" ? (
        <path
          d={`M ${mx - 14 * k} ${my + 8 * k} Q ${mx} ${my - (face === "bored" ? 0 : 6) * k} ${mx + 14 * k} ${my + 8 * k}`}
          stroke={INK}
          strokeWidth={5.5 * k}
          fill="none"
          strokeLinecap="round"
        />
      ) : face === "joy" ? (
        <path d={`M ${mx - 18 * k} ${my - 4 * k} Q ${mx} ${my + 26 * k} ${mx + 18 * k} ${my - 4 * k} Z`} fill="#8a2f3f" />
      ) : (
        <path
          d={`M ${mx - 16 * k} ${my - 2 * k} Q ${mx} ${my + 14 * k} ${mx + 16 * k} ${my - 2 * k}`}
          stroke={INK}
          strokeWidth={5.5 * k}
          fill="none"
          strokeLinecap="round"
        />
      )}
      {face !== "bored" && face !== "worried" ? (
        <>
          <ellipse cx={cx + fx - 34 * k} cy={cy + 12 * k} rx={9 * k} ry={5 * k} fill="#ffadb4" opacity={0.8} />
          <ellipse cx={cx + fx + 34 * k} cy={cy + 12 * k} rx={9 * k} ry={5 * k} fill="#ffadb4" opacity={0.8} />
        </>
      ) : null}
    </g>
  );
};
