# Satisfaction score s in (-1,1) as a monotone transform of the margin: s=(M-1)/(M+1), accept iff s>=0.
# Baseline learning task: k_L=1/4, k_H=4  =>  LR(s) = ((5-3s)/(5+3s))^2
import numpy as np
from math import log
from agent_model import model
M_=model(); ne,nh,pi0,s_tok=M_['ne'],M_['nh'],M_['pi0'],M_['s']
def G(pi,B,me=ne,mh=nh): return M_['solve'](pi,B,me,mh)[0]
kL,kH=0.25,4.0
LR=lambda s:((5-3*s)/(5+3*s))**2
print("score s -> LR(strict:lenient) -> posterior P(strict);   P(S<=s | lenient), P(S<=s | strict)")
for s in [-0.9,-0.8,-0.4,-0.05,0,0.05,0.4,0.8,0.9]:
    m=(1+s)/(1-s); cL=1-1/(1+kL*m); cH=1-1/(1+kH*m)
    print("  s=%+.2f  LR=%7.3f  post=%.3f    %.3f  %.3f"%(s,LR(s),LR(s)/(1+LR(s)),cL,cH))
Es=lambda k:1-2*k*(k-1-log(k))/(k-1)**2
print("mean score at probe effort: lenient %.3f, strict %.3f ; 2p-1 would be %.1f, %.1f"%(Es(kL),Es(kH),0.6,-0.6))

# exact premium with the continuous score (Monte Carlo over the posterior), same token cost per evaluation
rng=np.random.default_rng(0); NS=400000
def llr(k,size):
    U=1/rng.random(size)-1; Mg=U/k
    return np.log(16)+2*np.log((1+kL*Mg)/(1+kH*Mg))
grid=np.linspace(0,1,401)
def V_score(tau,B):
    Br=B-tau*s_tok
    if Br<0: return -1e9
    Gg=np.array([G(p,Br,ne-tau,nh) for p in grid])
    out=0.0
    for k,wt in ((kH,pi0),(kL,1-pi0)):
        S=llr(k,(NS,tau)).sum(axis=1)
        post=1/(1+np.exp(-S)*(1-pi0)/pi0)
        out+=wt*np.interp(post,grid,Gg).mean()
    return tau*(pi0*0.2+(1-pi0)*0.8)+out
print("\n    B     W    0/1: R (tau*)   continuous score: R (tau*)")
for B in [30,60,100,150,250,400]:
    W=G(pi0,B)
    b0=max(((M_['Vb'](t,B)[0],t) for t in range(1,13)))
    bc=max(((V_score(t,B),t) for t in range(1,10)))
    print(" %5g %6.2f   %6.3f (%d)        %6.3f (%d)"%(B,W,max(b0[0]-W,0),b0[1],max(bc[0]-W,0),bc[1]))
# sanity: the same Monte Carlo routine applied to the binary signal should reproduce the exact 0/1 number at B=100
def V_bin_mc(tau,B):
    Br=B-tau*s_tok; Gg=np.array([G(p,Br,ne-tau,nh) for p in grid]); out=0
    for q,wt in ((0.2,pi0),(0.8,1-pi0)):
        w=rng.binomial(tau,q,NS); S=(tau-w)*np.log(4)+w*np.log(.25)
        post=1/(1+np.exp(-S)*(1-pi0)/pi0); out+=wt*np.interp(post,grid,Gg).mean()
    return tau*0.5+out
print("sanity (0/1 by the same Monte Carlo, B=100, tau=8): %.3f vs exact %.3f"%(V_bin_mc(8,100)-G(pi0,100),M_['Vb'](8,100)[0]-G(pi0,100)))
