# Two-point prior against a lognormal prior on the standard with the same mean and sd of log(theta), at B=K:
# optimal learning length and premium as the number of tasks K grows.
import numpy as np, time
from scipy.optimize import minimize_scalar
from scipy.stats import binom
de,dh,c,xp=0.25,4.0,0.2,2.0      # probe: normalized effort 2 on an easy task (0.5 tokens) + fee
def make(prior_th,prior_w):
    th=np.asarray(prior_th); pw=np.asarray(prior_w)/np.sum(prior_w)
    qp=xp/(xp+th)
    def G(post,R,me,mh):
        if R<=0: return 0.0
        def obj(s):
            be=s*R/me; bh=(1-s)*R/mh
            v=me*np.dot(post,be/(be+th*de)) if be>0 else 0.0
            if bh>0: v+=mh*np.dot(post,bh/(bh+th*dh))
            return -v
        r=minimize_scalar(obj,bounds=(0,1),method='bounded',options={'xatol':1e-9})
        return max(-r.fun,-obj(0.0),-obj(1.0))
    def V(tau,B,K):
        R=B-tau*(de*xp+c)
        if R<=0 or tau>=K//2: return -1
        if tau==0: return G(pw,B,K//2,K//2)
        v=0.0
        for w in range(tau+1):
            lik=binom.pmf(w,tau,qp); pwv=np.dot(pw,lik)
            if pwv<1e-14: continue
            v+=pwv*(w+G(pw*lik/pwv,R,K//2-tau,K//2))
        return v
    return V
V2=make([0.5,8.0],[0.5,0.5])
sig=np.log(4.0); lg=np.linspace(np.log(2)-4*sig,np.log(2)+4*sig,161)
Vc=make(np.exp(lg),np.exp(-0.5*((lg-np.log(2))/sig)**2))
def best(V,K,tmax):
    B=float(K); W=V(0,B,K); bv,bt=W,0; miss=0
    for tau in range(1,tmax+1):
        v=V(tau,B,K)
        if v>bv+1e-9: bv,bt,miss=v,tau,0
        else:
            miss+=1
            if miss>12: break
    return bt,bv-W,W
print("K   | two-point: tau* premium  | continuous (lognormal, same log-sd): tau* premium")
for K in (100,200,400,800,1600,3200):
    t0=time.time()
    a=best(V2,K,120); b=best(Vc,K,min(K//2-1,220))
    print("%5d | %3d  %6.2f (%.2f%% of W) | %3d  %6.2f (%.2f%% of W)   [%.0fs]"%(K,a[0],a[1],100*a[1]/a[2],b[0],b[1],100*b[1]/b[2],time.time()-t0))
