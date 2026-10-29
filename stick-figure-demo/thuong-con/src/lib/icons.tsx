import React from "react";
import { INK } from "./figure";
import { clamp, rand } from "./time";

type XY = { x: number; y: number };

export const Sun: React.FC<XY & { r?: number; t?: number; rays?: boolean }> = ({ x, y, r = 80, t = 0, rays = true }) => (
  <g>
    <circle cx={x} cy={y} r={r * 1.9} fill="#ffd66b" opacity={0.18} />
    <circle cx={x} cy={y} r={r * 1.4} fill="#ffd66b" opacity={0.25} />
    {rays
      ? Array.from({ length: 12 }).map((_, i) => {
          const a = (i / 12) * Math.PI * 2 + t * 0.4;
          return (
            <line
              key={i}
              x1={x + Math.cos(a) * r * 1.15}
              y1={y + Math.sin(a) * r * 1.15}
              x2={x + Math.cos(a) * r * (1.45 + 0.08 * Math.sin(t * 3 + i))}
              y2={y + Math.sin(a) * r * (1.45 + 0.08 * Math.sin(t * 3 + i))}
              stroke="#ffc53d"
              strokeWidth={r * 0.12}
              strokeLinecap="round"
            />
          );
        })
      : null}
    <circle cx={x} cy={y} r={r} fill="#ffcf4a" />
    <circle cx={x - r * 0.25} cy={y - r * 0.25} r={r * 0.55} fill="#ffe28a" />
  </g>
);

export const Cloud: React.FC<XY & { s?: number; fill?: string; opacity?: number }> = ({
  x,
  y,
  s = 1,
  fill = "#ffffff",
  opacity = 1,
}) => (
  <g opacity={opacity}>
    {(
      [
        [-70, 10, 55],
        [0, -20, 75],
        [75, 5, 60],
        [30, 25, 55],
        [-30, 28, 50],
      ] as const
    ).map(([dx, dy, r], i) => (
      <circle key={i} cx={x + dx * s} cy={y + dy * s} r={r * s} fill={fill} />
    ))}
  </g>
);

export const Heart: React.FC<XY & { s?: number; fill?: string }> = ({ x, y, s = 40, fill = "#ff5a7a" }) => {
  const d: string[] = [];
  for (let i = 0; i <= 40; i++) {
    const a = (i / 40) * Math.PI * 2;
    const hx = 16 * Math.sin(a) ** 3;
    const hy = -(13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a));
    d.push(`${i ? "L" : "M"} ${x + (hx * s) / 16} ${y + (hy * s) / 16}`);
  }
  return <path d={d.join(" ") + " Z"} fill={fill} />;
};

export const Tree: React.FC<{ x: number; base: number; s?: number; t?: number; color?: string }> = ({
  x,
  base,
  s = 1,
  t = 0,
  color = "#4fb26b",
}) => {
  const sway = Math.sin(t * 1.6 + x) * 6 * s;
  return (
    <g>
      <path
        d={`M ${x - 16 * s} ${base} L ${x - 10 * s} ${base - 220 * s} L ${x + 10 * s} ${base - 220 * s} L ${x + 16 * s} ${base} Z`}
        fill="#8a5a3c"
      />
      <circle cx={x + sway} cy={base - 300 * s} r={115 * s} fill={color} />
      <circle cx={x - 75 * s + sway * 0.8} cy={base - 235 * s} r={85 * s} fill={color} />
      <circle cx={x + 75 * s + sway * 0.8} cy={base - 235 * s} r={85 * s} fill={color} />
      <circle cx={x - 30 * s + sway} cy={base - 340 * s} r={55 * s} fill="#ffffff" opacity={0.12} />
    </g>
  );
};

export const Sprout: React.FC<{ x: number; base: number; grow: number; s?: number }> = ({ x, base, grow, s = 1 }) => {
  const h = 150 * s * grow;
  const leaf = 55 * s * clamp(grow * 1.4 - 0.3);
  return (
    <g>
      <ellipse cx={x} cy={base} rx={80 * s} ry={22 * s} fill="#7a4e31" />
      <line x1={x} y1={base} x2={x} y2={base - h} stroke="#3e9e57" strokeWidth={10 * s} strokeLinecap="round" />
      {leaf > 1 ? (
        <>
          <ellipse cx={x - leaf * 0.7} cy={base - h * 0.75} rx={leaf} ry={leaf * 0.45} fill="#5cc777" transform={`rotate(-25 ${x - leaf * 0.7} ${base - h * 0.75})`} />
          <ellipse cx={x + leaf * 0.7} cy={base - h * 0.95} rx={leaf} ry={leaf * 0.45} fill="#5cc777" transform={`rotate(25 ${x + leaf * 0.7} ${base - h * 0.95})`} />
        </>
      ) : null}
    </g>
  );
};

