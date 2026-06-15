from PIL import Image
import numpy as np
a=np.asarray(Image.open("project2_orig.png").convert("RGB")).astype(np.int32)
lum=0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]
mask=lum<45
# save mask for viewing
Image.fromarray(np.where(mask,0,255).astype('uint8')).save("mask.png")

def bbox(name,x0,y0,x1,y1):
    m=mask[y0:y1,x0:x1]
    rc=m.sum(axis=1); cc=m.sum(axis=0)
    xs=np.where(cc>2)[0]; ys=np.where(rc>4)[0]
    if len(xs)==0: print(f"{name}: none");return
    print(f"{name}: x[{x0+xs.min()}..{x0+xs.max()}] y[{y0+ys.min()}..{y0+ys.max()}]")
    lines=[];inrun=False
    for i,c in enumerate(rc):
        if c>4 and not inrun:start=i;inrun=True
        elif c<=4 and inrun:lines.append((y0+start,y0+i-1));inrun=False
    if inrun:lines.append((y0+start,y0+len(rc)-1))
    print("   lines:",[f"{s}-{e}(h{e-s+1})" for s,e in lines])

bbox("SMALL-TITLE",70,305,400,420)
bbox("BIG-HEADING",100,478,780,512)
bbox("DESCRIPTION",108,512,840,652)
bbox("SKILLS-LIST",155,655,840,690)
print("saved mask.png")
