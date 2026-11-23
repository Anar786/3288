"""Оригинальная фоновая музыка + SFX для ролика (синтез, без сторонних семплов -> без проблем с правами).
python3 music.py out.wav   — 38 с, 48 кГц, стерео, 100 BPM, Cmaj7–Am7–Fmaj7–G6."""
import sys, wave, numpy as np
SR=48000; DUR=38.0; BPM=100; B=60/BPM
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(7)
def f(m): return 440*2**((m-69)/12)
def env(n,a,d,s=0.0):
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))*((1-s)*np.exp(-t/d)+s); return e
def add(sig,t0,gain=1.0,pan=0.0):
    i=int(t0*SR); j=min(N,i+len(sig));
    if i>=N: return
    s=sig[:j-i]*gain; L[i:j]+=s*(1-pan)/1.0*0.5**0.5*(1+0) if False else s*np.sqrt((1-pan)/2); R[i:j]+=s*np.sqrt((1+pan)/2)
def smooth(x,k):
    return np.convolve(x,np.ones(k)/k,mode='same')
chords=[[48,52,55,59,64],[45,48,52,55,60],[41,45,48,52,57],[43,47,50,52,55]]  # C maj7, Am7, Fmaj7, G6
bar=4*B; clen=2*bar
# pad
for k in range(int(DUR/clen)+1):
    t0=k*clen; ch=chords[k%4]; n=int((clen+0.6)*SR); t=np.arange(n)/SR
    e=np.minimum(1,t/0.8)*np.minimum(1,np.maximum(0,(clen+0.6-t)/0.8))
    sig=np.zeros(n)
    for m in ch[1:]:
        for det in (-0.08,0.08):
            fr=f(m+12)*(1+det/100*12)
            sig+=np.sin(2*np.pi*fr*t)+0.25*np.sin(4*np.pi*fr*t+0.3)
    add(smooth(sig*e,6),t0,0.022,pan=0.0)
    # bass
    for b in range(0,8,2):
        if t0+b*B>=DUR: break
        n2=int(B*1.8*SR); tt=np.arange(n2)/SR
        bs=np.sin(2*np.pi*f(ch[0]-12)*tt)*env(n2,0.01,0.9)
        add(bs,t0+b*B,0.16 if t0>=3.5 else 0.08)
# pluck arpeggio (8ths)
pat=[1,2,3,4,3,2,4,3]
for i in range(int(DUR/(B/2))):
    t0=i*B/2; ch=chords[int(t0//clen)%4]; m=ch[pat[i%8]]+12
    n=int(0.6*SR); t=np.arange(n)/SR
    s=(np.sin(2*np.pi*f(m)*t)+0.3*np.sin(4*np.pi*f(m)*t))*env(n,0.004,0.18)
    add(s,t0,0.07,pan=0.35 if i%2 else -0.35)
# drums (после хука)
for i in range(int(DUR/B)):
    t0=i*B
    if t0<3.5 or t0>DUR-1.8: continue
    if i%2==0:
        n=int(0.35*SR); t=np.arange(n)/SR; fr=45+80*np.exp(-t/0.04)
        add(np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,0.002,0.12),t0,0.32)
    else:
        n=int(0.25*SR); nz=rng.standard_normal(n); nz=nz-smooth(nz,4)  # грубый highpass
        add(smooth(nz,2)*env(n,0.003,0.07),t0,0.06)
    n=int(0.06*SR); nz=rng.standard_normal(n); nz=nz-smooth(nz,3)
    add(nz*env(n,0.001,0.015),t0+B/2,0.035,pan=0.3)
# SFX
def whoosh(t0,dur=0.5,g=0.10):
    n=int(dur*SR); t=np.arange(n)/SR; nz=rng.standard_normal(n)
    e=np.sin(np.pi*t/dur)**2; add(smooth(nz,10)*e,t0-dur*0.6,g)
def tick(t0,m=84,g=0.10):
    n=int(0.25*SR); t=np.arange(n)/SR; add(np.sin(2*np.pi*f(m)*t)*env(n,0.002,0.05),t0,g)
def pop(t0,g=0.2):
    n=int(0.2*SR); t=np.arange(n)/SR; fr=300+600*np.exp(-t/0.02); add(np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,0.002,0.06),t0,g)
for t in (3.5,8,14,21.5,26.5,32): whoosh(t)
for t in (15,16.8,18.6,27.3,28.3,29.3): tick(t+0.05)
pop(0.85); pop(10.35,0.16); pop(23.85,0.14); tick(32.95,88,0.12)
# capsule shake rattles
for k in range(5): tick(1.4+k*0.22,96,0.05)
# fade & normalize
fade=np.ones(N); fl=int(2.2*SR); fade[-fl:]=np.linspace(1,0,fl)**1.5; fade[:int(0.05*SR)]=np.linspace(0,1,int(0.05*SR))
L*=fade; R*=fade; pk=max(abs(L).max(),abs(R).max()); g=0.89/pk; L*=g; R*=g
data=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open(sys.argv[1],'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
