import React from "react";
import { GROUND, Park } from "../lib/backdrops";
import { Figure, gesture, hop, idle, KID1, MOM } from "../lib/figure";
import { Bird, Cloud, Sparkles, Umbrella } from "../lib/icons";
import { L, mix, ramp, sp } from "../lib/time";

// "Thương con, là cho con sự bảo vệ, và cả khoảng trời để lớn lên."
export const Final: React.FC<{ t: number }> = ({ t }) => {
  const z1 = L("z1");
  const z2 = L("z2");
  const open = ramp(t, z2.start - 0.1, z2.start + 0.8);
  const umbrellaY = mix(560, -600, ramp(t, z2.start, z2.start + 1.2));
  const cloudsOut = open * 900;
  const kidK = 0.62 + 0.12 * sp(t, z2.start + 0.6);
  const kid = t > z2.start + 0.3 ? hop(t - z2.start - 0.3, 600, 0.7, 120) : gesture(idle(t, 600), "rest");
  return (
    <g>
      <Park id="final" t={t} sky={[mixHex(open), "#fff1dc"]} sunY={mix(900, 330, open)} />
      <Cloud x={300 - cloudsOut} y={360} s={1.6} fill="#c7cbe0" opacity={1 - open * 0.8} />
      <Cloud x={800 + cloudsOut} y={300} s={1.5} fill="#c7cbe0" opacity={1 - open * 0.8} />
      {t < z2.start + 0.3
        ? Array.from({ length: 14 }).map((_, i) => {
            const ph = (t * 1.5 + i * 0.13) % 1;
            const x = 80 + i * 70;
            return <line key={i} x1={x} y1={380 + ph * 900} x2={x - 8} y2={410 + ph * 900} stroke="#8fc7ff" strokeWidth={6} strokeLinecap="round" opacity={0.7 * (1 - open)} />;
          })
        : null}
      {open > 0
        ? Array.from({ length: 5 }).map((_, i) => <Bird key={i} x={200 + i * 150 + (t - z2.start) * 60} y={420 - i * 30 + 10 * Math.sin(t * 2 + i)} t={t} s={1.1} />)
        : null}
      <g transform={`translate(0 ${umbrellaY - 560})`} opacity={1 - ramp(t, z2.start + 0.6, z2.start + 1.2)}>
        <g transform={`translate(560 560) scale(${sp(t, z1.start - 0.3)}) translate(-560 -560)`}>
          <circle cx={560} cy={720} r={340} fill="#ffffff" opacity={0.16} />
          <Umbrella x={560} y={600} s={1.25} />
        </g>
      </g>
      <Figure p={gesture(idle(t, 430), t > z2.start + 0.3 ? "open" : "reach")} ch={MOM} facing={1} face="happy" t={t} ground={GROUND} />
      <Figure p={kid} ch={{ ...KID1, k: kidK }} facing={-1} face="joy" t={t} ground={GROUND} />
      {open > 0.5 ? <Sparkles x={600} y={850} t={t} r={250} n={10} /> : null}
    </g>
  );
};

function mixHex(k: number) {
  const a = [154, 160, 190];
  const b = [111, 195, 255];
  return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(",")})`;
}
