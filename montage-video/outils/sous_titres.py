import json,re,sys
words=[]
for s in json.load(open(sys.argv[1])):
    for w in s['words']:
        t=w['w']
        if words and (t.startswith("'") or t.startswith("-")) and not t.startswith(" "):
            words[-1]['w']+=t.strip(); words[-1]['e']=w['e']; continue
        words.append({'w':t.strip(),'s':w['s'],'e':w['e']})
FIX={"Tiktok":"TikTok","Watnot":"Whatnot","Watnot,":"Whatnot,","!":"!","etc,":"etc.","etc.":"etc."}
for w in words: w['w']=FIX.get(w['w'],w['w']).replace("Watnot","Whatnot")
# fusion ponctuation isolée
m=[]
for w in words:
    if m and w['w'] in "!?.,": m[-1]['w']+=" "+w['w'] if w['w'] in "!?" else w['w']; continue
    m.append(w)
words=m
KEY=re.compile(r"^(palettes?|Amazon|simple|livraison|gratuite|enchères|1€|toi|grossiste|Whatnot|suivi|live|240|000|produits|l'avenir|TikTok|yeux)\W*$",re.I)
phr=[];cur=[]
for w in words:
    cur.append(w)
    if re.search(r"[.,!?]$",w['w']): phr.append(cur);cur=[]
if cur: phr.append(cur)
groups=[]
for p in phr:
    n=len(p); k=max(1,-(-len(" ".join(x['w'] for x in p))//22)); k=max(k,-(-n//4))
    size=-(-n//k)
    for i in range(0,n,size): groups.append(p[i:i+size])
L=lambda g:len(" ".join(x['w'] for x in g))
out=[]
for g in groups:
    if out and (len(g)==1 or len(out[-1])==1) and L(out[-1]+g)<=24 and g[0]['s']-out[-1][-1]['e']<0.6:
        out[-1]=out[-1]+g
    else: out.append(g)
groups=out
def ts(t):
    h=int(t//3600);m_=int(t%3600//60);s=t%60; return f"{h}:{m_:02d}:{s:05.2f}"
OR="&H78BEF0&"
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Black,82,&H00FFFFFF,&H00FFFFFF,&H00111111,&H64000000,0,0,0,0,100,100,3,0,1,6,3,2,70,150,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines=[]
for i,g in enumerate(groups):
    st=g[0]['s']; en=groups[i+1][0]['s'] if i+1<len(groups) else g[-1]['e']+0.4
    en=min(en, g[-1]['e']+0.8)
    if en>64.7: en=64.7
    parts=[]
    for w in g:
        t=w['w']
        parts.append(f"{{\\c{OR}}}{t}{{\\c&HFFFFFF&}}" if KEY.match(t) else t)
    txt=" ".join(parts)
    lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},Sub,,0,0,0,,{{\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}}{txt}")
open(sys.argv[2],"w").write(hdr+"\n".join(lines)+"\n")
# srt pour les plateformes
with open(sys.argv[3],"w") as f:
    for i,g in enumerate(groups):
        st=g[0]['s']; en=groups[i+1][0]['s'] if i+1<len(groups) else g[-1]['e']+0.4
        st2=lambda t:f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(t*1000%1000):03d}"
        f.write(f"{i+1}\n{st2(st)} --> {st2(min(en,g[-1]['e']+0.8))}\n{' '.join(w['w'] for w in g)}\n\n")
print(len(groups)); [print(" ".join(w['w'] for w in g)) for g in groups]
