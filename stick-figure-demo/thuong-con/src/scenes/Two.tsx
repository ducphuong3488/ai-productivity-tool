import React from "react";
import { Studio } from "../lib/backdrops";
import { Figure, gesture, hop, idle, KID1, KID2 } from "../lib/figure";
import { Cloud, Sun, Tablet, Tree } from "../lib/icons";
import { L, sp } from "../lib/time";
import { Card, Chip } from "../lib/ui";

// "Thử hình dung hai đứa trẻ." Two framed portraits slide in.
export const Two: React.FC<{ t: number }> = ({ t }) => {
  const t0 = L("t1").start - 0.3;
  const a = sp(t, t0, 14, 120);
  const b = sp(t, t0 + 0.25, 14, 120);
  return (
    <g>
      <Studio id="two" top="#ffe9d6" bottom="#ffc9b9" dots="#ff8f6b" t={t} />
      <g transform={`translate(${-500 + 790 * a} 760) rotate(${-4 * a})`}>
        <Card w={440} h={720} r={48} fill="#cfd5ec">
          <rect x={-220} y={110} width={440} height={250} fill="#a7aecb" />
          <rect x={-140} y={-280} width={180} height={200} rx={12} fill="#ffffff" opacity={0.7} />
          <rect x={-140} y={-280} width={180} height={200} rx={12} fill="#8287ad" opacity={0.6} />
          <g transform="translate(-540 -760) translate(0 0)">
            <Figure p={gesture(idle(t, 540), "phone")} ch={{ ...KID1, k: 0.55 }} facing={1} face="bored" t={t} ground={1110} />
          </g>
          <Tablet x={88} y={92} s={0.5} glow={0.8} />
          <g transform="translate(0 -320)">
            <Chip text="BÉ 1" fill="#4f86f7" size={44} />
          </g>
        </Card>
      </g>
      <g transform={`translate(${1580 - 790 * b} 760) rotate(${4 * b})`}>
        <Card w={440} h={720} r={48} fill="#bfe6ff">
          <rect x={-220} y={110} width={440} height={250} fill="#7fcb76" />
          <Sun x={110} y={-200} r={55} t={t} />
          <Cloud x={-90} y={-170} s={0.45} />
          <Tree x={-140} base={130} s={0.55} t={t} />
          <g transform="translate(-540 -760)">
            <Figure p={hop(t, 560, 0.7, 70)} ch={{ ...KID2, k: 0.55 }} facing={1} face="joy" t={t} ground={1110} />
          </g>
          <g transform="translate(0 -320)">
            <Chip text="BÉ 2" fill="#ff9a2e" size={44} />
          </g>
        </Card>
      </g>
    </g>
  );
};
