import json, os, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from kokoro_onnx import Kokoro
FD='/usr/share/fonts/opentype/inter/'
def F(w,s): return ImageFont.truetype(FD+f'Inter-{w}.otf',s)
W,H=1080,1920; FPS=30
j=json.load(open('cap.json')); fr=[f for f in j['frames'] if f[2] not in ('empty','scroll2','read2')]
segs={'type':[f for f in fr if f[2] in('type','typed','hover')],'wait':[f for f in fr if f[2]=='wait'],'cards':[f for f in fr if f[2] in('cards','scroll','read')]}
k=Kokoro('/tmp/tts/kokoro.onnx','/tmp/tts/voices.bin')
lines={'hook':"History test tomorrow. Zero flashcards.",'type':"Paste the notes you have.",'wait':"Tap once.",'cards':"Three exam-style flashcards. From my own notes. Two seconds.",'end':"IntelliStudy. Free to try, no account needed. Link in bio."}
aud={}
for key,t in lines.items():
    a,sr=k.create(t,voice='af_heart',speed=1.1,lang='en-us'); aud[key]=a
# timeline: hook plays over first typing frames
def expand(frames,min_d):
    seq=[[f[0],f[1]] for f in frames]; tot=sum(d for _,d in seq)
    if tot<min_d: seq[-1][1]+=min_d-tot
    return seq
hook_d=len(aud['hook'])/sr+0.25
type_seq=expand(segs['type'],hook_d+len(aud['type'])/sr+0.3)
wait_seq=[[f[0],j['gen_seconds']/len(segs['wait'])] for f in segs['wait']]
cards_seq=expand(segs['cards'],len(aud['cards'])/sr+0.6)
end_d=len(aud['end'])/sr+0.8
t_type=0; t_wait=sum(d for _,d in type_seq); t_cards=t_wait+sum(d for _,d in wait_seq); t_end=t_cards+sum(d for _,d in cards_seq); T=t_end+end_d
print('times',t_wait,t_cards,t_end,T)
# audio
mix=np.zeros(int(T*sr)+sr)
for key,st in [('hook',0.05),('type',hook_d),('wait',t_wait+0.05),('cards',t_cards+0.1),('end',t_end+0.15)]:
    a=aud[key]; i=int(st*sr); mix[i:i+len(a)]+=a
sf.write('out/voice.wav',mix[:int(T*sr)],sr)
bg=Image.new('RGB',(W,H))
g=np.zeros((H,W,3),np.uint8)
for y in range(H):
    c=np.array([18,14,48])*(1-y/H)+np.array([60,40,150])*(y/H); g[y,:]=c
bg=Image.fromarray(g)
PH=1380; PW=int(1170*PH/2280); PX=(W-PW)//2; PY=430
mask=Image.new('L',(PW,PH),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,PW-1,PH-1],46,fill=255)
def phone(path,zoom=1.0,zy=0.5):
    im=Image.open(path).convert('RGB')
    if zoom>1:
        w,h=im.size; cw,ch=w/zoom,h/zoom; y0=(h-ch)*zy; im=im.crop((int((w-cw)/2),int(y0),int((w+cw)/2),int(y0+ch)))
    return im.resize((PW,PH),Image.LANCZOS)
def text_center(d,y,txt,font,fill,stroke=0):
    w=d.textlength(txt,font=font); d.text(((W-w)/2,y),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0))
def sticker(img,txt,y,bg,fg=(255,255,255),size=64,angle=-4):
    f=F('ExtraBold',size); tw=int(ImageDraw.Draw(img).textlength(txt,font=f))
    s=Image.new('RGBA',(tw+60,size+40),(0,0,0,0)); dd=ImageDraw.Draw(s); dd.rounded_rectangle([0,0,tw+59,size+39],18,fill=bg+(255,)); dd.text((30,12),txt,font=f,fill=fg)
    s=s.rotate(angle,expand=True,resample=Image.BICUBIC); img.paste(s,((W-s.width)//2,y),s)
def frame_at(t):
    # pick screenshot
    if t<t_wait: seq,base=type_seq,0
    elif t<t_cards: seq,base=wait_seq,t_wait
    elif t<t_end: seq,base=cards_seq,t_cards
    else: seq=None
    img=bg.copy(); d=ImageDraw.Draw(img)
    if seq:
        acc=base; path=seq[-1][0]
        for p,dur in seq:
            if t<acc+dur: path=p; break
            acc+=dur
        zoom=1.0; zy=0.45
        if t<t_wait: zoom,zy=1.12,1.0
        if t>=t_cards: zoom=1.0+0.12*min(1,(t-t_cards)/0.6)
        ph=phone(path,zoom,zy)
        sh=Image.new('RGBA',(PW+60,PH+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([30,30,PW+30,PH+30],50,fill=(0,0,0,140)); sh=sh.filter(ImageFilter.GaussianBlur(18))
        img.paste(sh,(PX-30,PY-10),sh); img.paste(ph,(PX,PY),mask)
        d=ImageDraw.Draw(img)
        if t<hook_d:
            text_center(d,120,"POV: history test",F('ExtraBold',100),(255,255,255))
            text_center(d,240,"tomorrow. 0 flashcards.",F('ExtraBold',84),(255,214,102))
        elif t<t_wait:
            text_center(d,150,"Paste your notes.",F('ExtraBold',96),(255,255,255))
            text_center(d,275,"(my real WW1 notes)",F('SemiBold',44),(200,200,235))
        elif t<t_cards:
            text_center(d,150,"Tap once.",F('ExtraBold',110),(255,255,255))
            el=min(t-t_wait,j['gen_seconds']); sticker(img,f"⏱ {el:0.1f} s".replace('⏱ ',''),1560,(235,80,95),size=90,angle=3)
        else:
            text_center(d,110,"3 flashcards.",F('ExtraBold',104),(255,255,255))
            text_center(d,235,"2 seconds.",F('ExtraBold',104),(120,225,120))
            if t>t_cards+0.8: sticker(img,"FROM YOUR OWN NOTES",1600,(255,214,102),(15,15,15),size=66,angle=-3)
    else:
        d=ImageDraw.Draw(img)
        text_center(d,600,"IntelliStudy",F('ExtraBold',130),(255,255,255))
        text_center(d,790,"Notes → flashcards, quizzes",F('SemiBold',56),(220,220,245))
        text_center(d,870,"and a revision schedule",F('SemiBold',56),(220,220,245))
        sticker(img,"FREE · NO ACCOUNT TO TRY",1030,(120,225,120),(15,15,15),size=62,angle=-2)
        text_center(d,1260,"intelli-study.com",F('Bold',70),(255,214,102))
        text_center(d,1360,"link in bio",F('SemiBold',54),(220,220,245))
    return img
n=int(T*FPS)
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','out/voice.wav','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','out/final.mp4'],stdin=subprocess.PIPE)
for i in range(n):
    im=frame_at(i/FPS); p.stdin.write(im.tobytes())
    if i in (5,int((hook_d+0.5)*FPS),int((t_wait+0.8)*FPS),int((t_cards+1.5)*FPS),n-10): im.save(f'out/still_{i:04d}.jpg',quality=80)
p.stdin.close(); p.wait()
frame_at(t_cards+1.5).save('out/cover.jpg',quality=92)
print('T',T)
