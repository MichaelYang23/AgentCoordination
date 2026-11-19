# How a report enters the Bayes update: a report is a signal with a likelihood under each standard.
# Latent representation of the pass probability b/(b+theta d):
#   margin M = (b/d) U / theta,  P(U>t)=1/(1+t),  pass iff M>=1   =>  P_theta(M>m) = 1/(1+k m), k = theta d/b
import numpy as np, itertools
from math import lgamma, exp, log, sqrt
from agent_model import model
M_=model(); ne,nh,pi0,s=M_['ne'],M_['nh'],M_['pi0'],M_['s']
def G(pi,B,me=ne,mh=nh): return M_['solve'](pi,B,me,mh)[0]
kL,kH=0.5/2,8/2          # learning task: b/d = b^I = 2
S=lambda k,m:1/(1+k*m)
f=lambda k,m:k/(1+k*m)**2
LR=lambda m:f(kH,m)/f(kL,m)
post=lambda lr:pi0*lr/(pi0*lr+1-pi0)
print("continuous margin: m, LR(H:L), posterior P(strict)")
for m in [0.1,0.5,0.9,0.99,1.0,1.1,2,10]:
    print("  m=%5.2f  LR=%7.3f  post=%.3f"%(m,LR(m),post(LR(m))))
print("  0/1 verdict: fail LR=%.2f post=%.3f ; pass LR=%.2f post=%.3f"%(0.8/0.2,post(4),0.2/0.8,post(.25)))
cuts=[0.25,1.0,4.0]
def cat(k):
    e=[1.0]+[S(k,c) for c in cuts]+[0.0]
    return np.array([e[i]-e[i+1] for i in range(4)])
pL,pH=cat(kL),cat(kH)
names=["far fail (m<0.25)","near fail (0.25<=m<1)","near pass (1<=m<4)","clear pass (m>=4)"]
print("\n4-category report:  P under lenient, P under strict, LR, posterior")
for n,a,b in zip(names,pL,pH): print("  %-24s %.4f  %.4f  %6.3f  %.3f"%(n,a,b,b/a,post(b/a)))
print("Bhattacharyya coefficient: 0/1 = %.4f ; 4 categories = %.4f ; continuous margin = %.4f"%(
    2*sqrt(.16), np.sum(np.sqrt(pL*pH)), sqrt(kL*kH)*log(kH/kL)/(kH-kL)))

def logmult(n,p): return lgamma(sum(n)+1)-sum(lgamma(x+1) for x in n)+sum(x*log(q) for x,q in zip(n,p))
def V_report(tau,B):
    Br=B-tau*s
    if Br<0: return -1e9
    tot=0.0
    for n in itertools.product(range(tau+1),repeat=3):
        if sum(n)>tau: continue
        n=n+(tau-sum(n),)
        a=exp(logmult(n,pH)); b=exp(logmult(n,pL)); P=pi0*a+(1-pi0)*b
        tot+=P*((n[2]+n[3])+G(pi0*a/P,Br,ne-tau,nh))
    return tot
print("\nexact premium, same cost per evaluation s=%.2f"%s)
print("    B     W     0/1: R (tau*)     4-category report: R (tau*)")
for B in [30,60,100,150,250,400]:
    W=G(pi0,B)
    b0=max(((M_['Vb'](t,B)[0],t) for t in range(1,13)))
    b4=max(((V_report(t,B),t) for t in range(1,11)))
    print(" %5g %6.2f   %6.3f (%d)          %6.3f (%d)"%(B,W,max(b0[0]-W,0),b0[1],max(b4[0]-W,0),b4[1]))
