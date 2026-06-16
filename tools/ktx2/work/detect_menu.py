from PIL import Image
import numpy as np
a=np.asarray(Image.open("menu_orig.png").convert("RGB")).astype(np.int32)
lum=0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]
mask=lum<50

COLS=[(40,235),(245,445),(450,640),(648,845)]   # 4 column x-windows
def detect(y0,y1,tag):
    for i,(cx0,cx1) in enumerate(COLS):
        sub=mask[y0:y1,cx0:cx1]
        ys,xs=np.where(sub)
        if len(xs)==0: print(f"{tag} col{i+1}: empty"); continue
        # per-line rows
        rc=sub.sum(1); lines=[]; inr=False
        for r in range(len(rc)):
            if rc[r]>1 and not inr: s=r; inr=True
            elif rc[r]<=1 and inr: lines.append((y0+s,y0+r-1)); inr=False
        if inr: lines.append((y0+s,y0+len(rc)-1))
        print(f"{tag} col{i+1}: x[{cx0+xs.min()}..{cx0+xs.max()}] y[{y0+ys.min()}..{y0+ys.max()}] lines={[f'{a}-{b}' for a,b in lines]}")
detect(290,398,"R1")
detect(660,768,"R2")
print("tile mint:", tuple(int(v) for v in np.median(a[300:303,150:205].reshape(-1,3),0)))
print("text color:", tuple(int(v) for v in np.median(a[300:388,80:200].reshape(-1,3)[ (0.299*a[300:388,80:200].reshape(-1,3)[:,0]+0.587*a[300:388,80:200].reshape(-1,3)[:,1]+0.114*a[300:388,80:200].reshape(-1,3)[:,2])<60 ],0)))
