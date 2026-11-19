# First pass of the move from bidding to agent teams (14 November): (1) with identical tasks, knowing the
# standard is worth nothing; (2) premium with easy and hard tasks; (3) the cap / give-up alternative.
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import binom
thL, thH, pi0 = 0.5, 8.0, 0.5
r = thH/thL
def post(tau,w):
    k=(pi0/(1-pi0))*r**((tau-2*w)/2); return k/(1+k)
def f(pi,b,d):
    return pi*b/(b+thH*d)+(1-pi)*b/(b+thL*d) if b>0 else 0.0
def val(pi,R,ne,nh,de,dh):
    if R<=0: return 0.0
    if nh==0: return ne*f(pi,R/ne,de)
    if ne==0: return nh*f(pi,R/nh,dh)
    obj=lambda s: -(ne*f(pi,s*R/ne,de)+nh*f(pi,(1-s)*R/nh,dh))
    res=minimize_scalar(obj,bounds=(0,1),method='bounded',options={'xatol':1e-10})
    return max(-res.fun,-obj(0.0),-obj(1.0))
def Vtau(tau,B,c,de,dh,ne,nh):
    bI=de*np.sqrt(thL*thH); R=B-tau*(bI+c)
    if R<=0: return -1
    v=0.0
    for th,p0 in ((thH,pi0),(thL,1-pi0)):
        qq=bI/(bI+th*de)
        for w in range(tau+1):
            v+=p0*binom.pmf(w,tau,qq)*(w+val(post(tau,w),R,ne-tau,nh,de,dh))
    return v

# (1) homogeneous example quoted in text
K=100
W=K*f(pi0,1.0,1.0)
print("homogeneous: W(100)=%.3f ; tau=8,c=1: V=%.3f ; tau=8,c=0: V=%.3f"%(W,Vtau(8,100,1.0,1.0,1.0,50,50),Vtau(8,100,0.0,1.0,1.0,50,50)))

# (2) heterogeneous: finer grid, premium shape
de,dh,c=0.25,4.0,0.2
print("\nhetero d=(.25,4), c=.2 :  B  tau*  premium")
prev=None
for B in [20,25,28,30,32,34,36,38,40,45,50,60,80,100,130,160,200,250,300,400,500,600,700,800]:
    W=val(pi0,B,50,50,de,dh); best,bt=W,0
    for tau in range(1,26):
        v=Vtau(tau,B,c,de,dh,50,50)
        if v>best+1e-9: best,bt=v,tau
    print("%5d  %2d  %+.4f"%(B,bt,best-W))

# (3) cap / give-up model: tokens needed X ~ log-logistic(theta); pass iff X<=cap b; spend=min(X,b)
e=lambda th,b: th*np.log1p(b/th)          # expected tokens consumed with cap b
q=lambda th,b: b/(b+th)
print("\ncap model (homogeneous tasks, expected-spend pacing):  B   W   informed-W")
for B in [5,20,50,100,200,400,1000]:
    rho=B/K
    b0=brentq(lambda b: pi0*e(thH,b)+(1-pi0)*e(thL,b)-rho,1e-12,1e9)
    W=K*(pi0*q(thH,b0)+(1-pi0)*q(thL,b0))
    O=0
    for th,p in ((thH,pi0),(thL,1-pi0)):
        bt=brentq(lambda b: e(th,b)-rho,1e-12,1e12); O+=p*K*q(th,bt)
    print("%5d %7.2f %+7.2f   (cap b0=%.2f; spend if hard %.2f, if easy %.2f per task)"%(B,W,O-W,b0,e(thH,b0),e(thL,b0)))
# failed vs successful consumption at cap b0 for B=100
b0=brentq(lambda b: pi0*e(thH,b)+(1-pi0)*e(thL,b)-1,1e-12,1e9)
for th in (thL,thH):
    succ=(e(th,b0)-b0*(1-q(th,b0)))/q(th,b0)
    print("theta=%.1f: failed run burns %.2f, successful run burns %.2f on average"%(th,b0,succ))
