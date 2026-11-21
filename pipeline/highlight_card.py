"""Highlight card (Boris, Nov 21): character photo up front, big DAY N + title sticker, 3 info rows, CTA.
Usage: python3 -I pipeline/highlight_card.py spec.json
spec = {"out": "highlights/theo/day06.jpg", "image": "theo_d02_clearskin.jpg", "big": "DAY 6", "small": "NEW FIT",
        "rows": [["✅","You voted","New fit 4, gym 2"],["👕","The fix","..."],["💬","The twist","..."]],
        "cta": "DAY 6 IS ON OUR PAGE", "color": [236,110,160], "days": "25", "cx": 0.5}
Covers: highlights/<acc>/cover_*.jpg (photo crops). Don't use 🗳️ (renders as a box)."""
import sys,os,json; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(os.path.dirname(HERE))
from common import F, emoji, center_paste, W, H
from extras import Extras, scaled
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import numpy as np
class X(Extras):
    def __init__(s): s.c={}
x=X(); A='pipeline/assets/'
def card(out,img,big,small,rows,cta,col=(236,110,160),days=None,cx=0.5,top=0.0):
    src=Image.open(A+img).convert("RGB")
    k=W/src.width; r=src.resize((W,int(src.height*k)),Image.LANCZOS)
    if r.height<1200: r=src.resize((int(src.width*1200/src.height),1200),Image.LANCZOS)
    ox=int((r.width-W)*cx); oy=int((r.height-1200)*top)
    photo=r.crop((ox,oy,ox+W,oy+1200))
    im=Image.new("RGB",(W,H),(14,14,20)); im.paste(photo,(0,0))
    im=im.convert("RGBA")
    y=np.linspace(0,1,H)[:,None]; a=np.clip((y-0.42)/0.22,0,1)
    ov=np.zeros((H,W,4),np.uint8); ov[...,:3]=(14,14,20); ov[...,3]=(a*255).astype(np.uint8).repeat(W,1); im.alpha_composite(Image.fromarray(ov))
    if days:
        cal=scaled(x.calendar_img({"text":days,"angle":5}),0.62); im.alpha_composite(cal,(W-cal.width-24,120))
    big_l=Image.new("RGBA",(W,260),(0,0,0,0)); d=ImageDraw.Draw(big_l)
    d.text((W//2,130),big,font=F("Black",180),fill=(255,214,102),anchor="mm",stroke_width=13,stroke_fill=(12,12,14))
    center_paste(im,big_l.rotate(-3,resample=Image.BICUBIC),1030)
    st=x.sticker_img({"text":small,"bg":list(col),"size":72,"angle":-3}); center_paste(im,st,1190)
    L=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(L); y0=1300
    d.rounded_rectangle((60,y0,1020,y0+40+96*len(rows)),radius=40,fill=(255,255,255,22),outline=(255,255,255,60),width=3)
    ems=[]
    for i,(e,lab,txt) in enumerate(rows):
        yy=y0+68+i*96; ems.append((emoji(e,56),yy))
        d.text((180,yy-20),lab.upper(),font=F("ExtraBold",30),fill=(255,214,102),anchor="lm")
        d.text((180,yy+18),txt,font=F("Bold",42),fill=(255,255,255),anchor="lm")
    im.alpha_composite(L)
    for em,yy in ems: im.alpha_composite(em,(100,yy-em.height//2))
    s2=x.sticker_img({"text":cta,"bg":[102,200,92],"size":54,"angle":-2}); center_paste(im,s2,1800)
    im.convert("RGB").save(out,quality=92)

if __name__=="__main__":
    s=json.load(open(sys.argv[1]))
    card(s["out"],s["image"],s["big"],s["small"],[tuple(r) for r in s["rows"]],s["cta"],tuple(s.get("color",[236,110,160])),s.get("days"),s.get("cx",0.5))
    print(s["out"])
