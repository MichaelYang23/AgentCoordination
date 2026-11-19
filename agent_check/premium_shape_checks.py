"""Numerical checks of the algebra in theory/agent_teams/agent_premium_shape.tex.
These checks are not part of any proof; they guard against algebra slips."""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom
rng=np.random.default_rng(3)

class Static:
    def __init__(s,thL,thH,de,dh,me,mh,pi):
        s.thL,s.thH,s.de,s.dh,s.me,s.mh,s.pi=thL,thH,de,dh,me,mh,pi
        s.De,s.Dh=me*de,mh*dh; s.Se,s.Sh=me*np.sqrt(de),mh*np.sqrt(dh); s.S=s.Se+s.Sh; s.D=s.De+s.Dh
        s.k=np.sqrt(dh/de); s.BL=thL*s.De*(s.k-1); s.BH=thH*s.De*(s.k-1); s.M=me+mh
        s.Bpi=brentq(lambda B:s.dl_dy(0.0,B),s.BL,s.BH)
    def eps(s,th,y,B): return th*s.Se**2/(B-y+th*s.De)**2
    def eta(s,th,y,B): return th*s.Sh**2/(y+th*s.Dh)**2
    def Phi(s,th,y,B): return th*s.Se**2/(B-y+th*s.De)+th*s.Sh**2/(y+th*s.Dh)
    def G(s,th,B):
        return s.M-(s.Phi(th,0.0,B) if B<=th*s.De*(s.k-1) else th*s.S**2/(B+th*s.D))
    def lam(s,th,B):
        return th*s.Se**2/(B+th*s.De)**2 if B<=th*s.De*(s.k-1) else th*s.S**2/(B+th*s.D)**2
    def L(s,th,y,B): return s.G(th,B)-(s.M-s.Phi(th,y,B))
    def dl_dy(s,y,B):  # derivative in y of pi*L_H+(1-pi)*L_L
        return s.pi*(s.eps(s.thH,y,B)-s.eta(s.thH,y,B))+(1-s.pi)*(s.eps(s.thL,y,B)-s.eta(s.thL,y,B))
    def ystar(s,B):
        if s.dl_dy(0.0,B)>=0: return 0.0
        return brentq(lambda y:s.dl_dy(y,B),0.0,B,xtol=1e-15,rtol=1e-15)
    def N(s,B):
        y=s.ystar(B); return s.pi*s.L(s.thH,y,B)+(1-s.pi)*s.L(s.thL,y,B)
    def Lam(s,B):
        y=s.ystar(B); return s.pi*s.eps(s.thH,y,B)+(1-s.pi)*s.eps(s.thL,y,B)
    def NB(s,B): return s.pi*s.lam(s.thH,B)+(1-s.pi)*s.lam(s.thL,B)-s.Lam(B)

# ---------- 1. baseline static objects
b=Static(0.5,8.0,0.25,4.0,50,50,0.5)
Bhat=brentq(b.NB,b.Bpi*1.001,b.BH)
print("1. baseline: B_L=%.2f  B_pi0=%.2f  B_H=%.2f  peak of N at %.2f  N there=%.4f"%(b.BL,b.Bpi,b.BH,Bhat,b.N(Bhat)))
print("   B      N(pi0;B)   ratio sum pi*lam_theta / lam(pi0)")
for B in (15,18.75,26,30,40,60,100,122,160,250,300,400,600,1000,5000):
    print("   %-7g %8.4f   %8.4f"%(B,b.N(B),(b.pi*b.lam(b.thH,B)+(1-b.pi)*b.lam(b.thL,B))/b.Lam(B)))
# loss representation against a direct maximization
from scipy.optimize import minimize_scalar
for B in (40.,100.,250.,400.):
    r=minimize_scalar(lambda y:-(b.M-b.pi*b.Phi(b.thH,y,B)-(1-b.pi)*b.Phi(b.thL,y,B)),bounds=(0,B),method='bounded',options=dict(xatol=1e-12))
    print("   check N = sum pi*G_theta - G(pi0):  B=%g  %.8f vs %.8f"%(B,b.N(B),b.pi*b.G(b.thH,B)+(1-b.pi)*b.G(b.thL,B)+r.fun))

