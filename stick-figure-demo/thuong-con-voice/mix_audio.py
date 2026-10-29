"""Mix voice.wav with a soft synthesized music bed and light sound effects
(whoosh on scene changes, pops on the "Đừng" cards, chimes on key beats).

Usage: python3 mix_audio.py <voice_dir> <out.wav>
"""
import json, os, sys, wave
import numpy as np

SR = 44100
vdir, out = sys.argv[1], sys.argv[2]
tl = json.load(open(os.path.join(vdir, "timeline.json")))
with wave.open(os.path.join(vdir, "voice.wav")) as w:
    vsr = w.getframerate()
    voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
voice = np.interp(np.arange(int(len(voice) * SR / vsr)) / SR, np.arange(len(voice)) / vsr, voice)
n = len(voice)
t = np.arange(n) / SR
music = np.zeros(n)
sfx = np.zeros(n)

def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= n or i < 0:
        return
    sig = sig[: n - i]
    buf[i:i + len(sig)] += sig * gain

def env(length, attack=0.005, decay=0.3):
    tt = np.arange(int(length * SR)) / SR
    return np.minimum(tt / attack, 1) * np.exp(-tt / decay)

def pluck(freq, length=1.2, decay=0.45):
    tt = np.arange(int(length * SR)) / SR
    tone = np.sin(2 * np.pi * freq * tt) + 0.35 * np.sin(4 * np.pi * freq * tt) + 0.12 * np.sin(6 * np.pi * freq * tt)
    return tone * env(length, 0.004, decay)

# warm chord loop: C - G - Am - F at 84 bpm, soft pad + gentle arpeggio
bpm = 84
beat = 60 / bpm
bar = beat * 4
CH = [(261.63, 329.63, 392.0), (196.0, 246.94, 293.66), (220.0, 261.63, 329.63), (174.61, 220.0, 261.63)]
for b in range(int(tl["duration"] / bar) + 1):
    chord = CH[b % 4]
    L = int(bar * SR)
    tt = np.arange(L) / SR
    pad = sum(np.sin(2 * np.pi * f / 2 * tt) * 0.6 + np.sin(2 * np.pi * f * tt) * 0.25 for f in chord)
    shape = np.minimum(tt / 0.6, 1) * np.minimum((bar - tt) / 0.6, 1)
    add(music, b * bar, pad * shape, 0.035)
    for k in range(8):  # eighth-note arpeggio
        f = chord[[0, 1, 2, 1, 0, 2, 1, 2][k]] * 2
        add(music, b * bar + k * beat / 2, pluck(f, 0.9, 0.3), 0.05)
    add(music, b * bar, pluck(chord[0] / 2, 2.0, 0.8), 0.08)

def whoosh():
    rng = np.random.default_rng(1)
    L = int(0.45 * SR)
    noise = rng.standard_normal(L)
    k = np.ones(40) / 40
    lowp = np.convolve(noise, k, mode="same")
    shape = np.sin(np.linspace(0, np.pi, L)) ** 2
    return (noise - lowp) * shape * 0.06 + lowp * shape * 0.5

def pop(freq=600):
    tt = np.arange(int(0.12 * SR)) / SR
    f = freq * (1.7 - 0.7 * np.minimum(tt / 0.05, 1))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(0.12, 0.002, 0.035)

def chime(base=880):
    return pluck(base, 1.5, 0.5) + 0.6 * pluck(base * 1.5, 1.5, 0.4)

lines = {l["id"]: l for l in tl["lines"]}
prev = None
for l in tl["lines"]:
    if prev and prev != l["scene"]:
        add(sfx, l["start"] - 0.6, whoosh(), 0.5)
    prev = l["scene"]
for i, lid in enumerate(["h1", "h2", "h3", "h4", "h5"]):
    add(sfx, lines[lid]["start"], pop(520 + 40 * i), 0.35)
for lid, ph in (("l3", 1), ("l3", 2), ("l3", 3)):
    add(sfx, lines[lid]["phrases"][ph][0]["s"], pop(700 + 80 * ph), 0.3)
for lid in ("n3", "n4", "n5", "n6", "n7"):
    add(sfx, lines[lid]["start"] - 0.25, pop(820), 0.25)
add(sfx, lines["e5"]["start"], chime(784), 0.25)
add(sfx, lines["z2"]["end"] + 0.15, chime(1046), 0.3)

# duck the music under the voice
venv = np.convolve(np.abs(voice), np.ones(4410) / 4410, mode="same")
duck = 1 - 0.45 * np.clip(venv / 0.05, 0, 1)
fade = np.minimum(1, t / 1.0) * np.minimum(1, (tl["duration"] - t) / 1.5)
mix = voice * 1.0 + (music * duck + sfx) * fade
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
with wave.open(out, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("wrote", out, n / SR)
