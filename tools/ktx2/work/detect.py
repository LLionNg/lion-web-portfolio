from PIL import Image
import numpy as np
a=np.asarray(Image.open("project2_orig.png").convert("RGB")).astype(np.int32)
lum=0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]

def bbox(name,x0,y0,x1,y1,thr=70):
    sub=lum[y0:y1,x0:x1]
    mask=sub<thr
    ys,xs=np.where(mask)
    if len(xs)==0:
        print(f"{name}: NO TEXT");return
    print(f"{name}: x[{x0+xs.min()}..{x0+xs.max()}] y[{y0+ys.min()}..{y0+ys.max()}]  px={len(xs)}")
    # per-row line detection
    rowcount=mask.sum(axis=1)
    lines=[];inrun=False
    for i,c in enumerate(rowcount):
        if c>3 and not inrun: start=i;inrun=True
        elif c<=3 and inrun: lines.append((y0+start,y0+i-1));inrun=False
    if inrun: lines.append((y0+start,y0+len(rowcount)-1))
    print("   lines(y0..y1):",lines)

bbox("SMALL-TITLE", 70, 305, 400, 425)
bbox("BIG-HEADING", 100, 470, 780, 520)
bbox("DESCRIPTION", 108, 512, 840, 652)
bbox("SKILLS-LIST", 155, 652, 840, 692)
