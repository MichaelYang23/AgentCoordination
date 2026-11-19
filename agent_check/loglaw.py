# Bidding model (WITS version): optimal learning length as the horizon K doubles, exact model against the
# averaged (smoothed) model, with the rates predicted by the Chernoff information and by the KL rate.
import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom
thL, thH, pi0 = 0.5, 8.0, 0.5
r=thH/thL; bI=np.sqrt(thL*thH)
q=lambda th,b:b/(b+th)
qb=lambda pi,b:pi*q(thH,b)+(1-pi)*q(thL,b)
def g(pi,rho):
    if rho<=0: return 0.0
    return rho/brentq(lambda b:b*qb(pi,b)-rho,1e-14,rho+thH+10)
def post(tau,w):
    k=(pi0/(1-pi0))*r**((tau-2*w)/2); return k/(1+k)
def V(tau,B,K):
    v=0.0
    for th,p0 in ((thH,pi0),(thL,1-pi0)):
        for w in range(tau+1):
            v+=p0*binom.pmf(w,tau,q(th,bI))*(w+(K-tau)*g(post(tau,w),(B-w*bI)/(K-tau)))
    return v
# averaged model
c=(np.sqrt(r)-1)/(2*(np.sqrt(r)+1))
def Vbar(tau,B,K):
    v=0.0
    for th,p0,sgn in ((thH,pi0,+1),(thL,1-pi0,-1)):
        k=(pi0/(1-pi0))*r**(sgn*tau*c); pi=k/(1+k)
        rho=(B-tau*bI*q(th,bI))/(K-tau)
        b=brentq(lambda b:b*qb(pi,b)-rho,1e-14,rho+thH+10)
        v+=p0*(tau*q(th,bI)+(K-tau)*q(th,b))
    return v
from scipy.optimize import minimize_scalar
print("rate per doubling predicted: KL %.2f, Chernoff %.2f"%(np.log(2)/0.8318,np.log(2)/0.2231))
for x in (1.0,2.0):
    print("B/K =",x)
    for K in (100,200,400,800,1600,3200,6400):
        B=x*K
        vals=[V(t,B,K) for t in range(0,61)]
        te=int(np.argmax(vals))
        res=minimize_scalar(lambda t:-Vbar(t,B,K),bounds=(0.01,40),method='bounded')
        print("  K=%5d exact tau*=%2d  averaged tau*=%.2f"%(K,te,res.x))