# ---------- 2. curvature of the level curves, random parameters and points
def draw():
    r=np.exp(rng.uniform(np.log(1.05),np.log(2000))); k=np.exp(rng.uniform(np.log(1.05),np.log(40)))
    mu=np.exp(rng.uniform(np.log(0.02),np.log(50))); pi=rng.uniform(0.03,0.97)
    return Static(1.0,r,1.0,k*k,1.0,mu,pi)
badL=badH=0;nL=nH=0;badLx=badHx=0
for _ in range(3000):
    s=draw(); sig_e=s.Se/s.S; sig_h=s.Sh/s.S
    # lenient state: B>B_L, 0<=y<y_L(B); finite differences are unreliable next to y_L, where the curvature vanishes
    B=s.BL*np.exp(rng.uniform(0.01,6)); yL=sig_h*B-s.thL*(s.Se*s.Dh-s.Sh*s.De)/s.S
    y=rng.uniform(0,0.97)*yL
    def slopeL(y,B): return (s.lam(s.thL,B)-s.eps(s.thL,y,B))/(s.eta(s.thL,y,B)-s.eps(s.thL,y,B))
    p=slopeL(y,B); h=1e-5*B
    curv=(slopeL(y+p*h,B+h)-slopeL(y-p*h,B-h))/(2*h)   # derivative of the slope along the level curve
    nL+=1; badL+= curv>=0
    badLx+= (p/(y+s.thL*s.Dh)-(1-p)/(B-y+s.thL*s.De))>=0   # exact sign of d log t / dB
    # strict state: 0<y<B<B_H
    B=rng.uniform(0.02,0.999)*s.BH; y=rng.uniform(0.001,0.999)*B
    def slopeH(y,B): return (s.eps(s.thH,y,B)-s.lam(s.thH,B))/(s.eps(s.thH,y,B)-s.eta(s.thH,y,B))
    p=slopeH(y,B); h=1e-6*B
    curv=(slopeH(y+p*h,B+h)-slopeH(y-p*h,B-h))/(2*h)
    nH+=1; badH+= curv<=0
    a=s.Se/(B-y+s.thH*s.De); bb=s.Sh/(y+s.thH*s.Dh); c=s.Se/(B+s.thH*s.De)
    badHx+= not (bb<c<a and c**3-(1-p)**2*a**3-p**2*bb**3*s.Se/s.Sh>0)
print("2. level curves, finite differences: lenient not concave in %d of %d draws; strict not convex in %d of %d draws"%(badL,nL,badH,nH))
print("   level curves, exact criteria of the proofs: lenient fails %d, strict fails %d"%(badLx,badHx))

# ---------- 3. sign pattern of N_B and second derivative at the peak
bad=0;tot=0;bad2=0
for _ in range(400):
    s=draw(); tot+=1
    Bs=np.exp(np.linspace(np.log(s.BL*1.001),np.log(s.BH*30),600)); v=np.array([s.NB(B) for B in Bs])
    sc=np.array([s.Lam(B) for B in Bs]); sg=np.sign(np.where(np.abs(v)<1e-11*sc,0,v)); sg=sg[sg!=0]
    if not (sg[0]>0 and np.sum(sg[1:]!=sg[:-1])==1): bad+=1
    Bh=brentq(s.NB,s.Bpi*(1+1e-9),s.BH); h=1e-5*Bh
    if not (s.Bpi<Bh<s.BH and (s.NB(Bh+h)-s.NB(Bh-h))<0): bad2+=1
print("3. N_B positive then negative with one change: fails in %d of %d draws; peak outside (B_pi,B_H) or N_BB>=0 there: %d"%(bad,tot,bad2))

# ---------- 4. exact model at the baseline: sandwich, rising side, scallop example

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

