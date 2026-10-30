# Công thức prompt Seedance 2.0

## Công thức 8 phần

| # | Thành phần | Câu hỏi | Ví dụ |
|---|---|---|---|
| 1 | Style / format | Trông như loại phim gì? | `Cinematic commercial, 35mm film look` |
| 2 | Subject | Ai/cái gì? Ngoại hình? | `a young Vietnamese woman, shoulder-length black hair, white linen shirt` |
| 3 | Action | Làm gì? (động từ cụ thể) | `slowly pours iced coffee into a glass` |
| 4 | Scene | Ở đâu? Lúc nào? | `on a wooden table in a sunlit Hanoi café, morning` |
| 5 | Camera | Cỡ cảnh + chuyển động | `close-up, slow push-in` |
| 6 | Lighting & color | Ánh sáng, tông màu | `warm golden backlight, soft shadows, teal-orange grade` |
| 7 | Audio | Âm thanh, nhạc, thoại | `sound of ice clinking, soft lo-fi music` |
| 8 | Constraints | Điều cần tránh / giữ | `no text, no logo, stable face, realistic physics` |

Thứ tự ưu tiên khi prompt quá dài: giữ 2–3–5 (chủ thể, hành động, camera), rút gọn 1–6–7, cuối cùng mới cắt 8.

## Độ dài
- Một shot: 30–80 từ tiếng Anh.
- Cả clip 15s nhiều shot: 120–300 từ. Dài hơn thường làm model bỏ qua chi tiết.

## Prompt một shot (5–10s)

```
Cinematic commercial, shallow depth of field. A young Vietnamese woman with
shoulder-length black hair and a white linen shirt slowly pours iced coffee
into a tall glass on a wooden café table. Morning sunlight streams through the
window behind her. Close-up, slow push-in toward the glass. Warm golden
backlight, soft shadows. Audio: ice clinking, gentle café ambience.
No text, realistic liquid physics, stable hands.
```

## Prompt nhiều shot (15s)

```
Cinematic commercial, 9:16 vertical, warm color grade. Main character: a young
Vietnamese woman with shoulder-length black hair and a white linen shirt.

[0-3s] Shot 1: Extreme close-up of coffee drip falling into a glass, slow motion,
macro lens. Audio: single drip echo.
[3-7s] Shot 2: Medium shot, the same woman lifts the glass and smiles, camera
slowly orbits around her. Audio: soft lo-fi beat begins.
[7-11s] Shot 3: Wide shot of the sunlit café, she sits by the window, camera
dollies back. Audio: café ambience.
[11-15s] Shot 4: Close-up of the glass on the table, condensation drops slide
down, slow push-in, background softly blurred. Audio: music resolves.

Constraints: consistent character across shots, no on-screen text, no logos,
realistic physics, smooth camera.
```

## Image-to-video
Ảnh đã quyết định chủ thể, bố cục, màu. Prompt chỉ cần:

```
[Chuyển động của chủ thể] + [Chuyển động camera] + [Chuyển động môi trường] + [Âm thanh]
```

Ví dụ:
```
She turns her head toward the camera and smiles gently. Hair moves slightly in
the breeze. Slow push-in. Steam rises from the cup. Audio: soft wind, birds.
```

## Tham chiếu đa phương tiện
Khi nền tảng cho phép gắn nhiều file tham chiếu, nói rõ vai trò của từng file:

```
Use @Image1 as the main character's appearance and @Image2 as the product.
Follow the camera movement of @Video1. Match the rhythm of @Audio1.
```

Cú pháp (`@Image1`, `@图片1`, kéo-thả…) và số file tối đa khác nhau theo nền tảng — kiểm tra trước.

## Thoại và lip-sync
- Đặt thoại trong ngoặc kép, ghi rõ ai nói và giọng: `She says in Vietnamese, warm tone: "Sáng nay uống gì nhỉ?"`
- Mỗi shot tối đa một câu ngắn (≤ 10 từ). Thoại dài dễ lệch khẩu hình.

## Negative / constraints hay dùng
`no on-screen text, no watermark, no logo, no extra fingers, stable face,
consistent character, realistic physics, no flicker, smooth motion`
