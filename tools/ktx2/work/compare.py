from PIL import Image
o=Image.open("project2_orig.png").convert("RGB")
e=Image.open("project2_edited.png").convert("RGB")
def stack(x0,y0,x1,y1,scale,name):
    co=o.crop((x0,y0,x1,y1)); ce=e.crop((x0,y0,x1,y1))
    w,h=co.size
    canvas=Image.new("RGB",(w, h*2+6),(40,40,40))
    canvas.paste(co,(0,0)); canvas.paste(ce,(0,h+6))
    canvas=canvas.resize((canvas.width*scale,canvas.height*scale),Image.NEAREST)
    canvas.save(name); print("saved",name,canvas.size)
# main card: heading+desc+skills (orig top / edited bottom)
stack(105,478,770,690,2,"cmp_card.png")
# small title
stack(78,300,200,420,3,"cmp_small.png")
