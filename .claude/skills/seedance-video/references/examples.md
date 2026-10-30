# Ví dụ hoàn chỉnh

## Ví dụ 1 — Quảng cáo cà phê, 15s, 9:16

**Yêu cầu người dùng:** "video quảng cáo cà phê muối cho quán, đăng TikTok"

**Thông số:** 15s · 9:16 · text-to-video · 4 shot

```
Premium cinematic food commercial, 9:16 vertical, warm color grade, shallow
depth of field.

[0-3s] Shot 1: Extreme close-up of thick salted cream slowly pouring over dark
iced coffee in a clear glass, the cream swirls into marbled patterns, slow
motion, macro lens, static camera. Audio: deep pour sound, ice clinking.
[3-7s] Shot 2: Close-up of a hand stirring the glass with a metal spoon,
camera slowly orbits around the glass on a rustic wooden table. Audio: soft
spoon clinks, lo-fi beat starts.
[7-11s] Shot 3: Medium shot of a young Vietnamese woman in a cream sweater
taking a sip by a window in a cozy café, morning sunlight, she closes her eyes
and smiles. Slow push-in. Audio: gentle café ambience.
[11-15s] Shot 4: The glass centered on the table, condensation drops sliding
down, background softly blurred with warm bokeh, slow push-in, empty space
above the glass. Audio: music resolves.

Constraints: no on-screen text, no logos, realistic liquid physics, stable
hands and face, smooth camera motion.
```

`shots.json` tương ứng cho script:

```json
{
  "style": "Premium cinematic food commercial, 9:16 vertical, warm color grade, shallow depth of field.",
  "shots": [
    {"duration": 3, "description": "Extreme close-up of thick salted cream slowly pouring over dark iced coffee in a clear glass, slow motion", "camera": "macro lens, static camera", "audio": "deep pour sound, ice clinking"},
    {"duration": 4, "description": "Close-up of a hand stirring the glass with a metal spoon on a rustic wooden table", "camera": "slow orbit", "audio": "soft spoon clinks, lo-fi beat starts"},
    {"duration": 4, "description": "Medium shot of a young Vietnamese woman in a cream sweater taking a sip by a sunlit café window, she smiles", "camera": "slow push-in", "audio": "gentle café ambience"},
    {"duration": 4, "description": "The glass centered on the table, condensation drops sliding down, warm bokeh background", "camera": "slow push-in", "audio": "music resolves"}
  ],
  "constraints": "no on-screen text, no logos, realistic liquid physics, stable hands and face, smooth camera motion"
}
```

## Ví dụ 2 — Image-to-video, 5s

**Yêu cầu:** "làm ảnh chân dung cô gái áo dài này chuyển động"

```
She slowly turns her head toward the camera and smiles softly. The flaps of
her áo dài flutter gently in the breeze, a few petals drift past. Slow push-in.
Soft natural light. Audio: light wind, distant birdsong.
Constraints: keep her face identical to the image, no text, smooth motion.
```

## Ví dụ 3 — Hook TikTok "trước/sau" dọn phòng, 15s

```
Handheld smartphone style, 9:16 vertical, bright natural light.

[0-2s] Shot 1: Close-up of a perfectly tidy minimalist desk, fast push-in.
Audio: satisfying "ding".
[2-6s] Shot 2: Hard cut to the same desk completely messy with papers, cups and
cables, handheld medium shot. Audio: record scratch.
[6-11s] Shot 3: Time-lapse of a young man in a grey hoodie quickly tidying the
desk, top-down view, speed ramp. Audio: upbeat music.
[11-15s] Shot 4: The same young man sits at the clean desk and gives a thumbs
up to the camera, medium close-up, static. Audio: music hit.

Constraints: consistent character and desk across shots, no on-screen text,
natural hands.
```
