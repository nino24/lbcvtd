import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device="cpu", compute_type="int8")
import numpy as np
audio=np.fromfile(sys.argv[1],dtype=np.float32)
segs, info = m.transcribe(audio, language="fr", word_timestamps=True, vad_filter=True)
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"s":w.start,"e":w.end,"w":w.word} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
json.dump(out, open("transcript.json","w"), ensure_ascii=False, indent=1)
