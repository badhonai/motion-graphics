import sys,base64,subprocess,time,imageio_ffmpeg
from playwright.sync_api import sync_playwright
FPS=int(sys.argv[1]);start=float(sys.argv[2]);end=float(sys.argv[3]);out=sys.argv[4]
ff=imageio_ffmpeg.get_ffmpeg_exe()
proc=subprocess.Popen([ff,'-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p','-color_range','tv','-movflags','+faststart',out],stdin=subprocess.PIPE)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]);pg=b.new_page(viewport={"width":1920,"height":1080})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.add_init_script("window.__render=true");pg.goto("file:///home/user/fluton/index.html");pg.evaluate("window.ready")
    n0=round(start*FPS);n1=round(end*FPS);t0=time.time()
    for n in range(n0,n1):
        d=pg.evaluate(f"(frame({n/FPS}),document.getElementById('c').toDataURL('image/jpeg',0.97))")
        proc.stdin.write(base64.b64decode(d[23:]))
        if n%120==0:print(n,round(time.time()-t0),flush=True)
    b.close();print("errs",errs[:3])
proc.stdin.close();proc.wait();print("done",time.time()-t0)
