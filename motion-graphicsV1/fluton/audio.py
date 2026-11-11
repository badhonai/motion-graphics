import numpy as np
from scipy import signal
from scipy.io import wavfile
SR=44100;B=0.46875;DUR=32.0;N=int(SR*DUR)
rng=np.random.default_rng(7)
L=np.zeros(N);R=np.zeros(N)
def add(buf,t0,pan=0.0,g=1.0):
    i=int(round(t0*SR));
    if i>=N:return
    n=min(len(buf),N-i);l=np.cos((pan+1)*np.pi/4);r=np.sin((pan+1)*np.pi/4)
    L[i:i+n]+=buf[:n]*g*l*1.414;R[i:i+n]+=buf[:n]*g*r*1.414
def env(n,a=0.002,d=0.2):
    t=np.arange(n)/SR;return np.minimum(t/a,1)*np.exp(-t/d)
def lp(x,f,o=2):return signal.sosfilt(signal.butter(o,f,'low',fs=SR,output='sos'),x)
def hp(x,f,o=2):return signal.sosfilt(signal.butter(o,f,'high',fs=SR,output='sos'),x)
def lpsweep(x,f0,f1,K=32):
    n=len(x);out=np.zeros(n);q=np.arange(n)/n
    for k in range(K):
        fc=f0+(f1-f0)*((k+0.5)/K)**2;w=np.clip(1-np.abs(q*K-(k+0.5)),0,1)
        if k==0:w[q*K<0.5]=1
        if k==K-1:w[q*K>K-0.5]=1
        out+=lp(x,fc)*w
    return out
def bp(x,f1,f2):return signal.sosfilt(signal.butter(2,[f1,f2],'band',fs=SR,output='sos'),x)
def kick(g=1.0):
    n=int(.42*SR);t=np.arange(n)/SR;f=46+150*np.exp(-t/0.028);ph=2*np.pi*np.cumsum(f)/SR
    x=np.sin(ph)*np.exp(-t/0.16)+0.5*hp(rng.standard_normal(n),3000)*np.exp(-t/0.004)
    return np.tanh(x*1.8)*g
def hat(d=0.03,g=1.0):
    n=int(.2*SR);return hp(rng.standard_normal(n),7500,4)*env(n,0.001,d)*g
def clap(g=1.0):
    n=int(.35*SR);t=np.arange(n)/SR;e=sum(np.exp(-np.maximum(t-o,0)/0.012)*(t>=o) for o in(0,0.011,0.023))/2+np.exp(-t/0.09)*0.6
    return bp(rng.standard_normal(n),900,5200)*e*g
def snare(g=1.0):
    n=int(.3*SR);t=np.arange(n)/SR
    return (bp(rng.standard_normal(n),1200,8000)*np.exp(-t/0.07)+0.7*np.sin(2*np.pi*190*t)*np.exp(-t/0.05))*g
def saw(f,n,det=0.0):
    t=np.arange(n)/SR;return 2*((f*(1+det)*t)%1)-1
def note(m):return 440*2**((m-69)/12)
def pluck(m,d=0.14,g=1.0,cut=2600):
    n=int(.5*SR);x=(saw(note(m),n)+saw(note(m),n,0.006)+saw(note(m),n,-0.005))/3
    return lp(x,cut)*env(n,0.002,d)*g
def bassn(m,dur,g=1.0):
    n=int(dur*SR);t=np.arange(n)/SR;f=note(m)
    x=np.sin(2*np.pi*f*t)*0.9+lp(saw(f*2,n),500)*0.45+lp(saw(f,n),300)*0.4
    e=np.minimum(t/0.004,1)*np.minimum((dur-t)/0.015,1).clip(0,1)*np.exp(-t/0.35)
    return np.tanh(x*1.4)*e*g
def boom(g=1.0,d=1.4):
    n=int(3.2*SR);t=np.arange(n)/SR;f=30+60*np.exp(-t/0.08)
    x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/d)+lp(rng.standard_normal(n),2500)*np.exp(-t/0.25)*0.5+hp(rng.standard_normal(n),4000)*np.exp(-t/0.5)*0.12
    return np.tanh(x*1.5)*g
def riser(dur,g=1.0,f0=200,f1=9000):
    n=int(dur*SR);t=np.arange(n)/SR;q=t/dur;x=rng.standard_normal(n);out=np.zeros(n);K=24;seg=n//K
    for k in range(K):
        fc=f0*(f1/f0)**((k+0.5)/K);s=slice(k*seg,(k+1)*seg if k<K-1 else n)
        out[s]=bp(x,fc*0.7,min(fc*1.4,20000))[s]
    sw=np.sin(2*np.pi*np.cumsum(110*4**q)/SR)*0.25
    return (out*1.2+sw)*q**2.2*g
