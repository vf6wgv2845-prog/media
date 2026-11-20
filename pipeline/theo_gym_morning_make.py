import sys, math, subprocess, numpy as np, soundfile as sf
sys.path.insert(0,'/home/claude/glowup/posts'); sys.path.insert(0,'/home/claude/glowup/day1v3')
from cards import F, emoji
from common import snow
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
W,H,FPS=1080,1920,30
# ---------- voice ----------
from kokoro_onnx import Kokoro
K=Kokoro('/home/claude/tts/kokoro.onnx','/home/claude/tts/voices.bin'); SR=24000
SC={'s1':[(0.1,"Six A.M. Before school."),(0.25,"And for once... Theo didn't hit snooze.")],
    's2':[(0.2,"He walked into the gym..."),(0.25,"and signed up. For real.")],
    's3':[(0.2,"First bench press. Ever."),(0.2,"Just the bar. Forty-five pounds."),(0.3,"One. Two. Three. Four. Five. Six. Seven..."),(0.5,"Eight."),(0.35,"He racked it. Barely.")],
    's4':[(0.2,"Fitness? Up to four."),(0.15,"Confidence? Up to five."),(0.25,"Twenty-seven days until he sees his ex.")],
    's5':[(0.2,"Day four drops tonight at five forty-five."),(0.2,"Vote on day three now. Hair, brows, fit, gym... or reply to Maya?")]}
TM={};DUR={};aud=[]
for s,L in SC.items():
    P=[];st=[];t=0
    for g,txt in L:
        a,_=K.create(txt,voice='am_michael',speed=1.08,lang='en-us'); nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-300):nz[-1]+1200]
        P.append(np.zeros(int(g*SR))); t+=g; st.append(t); P.append(a); t+=len(a)/SR
    tail=1.6 if s=='s5' else 0.35; P.append(np.zeros(int(tail*SR))); t+=tail
    TM[s]=st; DUR[s]=round(t*FPS)/FPS; v=np.concatenate(P); v=np.concatenate([v,np.zeros(max(0,int(DUR[s]*SR)-len(v)))])[:int(DUR[s]*SR)]; aud.append(v)
mix=np.concatenate(aud); 
# alarm beeps at start
for k in range(3):
    s0=int((0.05+k*0.28)*SR); tt=np.arange(int(0.12*SR))/SR; mix[s0:s0+len(tt)]+=0.18*np.sign(np.sin(2*np.pi*1100*tt))*np.exp(-tt*8)
