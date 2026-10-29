import React from "react";
import { GROUND, Studio } from "../lib/backdrops";
import { Figure, gesture, hop, idle, INK, KID1, KID2, MOM } from "../lib/figure";
import { Check } from "../lib/icons";
import { clamp, L, PH, ramp, sp, WD } from "../lib/time";
import { Card, Chip, Label, Pop } from "../lib/ui";

const GROUPS = [
  { label: "Vận động", word: "động", a: 0.32, b: 0.9 },
  { label: "Kỹ năng", word: "năng", a: 0.38, b: 0.86 },
  { label: "Tự tin", word: "tin", a: 0.3, b: 0.94 },
];
const PRACTICE = ["Chạy trên cỏ", "Trồng cây", "Giữ thăng bằng", "Tự đứng dậy"];

export const Compare: React.FC<{ t: number }> = ({ t }) => {
  const [c1, c2, c3, c4] = ["c1", "c2", "c3", "c4"].map(L);
  const chartOut = ramp(t, c2.start - 0.2, c2.start + 0.3);
  const listOut = ramp(t, c3.start - 0.2, c3.start + 0.3);
  const blockAt = [WD("c3", "ngăn"), WD("c3", "làm"), WD("c3", "sợ")];
  const qAt = PH("c4", 1);
  return (
    <g>
      <Studio id="cmp" top="#efe8ff" bottom="#d3c6ff" dots="#8f74ff" t={t} />
      {/* chart */}
      {chartOut < 1 ? (
        <g transform={`translate(540 ${760 - chartOut * 200}) scale(${sp(t, c1.start - 0.3) * (1 - chartOut * 0.3)})`} opacity={1 - chartOut}>
          <Card w={900} h={880} r={56}>
            <g transform="translate(-200 -360)">
              <Chip text="BÉ 1" fill="#4f86f7" size={38} />
            </g>
            <g transform="translate(200 -360)">
              <Chip text="BÉ 2" fill="#ff9a2e" size={38} />
            </g>
            <line x1={-380} y1={300} x2={380} y2={300} stroke={INK} strokeWidth={6} opacity={0.3} />
            {GROUPS.map((g, i) => {
              const x = -270 + i * 270;
              const k = sp(t, WD("c1", g.word) - 0.3, 14, 110);
              const maxH = 520;
              return (
                <g key={g.label}>
                  <rect x={x - 95} y={300 - maxH * g.a * k} width={85} height={maxH * g.a * k} rx={18} fill="#4f86f7" />
                  <rect x={x + 10} y={300 - maxH * g.b * k} width={85} height={maxH * g.b * k} rx={18} fill="#ff9a2e" />
                  <Label x={x} y={355} size={44}>
                    {g.label}
                  </Label>
                </g>
              );
            })}
          </Card>
        </g>
      ) : null}
      {/* practice checklist */}
      {t > c2.start - 0.3 && listOut < 1 ? (
        <g transform={`translate(540 ${700}) scale(${sp(t, c2.start - 0.3)})`} opacity={1 - listOut}>
          <Card w={820} h={700} r={56}>
            <Label y={-260} size={56} fill="#7b5cff">
              ĐƯỢC THỰC HÀNH
            </Label>
            {PRACTICE.map((p, i) => {
              const at = c2.start + 0.5 + i * 0.55;
              const y = -130 + i * 125;
              return (
                <g key={p} opacity={clamp((t - at + 0.3) * 4)}>
                  <circle cx={-300} cy={y} r={42} fill="#d9f7e5" />
                  <g transform={`translate(-300 ${y}) scale(0.5)`}>
                    <Check x={0} y={0} p={ramp(t, at, at + 0.3)} />
                  </g>
                  <text x={-230} y={y} fontFamily="Inter Display" fontWeight={800} fontSize={52} fill={INK} dominantBaseline="central">
                    {p}
                  </text>
                </g>
              );
            })}
          </Card>
        </g>
      ) : null}
      {t > c2.start - 0.3 && t < c3.start ? (
        <Figure p={hop(t, 860, 0.65, 80)} ch={KID2} facing={-1} face="joy" t={t} ground={GROUND + 20} />
      ) : null}
      {/* "ngăn trước, làm thay, sợ thay" */}
      {t > c3.start - 0.3 ? (
        <g>
          <Figure p={gesture(idle(t, 760), t < c4.start ? "stop" : "rest", t, 4)} ch={{ ...MOM, k: 1.15 }} facing={-1} face="worried" t={t} ground={GROUND + 40} />
          <Figure p={gesture(idle(t, 300), t > qAt ? "scratch" : "sad")} ch={KID1} facing={1} face={t > qAt ? "surprised" : "sad"} t={t} ground={GROUND + 40} />
          {["NGĂN TRƯỚC", "LÀM THAY", "SỢ THAY"].map((w, i) => (
            <Pop key={w} t={t} t0={blockAt[i] - 0.1} t1={c4.start + 0.2 + i * 0.08} x={330} y={500 + i * 150} rot={i % 2 ? 8 : -8}>
              <Card w={470} h={120} r={60} fill="#ff6b7d">
                <Label size={52} fill="#ffffff">
                  {w}
                </Label>
              </Card>
            </Pop>
          ))}
          {t > qAt - 0.2 ? (
            <g transform={`translate(300 ${640 + 20 * Math.sin(t * 5)}) scale(${sp(t, qAt - 0.2)}) rotate(${8 * Math.sin(t * 3)})`}>
              <circle r={150} fill="#ffe27a" />
              <Label size={230} fill={INK}>
                ?
              </Label>
            </g>
          ) : null}
        </g>
      ) : null}
    </g>
  );
};
