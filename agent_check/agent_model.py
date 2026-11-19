# Exact agent-team model at the baseline form q_theta(x)=x/(x+theta).
#   model(...) returns the solver used by the other scripts in this folder:
#     solve(pi, R, me, mh) -> (G, lambda): commit problem, value and shadow price
#     Vb(tau, B)           -> (V(tau;B), dV/dB): value with tau learning tasks, 0/1 verdicts
# Run as a script: fine-grid scan of the exact premium R(B)=max_tau V(tau;B)-W(B) for B in [100,160],
# listing its local maxima and minima and the budgets at which tau* changes.
import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom
import sys

def model(thL=0.5,thH=8.0,pi0=0.5,K=None,ne=50,nh=50,de=0.25,dh=4.0,c=0.2):
    bI=np.sqrt(thL*thH); s=de*bI+c
    qL=bI/(bI+thL); qH=bI/(bI+thH)
    def Q(pi,x): return pi*thH/(x+thH)**2+(1-pi)*thL/(x+thL)**2
    def f(pi,x): return pi*x/(x+thH)+(1-pi)*x/(x+thL)
    def xof(pi,mu):
        if Q(pi,0.0)<=mu: return 0.0
        hi=1.0
        while Q(pi,hi)>mu: hi*=2
        return brentq(lambda x:Q(pi,x)-mu,0.0,hi,xtol=1e-14,rtol=1e-14)
    def solve(pi,R,me,mh):
        # returns (G, lam)
        if R<=0: return 0.0, Q(pi,0.0)/de
        types=[(m,d) for m,d in ((me,de),(mh,dh)) if m>0]
        def dem(l): return sum(m*d*xof(pi,d*l) for m,d in types)-R
        top=Q(pi,0.0)/min(d for m,d in types)
        lo=top
        while dem(lo)<0: lo/=2
        l=brentq(dem,lo,top*(1-1e-15),xtol=1e-16,rtol=1e-14)
        return sum(m*f(pi,xof(pi,d*l)) for m,d in types), l
    def Vb(tau,B):
        R=B-tau*s
        if R<0 or tau>ne: return -np.inf, np.nan
        w=np.arange(tau+1)
        pH=binom.pmf(w,tau,qH); pL=binom.pmf(w,tau,qL)
        P=pi0*pH+(1-pi0)*pL; post=pi0*pH/P
        v=0.0; vb=0.0
        for wi,p,po in zip(w,P,post):
            g,l=solve(po,R,ne-tau,nh); v+=p*(wi+g); vb+=p*l
        return v,vb
    return dict(s=s,solve=solve,Vb=Vb,ne=ne,nh=nh,pi0=pi0)

if __name__=="__main__":
    M=model()
    grid=np.arange(100.0,160.01,0.25)
    out=[]
    for B in grid:
        W,Wp=M['solve'](M['pi0'],B,M['ne'],M['nh'])
        best=(-1,-np.inf,0)
        for tau in range(0,14):
            v,vb=M['Vb'](tau,B)
            if v>best[1]: best=(tau,v,vb)
        out.append((B,best[0],best[1]-W,best[2]/Wp))
    out=np.array(out)
    R=out[:,2]; d=np.diff(R)
    print("local maxima of R on the fine grid:")
    for i in range(1,len(R)-1):
        if R[i]>R[i-1] and R[i]>R[i+1]: print("  B=%.2f  R=%.6f  tau=%d"%(out[i,0],R[i],out[i,1]))
    print("local minima:")
    for i in range(1,len(R)-1):
        if R[i]<R[i-1] and R[i]<R[i+1]: print("  B=%.2f  R=%.6f  tau=%d"%(out[i,0],R[i],out[i,1]))
    print("tau switches and H just before/after:")
    for i in range(1,len(R)):
        if out[i,1]!=out[i-1,1]: print("  B in (%.2f,%.2f): tau %d->%d, H %.4f -> %.4f"%(out[i-1,0],out[i,0],out[i-1,1],out[i,1],out[i-1,3],out[i,3]))
