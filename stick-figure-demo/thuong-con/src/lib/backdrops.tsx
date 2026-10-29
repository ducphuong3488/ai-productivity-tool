import React from "react";
import { INK } from "./figure";
import { Cloud, Mountains, Sun, Tree } from "./icons";
import { H, W } from "./time";

export const GROUND = 1300;

export const Gradient: React.FC<{ id: string; top: string; bottom: string; y0?: number; y1?: number }> = ({
  id,
  top,
  bottom,
  y0 = 0,
  y1 = H,
}) => (
  <linearGradient id={id} x1="0" y1={y0} x2="0" y2={y1} gradientUnits="userSpaceOnUse">
    <stop offset="0" stopColor={top} />
    <stop offset="1" stopColor={bottom} />
  </linearGradient>
);

/** Living room: wall, floor, window, door, sofa. `cool` gives the gloomy look. */
export const Room: React.FC<{ id: string; cool?: boolean; curtain?: number; door?: boolean; sofa?: boolean; t?: number }> = ({
  id,
  cool = false,
  curtain = 0,
  door = true,
  sofa = true,
  t = 0,
}) => {
  const wall = cool ? ["#c9d0e6", "#aeb6d3"] : ["#fbefe4", "#f3dcc8"];
  const floor = cool ? ["#8f93ad", "#5f6380"] : ["#e3b28a", "#b9825c"];
  return (
    <g>
      <defs>
        <Gradient id={`${id}-wall`} top={wall[0]} bottom={wall[1]} y1={GROUND} />
        <Gradient id={`${id}-floor`} top={floor[0]} bottom={floor[1]} y0={GROUND} />
        <Gradient id={`${id}-sky`} top="#8fd3ff" bottom="#e6f6ff" y0={330} y1={760} />
      </defs>
      <rect width={W} height={GROUND} fill={`url(#${id}-wall)`} />
      <rect y={GROUND} width={W} height={H - GROUND} fill={`url(#${id}-floor)`} />
      <rect y={GROUND - 16} width={W} height={16} fill="rgba(0,0,0,0.12)" />
      {/* window */}
      <rect x={640} y={310} width={360} height={470} rx={18} fill="#ffffff" />
      <rect x={662} y={332} width={316} height={426} rx={8} fill={`url(#${id}-sky)`} />
      <Sun x={880} y={430} r={46} t={t} rays={false} />
      <Cloud x={740} y={560} s={0.5} />
      <rect x={815} y={332} width={10} height={426} fill="#ffffff" />
      <rect x={662} y={540} width={316} height={10} fill="#ffffff" />
      {/* curtains */}
      <rect x={622} y={290} width={30 + 170 * curtain} height={520} rx={14} fill={cool ? "#7d7fa8" : "#f59fae"} />
      <rect x={988 - 170 * curtain} y={290} width={30 + 170 * curtain} height={520} rx={14} fill={cool ? "#7d7fa8" : "#f59fae"} />
      <rect x={600} y={278} width={440} height={18} rx={9} fill={INK} opacity={0.75} />
      {door ? (
        <g>
          <rect x={60} y={680} width={260} height={GROUND - 680} rx={10} fill={cool ? "#8a7a92" : "#c98a5e"} />
          <rect x={86} y={706} width={208} height={250} rx={8} fill="#ffffff" opacity={0.15} />
          <circle cx={282} cy={1010} r={14} fill="#ffd66b" />
        </g>
      ) : null}
      {sofa ? (
        <g>
          <rect x={470} y={1050} width={560} height={200} rx={50} fill={cool ? "#6e7499" : "#7fb6c9"} />
          <rect x={440} y={1120} width={620} height={150} rx={50} fill={cool ? "#5d6388" : "#6aa3b8"} />
          <rect x={470} y={1260} width={24} height={40} fill={INK} />
          <rect x={1006} y={1260} width={24} height={40} fill={INK} />
        </g>
      ) : null}
    </g>
  );
};

/** Sunny park with hills and trees. `pan` shifts the far layers for parallax. */
export const Park: React.FC<{ id: string; t: number; pan?: number; sky?: [string, string]; sunY?: number; trees?: boolean }> = ({
  id,
  t,
  pan = 0,
  sky = ["#7cc8ff", "#dff3ff"],
  sunY = 300,
  trees = true,
}) => (
  <g>
    <defs>
      <Gradient id={`${id}-sky`} top={sky[0]} bottom={sky[1]} y1={GROUND} />
      <Gradient id={`${id}-grass`} top="#8fd47f" bottom="#4e9a5a" y0={GROUND - 120} />
    </defs>
    <rect width={W} height={H} fill={`url(#${id}-sky)`} />
    <Sun x={860} y={sunY} r={80} t={t} />
    <Cloud x={(200 - pan * 0.1 + t * 8) % 1300 - 100} y={260} s={0.9} />
    <Cloud x={(650 - pan * 0.1 + t * 5) % 1300 - 100} y={420} s={0.6} opacity={0.9} />
    <g transform={`translate(${-pan * 0.25} 0)`}>
      <Mountains base={GROUND - 120} color="#a9d7c0" seed={2} h={300} />
    </g>
    <ellipse cx={300 - pan * 0.4} cy={GROUND + 40} rx={700} ry={230} fill="#83c97a" />
    <ellipse cx={950 - pan * 0.4} cy={GROUND + 60} rx={650} ry={210} fill="#76c06f" />
    {trees ? (
      <g transform={`translate(${-pan * 0.6} 0)`}>
        <Tree x={110} base={GROUND - 40} s={1.05} t={t} />
        <Tree x={980} base={GROUND - 30} s={1.2} t={t} color="#46a862" />
      </g>
    ) : null}
    <rect y={GROUND} width={W} height={H - GROUND} fill={`url(#${id}-grass)`} />
    {Array.from({ length: 26 }).map((_, i) => {
      const x = ((i * 47 - pan) % (W + 60) + W + 60) % (W + 60) - 30;
      const sway = Math.sin(t * 3 + i) * 6;
      return (
        <path
          key={i}
          d={`M ${x} ${GROUND + 6} q ${4 + sway} -22 ${8 + sway} -34 M ${x + 8} ${GROUND + 6} q ${2 + sway} -16 ${-4 + sway} -26`}
          stroke="#3f8f4e"
          strokeWidth={5}
          fill="none"
          strokeLinecap="round"
        />
      );
    })}
  </g>
);

/** Soft gradient studio background for "info" scenes. */
export const Studio: React.FC<{ id: string; top: string; bottom: string; dots?: string; t?: number }> = ({
  id,
  top,
  bottom,
  dots = "#ffffff",
  t = 0,
}) => (
  <g>
    <defs>
      <Gradient id={`${id}-bg`} top={top} bottom={bottom} />
      <radialGradient id={`${id}-glow`} cx="540" cy="760" r="760" gradientUnits="userSpaceOnUse">
        <stop offset="0" stopColor="#ffffff" stopOpacity={0.35} />
        <stop offset="1" stopColor="#ffffff" stopOpacity={0} />
      </radialGradient>
    </defs>
    <rect width={W} height={H} fill={`url(#${id}-bg)`} />
    <rect width={W} height={H} fill={`url(#${id}-glow)`} />
    {Array.from({ length: 24 }).map((_, i) => {
      const x = ((i * 137) % W) + 20 * Math.sin(t * 0.6 + i);
      const y = ((i * 263 + 1000 - t * (14 + (i % 5) * 6)) % H + H) % H;
      return <circle key={i} cx={x} cy={y} r={3 + (i % 4) * 2} fill={dots} opacity={0.18} />;
    })}
  </g>
);
