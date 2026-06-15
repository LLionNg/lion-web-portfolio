import sys, json
from PIL import Image, ImageDraw, ImageFont
import numpy as np

N = sys.argv[1]
data = json.load(open("projects.json"))[N]
SRC = f"project{N}_orig.png"
OUT = f"project{N}_edited.png"
BOLD = "C:/Windows/Fonts/calibrib.ttf"
REG  = "C:/Windows/Fonts/calibri.ttf"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(np.int32)
def sample(x0,y0,x1,y1): return tuple(int(v) for v in np.mean(a[y0:y1,x0:x1].reshape(-1,3),0))
BG   = sample(200,516,700,527)        # clean mint band below the heading
TEXT = (12,40,27)
PILL = (17,18,18)
d = ImageDraw.Draw(im)
def erase(x0,y0,x1,y1): d.rectangle([x0,y0,x1,y1], fill=BG)

def card_bottom(xc, y0, y1):
    # bottom y of the contiguous mint card at column xc (stops at chroma gap)
    last=y0; gap=0; seen=False
    for y in range(y0,y1):
        mint = a[y, xc-15:xc+15, 0].mean()>40
        if mint: last=y; gap=0; seen=True
        elif seen:
            gap+=1
            if gap>12: break
    return last
BIG_BOT   = card_bottom(400, 478, 845)   # info card bottom (varies per project)
SMALL_BOT = card_bottom(80, 311, 560)    # small title card bottom

def wrap(text, font, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

# ===== SMALL TITLE CARD (clear whole title zone under the icon, redraw) =====
erase(76,311,282,SMALL_BOT-2)
SMW=176
for sz in range(26,17,-1):
    f_small=ImageFont.truetype(BOLD,sz); sl=wrap(data["title"],f_small,SMW)
    if len(sl)<=4 and not any(d.textlength(w,font=f_small)>SMW for w in data["title"].split()): break
sy=316; lh=sz+7
for i,l in enumerate(sl): d.text((88, sy+i*lh), l, font=f_small, fill=TEXT)

# ===== BIG INFO CARD: clear entire interior text zone, redraw everything =====
erase(108,479,797,BIG_BOT-2)

# heading (bold, 1 line, auto-shrink)
for hs in range(30,21,-1):
    f_head=ImageFont.truetype(BOLD,hs)
    if d.textlength(data["title"],font=f_head)<=675: break
d.text((112, 512-hs-2), data["title"], font=f_head, fill=TEXT)

# description (regular, wrapped, <=6 lines, auto-shrink)
for ds in range(19,14,-1):
    f_desc=ImageFont.truetype(REG,ds); dl=wrap(data["desc"],f_desc,643)
    if len(dl)<=6: break
for i,l in enumerate(dl): d.text((112, 531+i*ds), l, font=f_desc, fill=TEXT)

# recreate "Skills" pill + skills list
d.rounded_rectangle([114,651,185,678], radius=7, fill=PILL)
d.text((121, 653), "Skills", font=ImageFont.truetype(BOLD,16), fill=(255,255,255))
for ks in range(19,14,-1):
    f_sk=ImageFont.truetype(REG,ks)
    if d.textlength(data["skills"],font=f_sk)<=625: break
d.text((194, 657), data["skills"], font=f_sk, fill=TEXT)

im.save(OUT)
print(f"project{N}: '{data['title']}' small={sz}({len(sl)}ln) head={hs} desc={ds}({len(dl)}ln) skill={ks} | cardBottom={BIG_BOT} smallBottom={SMALL_BOT}")
