import React from "react";
import { GROUND, Park } from "../lib/backdrops";
import { blend, Figure, gesture, hop, idle, KID1, MOM, move } from "../lib/figure";
import { Bone, Bowl, Drop, Eye, Moon, Mountains, Sparkles, Sun, Tree, Wind } from "../lib/icons";
import { clamp, L, mix, ramp, sp } from "../lib/time";
import { Card, Label } from "../lib/ui";

type Benefit = { id: string; title: string; icon: (t: number) => React.ReactNode; color: string };

const BENEFITS: Benefit[] = [
  {
    id: "n3",
    title: "XƯƠNG CHẮC KHOẺ",
    color: "#fff1c9",
    icon: (t) => (
      <g>
        <Sun x={-110} y={0} r={60} t={t} />
        <g transform="translate(110 0) rotate(-20)">
          <g transform="scale(0.85)">
            <rect x={-95} y={-60} width={190} height={120} rx={60} fill="#ffd66b" opacity={0.35} />
            <Bone x={0} y={0} />
          </g>
        </g>
      </g>
    ),
  },
  {
    id: "n4",
    title: "KHÍ TRỜI TRONG LÀNH",
    color: "#dcf6e4",
    icon: (t) => (
      <g>
        <Tree x={-110} base={110} s={0.5} t={t} />
        <g transform="translate(70 -20) scale(0.8)">
          <Wind x={0} y={-20} t={t} color="#46a862" />
        </g>
      </g>
    ),
  },
  {
    id: "n5",
    title: "SẢNG KHOÁI",
    color: "#dff1ff",
    icon: (t) => (
      <g>
        {[0, 1, 2, 3, 4].map((i) => (
          <Drop key={i} x={-120 + i * 60} y={-10 + 20 * Math.sin(t * 6 + i)} s={0.9 + 0.2 * (i % 2)} />
        ))}
      </g>
    ),
  },
  {
    id: "n6",
    title: "ĂN NGON · NGỦ SÂU",
    color: "#ffe6dc",
    icon: () => (
      <g>
        <Bowl x={-100} y={40} s={0.9} />
        <g transform="translate(110 -10)">
          <circle r={85} fill="#3b3f78" />
          <Moon x={0} y={0} s={0.9} />
        </g>
      </g>
    ),
  },
  {
    id: "n7",
    title: "MẮT ĐƯỢC NGHỈ",
    color: "#e6efff",
    icon: () => (
      <g>
        <g transform="translate(-110 0)">
          <Eye x={0} y={0} s={0.9} />
        </g>
        <g transform="translate(20 -150) scale(0.35)">
          <Mountains base={500} color="#8fbfa8" h={260} />
        </g>
      </g>
    ),
  },
];

// Thuận theo tự nhiên: dawn turns into a bright day; each benefit gets a card.
export const Nature: React.FC<{ t: number }> = ({ t }) => {
  const [n1, n2, n3, n4, n5, n6, n7] = ["n1", "n2", "n3", "n4", "n5", "n6", "n7"].map(L);
  const day = ramp(t, n1.start, n3.start + 0.5);
  const sky: [string, string] = [mixColor("#ffb58a", "#6fc3ff", day), mixColor("#ffe7c7", "#e3f5ff", day)];
  const sunY = mix(1150, 330, ramp(t, n2.start - 0.4, n3.start + 0.4));

  let kid = idle(t, 560);
  let face: "joy" | "happy" | "focus" = "happy";
  let facing = 1;
  if (t < n2.start) {
    kid = move(t, -100, 560, n1.start - 0.4, n1.end, true).pose;
    face = "joy";
  } else if (t < n3.start) {
    kid = gesture(idle(t, 560), "up", t, 6);
    face = "joy";
  } else if (t < n4.start) {
    kid = gesture(idle(t, 560), "up");
    face = "happy";
  } else if (t < n5.start) {
    const breathe = 0.5 + 0.5 * Math.sin((t - n4.start) * 3);
    kid = { ...gesture(idle(t, 560), "open"), lean: -8 * breathe, la: -70 - 30 * breathe, ra: 80 + 30 * breathe };
    face = "happy";
  } else if (t < n6.start) {
    kid = blend(gesture(idle(t, 560), "dig"), gesture(idle(t, 560), "splash"), clamp(0.5 + 0.5 * Math.sin((t - n5.start) * 5)));
    face = "joy";
    facing = -1;
  } else if (t < n7.start) {
    kid = hop(t - n6.start, 560, 0.62, 95);
    face = "joy";
  } else {
    kid = gesture(idle(t, 560), "visor");
    face = "focus";
  }
  const cardIdx = BENEFITS.findIndex((b, i) => t >= L(b.id).start - 0.25 && (i === BENEFITS.length - 1 || t < L(BENEFITS[i + 1].id).start - 0.25));
  return (
    <g>
      <Park id="nature" t={t} sky={sky} sunY={sunY} />
      <Figure p={idle(t, 860)} ch={MOM} facing={-1} face="happy" t={t} ground={GROUND} />
      {t >= n5.start && t < n6.start + 0.2 ? (
        <g>
          <ellipse cx={440} cy={GROUND - 20} rx={95} ry={30} fill="#5bb7ff" />
          <path d={`M 345 ${GROUND - 20} L 370 ${GROUND + 20} L 510 ${GROUND + 20} L 535 ${GROUND - 20} Z`} fill="#ffcf4a" />
          {Array.from({ length: 6 }).map((_, i) => {
            const ph = (t * 1.8 + i / 6) % 1;
            return <Drop key={i} x={440 + (i - 2.5) * 30 + ph * (i - 2.5) * 40} y={GROUND - 60 - Math.sin(ph * Math.PI) * 220} s={0.55} />;
          })}
        </g>
      ) : null}
      <Figure p={kid} ch={KID1} facing={facing} face={face} t={t} ground={GROUND} />
      {t >= n2.start - 0.2 && t < n3.start ? <Sparkles x={560} y={820} t={t} r={230} n={8} /> : null}
      {t >= n2.start - 0.2 && t < n3.start + 0.2 ? (
        <g transform={`translate(540 560) scale(${sp(t, n2.start - 0.2)})`} opacity={1 - ramp(t, n3.start - 0.2, n3.start + 0.2)}>
          <Label size={110} fill="#ffffff" stroke="#e86f3a">
            THUẬN
          </Label>
          <Label y={120} size={90} fill="#fff3c4" stroke="#e86f3a">
            TỰ NHIÊN
          </Label>
        </g>
      ) : null}
      {cardIdx >= 0
        ? BENEFITS.map((b, i) => {
            const at = L(b.id).start - 0.25;
            const nextAt = i < BENEFITS.length - 1 ? L(BENEFITS[i + 1].id).start - 0.25 : 1e9;
            if (t < at || t > nextAt + 0.5) return null;
            const inK = sp(t, at, 13, 140);
            const outK = ramp(t, nextAt, nextAt + 0.45);
            const x = 540 + (1 - inK) * 900 - outK * 1000;
            return (
              <g key={b.id} transform={`translate(${x} 470) rotate(${(1 - inK) * 10 - outK * 8})`}>
                <Card w={820} h={380} r={60} fill={b.color}>
                  <g transform="translate(0 -40)">{b.icon(t)}</g>
                  <Label y={135} size={60}>
                    {b.title}
                  </Label>
                </Card>
              </g>
            );
          })
        : null}
    </g>
  );
};

function mixColor(a: string, b: string, k: number) {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return `rgb(${pa.map((v, i) => Math.round(v + (pb[i] - v) * k)).join(",")})`;
}
