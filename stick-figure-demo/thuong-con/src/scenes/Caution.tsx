import React from "react";
import { GROUND, Park } from "../lib/backdrops";
import { Figure, gesture, KID1, MOM, walkCycle } from "../lib/figure";
import { Check, Clock, Heart, Ice, Rain, Sun, XMark } from "../lib/icons";
import { L, PH, ramp, sp } from "../lib/time";
import { Card, Chip, Label, Pop } from "../lib/ui";

const DAYS = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];

// "Không có nghĩa là để con dầm mưa, phơi nắng gắt hay tắm nước lạnh buốt.
//  Mà là mỗi ngày cho con ra ngoài trời đúng lúc, đủ lâu, có bố mẹ ở bên."
export const Caution: React.FC<{ t: number }> = ({ t }) => {
  const n9 = L("n9");
  const noAt = [PH("n8", 2), PH("n8", 3), PH("n8", 4)];
  const outK = ramp(t, n9.start - 0.3, n9.start + 0.2);
  const weekAt = PH("n9", 0) + 0.3;
  const clockAt = PH("n9", 2);
  const familyAt = PH("n9", 3) - 0.2;
  const walking = t > n9.start;
  const pan = walking ? (t - n9.start) * 160 : 0;
  return (
    <g>
      <Park id="caution" t={t} pan={pan} />
      {outK < 1 ? (
        <g opacity={1 - outK} transform={`translate(0 ${-outK * 120})`}>
          <Pop t={t} t0={PH("n8", 1)} x={540} y={300}>
            <Chip text="KHÔNG PHẢI LÀ" fill="#ff4d5e" size={46} />
          </Pop>
          {[
            <Rain key="r" x={0} y={-30} t={t} s={1} />,
            <g key="s">
              <circle r={110} fill="#ff7a3d" opacity={0.25} />
              <Sun x={0} y={0} r={62} t={t * 3} />
            </g>,
            <Ice key="i" x={0} y={0} s={0.95} />,
          ].map((icon, i) => (
            <Pop key={i} t={t} t0={noAt[i] - 0.1} x={200 + i * 340} y={620} rot={i === 1 ? 0 : i ? 10 : -10}>
              <Card w={290} h={330} r={48}>
                <g transform="translate(0 -30)">{icon}</g>
                <Label y={120} size={44}>
                  {["DẦM MƯA", "NẮNG GẮT", "LẠNH BUỐT"][i]}
                </Label>
                <XMark x={0} y={-30} s={1.35} p={ramp(t, noAt[i] + 0.25, noAt[i] + 0.6)} />
              </Card>
            </Pop>
          ))}
        </g>
      ) : null}
      {walking ? (
        <g>
          <g transform={`translate(540 380) scale(${sp(t, weekAt - 0.2)})`}>
            <Card w={900} h={190} r={50}>
              {DAYS.map((d, i) => {
                const x = -360 + i * 120;
                const at = weekAt + i * 0.1;
                return (
                  <g key={d}>
                    <Label x={x} y={-45} size={34} fill="#7a7f9f">
                      {d}
                    </Label>
                    <circle cx={x} cy={30} r={38} fill="#d9f7e5" />
                    <g transform={`translate(${x} 30) scale(0.42)`}>
                      <Check x={0} y={0} p={ramp(t, at, at + 0.25)} />
                    </g>
                  </g>
                );
              })}
            </Card>
          </g>
          <Pop t={t} t0={clockAt - 0.1} x={270} y={690}>
            <Card w={330} h={250} r={48}>
              <Clock x={-75} y={-10} r={62} hour={7} />
              <Label x={75} y={-30} size={40} fill="#2fbf71">
                ĐÚNG
              </Label>
              <Label x={75} y={20} size={40} fill="#2fbf71">
                LÚC
              </Label>
            </Card>
          </Pop>
          <Pop t={t} t0={clockAt + 0.45} x={810} y={690}>
            <Card w={330} h={250} r={48}>
              <Label y={-30} size={40} fill="#2fbf71">
                ĐỦ LÂU
              </Label>
              <rect x={-110} y={20} width={220} height={36} rx={18} fill="#e5ecf5" />
              <rect x={-110} y={20} width={220 * ramp(t, clockAt + 0.5, clockAt + 1.3)} height={36} rx={18} fill="#2fbf71" />
            </Card>
          </Pop>
          <Figure p={gesture(walkCycle(t, 450), "hold")} ch={MOM} facing={1} face="happy" t={t} ground={GROUND} />
          <Figure p={{ ...walkCycle(t + 0.3, 620), la: -60, le: 10 }} ch={KID1} facing={1} face="joy" t={t} ground={GROUND} />
          {t > familyAt ? (
            <g transform={`translate(560 ${880 - 10 * Math.sin(t * 4)}) scale(${sp(t, familyAt)})`}>
              <Heart x={0} y={0} s={70} />
            </g>
          ) : null}
        </g>
      ) : null}
    </g>
  );
};
