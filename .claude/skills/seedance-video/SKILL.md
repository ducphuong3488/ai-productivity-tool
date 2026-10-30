---
name: seedance-video
description: Viết prompt video cho Seedance 2.0 (ByteDance) — text-to-video, image-to-video và multi-shot 15 giây có timecode, chuyển động camera, ánh sáng, phong cách và âm thanh. Dùng khi người dùng muốn "viết prompt Seedance", "tạo kịch bản video 15s", "chia shot cho video AI", "prompt video quảng cáo/TikTok/Reels", hoặc đưa ảnh/video tham chiếu và muốn prompt để dựng thành clip.
---

# Seedance 2.0 — Skill viết prompt video

Skill này biến một ý tưởng (thường rất ngắn) thành prompt Seedance 2.0 sẵn để dán vào nền tảng: rõ chủ thể, hành động, camera, ánh sáng, phong cách, âm thanh, và chia shot theo thời gian cho clip tối đa 15 giây.

Skill **chỉ viết prompt và kịch bản**. Việc tạo video diễn ra trên nền tảng người dùng đang dùng (Dreamina/Jimeng, CapCut, BytePlus ModelArk hoặc bên thứ ba), theo hạn mức và điều khoản của tài khoản đó. Không hứa "không giới hạn", không hướng dẫn lách quota, watermark hay giới hạn tải xuống.

## Quy trình

### 1. Chốt brief (hỏi tối đa 3 câu, chỉ khi thiếu)
Nếu người dùng chưa nói, tự chọn mặc định hợp lý và ghi rõ giả định:

| Mục | Mặc định |
|---|---|
| Thời lượng | 15s (hoặc 5s / 10s nếu chỉ một hành động) |
| Tỉ lệ khung | 9:16 cho TikTok/Reels/Shorts, 16:9 cho YouTube/web |
| Chế độ | Text-to-video; image-to-video nếu có ảnh |
| Phong cách | Cinematic, chân thực |
| Âm thanh | Âm thanh môi trường + nhạc nền phù hợp, không lời thoại |
| Ngôn ngữ prompt | Tiếng Anh (ổn định nhất); thoại có thể giữ tiếng Việt trong ngoặc kép |

### 2. Chọn khung thời gian
Đọc `references/shot-templates.md` và chọn mẫu phù hợp (quảng cáo sản phẩm, kể chuyện, hook TikTok, showcase món ăn, du lịch, talking head…). Quy tắc nhịp:
- 1 shot ≈ 2–5 giây. Clip 15s: 3–5 shot là đẹp nhất. Không quá 6 shot.
- Mỗi shot chỉ **một** hành động chính và **một** chuyển động camera.
- Shot đầu (0–2s) phải là hook thị giác.

### 3. Viết prompt theo công thức
Công thức đầy đủ trong `references/prompt-formula.md`:

```
[Style/format] + [Subject + appearance] + [Action] + [Scene/environment]
+ [Camera: shot size + movement] + [Lighting + color] + [Audio] + [Constraints]
```

Với video nhiều shot, dùng timecode:

```
[0-3s] Shot 1: ...
[3-7s] Shot 2: ...
```

Từ vựng camera, ánh sáng, phong cách: `references/camera-and-style.md`.

### 4. Giữ nhất quán nhân vật / sản phẩm
- Mô tả nhân vật/sản phẩm **một lần thật cụ thể** ở đầu, sau đó gọi lại đúng cụm đó ("the same woman in the red trench coat").
- Có ảnh tham chiếu: gắn vai trò cho từng file, ví dụ `@Image1 as the main character`, `@Image2 as the product`, `@Video1 for camera movement reference`. Cú pháp tham chiếu và số file tối đa tuỳ nền tảng — nhắc người dùng kiểm tra.
- Image-to-video: **không mô tả lại** những gì ảnh đã có; chỉ mô tả chuyển động, camera và thay đổi.

### 5. Kiểm tra trước khi giao
Chạy script để kiểm tra tổng thời lượng, độ chồng/khoảng trống timecode và độ dài prompt:

```bash
python3 .claude/skills/seedance-video/scripts/build_prompt.py shots.json
```

Định dạng `shots.json` xem trong docstring của script hoặc `references/examples.md`. Script in ra prompt hoàn chỉnh đã ghép timecode.

Checklist tự soát:
- [ ] Tổng thời lượng ≤ 15s, timecode liền mạch
- [ ] Mỗi shot có shot size + chuyển động camera
- [ ] Không quá 2 nhân vật hành động cùng lúc trong một shot
- [ ] Không có chữ dài trên hình (AI dựng chữ hay lỗi) — chữ/logo nên chèn ở bước hậu kỳ
- [ ] Không dùng tên người thật, nhân vật có bản quyền, logo thương hiệu của người khác
- [ ] Có dòng negative/constraints

### 6. Định dạng đầu ra
Luôn trả về theo thứ tự:

1. **Tóm tắt ý tưởng** (1–2 câu, tiếng Việt)
2. **Thông số**: thời lượng · tỉ lệ · chế độ · số shot
3. **Prompt chính** trong code block (tiếng Anh), sẵn để copy
4. **Bảng shot** (tiếng Việt): thời gian · nội dung · camera · âm thanh
5. **2 biến thể** ngắn (đổi phong cách hoặc đổi hook)
6. **Mẹo chỉnh** nếu kết quả chưa đạt (ví dụ: chuyển động bị méo → giảm tốc độ camera, bớt hành động)

## Xử lý lỗi thường gặp

| Hiện tượng | Cách sửa trong prompt |
|---|---|
| Mặt/tay bị biến dạng | Bớt hành động nhanh, thêm `stable anatomy, natural hand pose`, dùng shot rộng hơn |
| Nhân vật đổi mặt giữa các shot | Lặp lại mô tả cố định; dùng ảnh tham chiếu |
| Camera giật | Một chuyển động mỗi shot, thêm `smooth, slow` |
| Video "lặng", ít chuyển động | Thêm động từ cụ thể + yếu tố môi trường động (gió, khói, ánh sáng nhấp nháy) |
| Chữ trên hình sai chính tả | Bỏ chữ khỏi prompt, chèn ở hậu kỳ |
| Quá nhiều thứ xảy ra | Cắt bớt shot; mỗi shot một ý |

## Ranh giới
- Không viết prompt deepfake người thật, nội dung người lớn, bạo lực cực đoan hay mạo danh thương hiệu.
- Không hỗ trợ lách hạn mức, xoá watermark, hay tải video vượt giới hạn của nền tảng.
- Video AI dùng cho quảng cáo: khuyên người dùng gắn nhãn nội dung AI theo quy định của nền tảng.
