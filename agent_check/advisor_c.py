# Two quick computations for the discussion of the evaluation fee c.
import numpy as np
from scipy.stats import binom
from agent_model import model
M=model(); ne,nh,pi0,s=M['ne'],M['nh'],M['pi0'],M['s']
qL,qH=0.8,0.2
def G(pi,B,me=ne,mh=nh): return M['solve'](pi,B,me,mh)[0]
def lam(pi,B,me=ne,mh=nh): return M['solve'](pi,B,me,mh)[1]

# (1) value of the k-th evaluation at B=100 if evaluations were free and did not distort effort:
#     A(tau) = E G(posterior; B) - G(prior; B)
B=100.0; W=G(pi0,B); N=0.5*G(1.0,B)+0.5*G(0.0,B)-W
print("B=100: value of knowing the standard N = %.3f"%N)
prev=0.0
print(" k   info value of k evaluations   value added by the k-th")
for tau in range(1,13):
    w=np.arange(tau+1); pH=binom.pmf(w,tau,qH); pL=binom.pmf(w,tau,qL); P=pi0*pH+(1-pi0)*pL; post=pi0*pH/P
    A=sum(p*G(po,B) for p,po in zip(P,post))-W
    print("%2d   %8.3f                     %8.3f"%(tau,A,A-prev)); prev=A
print("token cost of one evaluation valued at the shadow price: s*lambda = %.3f passes (s=%.2f, lambda=%.4f)"%(s*lam(pi0,B),s,lam(pi0,B)))

# (2) variant: ONE report reveals the standard. Same tokens per evaluated task (s), task held at probe effort.
def Vrev(B):
    if B<s: return -1e9
    return pi0*qH+(1-pi0)*qL + pi0*G(1.0,B-s,ne-1,nh)+(1-pi0)*G(0.0,B-s,ne-1,nh)
# variant 2b: report on a task done at the effort the team would choose anyway; only the fee c=0.2 is lost
c=0.2
def Vrev2(B):
    if B<c: return -1e9
    return pi0*G(1.0,B-c)+(1-pi0)*G(0.0,B-c)
grid=[20,22,25,30,40,60,100,150,250,400,700,1000,1500,2500,5000]
print("\n   B      W      R (binary, exact)   R one report, probe effort   R one report, normal effort")
for B in grid:
    W=G(pi0,B)
    best=W
    for tau in range(1,13):
        v,_=M['Vb'](tau,B)
        if v>best: best=v
    print("%6g %7.2f   %8.3f            %8.3f                    %8.3f"%(B,W,best-W,max(Vrev(B)-W,0),max(Vrev2(B)-W,0)))
from scipy.optimize import brentq
f=lambda B:Vrev(B)-G(pi0,B)
print("one report, probe effort: learns for B in (%.1f, %.0f)"%(brentq(f,19,40),brentq(f,700,20000)))
f2=lambda B:Vrev2(B)-G(pi0,B)
lo=brentq(f2,18.76,40)
try: hi=brentq(f2,700,1e6); print("one report, normal effort: learns for B in (%.2f, %.0f)"%(lo,hi))
except ValueError: print("one report, normal effort: learns for B above %.2f; still positive at B=1e6 (%.2e)"%(lo,f2(1e6)))