# clank when racked
off3=DUR['s1']+DUR['s2']; s0=int((off3+TM['s3'][4]-0.1)*SR); tt=np.arange(int(0.4*SR))/SR
mix[s0:s0+len(tt)]+=0.25*np.sin(2*np.pi*180*tt)*np.exp(-tt*12)+0.12*np.random.default_rng(0).standard_normal(len(tt))*np.exp(-tt*20)
mix/=np.abs(mix).max()*1.05; sf.write('mix.wav',mix.astype(np.float32),SR)
# ---------- visuals ----------
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x):
    x=max(0,min(1,x)); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def T(d,y,t,sz,w="Black",fill=(255,255,255),a=255,x=W//2):
    d.text((x+4,y+5),t,font=F(w,sz),fill=(0,0,0,int(170*a/255)),anchor="mm"); d.text((x,y),t,font=F(w,sz),fill=tuple(fill[:3])+(a,),anchor="mm")
def cover(p,b=1.0,blur=0):
    s=Image.open(p).convert('RGB'); k=max(W*1.1/s.width,H*1.1/s.height); s=s.resize((int(s.width*k),int(s.height*k)),Image.LANCZOS)
    if blur: s=s.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(s).enhance(b)
THEO=Image.open('/home/claude/glowup/assets/theo_d02_clearskin.jpg').convert('RGB')
FACE=THEO.crop((230,250,600,620)).resize((300,300),Image.LANCZOS)
fm=Image.new('L',(300,300),0); ImageDraw.Draw(fm).ellipse([0,0,299,299],fill=255)
BG1=cover('/home/claude/glowup/assets/theo_gaming.jpg',0.35,6)
GYM=Image.new('RGB',(W,H)); d=ImageDraw.Draw(GYM)
for y in range(H): t=y/H; d.line([(0,y),(W,y)],fill=(int(18+14*t),int(20+10*t),int(28+20*t)))
for x in range(0,W,120): d.rectangle([x,0,x+4,H],fill=(30,34,46))
d.rectangle([0,1500,W,H],fill=(22,22,28))
GYMRGBA=GYM.convert('RGBA'); Y=(255,214,102); RED=(214,48,64)
def crop_pan(img,t,dur,z0,z1):
    z=z0+(z1-z0)*t/dur; cw,ch=W/z*1.0,H/z*1.0; x0=(img.width-cw)/2; y0=(img.height-ch)/2
    return img.crop((int(x0),int(y0),int(x0+cw),int(y0+ch))).resize((W,H),Image.BILINEAR).convert('RGBA')
def s1(t):
    im=crop_pan(BG1,t,DUR['s1'],1.0,1.06); d=ImageDraw.Draw(im)
    sh=math.sin(t*40)*10*max(0,1-t/1.0)
    p=back(t/0.35); f=F("Black",int(220*max(0.3,p)))
    d.text((W//2+sh+5,560+6),"6:00",font=f,fill=(0,0,0,170),anchor="mm"); d.text((W//2+sh,560),"6:00",font=f,fill=Y,anchor="mm")
    T(d,720,"AM",90,"Black")
    e=emoji("⏰",150); im.alpha_composite(e,(int(W//2-e.width//2+sh),250))
    T(d,880,"Before school.",76,"ExtraBold",a=int(255*ease(t/0.4)))
    if t>TM['s1'][1]: T(d,1350,"Theo didn't hit snooze.",68,"Black",a=int(255*ease((t-TM['s1'][1])/0.3)))
    d.rounded_rectangle([W//2-200,1560,W//2+200,1630],radius=35,fill=RED); T(d,1595,"DAY 4  •  MORNING",38,"ExtraBold")
    return im
def card():
    c=Image.new('RGBA',(860,520),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([0,0,859,519],radius=40,fill=(25,25,32),outline=Y,width=6)
    d.rectangle([0,0,859,110],fill=Y); d.rounded_rectangle([0,0,859,120],radius=40,fill=Y)
    d.text((430,62),"IRONWORKS GYM",font=F("Black",58),fill=(20,20,24),anchor="mm")
    f=FACE.resize((230,230)); m=fm.resize((230,230)); c.paste(f,(45,175),m)
    d.text((310,200),"MEMBER",font=F("Bold",32),fill=(170,170,180)); d.text((310,240),"Theo",font=F("Black",72),fill="white")
    d.text((310,335),"Since: Day 4",font=F("Bold",36),fill=Y); d.text((310,385),"Status: ACTIVE",font=F("Bold",36),fill=(120,230,120))
    for i in range(40): x=310+i*13; d.rectangle([x,450,x+(4 if i%3 else 8),495],fill="white")
    return c
CARD=card()
def s2(t):
    im=GYMRGBA.copy(); d=ImageDraw.Draw(im)
    T(d,330,"He walked in...",80,"Black",a=int(255*ease(t/0.3)))
    st=TM['s2'][1]-0.1
    if t>st:
        p=back((t-st)/0.5); ang=(1-ease((t-st)/0.6))*-14
        c=CARD.rotate(ang,expand=True,resample=Image.BICUBIC); s=0.6+0.4*p; c=c.resize((int(c.width*s),int(c.height*s)))
        im.alpha_composite(c,(W//2-c.width//2,int(960-c.height//2+(1-ease((t-st)/0.5))*500)))
        T(d,1380,"and signed up. For real.",64,"Black",Y,int(255*ease((t-st-0.3)/0.3)))
    return im
def s3(t):
    im=GYMRGBA.copy(); d=ImageDraw.Draw(im); st=TM['s3']
    T(d,260,"FIRST BENCH PRESS. EVER.",58,"Black",Y)
    if t>st[1]: T(d,340,"just the bar: 45 lb",48,"ExtraBold",a=int(255*ease((t-st[1])/0.3)))
    # bench
    d.rounded_rectangle([200,1240,880,1300],radius=20,fill=(60,60,70)); d.rectangle([260,1300,290,1500],fill=(70,70,80)); d.rectangle([790,1300,820,1500],fill=(70,70,80))
    d.rectangle([150,700,175,1500],fill=(80,80,92)); d.rectangle([905,700,930,1500],fill=(80,80,92))
    # reps
    r0,r1=st[2],st[3]+0.6; reps=8
    if t<r0: ph=0; rep=0
    elif t<r1:
        u=(t-r0)/(r1-r0)*reps; rep=int(u)+0; ph=math.sin(math.pi*(u%1))
    else: rep=reps; ph=0
    strain= 1 if (r0<t<r1 and rep>=6) else 0
    by=820+int(ph*(260 if rep<6 else 180))
    shake=int(math.sin(t*50)*6*strain)
    # face lying on bench
    f=FACE.rotate(-90 if False else 0); im.paste(f,(W//2-150+shake,1000),fm)
    if strain: e=emoji("💦",70); im.alpha_composite(e,(W//2+120,980))
    # bar + plates
    d=ImageDraw.Draw(im)
    d.rectangle([110,by-10,970,by+10],fill=(200,200,210))
    for x in (95,955): d.rounded_rectangle([x-12,by-30,x+12,by+30],radius=6,fill=(150,150,160))
    d.rounded_rectangle([W//2-200,by+10,W//2-170,by+150],radius=12,fill=(240,200,170)); d.rounded_rectangle([W//2+170,by+10,W//2+200,by+150],radius=12,fill=(240,200,170))
    if t>=r0:
        n=min(rep,reps) if t<r1 else reps
        T(d,560,f"{n}",200 if t<r1 else 220,"Black",Y if n<reps else (120,230,120))
        T(d,680,"REPS",44,"ExtraBold")
    if t>st[4]: 
        a=int(255*ease((t-st[4])/0.3)); d.rounded_rectangle([140,1560,940,1700],radius=40,fill=(20,20,28,int(210*a/255)))
        T(d,1630,"Racked it. Barely.",70,"Black",a=a)
    return im
def s4(t):
    im=GYMRGBA.copy(); d=ImageDraw.Draw(im); st=TM['s4']
    f=FACE.resize((360,360)); m=fm.resize((360,360)); im.paste(f,(W//2-180,260),m); d=ImageDraw.Draw(im)
    rows=[("Fitness",3,4,st[0]),("Confidence",4,5,st[1])]
    for i,(lab,a0,a1,t0) in enumerate(rows):
        y=800+i*120; p=ease((t-t0-0.3)/0.6); v=a0+(a1-a0)*p
        d.text((150,y),lab,font=F("Bold",50),fill="white",anchor="lm")
        d.rounded_rectangle([500,y-18,860,y+18],radius=18,fill=(70,70,80)); d.rounded_rectangle([500,y-18,500+360*v/10,y+18],radius=18,fill=RED)
        d.text((950,y),f"{round(v)}/10",font=F("ExtraBold",48),fill=(120,230,120) if p>0.95 else (255,255,255),anchor="rm")
    if t>st[2]: T(d,1180,"27 days",120,"Black",Y,int(255*ease((t-st[2])/0.3))); T(d,1300,"until he sees his ex.",62,"ExtraBold",a=int(255*ease((t-st[2])/0.3)))
    return im
def s5(t):
    im=crop_pan(BG1,t,DUR['s5'],1.06,1.12); d=ImageDraw.Draw(im); st=TM['s5']
    T(d,420,"DAY 4",150,"Black",Y,int(255*ease(t/0.3))); T(d,560,"drops tonight 5:45 PM",64,"ExtraBold",a=int(255*ease(t/0.3)))
    if t>st[1]:
        a=int(255*ease((t-st[1])/0.4)); d.rounded_rectangle([90,850,990,1330],radius=40,fill=(20,20,28,int(215*a/255)),outline=RED+(a,),width=5)
        T(d,930,"Vote on Day 3 now:",54,"Black",a=a)
        for i,o in enumerate(["1 Hair   2 Brows   3 Fit","4 Gym again   5 Reply to Maya"]): T(d,1040+i*90,o,48,"ExtraBold",Y,a)
        T(d,1250,"New here? Day 1 is pinned.",42,"Bold",a=a)
    e=emoji("👇",100)
    if t>st[1]+0.5: im.alpha_composite(e,(W//2-e.width//2,1420+int(math.sin(t*6)*12)))
    return im
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","mix.wav","-map","0:v","-map","1:a","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","44100","-shortest","-movflags","+faststart","gym.mp4"],stdin=subprocess.PIPE)
for s,fn in (('s1',s1),('s2',s2),('s3',s3),('s4',s4),('s5',s5)):
    n=int(round(DUR[s]*FPS))
    for i in range(n):
        t=i/FPS; fr=fn(t).convert('RGB')
        fo=min(1,(t+1/FPS)/0.08,(DUR[s]-t)/0.08)
        if fo<1 and s!='s1': fr=Image.blend(Image.new('RGB',(W,H)),fr,max(0,fo))
        p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait(); print(DUR, TM)
