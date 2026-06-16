import sys, json, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

N = sys.argv[1]
data = json.load(open("projects.json", encoding="utf-8"))[N]
SRC = f"project{N}_orig.png"
OUT = f"project{N}_edited.png"
BOLD = "C:/Windows/Fonts/calibrib.ttf"
REG  = "C:/Windows/Fonts/calibri.ttf"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(np.int32)
def sample(x0,y0,x1,y1): return tuple(int(v) for v in np.median(a[y0:y1,x0:x1].reshape(-1,3),0))
BG   = sample(762,545,800,690)        # clean mint at card right margin (robust, median)
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

# ===== SCREENSHOT PANEL: replace with project image (contain-fit, rounded, covers green bleed) =====
PX0,PY0,PX1,PY1 = 277,100,815,370
pw,ph = PX1-PX0, PY1-PY0
imgf = data.get("image"); img_status="img=NONE"
if imgf and os.path.exists(os.path.join(ROOT,imgf)):
    src = Image.open(os.path.join(ROOT,imgf)).convert("RGB")
    scale = min(pw/src.width, ph/src.height)
    nw,nh = max(1,round(src.width*scale)), max(1,round(src.height*scale))
    src_r = src.resize((nw,nh), Image.LANCZOS)
    bgc = tuple(int(v) for v in np.median(np.asarray(src)[:4,:,:].reshape(-1,3),0))  # top-edge bg for bars
    panel = Image.new("RGB",(pw,ph), bgc)
    panel.paste(src_r, ((pw-nw)//2,(ph-nh)//2))
    mask = Image.new("L",(pw,ph),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,pw-1,ph-1], radius=12, fill=255)
    im.paste(panel,(PX0,PY0),mask)
    img_status=f"img={imgf}({src.width}x{src.height})"
else:
    img_status=f"img=MISSING({imgf})"

# cover the small-card right "tab" peeking below the panel with real dotted-chroma
# (blends in the flat preview; chroma is keyed out in-app so the card edge reads clean)
# hide the wide background band where it peeks out below the screenshot panel / right of the small card
sw = im.crop((278, 400, 815, 423))   # chroma from the gap just below the band, same columns (phase-aligned)
im.paste(sw, (278, 371))

im.save(OUT)
print(f"project{N}: '{data['title']}' small={sz}({len(sl)}ln) head={hs} desc={ds}({len(dl)}ln) skill={ks} | BG={BG} cardBot={BIG_BOT} | {img_status}")
