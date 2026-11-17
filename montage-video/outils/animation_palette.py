import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
FB="/usr/share/fonts/opentype/inter/Inter-Black.otf"
FX="/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
WOOD=(185,135,79); WOOD_D=(140,98,55); WOOD_L=(212,168,112)
CARD=(200,150,92); CARD_D=(165,118,68); CARD_L=(222,180,125); TAPE=(232,206,160); INK=(38,28,20)

def ease_out_back(t,s=1.6):
    t=min(max(t,0),1)-1; return t*t*((s+1)*t+s)+1
def ease_out(t): t=min(max(t,0),1); return 1-(1-t)**3
def ease_in(t): t=min(max(t,0),1); return t**3
def bounce(t):
    t=min(max(t,0),1)
    if t<1/2.75: return 7.5625*t*t
    if t<2/2.75: t-=1.5/2.75; return 7.5625*t*t+.75
    if t<2.5/2.75: t-=2.25/2.75; return 7.5625*t*t+.9375
    t-=2.625/2.75; return 7.5625*t*t+.984375

def font_fit(text,path,maxw,start):
    s=start
    while s>10:
        f=ImageFont.truetype(path,s)
        if f.getbbox(text)[2]-f.getbbox(text)[0]<=maxw: return f
        s-=2
    return ImageFont.truetype(path,s)

def pallet(d,x,y,w):
    h=int(w*0.22); top=int(h*0.28); blk=h-2*top
    sh=Image.new("RGBA",(1,1))
    d.rounded_rectangle([x+8,y+h-6,x+w+8,y+h+14],6,fill=(0,0,0,70))
    d.rectangle([x,y,x+w,y+top],fill=WOOD,outline=WOOD_D,width=4)
    for i in range(1,5):
        gy=y+top*i//5; d.line([x+12,gy,x+w-12,gy],fill=WOOD_D+(120,),width=2)
    bw=int(w*0.14)
    for bx in (x, x+(w-bw)//2, x+w-bw):
        d.rectangle([bx,y+top,bx+bw,y+top+blk],fill=WOOD_D,outline=(110,75,40),width=4)
    d.rectangle([x,y+top+blk,x+w,y+h],fill=WOOD,outline=WOOD_D,width=4)
    return h

def box(img,cx,bottom,w,h,lines,rot=0,alpha=255):
    pad=40
    b=Image.new("RGBA",(w+2*pad,h+2*pad),(0,0,0,0)); d=ImageDraw.Draw(b)
    x0,y0=pad,pad
    d.rounded_rectangle([x0+10,y0+14,x0+w+10,y0+h+14],10,fill=(0,0,0,80))
    d.rounded_rectangle([x0,y0,x0+w,y0+h],10,fill=CARD,outline=CARD_D,width=5)
    d.rectangle([x0+5,y0+5,x0+w-5,y0+int(h*0.12)],fill=CARD_L)
    tw=int(w*0.16); d.rectangle([x0+(w-tw)//2,y0+5,x0+(w+tw)//2,y0+int(h*0.30)],fill=TAPE)
    d.line([x0+w-int(w*0.06),y0+8,x0+w-int(w*0.06),y0+h-8],fill=CARD_D,width=3)
    # text block
    total=sum(f.getbbox(t)[3]+12 for t,f in lines); ty=y0+int(h*0.30)+(int(h*0.70)-total)//2
    for t,f in lines:
        bb=f.getbbox(t); tw2=bb[2]-bb[0]
        d.text((x0+(w-tw2)//2-bb[0],ty-bb[1]),t,font=f,fill=INK)
        ty+=bb[3]-bb[1]+22
    if rot: b=b.rotate(rot,resample=Image.BICUBIC,expand=False)
    if alpha<255:
        a=b.split()[3].point(lambda v:v*alpha//255); b.putalpha(a)
    img.alpha_composite(b,(int(cx-(w+2*pad)/2),int(bottom-h-pad)))

def text_center(img,y,text,f,fill=(255,255,255),stroke=8,alpha=255,hl=None):
    d=ImageDraw.Draw(img); bb=d.textbbox((0,0),text,font=f,stroke_width=stroke)
    x=(W-(bb[2]-bb[0]))//2
    layer=Image.new("RGBA",img.size,(0,0,0,0)); ld=ImageDraw.Draw(layer)
    ld.text((x,y),text,font=f,fill=fill+(255,),stroke_width=stroke,stroke_fill=(17,17,17,255))
    if alpha<255: layer.putalpha(layer.split()[3].point(lambda v:v*alpha//255))
    img.alpha_composite(layer)

def intro(out):
    os.makedirs(out,exist_ok=True); n=int(3.6*FPS)
    PW=600; PY=560; px_final=(W-PW)//2
    f1=ImageFont.truetype(FB,120); f2=font_fit("D'EXPÉRIENCE",FB,440,80)
    for i in range(n):
        t=i/FPS; img=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
        # slide in 0-0.45 from left, slide out 3.15-3.6 to right
        if t<3.15: px=-PW+(px_final+PW)*ease_out_back(t/0.45,1.2)
        else: px=px_final+(W+PW)*ease_in((t-3.15)/0.45)
        ph=pallet(d,px,PY,PW)
        if t>=0.35:
            k=(t-0.35)/0.5; drop=-700*(1-bounce(k)) if k<1 else 0
            squash=0
            box(img,px+PW/2,PY+6+drop,500,330,[("10 ANS",f1),("D'EXPÉRIENCE",f2)],rot=0)
        img.save(f"{out}/{i:04d}.png")
    return n

def outro(out,dur=3.6):
    os.makedirs(out,exist_ok=True); n=int(dur*FPS)
    PW=760; PY=1380
    fb=font_fit("SHOPTONSTOCK",FB,600,110); fs=font_fit("by AMZBOOSTER",FX,400,58)
    fA=ImageFont.truetype(FB,64); fB=ImageFont.truetype(FB,64)
    for i in range(n):
        t=i/FPS; img=Image.new("RGBA",(W,H),(0,0,0,0))
        dim=int(170*ease_out(t/0.4)); img.alpha_composite(Image.new("RGBA",(W,H),(10,8,6,dim)))
        d=ImageDraw.Draw(img)
        py=PY+(H-PY)*(1-ease_out_back(t/0.45,1.1))
        pallet(d,(W-PW)//2,py,PW)
        if t>=0.35:
            k=(t-0.35)/0.55; drop=-1100*(1-bounce(k)) if k<1 else 0
            box(img,W/2,py+6+drop,680,300,[("SHOPTONSTOCK",fb)])
        if t>=0.85:
            k=(t-0.85)/0.5; drop=-1100*(1-bounce(k)) if k<1 else 0
            box(img,W/2,py+6-300+drop,460,190,[("by AMZBOOSTER",fs)],rot=-3)
        if t>=1.5:
            a=int(255*ease_out((t-1.5)/0.35)); dy=int(30*(1-ease_out((t-1.5)/0.35)))
            text_center(img,330+dy,"LE GROSSISTE PRÉFÉRÉ",fA,alpha=a)
            text_center(img,420+dy,"DE TON",fA,alpha=a,fill=(240,190,120))
            text_center(img,510+dy,"GROSSISTE PRÉFÉRÉ",fA,alpha=a)
        img.save(f"{out}/{i:04d}.png")
    return n

if __name__=="__main__":
    print(intro("intro"), outro("outro"))
