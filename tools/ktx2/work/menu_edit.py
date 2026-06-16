from PIL import Image, ImageDraw, ImageFont
import numpy as np
im=Image.open("menu_orig.png").convert("RGB")
a=np.asarray(im).astype(np.int32)
BOLD="C:/Windows/Fonts/calibrib.ttf"
TEXT=(7,24,16)
d=ImageDraw.Draw(im)
def wrap(text,font,maxw):
    words=text.split();lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw:cur=t
        else:
            if cur:lines.append(cur)
            cur=w
    if cur:lines.append(cur)
    return lines
# (erase x0,y0,x1,y1), title_left_x, title_top_y, new title   (Three.js kept, not listed)
tiles=[
 ((260,311,418,390),282,315,"RAG for E-Commerce"),
 ((451,311,614,390),472,315,"TensorRT Optimization"),
 ((641,311,804,390),658,315,"Thai Image Captioning"),
 ((64,668,226,748),88,672,"Extractive Q&A"),
 ((260,668,418,748),282,672,"Efficient Chess AI"),
 ((451,668,614,748),472,672,"AI Flashcard Generator"),
 ((641,668,804,748),658,672,"AI To-Do List Agent"),
]
MAXW=142
for (ex0,ey0,ex1,ey1),tx,ty,title in tiles:
    bg=tuple(int(v) for v in np.median(a[ey0:ey1,ex0:ex1].reshape(-1,3),0))  # tile mint (robust)
    d.rectangle([ex0,ey0,ex1,ey1],fill=bg)
    for sz in range(22,15,-1):
        f=ImageFont.truetype(BOLD,sz);ls=wrap(title,f,MAXW)
        if len(ls)<=3 and not any(d.textlength(w,font=f)>MAXW for w in title.split()):break
    lh=sz-1
    for i,l in enumerate(ls): d.text((tx,ty+i*lh),l,font=f,fill=TEXT)
    print(f"{title!r}: sz={sz} lines={len(ls)} bg={bg}")
im.save("menu_edited.png")
print("saved menu_edited.png")