def whoosh(dur=0.5,g=1.0,rev=False):
    n=int(dur*SR);t=np.arange(n)/SR;q=t/dur;e=np.sin(np.pi*q)**2*(q**1.5 if not rev else (1-q)**1.5)*2
    return bp(rng.standard_normal(n),500,6000)*e*g
def stab(ms,g=1.0,d=0.5,cut=3200):
    n=int(1.6*SR);x=sum(saw(note(m),n,dt) for m in ms for dt in(0,0.007,-0.006))/(3*len(ms))
    return lp(x,cut)*env(n,0.004,d)*g
bt=lambda b:b*B
# ---------- intro 0–8 ----------
t=np.arange(int(bt(8)*SR))/SR
drone=lp(saw(note(29),len(t))+saw(note(29),len(t),0.01),160)*0.5*np.minimum(t/0.4,1)*(1+0.3*np.sin(2*np.pi*t/B))
add(drone,0,0,0.55)
for b in range(4):
    add(bassn(29,0.3,1.0),bt(b));add(lp(kick(0.8),900),bt(b));add(hat(0.02,0.25),bt(b)+B/2,0.4)
    add(pluck(77,0.1,0.25,1800),bt(b),-0.3)
add(boom(0.9,0.5),bt(4));add(stab([53,56,60],0.55,0.4,1500),bt(4))
for k in range(8):add(hat(0.015,0.18+0.03*k),bt(4)+k*B/4,(-1)**k*0.5)
for i,b in enumerate((5,6,7)):
    add(kick(1.1),bt(b));add(snare(0.8),bt(b));add(stab([53+i,56+i,60+i],0.5,0.22,2400+600*i),bt(b));add(bassn(29+i,0.25),bt(b))
    for k in range(4):add(hat(0.012,0.3),bt(b)+k*B/4,(-1)**k*0.6)
add(riser(bt(4)-0.16,0.7),bt(4))
for k in range(8):add(snare(0.25+0.07*k),bt(7)+k*B/8)   # roll
# ---------- groove ----------
ROOTS=[29,29,25,27]   # F  F  Db Eb  (bass, octave 1)
CH={29:[53,56,60,63],25:[49,53,56,60],27:[51,55,58,63]}
ARP=[0,2,1,3,2,1,3,2,0,3,1,2,3,1,2,3]
def groove(b0,b1,full=True,arp=True,clapOn=True,cut=3000):
    for b in range(b0,b1):
        bar=(b-8)//4;root=ROOTS[bar%4];ch=CH[root]
        add(kick(1.25),bt(b))
        add(hat(0.05,0.42),bt(b)+B/2,0.15)
        for k in (1,3):add(hat(0.012,0.16),bt(b)+k*B/4,-0.4 if k==1 else 0.5)
        if clapOn and b%2==1:add(clap(0.75),bt(b));add(snare(0.3),bt(b))
        for k in (1,2,3):add(bassn(root+12 if k==3 and b%4==3 else root,B/4*0.92,0.78),bt(b)+k*B/4)
        if arp:
            for k in range(4):
                m=ch[ARP[((b%4)*4+k)%16]]+12+(12 if (k+b)%7==0 else 0)
                add(pluck(m,0.11,0.6,cut),bt(b)+k*B/4,0.55*np.sin(b+k*1.3))
                add(pluck(m,0.11,0.22,cut*0.6),bt(b)+k*B/4+B*0.75,-0.55*np.sin(b+k*1.3))
        if full and b%4==0:add(stab(ch,0.7,0.7,2600),bt(b),0,1.0);add(stab([m+12 for m in ch],0.32,0.5,3800),bt(b)+B*1.5,0.3)
groove(8,40);groove(44,48,cut=4200)
# drops / impacts
for b,g in((8,1.0),(44,1.0),(56,1.1)):add(boom(g),bt(b));add(hp(rng.standard_normal(int(1.5*SR)),5000)*env(int(1.5*SR),0.002,0.45)*0.35,bt(b))
for b in(16,24,32,40):add(whoosh(0.5,0.5),bt(b)-0.42,-0.3);add(hp(rng.standard_normal(int(.8*SR)),6000)*env(int(.8*SR),0.002,0.25)*0.22,bt(b))
for b in(20,28):add(boom(0.6,0.5),bt(b))
add(boom(0.5,0.35),bt(26));add(boom(0.4,0.3),bt(30))
for b in range(32,35):                     # node pops
    for k in range(2):add(pluck(84+[0,3,7,10,12,15][(b-32)*2+k],0.08,0.3,5000),bt(b)+0.12+k*B/2,0.6*(-1)**k)
