import React from "react";
import { clamp, LINES, sp, Word } from "./lib/time";

const PHRASES: { words: Word[]; until: number }[] = (() => {
  const all = LINES.flatMap((l) => l.phrases);
  return all.map((words, i) => {
    const next = all[i + 1]?.[0].s ?? 1e9;
    return { words, until: Math.min(next - 0.03, words[words.length - 1].e + 0.8) };
  });
})();

const SIZE = 92;

const WordView: React.FC<{ w: Word; t: number; fade: number }> = ({ w, t, fade }) => {
  const k = sp(t, w.s - 0.06, 12, 220, 0.6);
  if (k <= 0.001) {
    return <span style={{ visibility: "hidden", fontSize: SIZE, fontWeight: 900 }}>{w.w.toUpperCase()}</span>;
  }
  const active = t >= w.s - 0.06 && t <= w.e + 0.05;
  const pulse = active ? 1 + 0.08 * Math.sin(clamp((t - w.s) / Math.max(0.1, w.e - w.s)) * Math.PI) : 1;
  const text = w.w.toUpperCase();
  const common: React.CSSProperties = {
    fontFamily: "Inter Display",
    fontWeight: 900,
    fontSize: SIZE * (w.key ? 1.1 : 1),
    lineHeight: 1.25,
    letterSpacing: -1.5,
    whiteSpace: "nowrap",
  };
  return (
    <span
      style={{
        position: "relative",
        display: "inline-block",
        scale: String((0.55 + 0.45 * k) * pulse),
        translate: `0px ${(1 - k) * 30}px`,
        opacity: clamp(k * 2) * fade,
      }}
    >
      {/* outline + glow layer */}
      <span
        style={{
          ...common,
          color: "#15122b",
          WebkitTextStroke: "14px #15122b",
          filter: w.key
            ? "drop-shadow(0 0 22px rgba(255,110,60,0.95)) drop-shadow(0 8px 10px rgba(0,0,0,0.45))"
            : "drop-shadow(0 8px 10px rgba(0,0,0,0.45))",
        }}
      >
        {text}
      </span>
      {/* fill layer */}
      <span
        style={{
          ...common,
          position: "absolute",
          left: 0,
          top: 0,
          ...(w.key
            ? {
                backgroundImage: "linear-gradient(180deg, #fff7b0 0%, #ffc045 45%, #ff6a4d 100%)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                color: "transparent",
              }
            : { color: active ? "#ffe14d" : "#ffffff" }),
        }}
      >
        {text}
      </span>
    </span>
  );
};

export const Captions: React.FC<{ t: number }> = ({ t }) => {
  const cur = PHRASES.find((p) => t >= p.words[0].s - 0.08 && t < p.until);
  if (!cur) return null;
  const fade = clamp((cur.until - t) / 0.15);
  return (
    <div
      style={{
        position: "absolute",
        left: 60,
        right: 60,
        top: 1440,
        height: 330,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignContent: "center",
        columnGap: 44,
        rowGap: 0,
        textAlign: "center",
      }}
    >
      {cur.words.map((w, i) => (
        <WordView key={i} w={w} t={t} fade={fade} />
      ))}
    </div>
  );
};