export const Stone: React.FC<XY & { s?: number; fill?: string }> = ({ x, y, s = 1, fill = "#9aa3b5" }) => (
  <g>
    <ellipse cx={x} cy={y - 16 * s} rx={40 * s} ry={26 * s} fill={fill} />
    <ellipse cx={x - 10 * s} cy={y - 24 * s} rx={16 * s} ry={8 * s} fill="#ffffff" opacity={0.3} />
  </g>
);

export const Drop: React.FC<XY & { s?: number; fill?: string }> = ({ x, y, s = 1, fill = "#5bb7ff" }) => (
  <path
    d={`M ${x} ${y - 30 * s} C ${x + 20 * s} ${y - 5 * s} ${x + 20 * s} ${y + 18 * s} ${x} ${y + 18 * s} C ${x - 20 * s} ${y + 18 * s} ${x - 20 * s} ${y - 5 * s} ${x} ${y - 30 * s} Z`}
    fill={fill}
  />
);

export const Bird: React.FC<XY & { s?: number; t?: number }> = ({ x, y, s = 1, t = 0 }) => {
  const f = Math.sin(t * 9 + x) * 14 * s;
  return (
    <path
      d={`M ${x - 26 * s} ${y - f} Q ${x - 12 * s} ${y - 14 * s} ${x} ${y} Q ${x + 12 * s} ${y - 14 * s} ${x + 26 * s} ${y - f}`}
      stroke={INK}
      strokeWidth={5 * s}
      fill="none"
      strokeLinecap="round"
    />
  );
};

/** Animated red cross, drawn stroke by stroke as `p` goes 0 -> 1. */
export const XMark: React.FC<XY & { s?: number; p: number; color?: string }> = ({ x, y, s = 1, p, color = "#ff4d5e" }) => {
  const a = clamp(p * 2);
  const b = clamp(p * 2 - 1);
  const L = 60 * s;
  return (
    <g strokeLinecap="round" stroke={color} strokeWidth={18 * s}>
      {a > 0 ? <line x1={x - L} y1={y - L} x2={x - L + 2 * L * a} y2={y - L + 2 * L * a} /> : null}
      {b > 0 ? <line x1={x + L} y1={y - L} x2={x + L - 2 * L * b} y2={y - L + 2 * L * b} /> : null}
    </g>
  );
};

export const Check: React.FC<XY & { s?: number; p: number; color?: string }> = ({ x, y, s = 1, p, color = "#2fbf71" }) => {
  const len = 150 * s;
  return (
    <path
      d={`M ${x - 45 * s} ${y} L ${x - 12 * s} ${y + 32 * s} L ${x + 50 * s} ${y - 36 * s}`}
      stroke={color}
      strokeWidth={18 * s}
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray={len}
      strokeDashoffset={len * (1 - clamp(p))}
    />
  );
};

export const Wind: React.FC<XY & { t: number; s?: number; color?: string }> = ({ x, y, t, s = 1, color = "#ffffff" }) => (
  <g stroke={color} strokeWidth={9 * s} fill="none" strokeLinecap="round" opacity={0.9}>
    {[0, 1, 2].map((i) => {
      const off = ((t * 180 + i * 90) % 300) * s;
      return (
        <path
          key={i}
          d={`M ${x - 120 * s + off} ${y + i * 40 * s} q ${60 * s} ${-20 * s} ${120 * s} 0 t ${80 * s} ${-25 * s}`}
          opacity={1 - off / (300 * s)}
        />
      );
    })}
  </g>
);

export const Mountains: React.FC<{ base: number; color: string; seed?: number; h?: number }> = ({ base, color, seed = 1, h = 260 }) => {
  const d: string[] = [`M -20 ${base}`];
  for (let i = 0; i <= 6; i++) {
    const x = -20 + i * 190;
    const peak = base - h * (0.6 + 0.4 * rand(seed * 10 + i));
    d.push(`L ${x + 95} ${peak} L ${x + 190} ${base - h * 0.25 * rand(seed + i)}`);
  }
  d.push(`L 1100 ${base} Z`);
  return <path d={d.join(" ")} fill={color} />;
};

