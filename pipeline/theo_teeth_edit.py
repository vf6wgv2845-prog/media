import cv2, numpy as np, sys
src, out_path = sys.argv[1], sys.argv[2]
im=cv2.imread(src).astype(np.float32); h,w=im.shape[:2]
X,Y=np.meshgrid(np.arange(w),np.arange(h)); X=X.astype(np.float32); Y=Y.astype(np.float32)
mx,my=X.copy(),Y.copy()
for i,(cx,cy) in enumerate(((379,578),(476,576))):          # lift mouth corners
    g=np.exp(-((X-cx)**2+(Y-(cy-4))**2)/(2*16*16)); my+=18*g; mx+=(5 if i==0 else -5)*g
g=np.exp(-((X-428)**2)/(2*34*34)-((Y-598)**2)/(2*14*14)); my-=10*g   # lower lip down (open)
for cx in (398,458):                                          # relax worried inner brows
    g=np.exp(-((X-cx)**2)/(2*22*22)-((Y-405)**2)/(2*16*16)); my-=5*g
for cx in (392,466):                                          # cheeks up a touch (eyes smile)
    g=np.exp(-((X-cx)**2)/(2*40*40)-((Y-520)**2)/(2*30*30)); my+=4*g
o=cv2.remap(im,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
poly=[]
for x in range(388,470,2):
    t=(x-429)/41.0; poly.append((x,582-6*t*t))
for x in range(470,386,-2):
    t=(x-429)/41.0; poly.append((x,583+10*(1-t*t)-6*t*t))
mask=np.zeros((h,w),np.float32); cv2.fillPoly(mask,[np.array(poly,np.int32)],1.0); mask=cv2.GaussianBlur(mask,(0,0),1.1)
teeth=np.zeros_like(o); base=np.array([206,220,232],np.float32)
for x in range(380,478):
    t=abs(x-429)/43.0; teeth[:,x]=base*(1.0-0.5*t**1.5)
for gx,s in ((429,0.72),(413,0.84),(445,0.84),(399,0.88),(459,0.88)):
    teeth[:,gx-1:gx+1]*=s
yy=np.arange(h)[:,None].astype(np.float32)
vg=np.clip(1-np.maximum(0,(yy-589))/7.0,0.3,1.0)*np.clip(0.72+(yy-579)/10.0,0.72,1.0)
teeth*=vg[...,None]
out=o*(1-mask[...,None])+teeth*mask[...,None]
cv2.imwrite(out_path,np.clip(out,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
