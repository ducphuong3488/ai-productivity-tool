import React from "react";
import { INK } from "./figure";
import { clamp, sp } from "./time";

export const FONT = "Inter Display";

/** Wraps children in a group that pops in with a spring at t0 (and out at t1). */
export const Pop: React.FC<{
  t: number;
  t0: number;
  t1?: number;
  x: number;
  y: number;
  rot?: number;
  from?: number;
  children: React.ReactNode;
}> = ({ t, t0, t1, x, y, rot = 0, from = 0, children }) => {
  const s = from + (1 - from) * sp(t, t0);
  const out = t1 === undefined ? 1 : 1 - clamp((t - t1) / 0.25);
  const scale = s * (0.6 + 0.4 * out);
  if (scale <= 0.01 || out <= 0) return null;
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot * (1 - sp(t, t0, 14))}) scale(${scale})`} opacity={out}>
      {children}
    </g>
  );
};

/** White rounded card with soft shadow, centered on (0, 0). */
export const Card: React.FC<{ w: number; h: number; fill?: string; children?: React.ReactNode; r?: number }> = ({
  w,
  h,
  fill = "#ffffff",
  r = 40,
  children,
}) => (
  <g>
    <rect x={-w / 2 + 6} y={-h / 2 + 14} width={w} height={h} rx={r} fill="rgba(20,20,50,0.18)" />
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={r} fill={fill} />
    {children}
  </g>
);

export const Label: React.FC<{
  x?: number;
  y?: number;
  size?: number;
  fill?: string;
  weight?: number;
  children: React.ReactNode;
  stroke?: string;
}> = ({ x = 0, y = 0, size = 48, fill = INK, weight = 900, children, stroke }) => (
  <text
    x={x}
    y={y}
    fontFamily={FONT}
    fontWeight={weight}
    fontSize={size}
    fill={fill}
    textAnchor="middle"
    dominantBaseline="central"
    stroke={stroke}
    strokeWidth={stroke ? size * 0.18 : 0}
    paintOrder="stroke"
    strokeLinejoin="round"
    letterSpacing={-0.5}
  >
    {children}
  </text>
);

/** Rubber stamp: scales down from 2.2x and rotates into place. */
export const Stamp: React.FC<{ t: number; t0: number; x: number; y: number; text: string; color?: string; rot?: number }> = ({
  t,
  t0,
  x,
  y,
  text,
  color = "#ff4d5e",
  rot = -12,
}) => {
  if (t < t0) return null;
  const k = sp(t, t0, 16, 260, 0.6);
  const s = 2.2 - 1.2 * k;
  const w = text.length * 34 + 70;
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`} opacity={clamp(k * 2)}>
      <rect x={-w / 2} y={-48} width={w} height={96} rx={20} fill="none" stroke={color} strokeWidth={10} />
      <Label size={56} fill={color}>
        {text}
      </Label>
    </g>
  );
};

/** Speech bubble with a tail pointing down-left or down-right toward (tx, ty). */
export const Bubble: React.FC<{
  t: number;
  t0: number;
  t1: number;
  x: number;
  y: number;
  w: number;
  h: number;
  tx: number;
  ty: number;
  fill?: string;
  children: React.ReactNode;
}> = ({ t, t0, t1, x, y, w, h, tx, ty, fill = "#ffffff", children }) => {
  if (t < t0 || t > t1 + 0.25) return null;
  const s = sp(t, t0, 12, 200, 0.7) * (1 - clamp((t - t1) / 0.25));
  const bx = clamp(tx, x - w / 2 + 50, x + w / 2 - 50);
  return (
    <g transform={`translate(${tx} ${ty}) scale(${s}) translate(${-tx} ${-ty})`}>
      <path d={`M ${bx - 24} ${y + h / 2 - 4} L ${tx} ${ty} L ${bx + 24} ${y + h / 2 - 4} Z`} fill={INK} />
      <rect x={x - w / 2 - 6} y={y - h / 2 - 6} width={w + 12} height={h + 12} rx={40} fill={INK} />
      <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx={34} fill={fill} />
      <path d={`M ${bx - 16} ${y + h / 2 - 8} L ${tx - (tx - bx) * 0.12} ${ty - 12} L ${bx + 16} ${y + h / 2 - 8} Z`} fill={fill} />
      <g transform={`translate(${x} ${y})`}>{children}</g>
    </g>
  );
};

/** Pill chip like "BÉ 1" used for labels above things. */
export const Chip: React.FC<{ text: string; fill: string; color?: string; size?: number }> = ({ text, fill, color = "#ffffff", size = 40 }) => {
  const w = text.length * size * 0.62 + size * 1.4;
  return (
    <g>
      <rect x={-w / 2} y={-size * 0.9} width={w} height={size * 1.8} rx={size * 0.9} fill={fill} />
      <Label size={size} fill={color}>
        {text}
      </Label>
    </g>
  );
};
