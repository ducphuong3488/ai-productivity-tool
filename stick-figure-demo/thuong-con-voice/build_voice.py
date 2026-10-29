"""Synthesize one TTS clip per script line (Piper, Vietnamese), trim silence,
lay the clips out with pauses, and write voice.wav + timeline.json.

timeline.json: {"duration": s, "lines": [{id, scene, start, end,
  phrases: [[{w, s, e, key}, ...], ...]}]}
Word times inside a line are spread over the clip by syllable length. A line
may set "tts": {"length", "noise"} to override the Piper settings.

Usage: python3 build_voice.py <piper_model.onnx> <out_dir>
"""
import json, os, re, subprocess, sys, tempfile, wave
import numpy as np

MODEL, OUT = sys.argv[1], sys.argv[2]
SR = 22050
PAUSE, SCENE_PAUSE, HOOK_PAUSE = 0.35, 0.8, 0.55
LEAD_IN, TAIL = 0.6, 2.5
PUNCT = re.compile(r"[,.:?!]$")

def tts(text, path, length=1.08, noise=0.4):
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "-f", path,
                    "--length-scale", str(length), "--noise-scale", str(noise)],
                   input=text.encode(), check=True, capture_output=True)

def load(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR, w.getframerate()
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def trim(a, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 200):idx[-1] + 800] if len(idx) else a

script = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "script.json")))
tmp = tempfile.mkdtemp()
pieces, lines, t = [np.zeros(int(LEAD_IN * SR), np.float32)], [], LEAD_IN
for i, ln in enumerate(script):
    plain = ln["text"].replace("|", " ").replace("*", "")
    plain = re.sub(r"\s+", " ", plain).strip()
    path = os.path.join(tmp, ln["id"] + ".wav")
    tts(plain, path, **ln.get("tts", {}))
    clip = trim(load(path))
    dur = len(clip) / SR
    groups = [g.split() for g in ln["text"].split("|")]
    toks = [w for g in groups for w in g]
    weights = [len(re.sub(r"\W", "", w)) + 2 for w in toks]
    pauses = [3 if PUNCT.search(w.rstrip("*")) else 0 for w in toks]
    total = sum(weights) + sum(pauses[:-1])
    acc, k, inkey, phrases = 0.0, 0, False, []
    for g in groups:
        ph = []
        for w in g:
            s = t + dur * acc / total
            acc += weights[k]
            e = t + dur * acc / total
            acc += pauses[k] if k < len(toks) - 1 else 0
            key = inkey or w.startswith("*")
            inkey = key and not w.endswith("*")
            ph.append({"w": w.strip("*"), "s": round(s, 3), "e": round(e, 3), "key": key})
            k += 1
        phrases.append(ph)
    lines.append({"id": ln["id"], "scene": ln["scene"], "start": round(t, 3), "end": round(t + dur, 3),
                  "phrases": phrases})
    pieces.append(clip)
    t += dur
    nxt = script[i + 1] if i + 1 < len(script) else None
    gap = TAIL if nxt is None else SCENE_PAUSE if nxt["scene"] != ln["scene"] else \
        HOOK_PAUSE if ln["scene"] == "hook" else PAUSE
    pieces.append(np.zeros(int(gap * SR), np.float32))
    t += gap
    print(f'{ln["id"]} {lines[-1]["start"]:6.2f}-{lines[-1]["end"]:6.2f} {plain}', flush=True)

audio = np.concatenate(pieces)
os.makedirs(OUT, exist_ok=True)
with wave.open(os.path.join(OUT, "voice.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump({"duration": round(len(audio) / SR, 3), "lines": lines},
          open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
print("total", len(audio) / SR)
