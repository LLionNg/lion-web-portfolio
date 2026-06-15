import sys
from PIL import Image, ImageDraw
# usage: crop.py x0 y0 x1 y1 scale out.png
x0,y0,x1,y1,scale,out = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
im = Image.open("project2_orig.png").convert("RGB").crop((x0,y0,x1,y1))
im = im.resize((im.width*scale, im.height*scale), Image.NEAREST)
d = ImageDraw.Draw(im)
for x in range(x0 - x0%10, x1, 10):
    sx=(x-x0)*scale
    col=(255,0,0) if x%50==0 else (255,120,120)
    d.line([(sx,0),(sx,im.height)], fill=col, width=1)
    if x%50==0: d.text((sx+1,1), str(x), fill=(255,255,0))
for y in range(y0 - y0%10, y1, 10):
    sy=(y-y0)*scale
    col=(255,0,0) if y%50==0 else (255,120,120)
    d.line([(0,sy),(im.width,sy)], fill=col, width=1)
    if y%50==0: d.text((1,sy+1), str(y), fill=(255,255,0))
im.save(out)
print("saved",out,im.size)
