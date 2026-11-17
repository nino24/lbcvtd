import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from animation_palette import *
EMO="/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
YEL=(255,229,0)
LOGO=os.environ.get("WHATNOT_LOGO")  # PNG officiel si fourni

def emoji(ch,size):
    f=ImageFont.truetype(EMO,109); im=Image.new("RGBA",(140,140),(0,0,0,0))
    ImageDraw.Draw(im).text((0,0),ch,font=f,embedded_color=True)
    im=im.crop(im.getbbox()); return im.resize((size,int(size*im.height/im.width)),Image.LANCZOS)

def logo_img(w):
    if LOGO and os.path.exists(LOGO):
        im=Image.open(LOGO).convert("RGBA"); return im.resize((w,int(w*im.height/im.width)),Image.LANCZOS)
    h=int(w*0.34); im=Image.new("RGBA",(w+20,h+20),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([10,14,w+10,h+14],h//2,fill=(0,0,0,90))
    d.rounded_rectangle([0,0,w,h],h//2,fill=YEL,outline=(20,20,20),width=6)
    f=font_fit("whatnot",FB,int(w*0.78),int(h*0.75)); bb=f.getbbox("whatnot")
    d.text(((w-(bb[2]-bb[0]))//2-bb[0],(h-(bb[3]-bb[1]))//2-bb[1]),"whatnot",font=f,fill=(17,17,17))
    return im

def paste_scaled(img,im,cx,cy,s,alpha=255):
    if s<=0.01: return
    im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
    if alpha<255: im.putalpha(im.split()[3].point(lambda v:v*alpha//255))
    img.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))

def card(out,dur):
    os.makedirs(out,exist_ok=True); n=int(dur*FPS)
    LG=logo_img(440); rocket=emoji("🚀",52)
    fbig=font_fit("25€",FB,300,110); fmid=font_fit("À L'INSCRIPTION",FB,420,52); fsm=ImageFont.truetype(FX,40)
    BW,BH=500,300; BOT=840; CX=W//2
    for i in range(n):
        t=i/FPS; img=Image.new("RGBA",(W,H),(0,0,0,0))
        out_k=ease_in((t-(dur-0.35))/0.35) if t>dur-0.35 else 0
        oy=-1100*out_k
        # boîte qui tombe
        k=t/0.5; drop=-900*(1-bounce(k)) if k<1 else 0
        bottom=BOT+drop+oy
        # rabats qui s'ouvrent (derrière le logo)
        fo=ease_out((t-0.45)/0.3)
        d=ImageDraw.Draw(img)
        top=bottom-BH
        if fo>0:
            fh=int(110*fo)
            d.polygon([(CX-BW/2,top),(CX-BW/2-60*fo,top-fh),(CX-10,top-fh),(CX,top)],fill=CARD_L,outline=CARD_D)
            d.polygon([(CX+BW/2,top),(CX+BW/2+60*fo,top-fh),(CX+10,top-fh),(CX,top)],fill=CARD_L,outline=CARD_D)
        # logo qui sort de la boîte
        if t>=0.7:
            lk=ease_out_back((t-0.7)/0.45,1.8)
            paste_scaled(img,LG,CX,top+40-(250*lk),0.55+0.45*min(lk,1.05))
        # boîte (devant)
        stamp=t>=0.55
        lines=[]
        box(img,CX,bottom,BW,BH,[] )
        if stamp:
            sk=ease_out((t-0.55)/0.18); s=1.5-0.5*sk
            layer=Image.new("RGBA",(BW,BH),(0,0,0,0)); ld=ImageDraw.Draw(layer)
            def ctext(y,txt,f,col=INK):
                bb=f.getbbox(txt); ld.text(((BW-(bb[2]-bb[0]))//2-bb[0],y-bb[1]),txt,font=f,fill=col)
            ctext(70,"25€",fbig,(180,40,20)); ctext(195,"À L'INSCRIPTION",fmid)
            paste_scaled(img,layer,CX,bottom-BH/2,s,int(255*sk))
        # pastille "lien en bio 🚀" sous la boîte
        if t>=1.0:
            pk=ease_out_back((t-1.0)/0.35,1.6)
            txt="Lien en bio"; bb=fsm.getbbox(txt); tw=bb[2]-bb[0]
            pw=tw+rocket.width+80; ph=74
            pill=Image.new("RGBA",(pw,ph),(0,0,0,0)); pd=ImageDraw.Draw(pill)
            pd.rounded_rectangle([0,0,pw-1,ph-1],ph//2,fill=(17,17,17))
            pd.text((30-bb[0],(ph-(bb[3]-bb[1]))//2-bb[1]),txt,font=fsm,fill=(255,255,255))
            pill.alpha_composite(rocket,(30+tw+14,(ph-rocket.height)//2))
            paste_scaled(img,pill,CX,bottom+60,pk)
        img.save(f"{out}/{i:04d}.png")

def pill_static(path):
    rocket=emoji("🚀",44); f=ImageFont.truetype(FX,40)
    txt="25€ à l'inscription · lien en bio"; bb=f.getbbox(txt); tw=bb[2]-bb[0]
    L=logo_img(150); pw=L.width+tw+rocket.width+90; ph=86
    img=Image.new("RGBA",(W,H),(0,0,0,0))
    p=Image.new("RGBA",(pw,ph),(0,0,0,0)); d=ImageDraw.Draw(p)
    d.rounded_rectangle([0,0,pw-1,ph-1],ph//2,fill=(17,17,17,230))
    p.alpha_composite(L,(14,(ph-L.height)//2+4))
    x=14+L.width+16; d.text((x-bb[0],(ph-(bb[3]-bb[1]))//2-bb[1]),txt,font=f,fill=(255,255,255))
    p.alpha_composite(rocket,(x+tw+12,(ph-rocket.height)//2))
    img.alpha_composite(p,((W-pw)//2,250)); img.save(path)

if __name__=="__main__":
    card("wn1",6.9); card("wn2",4.4); pill_static("pill.png")
