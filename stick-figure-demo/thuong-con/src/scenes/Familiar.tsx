import React from "react";
import { GROUND, Studio } from "../lib/backdrops";
import { Figure, gesture, idle, INK, KID1 } from "../lib/figure";
import { L, PH, rand, sp } from "../lib/time";
import { Card, Label } from "../lib/ui";

const DAYS = ["THỨ HAI", "THỨ BA", "THỨ TƯ", "THỨ NĂM", "THỨ SÁU", "THỨ BẢY", "CHỦ NHẬT"];

// "Nghe quen lắm, phải không? Đó là những câu ta vẫn nói với con mỗi ngày."
// A calendar flips through the week while "ĐỪNG!" bubbles pile up.
export const Familiar: React.FC<{ t: number }> = ({ t }) => {
  const f1 = L("f1");
  const start = f1.start - 0.3;
  const flipStart = PH("f2", 0);
  const dayF = Math.max(0, (t - flipStart) / 0.32);
  const day = Math.min(DAYS.length - 1, Math.floor(dayF));
  const flip = day < DAYS.length - 1 ? dayF - Math.floor(dayF) : 1;
  const n = Math.max(0, Math.floor((t - start) * 9));
  const calIn = sp(t, start);
  return (
    <g>
      <Studio id="fam" top="#2c3d8f" bottom="#141a3f" t={t} />
      {Array.from({ length: Math.min(n, 34) }).map((_, i) => {
        const x = 90 + rand(i) * 900;
        const y = 240 + rand(i + 99) * 1000;
        if (x > 300 && x < 780 && y > 360 && y < 780) return null;
        const born = start + i / 9;
        const s = sp(t, born) * (0.6 + rand(i + 7) * 0.7);
        const rot = (rand(i + 3) - 0.5) * 30;
        return (
          <g key={i} transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`} opacity={0.55 + 0.45 * rand(i + 5)}>
            <rect x={-105} y={-46} width={210} height={92} rx={46} fill="#ffffff" />
            <path d="M -30 40 L -50 72 L 0 44 Z" fill="#ffffff" />
            <Label size={46} fill="#ff4d5e">
              ĐỪNG!
            </Label>
          </g>
        );
      })}
      <g transform={`translate(540 570) scale(${calIn})`}>
        <Card w={420} h={380} r={44}>
          <rect x={-210} y={-190} width={420} height={110} rx={44} fill="#ff5a6e" />
          <rect x={-210} y={-130} width={420} height={50} fill="#ff5a6e" />
          {[-110, 110].map((x) => (
            <rect key={x} x={x - 14} y={-218} width={28} height={70} rx={14} fill={INK} />
          ))}
          <g transform={`translate(0 -135) scale(1 ${Math.abs(Math.cos(flip * Math.PI))})`}>
            <Label size={50} fill="#ffffff">
              {DAYS[flip > 0.5 && day < DAYS.length - 1 ? day + 1 : day]}
            </Label>
          </g>
          <g transform={`translate(0 55) scale(${1 + 0.06 * Math.sin(t * 8)})`}>
            <Label size={150} fill="#ff4d5e">
              ĐỪNG
            </Label>
          </g>
        </Card>
      </g>
      <Figure p={gesture(idle(t, 540), "ears")} ch={KID1} facing={1} face="worried" t={t} ground={GROUND} />
    </g>
  );
};