# breakdown 40–44: suns approach
n=int(bt(4)*SR);tt=np.arange(n)/SR
pad=lpsweep(sum(saw(note(m),n,d) for m in(41,53,56,60,65) for d in(0,0.006,-0.007))/15,900,2700)*np.minimum(tt/0.3,1)
add(pad,bt(40),0,0.9);add(riser(bt(4)-0.1,0.75),bt(40))
for k in range(16):add(pluck([65,68,72,75][k%4]+(12 if k>=8 else 0),0.12,0.2+0.012*k,1500+200*k),bt(40)+k*B/4,0.5*(-1)**k)
for k in range(8):add(kick(0.5+0.08*k),bt(43)+k*B/8);add(snare(0.2+0.06*k),bt(43)+k*B/8)
# montage 48–52
for i,b in enumerate(range(48,52)):
    add(kick(1.3),bt(b));add(snare(0.85),bt(b));add(clap(0.6),bt(b));add(bassn(29,0.3),bt(b))
    add(stab([53+2*i,56+2*i,60+2*i,65+2*i],0.5,0.25,3000+500*i),bt(b));add(whoosh(0.3,0.35,True),bt(b))
    for k in range(4):add(hat(0.012,0.3),bt(b)+k*B/4,(-1)**k*0.6)
    add(kick(0.9),bt(b)+B*0.75)
# question 52–56
n=int(bt(4)*SR);tt=np.arange(n)/SR
pad=lpsweep(sum(saw(note(m),n,d) for m in(41,53,56,60,63) for d in(0,0.006,-0.007))/15,700,3300)*np.minimum(tt/0.1,1)
add(pad,bt(52),0,0.85);add(riser(bt(4)-0.12,0.85),bt(52));add(boom(0.5,0.6),bt(52))
for k in range(7):add(pluck([77,80,84,87,89,92,96][k],0.16,0.4,4200),bt(52)+0.03+k*B*0.42,0.5*(-1)**k);add(hat(0.02,0.25),bt(52)+0.03+k*B*0.42)
for k in range(8):add(snare(0.2+0.08*k),bt(55)+k*B/8);add(kick(0.5+0.07*k),bt(55)+k*B/8)
# finale 56–64
groove(56,64,cut=4600)
for b in range(56,64,2):add(pluck(89 if b%4==0 else 92,0.3,0.3,5000),bt(b),0)
# tail
n=int(2.6*SR);tt=np.arange(n)/SR
tail=lp(sum(saw(note(m),n,d) for m in(29,41,53,56,60,65,72) for d in(0,0.005,-0.006))/21,1800)*np.minimum(tt/0.005,1)*np.exp(-tt/0.7)
add(tail,bt(64),0,1.5);add(boom(1.0,1.0),bt(64));add(hp(rng.standard_normal(n),5000)*env(n,0.002,0.6)*0.3,bt(64))
# silence gap before first drop
def duck(t0,t1):
    i0,i1=int(t0*SR),int(t1*SR);r=np.linspace(1,0,int(0.02*SR))
    for X in(L,R):X[i0:i0+len(r)]*=r;X[i0+len(r):i1]=0
duck(bt(8)-0.11,bt(8));duck(bt(56)-0.09,bt(56));duck(bt(44)-0.07,bt(44))
# sidechain-ish glue + simple stereo reverb
def verb(x,dl):
    out=np.zeros(N)
    for d,g in dl:
        k=int(d*SR);y=np.zeros(N);y[k:]=x[:-k];out+=lp(y,3800)*g
    return out
wl=verb(hp(L,300),[(0.031,.22),(0.047,.18),(0.089,.14),(0.141,.10),(B*0.75,.16),(B*1.5,.08)])
wr=verb(hp(R,300),[(0.037,.22),(0.053,.18),(0.097,.14),(0.151,.10),(B*0.75,.16),(B*1.5,.08)])
L+=wr*0.55;R+=wl*0.55
M=np.stack([L,R],1);M=hp(M.T,28).T
print('pre>1 frac',float((np.abs(M*0.42)>1).mean()),'pre rms',float(np.sqrt(((M*0.42)**2).mean())));M=np.tanh(M*0.42)
f=np.ones(N);k=int(0.75*SR);f[-k:]=np.linspace(1,0,k)**1.5;f[:int(0.01*SR)]=np.linspace(0,1,int(0.01*SR))
M*=f[:,None];M=M/np.abs(M).max()*0.94
print('rms',np.sqrt((M**2).mean()),'peak',np.abs(M).max())
wavfile.write('audio.wav',SR,(M*32767).astype(np.int16))
