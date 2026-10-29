import React from "react";
import { GROUND, Room } from "../lib/backdrops";
import { blend, crouch, Figure, gesture, idle, KID1, MOM, move, walkCycle } from "../lib/figure";
import { Bucket, Drop, Shoe, Sun, Wind, XMark } from "../lib/icons";
import { L, ramp, talking } from "../lib/time";
import { Bubble, Card, Label, Pop } from "../lib/ui";

// Five "Đừng..." lines: each pins a crossed-out card above the child.
const CARDS = [
  { id: "h1", x: 170, y: 470 },
  { id: "h2", x: 360, y: 380 },
  { id: "h3", x: 550, y: 340 },
  { id: "h4", x: 740, y: 380 },
  { id: "h5", x: 930, y: 470 },
];

const CardIcon: React.FC<{ i: number; t: number }> = ({ i, t }) => {
  switch (i) {
    case 0:
      return (
        <g transform="scale(0.7)">
          <Wind x={-10} y={-40} t={t} color="#7aa8ff" />
        </g>
      );
    case 1:
      return <Bucket x={0} y={10} s={0.8} />;
    case 2:
      return (
        <g>
          <Drop x={-35} y={-5} s={1.1} />
          <Drop x={30} y={-25} s={0.8} />
          <Drop x={20} y={35} s={0.9} />
        </g>
      );
    case 3:
      return <Sun x={0} y={0} r={36} t={t} />;
    default:
      return <Shoe x={0} y={0} s={0.8} />;
  }
};

export const Hook: React.FC<{ t: number }> = ({ t }) => {
  const [h1, h2, h3, h4, h5] = ["h1", "h2", "h3", "h4", "h5"].map(L);
  // child: heads for the door, digs, wants a shower, reaches for sun, runs
  let kid = idle(t, 420);
  let facing = -1;
  let face: "happy" | "sad" | "surprised" | "worried" = "happy";
  if (t < h1.start + 0.5) {
    const m = move(t, 470, 330, 0, h1.start + 0.5);
    kid = m.pose;
    facing = m.facing;
  } else if (t < h2.start) {
    kid = idle(t, 330);
    face = "surprised";
  } else if (t < h3.start) {
    kid = crouch(gesture(idle(t, 380), "dig", t, 10), Math.min(1, (t - h2.start) / 0.3));
    facing = 1;
    face = t > h2.start + 0.5 ? "surprised" : "happy";
  } else if (t < h4.start) {
    kid = gesture(idle(t, 400), "up", t, 6);
    facing = 1;
    face = t > h3.start + 0.5 ? "surprised" : "happy";
  } else if (t < h5.start) {
    kid = gesture(idle(t, 420), "reach");
    facing = 1;
    face = "worried";
  } else if (t < h5.start + 0.6) {
    kid = walkCycle(t, 420, true);
    facing = 1;
  } else {
    kid = blend(walkCycle(h5.start + 0.6, 420, true), gesture(idle(t, 420), "sad"), Math.min(1, (t - h5.start - 0.6) / 0.3));
    facing = 1;
    face = "sad";
  }
  // mom raises a hand on every line
  const lines = [h1, h2, h3, h4, h5];
  const speakingLine = lines.find((l) => t >= l.start - 0.1 && t <= l.end + 0.2);
  const mom = speakingLine ? gesture(idle(t, 790), "stop", t, 5) : idle(t, 790);
  return (
    <g>
      <Room id="hook" t={t} curtain={ramp(t, h4.start, h4.start + 0.6) * 0.9} />
      <Figure p={mom} ch={MOM} facing={-1} face="worried" talk={talking(t, "h1", "h2", "h3", "h4", "h5")} t={t} ground={GROUND} />
      <Figure p={kid} ch={KID1} facing={facing} face={face} t={t} ground={GROUND} />
      {CARDS.map((c, i) => {
        const l = lines[i];
        return (
          <Pop key={c.id} t={t} t0={l.start - 0.05} x={c.x} y={c.y} rot={i % 2 ? 14 : -14}>
            <Card w={170} h={170} r={34}>
              <CardIcon i={i} t={t} />
              <XMark x={0} y={0} s={1} p={ramp(t, l.start + 0.25, l.start + 0.65)} />
            </Card>
          </Pop>
        );
      })}
      {lines.map((l) => (
        <Bubble key={l.id} t={t} t0={l.start} t1={l.end + 0.1} x={820} y={560} w={150} h={120} tx={800} ty={660} fill="#fff1f2">
          <Label size={84} fill="#ff4d5e">
            !
          </Label>
        </Bubble>
      ))}
    </g>
  );
};
