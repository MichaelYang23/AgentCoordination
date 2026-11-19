# Illustration: how the belief, the plan and the remaining value of information move along one sample path.
import numpy as np
from scipy.optimize import brentq
from agent_model import model
M_=model(); ne,nh,pi0=M_['ne'],M_['nh'],M_['pi0']
thL,thH,de,dh=0.5,8.0,0.25,4.0
B=100.0
def G(pi): return M_['solve'](pi,B,ne,nh)
def alloc(pi,lam,d):
    fp=lambda b: pi*thH*d/(b+thH*d)**2+(1-pi)*thL*d/(b+thL*d)**2-lam
    if fp(0)<=0: return 0.0
    return brentq(fp,0,1e4)
GH,GL=G(1.0)[0],G(0.0)[0]
def row(pi):
    g,lam=G(pi); be,bh=alloc(pi,lam,de),alloc(pi,lam,dh)
    assert abs(ne*be+nh*bh-B)<1e-3,(pi,ne*be+nh*bh)
    return be,bh,pi*GH+(1-pi)*GL-g
print("belief P(strict) -> tokens per easy task, per hard task, remaining value of knowing the standard")
for pi in [0.5,0.8,16/17,64/65,256/257,1024/1025,1.0]:
    be,bh,N=row(pi); print("  %.4f   %.2f  %.2f   %.3f"%(pi,be,bh,N))
print("\nsample path, true standard strict: F F P F F F F P, then a 9th")
odds=1.0
for i,r in enumerate("FFPFFFFP",1):
    odds*=4 if r=="F" else 0.25
    pi=odds/(1+odds); be,bh,N=row(pi)
    print("  after %d (%s): belief %.3f  plan %.2f/%.2f  remaining value %.3f"%(i,r,pi,be,bh,N))
for r,m in (("F",4),("P",.25)):
    o=odds*m; pi=o/(1+o); be,bh,N=row(pi); print("  9th = %s: belief %.3f  plan %.2f/%.2f  remaining value %.3f"%(r,pi,be,bh,N))
