import React from "react";
import { GROUND, Room } from "../lib/backdrops";
import { crouch, Figure, gesture, hop, idle, KID1, MOM } from "../lib/figure";
import { Check, FloatingHearts, Heart, Sparkles } from "../lib/icons";
import { clamp, L, PH, ramp, sp, WD } from "../lib/time";
import { Card, Label, Pop } from "../lib/ui";

// "Câu nào cũng xuất phát từ tình thương. Nhưng nếu tuổi thơ của con chỉ toàn
// chữ đừng, thì con còn bao nhiêu cơ hội để được thử, được sai, và được lớn?"
export const Love: React.FC<{ t: number }> = ({ t }) => {
  const heartAt = WD("l1", "thương");
  const cageAt = WD("l2", "đừng");
  const freeAt = PH("l3", 1);
  const chips = [PH("l3", 1), PH("l3", 2), PH("l3", 3)];
  const heartK = sp(t, heartAt - 0.2) * (1 - 0.55 * ramp(t, PH("l2", 0), PH("l2", 1)));
  const kidX = 470;
  const hugging = t < L("l2").start;
  const mom = hugging ? gesture(crouch(idle(t, 640), 0.85), "hug") : gesture(idle(t, 700), t > freeAt ? "open" : "rest");
  const grown = 0.62 + 0.1 * sp(t, chips[2]);
  const kid =
    t > chips[2] + 0.2
      ? hop(t - chips[2], kidX, 0.6, 90)
      : t > freeAt
        ? gesture(idle(t, kidX), "up", t, 8)
        : gesture(idle(t, kidX), t > cageAt ? "sad" : "rest");
  const kidFace = t > freeAt ? "joy" : t > cageAt ? "sad" : "happy";
  const bars = [-170, -100, -30, 40, 110, 180];
  return (
    <g>
      <Room id="love" t={t} sofa={false} door={false} />
      <g transform={`translate(560 640) scale(${heartK * (1 + 0.04 * Math.sin(t * 6))})`}>
        <circle r={300} fill="#ff8fa6" opacity={0.18} />
        <Heart x={0} y={0} s={230} fill="#ff6b8a" />
        <Heart x={-60} y={-60} s={60} fill="#ffffff" />
      </g>
      <FloatingHearts x={560} y={900} t={t} t0={heartAt} n={7} spread={420} />
      <Figure p={mom} ch={MOM} facing={-1} face={t > cageAt && t < freeAt ? "worried" : "happy"} t={t} ground={GROUND} />
      <Figure p={kid} ch={{ ...KID1, k: grown }} facing={1} face={kidFace} t={t} ground={GROUND} />
      {/* cage made of "ĐỪNG" bars */}
      {bars.map((dx, i) => {
        const drop = sp(t, cageAt + i * 0.06, 12, 180);
        const fly = ramp(t, freeAt + i * 0.05, freeAt + 0.6 + i * 0.05);
        if (drop <= 0 || fly >= 1) return null;
        const y = -700 + 700 * drop - fly * 900;
        const x = kidX + dx + fly * dx * 3;
        return (
          <g key={i} transform={`translate(${x} ${1060 + y}) rotate(${fly * dx * 0.4})`} opacity={1 - fly}>
            <rect x={-26} y={-260} width={52} height={500} rx={26} fill="#5a5f86" />
            <g transform="rotate(90)">
              <Label size={34} fill="#ffffff">
                ĐỪNG
              </Label>
            </g>
          </g>
        );
      })}
      {sp(t, cageAt) > 0 && t < freeAt + 0.6 ? (
        <rect x={kidX - 230} y={780} width={460} height={30} rx={15} fill="#5a5f86" opacity={clamp(1 - ramp(t, freeAt, freeAt + 0.4)) * sp(t, cageAt + 0.35)} />
      ) : null}
      {["THỬ", "SAI", "LỚN"].map((w, i) => (
        <Pop key={w} t={t} t0={chips[i]} x={240 + i * 300} y={420 + (i === 1 ? -60 : 0)} rot={i === 1 ? 0 : i ? 12 : -12}>
          <Card w={250} h={150} r={75} fill={["#ffe27a", "#9fe6b8", "#9fd2ff"][i]}>
            <g transform="translate(-70 0) scale(0.55)">
              <Check x={0} y={0} p={ramp(t, chips[i] + 0.15, chips[i] + 0.5)} color="#1f8f55" />
            </g>
            <Label x={30} size={58}>
              {w}
            </Label>
          </Card>
        </Pop>
      ))}
      {t > chips[2] ? <Sparkles x={kidX} y={850} t={t} r={210} n={8} /> : null}
    </g>
  );
};
