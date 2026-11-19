# Baseline numbers of the agent-team model: the B=100 example (what the team does when it knows the
# standard and when it does not), the single-team curves on a grid of two tokens, and the two-team
# allocation table at v1/v2=2. Self-contained (does not use agent_model.py).
import numpy as np, json, time
from scipy.optimize import minimize_scalar
from scipy.stats import binom
thL, thH, pi0 = 0.5, 8.0, 0.5
r=thH/thL; de,dh,c=0.25,4.0,0.2; ne=nh=50
def post(tau,w):
    k=(pi0/(1-pi0))*r**((tau-2*w)/2); return k/(1+k)
def f(pi,b,d):
    return pi*b/(b+thH*d)+(1-pi)*b/(b+thL*d) if b>0 else 0.0
def alloc(pi,R,n_e,n_h):
    obj=lambda s: -(n_e*f(pi,s*R/n_e,de)+n_h*f(pi,(1-s)*R/n_h,dh))
    res=minimize_scalar(obj,bounds=(0,1),method='bounded',options={'xatol':1e-10})
    cand=[(obj(x),x) for x in (res.x,0.0,1.0)]
    v,s=min(cand); return -v,s
def val(pi,R,n_e,n_h):
    if R<=0: return 0.0
    return alloc(pi,R,n_e,n_h)[0]
def Vtau(tau,B):
    bI=de*np.sqrt(thL*thH); R=B-tau*(bI+c)
    if R<=0: return -1
    v=0.0
    for th,p0 in ((thH,pi0),(thL,1-pi0)):
        qq=bI/(bI+th*de)
        for w in range(tau+1):
            v+=p0*binom.pmf(w,tau,qq)*(w+val(post(tau,w),R,ne-tau,nh))
    return v

# --- the B=100 story in detail
B=100
for name,pi in (("lenient known",0.0),("strict known",1.0),("unknown (prior 1/2)",0.5)):
    v,s=alloc(pi,B,ne,nh); be,bh=s*B/ne,(1-s)*B/nh
    print("%-20s effort easy=%.2f hard=%.2f | if lenient: easy %.0f%% hard %.0f%% -> %.1f passes | if strict: easy %.0f%% hard %.0f%% -> %.1f"%(
        name,be,bh,100*be/(be+thL*de),100*bh/(bh+thL*dh) if bh>0 else 0,50*be/(be+thL*de)+(50*bh/(bh+thL*dh) if bh>0 else 0),
        100*be/(be+thH*de),100*bh/(bh+thH*dh) if bh>0 else 0,50*be/(be+thH*de)+(50*bh/(bh+thH*dh) if bh>0 else 0)))
print("W(100)=%.2f"%val(0.5,B,ne,nh))
for tau in (4,8):
    print("ETC tau=%d: V=%.2f"%(tau,Vtau(tau,B)))
# posterior after 8 probes
for w in range(9):
    print("  w=%d passes of 8: P(strict)=%.4f  prob of seeing this: %.3f"%(w,post(8,w),0.5*binom.pmf(w,8,0.2)+0.5*binom.pmf(w,8,0.8)))

# --- single-team value curves and planner
t0=time.time()
grid=np.arange(0,702,2.0)
Wv=np.array([val(0.5,B,ne,nh) for B in grid])
Vv=Wv.copy(); Tv=np.zeros(len(grid),int)
for i,B in enumerate(grid):
    for tau in range(1,13):
        v=Vtau(tau,B)
        if v>Vv[i]+1e-9: Vv[i]=v; Tv[i]=tau
print("curve time %.0fs"%(time.time()-t0))
learn=grid[Tv>0]
print("learning window on grid: [%.0f, %.0f]"%(learn.min(),learn.max()))
print("\nlocal ratio dV/dW (10-unit differences):")
for B in (20,30,40,60,80,100,130,160,200,250,300,400,500,600):
    i=int(B/2); j=i+5
    print("  B=%3d tau*=%d  ratio=%.3f"%(B,Tv[i],(Vv[j]-Vv[i])/(Wv[j]-Wv[i])))
print("\nplanner, v1/v2=2:  T   (E) split      (L) split     shift")
for T in (40,60,80,100,150,200,300,400,500,600,700):
    n=int(T/2)
    idx=np.arange(0,n+1)
    E=2*Wv[idx]+Wv[n-idx]; L=2*Vv[idx]+Vv[n-idx]
    aE=grid[idx[np.argmax(E)]]; aL=grid[idx[np.argmax(L)]]
    print("  %4d  (%3.0f,%3.0f)  (%3.0f,%3.0f)  %+3.0f   tau=(%d,%d)"%(T,aE,T-aE,aL,T-aL,aL-aE,Tv[int(aL/2)],Tv[int((T-aL)/2)]))
