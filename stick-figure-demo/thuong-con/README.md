# Thương con – stick-figure reel (Remotion)

Vertical 1080×1920 video, ~111 s, for the script "Đừng ra ngoài, gió đấy!…
Thương con, là cho con sự bảo vệ… và cả khoảng trời để lớn lên."

## Pipeline

1. **Voice** – `../thuong-con-voice/build_voice.py` reads `script.json` and
   synthesizes one Piper TTS clip per line (voice `vi_VN-vais1000-medium`),
   then writes `voice.wav` and `timeline.json` (line and word timings).
   `|` in a line marks caption phrase breaks, `*…*` marks keywords.
2. **Mix** – `../thuong-con-voice/mix_audio.py` adds a soft music bed and
   sound effects and writes `public/audio/mix.wav`.
3. **Video** – copy `timeline.json` to `src/data/` and render:

```bash
npm i
npx remotion studio                                   # preview
npx remotion render ThuongCon out/thuong_con.mp4 \
  --browser-executable=/opt/pw-browsers/chromium      # render
node scripts/stills.mjs /tmp/stills 5,30,60           # spot-check frames
```

Scenes live in `src/scenes/`, one per section of the script; shared drawing
code (stick figure, icons, cards, backdrops) is in `src/lib/`. Captions pop in
word by word from the timings in `timeline.json`.