export const Clock: React.FC<XY & { r?: number; hour?: number }> = ({ x, y, r = 70, hour = 7 }) => {
  const a = ((hour % 12) / 12) * Math.PI * 2;
  return (
    <g>
      <circle cx={x} cy={y} r={r} fill="#ffffff" stroke={INK} strokeWidth={10} />
      <line x1={x} y1={y} x2={x + Math.sin(a) * r * 0.5} y2={y - Math.cos(a) * r * 0.5} stroke={INK} strokeWidth={10} strokeLinecap="round" />
      <line x1={x} y1={y} x2={x} y2={y - r * 0.75} stroke={INK} strokeWidth={7} strokeLinecap="round" />
      <circle cx={x} cy={y} r={8} fill={INK} />
    </g>
  );
};

export const Umbrella: React.FC<XY & { s?: number; color?: string }> = ({ x, y, s = 1, color = "#ff6b8a" }) => (
  <g>
    <line x1={x} y1={y} x2={x} y2={y + 230 * s} stroke={INK} strokeWidth={9 * s} strokeLinecap="round" />
    <path d={`M ${x - 160 * s} ${y} A ${160 * s} ${120 * s} 0 0 1 ${x + 160 * s} ${y} Z`} fill={color} />
    {[-1, 0, 1].map((i) => (
      <path key={i} d={`M ${x + i * 107 * s - 53 * s} ${y} q ${53 * s} ${-28 * s} ${106 * s} 0`} fill="#ffffff" opacity={0.25} />
    ))}
  </g>
);

export const Tablet: React.FC<XY & { s?: number; glow?: number }> = ({ x, y, s = 1, glow = 1 }) => (
  <g>
    <circle cx={x} cy={y} r={160 * s} fill="#7fd3ff" opacity={0.25 * glow} />
    <rect x={x - 55 * s} y={y - 40 * s} width={110 * s} height={80 * s} rx={12 * s} fill="#2b2f4a" />
    <rect x={x - 45 * s} y={y - 31 * s} width={90 * s} height={62 * s} rx={6 * s} fill="#8fe0ff" opacity={0.6 + 0.4 * glow} />
  </g>
);

export const Bowl: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g>
    {[0, 1, 2].map((i) => (
      <path key={i} d={`M ${x - 30 * s + i * 30 * s} ${y - 60 * s} q ${12 * s} ${-20 * s} 0 ${-40 * s}`} stroke="#ffffff" strokeWidth={6 * s} fill="none" strokeLinecap="round" opacity={0.8} />
    ))}
    <ellipse cx={x} cy={y - 20 * s} rx={80 * s} ry={22 * s} fill="#fff2cc" />
    <path d={`M ${x - 85 * s} ${y - 20 * s} Q ${x} ${y + 90 * s} ${x + 85 * s} ${y - 20 * s} Z`} fill="#ff8a5c" />
  </g>
);

export const Moon: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g>
    <circle cx={x} cy={y} r={60 * s} fill="#ffe08a" />
    <circle cx={x + 28 * s} cy={y - 18 * s} r={52 * s} fill="#3b3f78" />
  </g>
);

export const Bone: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g fill="#ffffff">
    <rect x={x - 70 * s} y={y - 16 * s} width={140 * s} height={32 * s} rx={16 * s} />
    {[-1, 1].map((d) => (
      <g key={d}>
        <circle cx={x + d * 72 * s} cy={y - 16 * s} r={22 * s} />
        <circle cx={x + d * 72 * s} cy={y + 16 * s} r={22 * s} />
      </g>
    ))}
  </g>
);

export const Eye: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g>
    <path d={`M ${x - 90 * s} ${y} Q ${x} ${y - 75 * s} ${x + 90 * s} ${y} Q ${x} ${y + 75 * s} ${x - 90 * s} ${y} Z`} fill="#ffffff" />
    <circle cx={x} cy={y} r={32 * s} fill="#3aa0ff" />
    <circle cx={x} cy={y} r={15 * s} fill={INK} />
    <circle cx={x + 10 * s} cy={y - 10 * s} r={7 * s} fill="#ffffff" />
  </g>
);

