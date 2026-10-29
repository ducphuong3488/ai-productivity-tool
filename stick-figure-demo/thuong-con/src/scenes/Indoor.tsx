import React from "react";
import { GROUND, Room } from "../lib/backdrops";
import { blend, Figure, gesture, idle, KID1, sit, walkCycle } from "../lib/figure";
import { Bucket, Shoe, Sun, Tablet, Wind, XMark } from "../lib/icons";
import { L, PH, ramp, sp } from "../lib/time";
import { Card, Pop, Stamp } from "../lib/ui";

// Bé thứ nhất: every wish gets a "no"; the room darkens until only the
// tablet's glow is left.
export const Indoor: React.FC<{ t: number }> = ({ t }) => {
  const [i2, i3, i4, i5] = ["i2", "i3", "i4", "i5"].map(L);
  const no2 = PH("i2", 1);
  const no3 = PH("i3", 1);
  const no4 = PH("i4", 1);
  const screenAt = PH("i5", 1);
  const curtain = ramp(t, no4, no4 + 0.8);
  const dark = ramp(t, i5.start, screenAt + 0.6);
  let kid = sit(idle(t, 330));
  let face: "bored" | "happy" | "sad" | "surprised" = "bored";
  let facing = 1;
  if (t >= i2.start - 0.2 && t < no2) {
    kid = walkCycle(t, 330 + Math.min(1, (t - i2.start + 0.2) / 0.8) * 60, true);
    face = "happy";
  } else if (t >= no2 && t < i3.start) {
    kid = blend(walkCycle(no2, 390, true), gesture(idle(t, 390), "sad"), (t - no2) / 0.3);
    face = "sad";
  } else if (t >= i3.start && t < i4.start) {
    kid = t < no3 ? gesture(idle(t, 390), "point", t, 6) : gesture(idle(t, 390), "sad");
    face = t < no3 ? "happy" : "sad";
    facing = -1;
  } else if (t >= i4.start && t < i5.start) {
    kid = t < no4 ? gesture(idle(t, 420), "reach") : gesture(idle(t, 420), "sad");
    face = t < no4 ? "happy" : "sad";
  } else if (t >= i5.start) {
    kid = gesture(sit(idle(t, 700)), "phone");
    face = "bored";
  }
  const zoom = 1 + 0.18 * ramp(t, screenAt, i5.end + 0.4);
  const hands = kid.x + 70;
  return (
    <g transform={`translate(${700 * (1 - zoom)} ${1050 * (1 - zoom)}) scale(${zoom})`}>
      <Room id="indoor" cool t={t} curtain={curtain} />
      {t < i3.start + 0.2 ? null : (
        <g opacity={t < i4.start ? 1 : 0.4}>
          <Bucket x={180} y={1250} s={0.7} />
        </g>
      )}
      <Figure p={kid} ch={KID1} facing={facing} face={face} t={t} ground={i5.start <= t ? 1180 : GROUND} />
      <rect x={-200} y={-200} width={1500} height={2400} fill="#0b0f2a" opacity={dark * 0.55} />
      {t >= i5.start ? (
        <g>
          <circle cx={hands + 10} cy={1040} r={260} fill="#7fd3ff" opacity={0.22 * dark} />
          <Tablet x={hands + 10} y={1040} s={0.75} glow={1} />
          {/* screen light on the face */}
          <circle cx={kid.x + 30} cy={890} r={90} fill="#9fe3ff" opacity={0.25 * dark} />
        </g>
      ) : null}
      {[
        { at: no2, x: 230, y: 470, icon: <Shoe x={0} y={0} s={0.8} />, word: "SỢ NGÃ" },
        { at: no3, x: 520, y: 400, icon: <Bucket x={0} y={10} s={0.75} />, word: "SỢ BẨN" },
        {
          at: no4,
          x: 810,
          y: 470,
          icon: (
            <g>
              <Sun x={-20} y={-15} r={34} t={t} />
              <g transform="scale(0.45)">
                <Wind x={40} y={40} t={t} color="#7aa8ff" />
              </g>
            </g>
          ),
          word: "SỢ GIÓ",
        },
      ].map((c) => (
        <g key={c.word} opacity={1 - dark * 0.7}>
          <Pop t={t} t0={c.at - 0.15} x={c.x} y={c.y} rot={-10}>
            <Card w={180} h={180} r={36}>
              {c.icon}
              <XMark x={0} y={0} p={ramp(t, c.at + 0.1, c.at + 0.45)} />
            </Card>
          </Pop>
          <Stamp t={t} t0={c.at + 0.35} x={c.x} y={c.y + 150} text={c.word} rot={-8} />
        </g>
      ))}
      {t > screenAt ? (
        <g opacity={sp(t, screenAt)}>
          {Array.from({ length: 5 }).map((_, i) => {
            const a = -Math.PI / 2 + (i - 2) * 0.35;
            const len = 160 + 30 * Math.sin(t * 4 + i);
            return (
              <line
                key={i}
                x1={hands + 10 + Math.cos(a) * 90}
                y1={1040 + Math.sin(a) * 90}
                x2={hands + 10 + Math.cos(a) * len}
                y2={1040 + Math.sin(a) * len}
                stroke="#9fe3ff"
                strokeWidth={8}
                strokeLinecap="round"
                opacity={0.7}
              />
            );
          })}
        </g>
      ) : null}
    </g>
  );
};
