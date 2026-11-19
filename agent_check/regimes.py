# Agent-model analogue of the three bidding slides: sign of v1*R'(aE) - v2*R'(T-aE) at the benchmark split.
import numpy as np
from scipy.optimize import brentq
from agent_model import model
M=model(); ne,nh,pi0=M['ne'],M['nh'],M['pi0']; v1,v2=2.0,1.0
def Wp(B): return M['solve'](pi0,B,ne,nh)[1]
def Rp(B):
    W,wp=M['solve'](pi0,B,ne,nh); best=(0,W,wp)
    for tau in range(1,13):
        v,vb=M['Vb'](tau,B)
        if v>best[1]: best=(tau,v,vb)
    return best[2]-wp,best[0],best[1]-W
print("  T     aE      T-aE   tau*(1,2)   v1*R'(aE)    v2*R'(T-aE)   direction")
for T in (60,100,150,300,500,600,700,900):
    f=lambda a:v1*Wp(a)-v2*Wp(T-a)
    aE=brentq(f,T/2,T-1e-6) if f(T-1e-6)<0 else T
    r1,t1,_=Rp(aE); r2,t2,_=Rp(T-aE)
    d=v1*r1-v2*r2
    print("%4d  %7.2f %7.2f   (%d,%d)     %+.5f     %+.5f    %s"%(T,aE,T-aE,t1,t2,v1*r1,v2*r2,"more skewed" if d>0 else "less skewed"))