M=model(); ne,nh,pi0,sl=M['ne'],M['nh'],M['pi0'],M['s']
thL,thH,de=0.5,8.0,0.25
bI=2.0; qL=bI/(bI+thL); qH=bI/(bI+thH); rho=np.sqrt(qL*qH)+np.sqrt((1-qL)*(1-qH))
chi=1-(pi0*qH+(1-pi0)*qL)+sl*(pi0/thH+(1-pi0)/thL)/de
print("4. rho=%.4f  chi=%.4f"%(rho,chi))
print("   B     tau*   R(B)     N(pi0;B)   lower bound N-K*rho^tau/2-tau*chi at tau*")
for B in (26,40,60,100,122,160,250,400,600):
    W,Wp=M['solve'](pi0,B,ne,nh); best=(0,W)
    for tau in range(1,13):
        v,vb=M['Vb'](tau,B)
        if v>best[1]: best=(tau,v)
    print("   %-5g %3d   %7.4f  %8.4f   %9.3f"%(B,best[0],best[1]-W,b.N(B),b.N(B)-0.5*100*rho**max(best[0],1)-max(best[0],1)*chi))
# rising side
xbar=b.Bpi/b.De
Bup=ne*min(sl,de*xbar)
def xe0(B):
    y=b.ystar(B); return (B-y)/b.De
Bc=brentq(lambda B:de*xe0(B)-sl,1.0,2000.0)
print("   B_up = n_e*min(s,d_e*xbar(pi0)) = %.2f ;  budget at which the prior team's tokens per easy task equal s: %.1f"%(Bup,Bc))
worst=1e9
for B in np.arange(1.0,Bup+1e-9,0.5):
    W,Wp=M['solve'](pi0,B,ne,nh)
    for tau in range(1,int(B/sl)+1):
        v,vb=M['Vb'](tau,B); worst=min(worst,vb-Wp)
print("   min over B<=B_up and affordable tau>=1 of dV(tau;B)/dB - W'(B): %.3e (should be >= 0)"%worst)
# scallop
Ms=model(c=0.205)
def Rt(tau,B):
    v,vb=Ms['Vb'](tau,B); W,Wp=Ms['solve'](pi0,B,ne,nh); return v-W,vb/Wp
print("   scallop example, c=0.205:")
for B in (120.0,120.354,121.0,121.452,121.885,122.5):
    vals={t:Rt(t,B) for t in (5,6,7,8)}
    tb=max(vals,key=lambda t:vals[t][0])
    print("     B=%.3f  best tau=%d  R=%.6f  H=%.5f   (R_6=%.6f, R_7=%.6f; H_6=%.5f, H_7=%.5f)"%(B,tb,vals[tb][0],vals[tb][1],vals[6][0],vals[7][0],vals[6][1],vals[7][1]))

# ---------- 5. the polynomial identity at the end of the proof of the iso-loss lemma (needs sympy)
try:
    import sympy as sp
    a_,b_,c_=sp.symbols('a b c',positive=True)
    lhs=c_**3*(a_**2-b_**2)**2-a_**3*(c_**2-b_**2)**2-a_*b_**2*(c_-b_)*(a_-c_)*(a_+c_)**2
    rhs=(a_-b_)*(a_-c_)*(a_**2*(b_**3-b_**2*c_+c_**3)+a_*b_**3*c_+a_*b_*c_**3+b_**3*c_**2)
    print("5. factorization identity holds:",sp.expand(lhs-rhs)==0)
    sg_e,sg_h,t_=sp.symbols('sigma_e sigma_h t',positive=True)
    g=sg_h*t_**2*(1+sg_e+sg_h*t_)/((1+t_)*(sg_e+sg_h*t_)**2)
    raw=((sg_e+sg_h*t_)**-2-1)/(t_**-2-1)
    print("   slope formula g(t) holds:",sp.simplify((raw-g).subs(sg_e,1-sg_h))==0)
except ImportError:
    print("5. sympy not installed; skipping the two symbolic identities")
