from PIL import Image
import numpy as np

im = Image.open("project2_orig.png").convert("RGB")
a = np.asarray(im).astype(np.int32)
H, W, _ = a.shape
lum = (0.299*a[:,:,0] + 0.587*a[:,:,1] + 0.114*a[:,:,2])

def region_stats(name, x0, y0, x1, y1):
    r = a[y0:y1, x0:x1]
    print(f"{name}: mean RGB {r.reshape(-1,3).mean(0).round(1)}  std {r.reshape(-1,3).std(0).round(1)}")

# Sample backgrounds: chroma green (outside cards), mint info-card clean area
region_stats("chroma-green (top strip)", 0, 0, 1024, 20)
region_stats("info-card clean (below skills)", 200, 840, 850, 870)
region_stats("info-card clean (right pad)", 820, 660, 900, 700)

# Detect dark text rows in the info card column band (x ~ 130..900)
band = lum[600:900, 150:900]
row_dark = (band < 90).sum(axis=1)  # count of dark pixels per row
print("\nInfo-card text rows (y: dark-pixel-count) where count>15:")
for i,c in enumerate(row_dark):
    if c > 15:
        print(f"  y={600+i}: {c}")
