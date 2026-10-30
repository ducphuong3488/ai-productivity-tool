#!/usr/bin/env python3
"""Ghép shot list (JSON) thành prompt Seedance có timecode và kiểm tra lỗi.

Định dạng đầu vào:

{
  "style": "Cinematic commercial, 9:16 vertical",       # tuỳ chọn
  "character": "a young woman in a red trench coat",    # tuỳ chọn
  "shots": [
    {"duration": 3, "description": "...", "camera": "...", "audio": "..."}
  ],
  "constraints": "no on-screen text, no logos"           # tuỳ chọn
}

Cách dùng:
    python3 build_prompt.py shots.json [--max-seconds 15]

Trả về mã 1 nếu có lỗi (vượt thời lượng, shot thiếu trường bắt buộc...).
"""

import argparse
import json
import sys

MAX_SHOTS = 6
MIN_SHOT_SECONDS = 1.5
MAX_WORDS = 300


def fmt(seconds):
    return f"{seconds:g}"


def build(data, max_seconds):
    errors, warnings, lines = [], [], []

    shots = data.get("shots") or []
    if not shots:
        errors.append("Không có shot nào trong 'shots'.")
        return None, errors, warnings

    if data.get("style"):
        lines.append(data["style"].strip())
    if data.get("character"):
        lines.append(f"Main character: {data['character'].strip()}.")
    if lines:
        lines.append("")

    t = 0.0
    for i, shot in enumerate(shots, 1):
        duration = shot.get("duration")
        description = (shot.get("description") or "").strip()
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"Shot {i}: 'duration' phải là số dương.")
            continue
        if not description:
            errors.append(f"Shot {i}: thiếu 'description'.")
            continue
        if duration < MIN_SHOT_SECONDS:
            warnings.append(f"Shot {i}: {fmt(duration)}s quá ngắn, model khó thể hiện hành động.")
        if not shot.get("camera"):
            warnings.append(f"Shot {i}: chưa có chuyển động camera.")

        parts = [description.rstrip(".")]
        if shot.get("camera"):
            parts.append(shot["camera"].strip().rstrip("."))
        text = ", ".join(parts) + "."
        if shot.get("audio"):
            text += f" Audio: {shot['audio'].strip().rstrip('.')}."
        lines.append(f"[{fmt(t)}-{fmt(t + duration)}s] Shot {i}: {text}")
        t += duration

    if t > max_seconds:
        errors.append(f"Tổng thời lượng {fmt(t)}s vượt giới hạn {fmt(max_seconds)}s.")
    if len(shots) > MAX_SHOTS:
        warnings.append(f"{len(shots)} shot — nên giữ tối đa {MAX_SHOTS} cho clip ngắn.")

    if data.get("constraints"):
        lines.append("")
        lines.append(f"Constraints: {data['constraints'].strip().rstrip('.')}.")
    else:
        warnings.append("Chưa có 'constraints' (ví dụ: no on-screen text, stable face).")

    prompt = "\n".join(lines)
    words = len(prompt.split())
    if words > MAX_WORDS:
        warnings.append(f"Prompt dài {words} từ (> {MAX_WORDS}), model có thể bỏ sót chi tiết.")

    return prompt, errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Đường dẫn shots.json")
    parser.add_argument("--max-seconds", type=float, default=15)
    args = parser.parse_args()

    with open(args.file, encoding="utf-8") as f:
        data = json.load(f)

    prompt, errors, warnings = build(data, args.max_seconds)

    for w in warnings:
        print(f"CẢNH BÁO: {w}", file=sys.stderr)
    for e in errors:
        print(f"LỖI: {e}", file=sys.stderr)
    if errors:
        sys.exit(1)
    print(prompt)


if __name__ == "__main__":
    main()
