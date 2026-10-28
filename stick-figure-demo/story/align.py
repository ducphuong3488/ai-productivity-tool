"""Time-align script words to the voice track.

Each chunk of script.json covers one stretch of speech (times from the
transcription pass). Its words are spread over the non-silent audio inside it,
weighted by length. '|' marks caption phrase breaks, '*...*' marks keywords.
Writes timing.json: list of phrases, each a list of {w, s, e, key}.
"""
import json, re, subprocess, sys

wav = sys.argv[1]
script = json.load(open("script.json"))
log = subprocess.run(["ffmpeg", "-i", wav, "-af", "silencedetect=noise=-32dB:d=0.18", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
sil = list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)],
               [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]))

def speech_spans(a, b):
    spans, cur = [], a
    for s, e in sil:
        if e <= a or s >= b:
            continue
        if s > cur:
            spans.append((cur, s))
        cur = max(cur, e)
    if b > cur:
        spans.append((cur, b))
    return spans

def to_time(spans, frac):
    left = frac * sum(e - s for s, e in spans)
    for s, e in spans:
        if left <= e - s:
            return s + left
        left -= e - s
    return spans[-1][1]

PUNCT = re.compile(r"[,.:?!]$")
phrases = []
for c in script:
    groups = [g.split() for g in c["text"].split("|")]
    toks = [t for g in groups for t in g]
    weights = [len(re.sub(r"\W", "", t)) + 2 for t in toks]
    pauses = [4 if PUNCT.search(t.rstrip("*")) else 0 for t in toks]
    total = sum(weights) + sum(pauses)
    spans = speech_spans(c["start"], c["end"])
    acc, i, inkey = 0, 0, False
    for g in groups:
        ph = []
        for t in g:
            st = to_time(spans, acc / total)
            acc += weights[i]
            en = to_time(spans, acc / total)
            acc += pauses[i]
            i += 1
            start_key = t.startswith("*")
            key = inkey or start_key
            inkey = key and not t.endswith("*")
            ph.append({"w": t.strip("*"), "s": round(st, 3), "e": round(en, 3), "key": key})
        phrases.append(ph)
json.dump(phrases, open("timing.json", "w"), ensure_ascii=False)
for p in phrases:
    print(f'{p[0]["s"]:6.2f}-{p[-1]["e"]:6.2f}  ' + " ".join(("*" if w["key"] else "") + w["w"] for w in p))
