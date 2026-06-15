from PIL import Image, ImageDraw
im = Image.open("project2_orig.png").convert("RGB")
d = ImageDraw.Draw(im)
for x in range(0, 1024, 50):
    d.line([(x,0),(x,1023)], fill=(255,0,0), width=1)
    if x % 100 == 0:
        d.text((x+1, 2), str(x), fill=(255,255,0))
for y in range(0, 1024, 50):
    d.line([(0,y),(1023,y)], fill=(255,0,0), width=1)
    if y % 100 == 0:
        d.text((2, y+1), str(y), fill=(255,255,0))
im.save("project2_grid.png")
print("saved project2_grid.png")
