import sys,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image
ts=[float(x) for x in sys.argv[2:]];out=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]);pg=b.new_page(viewport={"width":960,"height":540})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.add_init_script("window.__render=true");pg.goto("file:///home/user/fluton/index.html");pg.evaluate("window.ready")
    ims=[]
    for t in ts:
        d=pg.evaluate(f"(frame({t}),document.getElementById('c').toDataURL('image/jpeg',0.85))")
        ims.append(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).resize((640,360)))
    cols=3;rows=(len(ims)+cols-1)//cols;s=Image.new('RGB',(640*cols,360*rows))
    for i,im in enumerate(ims):s.paste(im,((i%cols)*640,(i//cols)*360))
    s.save(out,quality=88);print("errs",errs[:5]);b.close()
