import React from "react";
import { GROUND, Park } from "../lib/backdrops";
import { blend, crouch, DAD, Figure, gesture, hop, idle, KID2, move, P } from "../lib/figure";
import { Bird, Drop, Sparkles, Sprout, Star } from "../lib/icons";
import { L, PH, ramp, sp, WD } from "../lib/time";

// Bé thứ hai: runs on the grass, plants a tree with dad, climbs over a log,
// balances, trips and gets back up.
export const Outdoor: React.FC<{ t: number }> = ({ t }) => {
  const [o1, o2, o3, o4] = ["o1", "o2", "o3", "o4"].map(L);
  const plantAt = PH("o2", 1);
  const logX = 330;
  const balanceAt = PH("o3", 1);
  const tripAt = o4.start + 0.1;
  const upAt = WD("o4", "dậy") - 0.15;
  const cheerAt = PH("o4", 1) + 0.2;

  let kid = idle(t, 760);
  let facing = 1;
  let face: "happy" | "joy" | "focus" | "surprised" | "sad" = "happy";
  let lean = 0;
  if (t < o1.end) {
    const m = move(t, -120, 760, o1.start - 0.3, o1.end, true);
    kid = m.pose;
    face = "joy";
  } else if (t < o2.start + 0.5) {
    const m = move(t, 760, 640, o1.end + 0.05, o2.start + 0.5);
    kid = m.pose;
    facing = -1;
  } else if (t < o3.start) {
    kid = crouch(gesture(idle(t, 640), "dig", t, 8), Math.min(1, (t - o2.start - 0.5) / 0.3));
    facing = -1;
    face = "focus";
  } else if (t < balanceAt) {
    const m = move(t, 640, 220, o3.start, balanceAt - 0.1);
    kid = m.pose;
    facing = -1;
    const x = kid.x;
    const near = Math.max(0, 1 - Math.abs(x - logX) / 70);
    kid = { ...kid, dy: kid.dy - 70 * Math.sin(near * Math.PI * 0.5), lt: kid.lt + 40 * near, lk: kid.lk + 40 * near };
    face = "focus";
  } else if (t < tripAt) {
    kid = gesture(P(220, { lt: 55, lk: 95, rt: -2, rk: 2 }), "balance");
    lean = 9 * Math.sin(t * 7);
    face = "focus";
  } else if (t < upAt) {
    const k = ramp(t, tripAt, tripAt + 0.25);
    const fallen = { ...gesture(idle(t, 300), "balance"), dy: 150, lean: 35, lt: 80, lk: 30, rt: 70, rk: 20 };
    kid = blend(gesture(idle(t, 260), "balance"), fallen, k);
    face = "surprised";
  } else if (t < cheerAt) {
    const fallen = { ...gesture(idle(t, 300), "balance"), dy: 150, lean: 35, lt: 80, lk: 30, rt: 70, rk: 20 };
    kid = blend(fallen, idle(t, 300), (t - upAt) / 0.45);
    face = "focus";
  } else {
    kid = hop(t - cheerAt, 300, 0.6, 100);
    face = "joy";
  }
  kid = { ...kid, lean: kid.lean + lean };

  const dadT = t < o2.start ? gesture(idle(t, 470), "wave", t, 10) : t < o3.start ? gesture(crouch(idle(t, 470), 0.8), "dig", t, 8) : gesture(idle(t, 760), t > cheerAt ? "clap" : "open", t, t > cheerAt ? 10 : 0);
  const dadPose = t >= o3.start && t < o3.start + 0.8 ? move(t, 470, 760, o3.start, o3.start + 0.8).pose : dadT;
  const dadFacing = t >= o3.start && t < o3.start + 0.8 ? 1 : t < o3.start ? 1 : -1;
  const pan = 0;
  return (
    <g>
      <Park id="outdoor" t={t} pan={pan} />
      {Array.from({ length: 3 }).map((_, i) => (
        <Bird key={i} x={((t * 60 + i * 260) % 1300) - 100} y={360 + i * 50} t={t} s={0.9} />
      ))}
      {/* flowers that pop up along the run */}
      {Array.from({ length: 7 }).map((_, i) => {
        const x = 80 + i * 140;
        const k = sp(t, PH("o1", 2) + i * 0.08);
        return (
          <g key={i} transform={`translate(${x} ${GROUND + 40}) scale(${k})`}>
            <line x1={0} y1={0} x2={0} y2={-40} stroke="#3f8f4e" strokeWidth={6} />
            {[0, 1, 2, 3, 4].map((p) => (
              <circle key={p} cx={Math.cos((p / 5) * Math.PI * 2) * 13} cy={-46 + Math.sin((p / 5) * Math.PI * 2) * 13} r={10} fill={["#ff7aa2", "#ffd23f", "#ffffff"][i % 3]} />
            ))}
            <circle cx={0} cy={-46} r={8} fill="#ffb02e" />
          </g>
        );
      })}
      <Sprout x={555} base={GROUND + 10} grow={sp(t, plantAt, 14, 90)} s={1.1} />
      {t > plantAt && t < o3.start + 0.3
        ? Array.from({ length: 3 }).map((_, i) => {
            const ph = (t * 1.6 + i / 3) % 1;
            return <Drop key={i} x={540 + i * 15} y={GROUND - 260 + ph * 200} s={0.5} />;
          })
        : null}
      {t > plantAt + 0.4 ? <Sparkles x={555} y={GROUND - 120} t={t} r={110} n={5} /> : null}
      {/* log obstacle */}
      <g>
        <rect x={logX - 70} y={GROUND - 46} width={140} height={46} rx={23} fill="#a8683f" />
        <circle cx={logX + 70} cy={GROUND - 23} r={23} fill="#c98a5e" />
        <circle cx={logX + 70} cy={GROUND - 23} r={11} fill="#a8683f" />
      </g>
      <Figure p={dadPose} ch={DAD} facing={dadFacing} face="happy" t={t} ground={GROUND} />
      <Figure p={kid} ch={KID2} facing={facing} face={face} t={t} ground={GROUND} />
      {t > tripAt && t < upAt + 0.5
        ? [0, 1, 2].map((i) => {
            const a = t * 5 + (i * Math.PI * 2) / 3;
            return <Star key={i} x={330 + Math.cos(a) * 60} y={1150 + Math.sin(a) * 18} r={16} rot={t * 4} />;
          })
        : null}
    </g>
  );
};
