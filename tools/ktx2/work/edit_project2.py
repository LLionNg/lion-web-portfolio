from PIL import Image, ImageDraw, ImageFont
import numpy as np

SRC = "project2_orig.png"
OUT = "project2_edited.png"
BOLD = "C:/Windows/Fonts/calibrib.ttf"
REG  = "C:/Windows/Fonts/calibri.ttf"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(np.int32)

def sample_bg(x0,y0,x1,y1):
    # mean = the "blurred" appearance of the dotted card (what shows when dots blur in-app)
    return tuple(int(v) for v in np.mean(a[y0:y1,x0:x1].reshape(-1,3),0))

bigbg   = sample_bg(560,632,750,648)   # clean mint right of last description line
smallbg = bigbg                        # small card uses same mint as big card
TEXT    = (12,40,27)
print("bigbg",bigbg,"smallbg",smallbg)

d = ImageDraw.Draw(im)
def erase(x0,y0,x1,y1,c): d.rectangle([x0,y0,x1,y1], fill=c)

def wrap(draw, text, font, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

# ---------- 1. SMALL TITLE (bold, 2 lines) ----------
erase(84,308,190,415, smallbg)
f_small = ImageFont.truetype(BOLD, 26)
sx=88; sy=315; lh=33
for i,line in enumerate(["RAG for","E-Commerce"]):
    d.text((sx, sy+i*lh), line, font=f_small, fill=TEXT)

# ---------- 2. BIG HEADING (bold, 1 line) ----------
erase(110,480,478,512, bigbg)
f_head = ImageFont.truetype(BOLD, 30)
# match baseline ~504; PIL draws from top, calibri bold size30 ascent ~ use anchor
d.text((112, 482), "RAG for E-Commerce", font=f_head, fill=TEXT)

# ---------- 3. DESCRIPTION (regular, wrapped) ----------
erase(108,528,760,653, bigbg)
DESC=("Built and deployed a domain-specific Retrieval-Augmented Generation pipeline "
      "for e-commerce: semantic chunking and pgvector similarity search over PostgreSQL "
      "with streaming LLM chat responses. Delivered full-stack — frontend UI plus API "
      "and concurrent load testing — and shipped to production on Kubernetes via GitOps "
      "(ArgoCD) for self-healing, scalable serving.")
f_desc = ImageFont.truetype(REG, 19)
lines = wrap(d, DESC, f_desc, 643)
print("desc lines:",len(lines))
dy=531; lh=19.2
for i,line in enumerate(lines):
    d.text((112, dy+round(i*lh)), line, font=f_desc, fill=TEXT)

# ---------- 4. SKILLS LIST (regular, keep pill) ----------
erase(176,654,835,683, bigbg)
f_sk = ImageFont.truetype(REG, 19)
d.text((180, 657), "Python, RAG, pgvector, Kubernetes, ArgoCD", font=f_sk, fill=TEXT)

im.save(OUT)
print("saved", OUT)
