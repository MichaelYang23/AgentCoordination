# Learning window of a single team at the baseline: the lower bound, the value of free information near it,
# entry and exit budgets, the peak of the premium on a coarse grid, and the conservative upper bound.
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import binom
thL, thH, pi0 = 0.5, 8.0, 0.5
r=thH/thL; de,dh,c=0.25,4.0,0.2; ne=nh=50; K=100
def post(tau,w):
    k=(pi0/(1-pi0))*r**((tau-2*w)/2); return k/(1+k)
def f(pi,b,d):
    return pi*b/(b+thH*d)+(1-pi)*b/(b+thL*d) if b>0 else 0.0
def val(pi,R,n_e,n_h):
    if R<=0: return 0.0
    obj=lambda s: -(n_e*f(pi,s*R/n_e,de)+n_h*f(pi,(1-s)*R/n_h,dh))
    res=minimize_scalar(obj,bounds=(0,1),method='bounded',options={'xatol':1e-12})
    return max(-res.fun,-obj(0.0),-obj(1.0))
def Vtau(tau,B):
    bI=de*np.sqrt(thL*thH); R=B-tau*(bI+c)
    if R<=0: return -1
    v=0.0
    for th,p0 in ((thH,pi0),(thL,1-pi0)):
        qq=bI/(bI+th*de)
        for w in range(tau+1):
            v+=p0*binom.pmf(w,tau,qq)*(w+val(post(tau,w),R,ne-tau,nh))
    return v
def prem(B,tmax=14):
    W=val(pi0,B,ne,nh); best,bt=W,0
    for tau in range(1,tmax+1):
        v=Vtau(tau,B)
        if v>best+1e-9: best,bt=v,tau
    return best-W,bt,W
print("lower bound formula: n_e d_e min{thL(sqrt(dh/de)-1), bI+c/de} =",ne*de*min(thL*(np.sqrt(dh/de)-1),np.sqrt(thL*thH)+c/de))
print("free-info value (informed - W) near the bound:")
for B in (15,18,18.75,19.5,21,24):
    O=pi0*val(1.0,B,ne,nh)+(1-pi0)*val(0.0,B,ne,nh)
    print("  B=%.2f  %.6f"%(B,O-val(pi0,B,ne,nh)))
print("entry:")
for B in np.arange(24,29.01,0.5):
    p,t,_=prem(B); print("  B=%.1f tau*=%d premium=%.4f"%(B,t,p))
print("exit:")
for B in (680,700,710,720,730,740,760):
    p,t,_=prem(B); print("  B=%d tau*=%d premium=%.5f"%(B,t,p))
pk=max(((prem(B)[0],B) for B in range(110,150,4)))
print("peak premium %.3f at B=%d"%pk)
dI=1-(pi0*0.2+(1-pi0)*0.8)
print("delta_I=",dI," conservative upper bound B with W(B)=K-delta_I:",brentq(lambda B: val(pi0,B,ne,nh)-(K-dI),1e3,1e7))
