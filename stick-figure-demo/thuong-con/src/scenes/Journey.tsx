import React from "react";
import { GROUND, Park } from "../lib/backdrops";
import { Figure, gesture, hop, idle, KID1, MOM, walkCycle } from "../lib/figure";
import { Heart, Sparkles, Star, Stone, Sun } from "../lib/icons";
import { L, PH, rand, ramp, sp } from "../lib/time";
import { Chip, Pop } from "../lib/ui";

// Đồng hành: love stays whole; mom can't clear every stone, but walks
// beside the child while they step over the small ones.
export const Journey: React.FC<{ t: number }> = ({ t }) => {
  const [e1, e2, e3, e4, e5] = ["e1", "e2", "e3", "e4", "e5"].map(L);
  const manyAt = PH("e3", 1);
  const smallAt = PH("e4", 2);
  // the walk: world scrolls left while walking
  const walkSpans: [number, number][] = [
    [e2.start - 0.2, e3.start + 0.3],
    [e4.start - 0.2, e5.start],
  ];
  let pan = 0;
  let walking = false;
  for (const [a, b] of walkSpans) {
    pan += Math.max(0, Math.min(t, b) - a) * 210;
    if (t > a && t < b) walking = true;
  }
  // stones in world space (x), sizes
  const stones = Array.from({ length: 14 }).map((_, i) => ({
    x: 700 + i * 170 + rand(i) * 60,
    s: 0.55 + rand(i + 20) * 0.5,
    at: manyAt + i * 0.05,
  }));
  const kidX = 600;
  const momX = 430;
  const nearStone = stones.reduce((d, st) => Math.min(d, Math.abs(st.x - pan - kidX)), 1e9);
  const stepping = walking && t > e4.start - 0.2 && nearStone < 60;
  let kid = walking ? walkCycle(t, kidX) : idle(t, kidX);
  if (stepping) kid = { ...kid, dy: kid.dy - 60 * (1 - nearStone / 60), lt: kid.lt + 40, lk: kid.lk + 40 };
  kid = { ...kid, la: -55, le: 10 };
  if (t > e5.start) kid = hop(t - e5.start, kidX, 0.6, 100);
  const mom = gesture(walking ? walkCycle(t + 0.4, momX) : idle(t, momX), t > e3.start && t < e4.start ? "stop" : "hold", t, t > e3.start && t < e4.start ? 5 : 0);
  const heartK = sp(t, e1.start - 0.2) * (1 + 0.15 * Math.sin(Math.max(0, t - PH("e1", 1)) * 6) * (t > PH("e1", 1) && t < e1.end ? 1 : 0));
  return (
    <g>
      <Park id="journey" t={t} pan={pan} sky={["#8fd0ff", "#fff0d8"]} sunY={t > e5.start - 0.3 ? 330 - 60 * sp(t, e5.start - 0.3) : 330} />
      {t > e5.start - 0.3 ? (
        <g opacity={sp(t, e5.start - 0.3)}>
          <Sun x={860} y={270} r={110} t={t} />
        </g>
      ) : null}
      {/* love stays whole */}
      {t < e2.start + 0.5 ? (
        <g transform={`translate(540 520) scale(${heartK})`} opacity={1 - ramp(t, e2.start, e2.start + 0.5)}>
          <circle r={260} fill="#ff8fa6" opacity={0.2} />
          <Heart x={0} y={0} s={190} />
          <g transform="translate(0 -235)">
            <Chip text="THƯƠNG CON" fill="#ff5a7a" size={44} />
          </g>
        </g>
      ) : null}
      {/* path */}
      <rect x={-20} y={GROUND - 6} width={1120} height={60} rx={30} fill="#e9d2a8" />
      {stones.map((st, i) => {
        const k = sp(t, st.at);
        const x = st.x - pan;
        if (x < -80 || x > 1160 || k <= 0) return null;
        const small = t > smallAt && st.s < 0.8;
        return (
          <g key={i} transform={`translate(${x} ${GROUND + 6}) scale(${k * st.s}) translate(${-x} ${-GROUND - 6})`}>
            <Stone x={x} y={GROUND + 6} s={1.3} fill={small ? "#9fc5a8" : "#9aa3b5"} />
            {small ? <Star x={x} y={GROUND - 70} r={14} fill="#ffd23f" rot={t * 3} /> : null}
          </g>
        );
      })}
      <Figure p={mom} ch={MOM} facing={1} face={t > e3.start && t < e4.start ? "worried" : "happy"} t={t} ground={GROUND} />
      <Figure p={kid} ch={KID1} facing={1} face={stepping ? "focus" : "joy"} t={t} ground={GROUND} />
      {t > e3.start && t < e4.start ? (
        <Pop t={t} t0={manyAt + 0.3} t1={e4.start - 0.2} x={540} y={520}>
          <Chip text="KHÔNG THỂ DỌN HẾT" fill="#7a7f9f" size={46} />
        </Pop>
      ) : null}
      {t > smallAt && t < e5.start ? (
        <Pop t={t} t0={smallAt} t1={e5.start - 0.2} x={540} y={520}>
          <Chip text="THỬ THÁCH VỪA SỨC" fill="#2fbf71" size={46} />
        </Pop>
      ) : null}
      {t > e5.start ? <Sparkles x={kidX} y={900} t={t} r={220} n={9} /> : null}
    </g>
  );
};
