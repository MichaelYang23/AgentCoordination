# Checks of theory/agent_teams/agent_theory.tex at the baseline: (a) closed forms under a known standard,
# (b) the slope formula against central differences, (c) the decomposition V-W=A-C,
# (d) the single-team table (tau*, R, H, value of knowing the standard), (e) token demand under a price.
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import binom
thL, thH, pi0 = 0.5, 8.0, 0.5
r=thH/thL; de,dh,c=0.25,4.0,0.2; ne=nh=50; K=100; bI=np.sqrt(thL*thH); kap=de*bI+c
qI={thH:bI/(bI+thH), thL:bI/(bI+thL)}
def post(tau,w):
    k=(pi0/(1-pi0))*r**((tau-2*w)/2); return k/(1+k)
def f(pi,b,d):  return pi*b/(b+thH*d)+(1-pi)*b/(b+thL*d) if b>0 else 0.0
def fp(pi,b,d): return pi*thH*d/(b+thH*d)**2+(1-pi)*thL*d/(b+thL*d)**2
def alloc(pi,R,me,mh):
    if mh==0: return me*f(pi,R/me,de),R/me,0.0
    if me==0: return mh*f(pi,R/mh,dh),0.0,R/mh
    obj=lambda s: -(me*f(pi,s*R/me,de)+mh*f(pi,(1-s)*R/mh,dh))
    res=minimize_scalar(obj,bounds=(0,1),method='bounded',options={'xatol':1e-13})
    cands=[(obj(x),x) for x in (res.x,0.0,1.0)]; v,s=min(cands)
    return -v,s*R/me,(1-s)*R/mh
def G(pi,R,me,mh): return alloc(pi,R,me,mh)[0] if R>0 else 0.0
def lam(pi,R,me,mh):
    v,be,bh=alloc(pi,R,me,mh)
    return fp(pi,be,de) if be>0 else fp(pi,bh,dh)
def Pw(tau,w): return pi0*binom.pmf(w,tau,qI[thH])+(1-pi0)*binom.pmf(w,tau,qI[thL])
def V(tau,B):
    if tau==0: return G(pi0,B,ne,nh)
    return sum(Pw(tau,w)*(w+G(post(tau,w),B-tau*kap,ne-tau,nh)) for w in range(tau+1))
def VB(tau,B):
    if tau==0: return lam(pi0,B,ne,nh)
    return sum(Pw(tau,w)*lam(post(tau,w),B-tau*kap,ne-tau,nh) for w in range(tau+1))
def best(B,tmax=14):
    W=V(0,B); bv,bt=W,0
    for t in range(1,tmax+1):
        if t*kap>=B: break
        v=V(t,B)
        if v>bv+1e-10: bv,bt=v,t
    return bv,bt,W

print("(a) closed forms under known theta")
for th,pi in ((thL,0.0),(thH,1.0)):
    for R,me,mh in ((100,50,50),(10,50,50),(300,42,50),(600,50,50)):
        S=me*np.sqrt(de)+mh*np.sqrt(dh); D=me*de+mh*dh; M=me+mh
        thr=me*de*th*(np.sqrt(dh/de)-1)
        Gc=M-th*S*S/(R+th*D) if R>=thr else me*R/(R+th*me*de)
        lc=th*S*S/(R+th*D)**2 if R>=thr else th*me*me*de/(R+th*me*de)**2
        print("  th=%.1f R=%4d (%d,%d) thr=%7.2f  G num %.8f cf %.8f | lam num %.8f cf %.8f"%(th,R,me,mh,thr,G(pi,R,me,mh),Gc,lam(pi,R,me,mh),lc))

print("(b) V_B(tau;B)=E[lambda] vs central difference")
for tau,B in ((8,100.),(5,200.),(3,30.),(0,100.),(1,26.)):
    h=1e-4; fd=(V(tau,B+h)-V(tau,B-h))/(2*h)
    print("  tau=%d B=%5.0f  formula %.8f  FD %.8f"%(tau,B,VB(tau,B),fd))

print("(c) decomposition V-W = A - C")
for tau,B in ((8,100.),(5,200.),(3,30.),(2,15.),(1,700.),(4,18.)):
    W=V(0,B)
    EG=sum(Pw(tau,w)*G(post(tau,w),B,ne,nh) for w in range(tau+1))
    A=EG-W; C=EG-V(tau,B)
    print("  tau=%d B=%5.0f  V-W=%+.6f  A=%+.6f  C=%+.6f  A-C=%+.6f"%(tau,B,V(tau,B)-W,A,C,A-C))

print("(d) H(B)=E[lambda at tau*]/lambda0, and VPI")
for B in (20,26,30,40,60,100,122,160,250,400,600,720):
    bv,bt,W=best(B)
    O=pi0*G(1.0,B,ne,nh)+(1-pi0)*G(0.0,B,ne,nh)
    print("  B=%4d tau*=%d  R=%.4f  H=%.4f   VPI=%.4f"%(B,bt,bv-W,VB(bt,B)/VB(0,B),O-W))

print("(e) token demand under a price p (v=1)")
for BE in (15,24,40,80,110,122,140,200,400):
    p=VB(0,float(BE))
    grid=np.arange(max(1.0,BE-70),BE+70.01,0.5)
    vals=[best(B)[0]-p*B for B in grid]; BL=grid[int(np.argmax(vals))]
    print("  B^E=%4d  p=%.5f  B^L=%.1f  H(B^E)=%.4f"%(BE,p,BL,VB(best(float(BE))[1],float(BE))/p))
