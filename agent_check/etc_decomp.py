# Bidding model (WITS version), exact: the learning premium split into the value of free information (A),
# win displacement (D1) and spend drain (D2), and the budget below which free perfect information lowers value.
import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom

thL, thH, K, pi0 = 0.5, 8.0, 100, 0.5
r = thH/thL; bI = np.sqrt(thL*thH)
q  = lambda th,b: b/(b+th)
qb = lambda pi,b: pi*q(thH,b)+(1-pi)*q(thL,b)

def bstar(pi,rho):
    if rho<=0: return 0.0
    f=lambda b: b*qb(pi,b)-rho
    return brentq(f,1e-14,rho+thH+10)
def g(pi,rho):
    if rho<=0: return 0.0
    return rho/bstar(pi,rho)
def W(B): return K*g(pi0,B/K)
def post(tau,w):
    k=(pi0/(1-pi0))*r**((tau-2*w)/2); return k/(1+k)

def parts(tau,B):
    """ETC-style split of V(tau;B)-W(B) = A + D1 + D2"""
    V=A=D1=D2=0.0
    for th,p0 in ((thH,pi0),(thL,1-pi0)):
        for w in range(tau+1):
            p=p0*binom.pmf(w,tau,q(th,bI))
            pi=post(tau,w)
            rho_w=(B-w*bI)/(K-tau)
            g_w=g(pi,rho_w); g_0=g(pi,B/K)
            V += p*(w+(K-tau)*g_w)
            A += p*K*g_0
            D1+= p*(w-tau*g_0)
            D2+= p*(K-tau)*(g_w-g_0)
    return V, A-W(B), D1, D2

def Vstar(B):
    best=(W(B),0)
    for tau in range(1,int(min(K-1,B//bI))+1):
        v=parts(tau,B)[0]
        if v>best[0]+1e-12: best=(v,tau)
    return best

def oracle(B):
    rho=B/K
    phi=lambda th:(np.sqrt(rho*rho+4*th*rho)-rho)/2/th  # = rho/beta
    return K*(pi0*phi(thH)+(1-pi0)*phi(thL))

print("bI=%.3f  I_KL=%.4f  Chernoff=%.4f"%(bI, 0.6*np.log(4), -np.log(2*np.sqrt(.16))))
print("\n B     W      V*    tau*  premium | oracle-W (free perfect info)")
for B in [5,10,20,30,40,56,80,100,150,224,300,600,1000,2000,3000]:
    v,t=Vstar(B)
    print("%5d %7.3f %7.3f %3d  %7.3f | %8.3f"%(B,W(B),v,t,v-W(B),oracle(B)-W(B)))

print("\nETC split at chosen tau:  R = A(info, free) + D1(win displacement) + D2(spend drain)")
for B,tau in [(30,2),(40,4),(56,2),(100,8),(224,8),(600,5),(2000,1),(3000,1)]:
    V,A,D1,D2=parts(tau,B)
    print("B=%5d tau=%2d  R=%+.3f  A=%+.3f  D1=%+.3f  D2=%+.3f"%(B,tau,V-W(B),A,D1,D2))

# where does free perfect info turn valuable?
f=lambda B: oracle(B)-W(B)
print("\noracle=W crossing at B = %.2f"%brentq(f,1,100))
# free tau-probe info value A as function of B for tau=2,8
print("\nA(tau;B) free-information value:")
for B in [5,10,20,30,40,50,60,80,100]:
    print(B, " ".join("%+.3f"%parts(t,B)[1] for t in (1,2,4,8)))
