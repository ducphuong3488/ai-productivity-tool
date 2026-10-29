import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame } from "remotion";
import { Captions } from "./Captions";
import { clamp, DURATION, FPS, H, L, ramp, SCENES, sp, W } from "./lib/time";
import { Caution } from "./scenes/Caution";
import { Compare } from "./scenes/Compare";
import { Familiar } from "./scenes/Familiar";
import { Final } from "./scenes/Final";
import { Hook } from "./scenes/Hook";
import { Indoor } from "./scenes/Indoor";
import { Journey } from "./scenes/Journey";
import { Love } from "./scenes/Love";
import { Nature } from "./scenes/Nature";
import { Outdoor } from "./scenes/Outdoor";
import { Two } from "./scenes/Two";

for (const [file, weight] of [
  ["InterDisplay-Black.otf", "900"],
  ["InterDisplay-ExtraBold.otf", "800"],
  ["InterDisplay-SemiBold.otf", "600"],
] as const) {
  loadFont({ family: "Inter Display", url: staticFile(`fonts/${file}`), weight });
}

const VIEWS: Record<string, { C: React.FC<{ t: number }>; label?: string; focus: [number, number] }> = {
  hook: { C: Hook, label: "Những câu quen thuộc", focus: [540, 900] },
  familiar: { C: Familiar, label: "Mỗi ngày", focus: [540, 600] },
  love: { C: Love, label: "Xuất phát từ tình thương", focus: [540, 700] },
  two: { C: Two, label: "Hai đứa trẻ", focus: [540, 760] },
  indoor: { C: Indoor, label: "Bé thứ nhất", focus: [400, 1000] },
  outdoor: { C: Outdoor, label: "Bé thứ hai", focus: [540, 900] },
  compare: { C: Compare, label: "Khác biệt", focus: [540, 760] },
  nature: { C: Nature, label: "Thuận tự nhiên", focus: [560, 900] },
  caution: { C: Caution, label: "Thuận tự nhiên là…", focus: [540, 700] },
  end: { C: Journey, label: "Đồng hành cùng con", focus: [540, 900] },
  final: { C: Final, focus: [560, 900] },
};

const TR = 0.6;

const SceneLayer: React.FC<{ i: number; t: number }> = ({ i, t }) => {
  const s = SCENES[i];
  const v = VIEWS[s.name];
  const into = i === 0 ? 1 : ramp(t, s.start, s.start + TR);
  const r = into * 1500;
  const zoom = 1 + 0.035 * clamp((t - s.start) / (s.end - s.start + TR));
  return (
    <AbsoluteFill
      style={{
        clipPath: into < 1 ? `circle(${r}px at ${v.focus[0]}px ${v.focus[1]}px)` : undefined,
      }}
    >
      <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H} style={{ scale: String(zoom) }}>
        <v.C t={t} />
      </svg>
      {into < 1 ? (
        <div
          style={{
            position: "absolute",
            left: v.focus[0] - r,
            top: v.focus[1] - r,
            width: 2 * r,
            height: 2 * r,
            borderRadius: "50%",
            border: "14px solid rgba(255,255,255,0.9)",
            boxSizing: "border-box",
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};

const Header: React.FC<{ t: number }> = ({ t }) => {
  const i = SCENES.findIndex((s) => t >= s.start && t < s.end);
  const s = SCENES[Math.max(0, i)];
  const label = VIEWS[s.name].label;
  if (!label) return null;
  const k = sp(t, s.start + 0.15, 12, 170, 0.7);
  const out = 1 - ramp(t, s.end - 0.25, s.end);
  return (
    <div
      style={{
        position: "absolute",
        top: 120,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          scale: String(k * (0.7 + 0.3 * out)),
          opacity: out,
          padding: "18px 44px",
          borderRadius: 60,
          background: "rgba(16,22,52,0.82)",
          border: "4px solid #9fe8ff",
          boxShadow: "0 0 26px rgba(80,200,255,0.9), inset 0 0 14px rgba(80,200,255,0.35)",
          color: "#a8ecff",
          fontFamily: "Inter Display",
          fontWeight: 900,
          fontSize: 46,
          letterSpacing: -0.5,
        }}
      >
        {label}
      </div>
    </div>
  );
};

const Outro: React.FC<{ t: number }> = ({ t }) => {
  const t0 = L("z2").end + 0.15;
  if (t < t0) return null;
  const a = sp(t, t0);
  const b = sp(t, t0 + 0.35);
  return (
    <div style={{ position: "absolute", top: 380, left: 60, right: 60, textAlign: "center" }}>
      <div
        style={{
          scale: String(a),
          fontFamily: "Inter Display",
          fontWeight: 900,
          fontSize: 128,
          lineHeight: 1.1,
          whiteSpace: "nowrap",
          letterSpacing: -3,
          backgroundImage: "linear-gradient(180deg, #fff7c2 0%, #ffb347 55%, #ff6a7a 100%)",
          WebkitBackgroundClip: "text",
          backgroundClip: "text",
          color: "transparent",
          filter: "drop-shadow(0 0 28px rgba(255,140,80,0.9)) drop-shadow(0 10px 12px rgba(0,0,0,0.35))",
        }}
      >
        THƯƠNG CON
      </div>
      <div
        style={{
          marginTop: 24,
          scale: String(b),
          opacity: clamp(b * 1.5),
          fontFamily: "Inter Display",
          fontWeight: 800,
          fontSize: 58,
          color: "#ffffff",
          textShadow: "0 4px 18px rgba(0,0,0,0.55)",
        }}
      >
        là cho con khoảng trời để lớn lên
      </div>
    </div>
  );
};

export const ThuongCon: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  return (
    <AbsoluteFill style={{ backgroundColor: "#0e1230" }}>
      {SCENES.map((s, i) =>
        t >= s.start && t < s.end + TR ? <SceneLayer key={s.name} i={i} t={t} /> : null,
      )}
      <AbsoluteFill
        style={{
          background: "linear-gradient(180deg, rgba(10,10,30,0) 70%, rgba(10,10,30,0.6) 86%, rgba(10,10,30,0.75) 100%)",
        }}
      />
      <Header t={t} />
      <Captions t={t} />
      <Outro t={t} />
      <div style={{ position: "absolute", top: 0, left: 0, height: 10, width: W * (t / DURATION), background: "#7fe0ff" }} />
      <Audio src={staticFile("audio/mix.wav")} />
    </AbsoluteFill>
  );
};