export const Rain: React.FC<XY & { t: number; s?: number }> = ({ x, y, t, s = 1 }) => (
  <g>
    <Cloud x={x} y={y} s={0.7 * s} fill="#8d97ad" />
    {Array.from({ length: 7 }).map((_, i) => {
      const ph = (t * 2.2 + i * 0.37) % 1;
      return <line key={i} x1={x - 80 * s + i * 27 * s} y1={y + 40 * s + ph * 110 * s} x2={x - 88 * s + i * 27 * s} y2={y + 62 * s + ph * 110 * s} stroke="#5bb7ff" strokeWidth={6 * s} strokeLinecap="round" />;
    })}
  </g>
);

export const Ice: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g>
    <rect x={x - 60 * s} y={y - 60 * s} width={120 * s} height={120 * s} rx={22 * s} fill="#bfe8ff" stroke="#7cc8f2" strokeWidth={8 * s} transform={`rotate(-10 ${x} ${y})`} />
    <rect x={x - 34 * s} y={y - 40 * s} width={30 * s} height={50 * s} rx={10 * s} fill="#ffffff" opacity={0.7} transform={`rotate(-10 ${x} ${y})`} />
  </g>
);

export const Shoe: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g>
    <path d={`M ${x - 70 * s} ${y + 25 * s} L ${x - 70 * s} ${y - 30 * s} Q ${x - 40 * s} ${y - 40 * s} ${x - 20 * s} ${y - 10 * s} Q ${x + 40 * s} ${y - 5 * s} ${x + 75 * s} ${y + 15 * s} L ${x + 75 * s} ${y + 25 * s} Z`} fill="#ff7a59" />
    <rect x={x - 72 * s} y={y + 18 * s} width={150 * s} height={16 * s} rx={8 * s} fill="#ffffff" />
  </g>
);

export const Bucket: React.FC<XY & { s?: number }> = ({ x, y, s = 1 }) => (
  <g>
    <path d={`M ${x - 60 * s} ${y - 50 * s} L ${x + 60 * s} ${y - 50 * s} L ${x + 45 * s} ${y + 45 * s} L ${x - 45 * s} ${y + 45 * s} Z`} fill="#ffcf4a" />
    <path d={`M ${x - 55 * s} ${y - 50 * s} Q ${x} ${y - 120 * s} ${x + 55 * s} ${y - 50 * s}`} stroke={INK} strokeWidth={7 * s} fill="none" />
    <ellipse cx={x} cy={y - 50 * s} rx={60 * s} ry={14 * s} fill="#e0a95c" />
  </g>
);

export const Star: React.FC<XY & { r?: number; fill?: string; rot?: number }> = ({ x, y, r = 20, fill = "#ffd23f", rot = 0 }) => {
  const d: string[] = [];
  for (let i = 0; i < 10; i++) {
    const a = rot + (i * Math.PI) / 5 - Math.PI / 2;
    const rr = i % 2 ? r * 0.45 : r;
    d.push(`${i ? "L" : "M"} ${x + Math.cos(a) * rr} ${y + Math.sin(a) * rr}`);
  }
  return <path d={d.join(" ") + " Z"} fill={fill} />;
};

/** Hearts drifting upward from (x, y). */
export const FloatingHearts: React.FC<XY & { t: number; t0: number; n?: number; spread?: number }> = ({ x, y, t, t0, n = 6, spread = 300 }) => {
  if (t < t0) return null;
  return (
    <g>
      {Array.from({ length: n }).map((_, i) => {
        const ph = ((t - t0) * 0.4 + i / n) % 1;
        const a = Math.sin(ph * Math.PI);
        return (
          <g key={i} opacity={a}>
            <Heart x={x + (i / Math.max(1, n - 1) - 0.5) * spread + 18 * Math.sin(t * 2 + i)} y={y - ph * 300} s={14 + 12 * a} />
          </g>
        );
      })}
    </g>
  );
};

/** Little sparkles twinkling around a point. */
export const Sparkles: React.FC<XY & { t: number; r?: number; n?: number; color?: string }> = ({ x, y, t, r = 140, n = 6, color = "#fff3a8" }) => (
  <g>
    {Array.from({ length: n }).map((_, i) => {
      const a = (i / n) * Math.PI * 2 + rand(i) * 0.6;
      const tw = 0.5 + 0.5 * Math.sin(t * 6 + i * 1.9);
      return <Star key={i} x={x + Math.cos(a) * r} y={y + Math.sin(a) * r * 0.8} r={8 + 12 * tw} fill={color} rot={t} />;
    })}
  </g>
);
