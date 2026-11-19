# Narrow scan of the fee c around 0.2: peaks of the branches tau=7 and tau=6 and the budget at which they cross.
# Two local maxima occur when the crossing lies between the two peaks (Example 1 of agent_premium_shape.tex).
import numpy as np
from scipy.optimize import brentq
from scallop import analyse
for c in (0.200,0.205,0.210,0.215,0.220,0.225,0.230):
    M,Rt,peaks=analyse(c,taus=(6,7))
    P7,v7=peaks[7]; P6,v6=peaks[6]
    g=lambda B:Rt(7,B)[0]-Rt(6,B)[0]
    try: x=brentq(g,110.0,135.0,xtol=1e-10)
    except ValueError: x=np.nan
    tag="TWO LOCAL MAXIMA" if (P7<x<P6) else ""
    print("c=%.3f  P7=%.4f (R=%.6f)  P6=%.4f (R=%.6f)  branches cross at %.4f  R there=%.6f  %s"%(c,P7,v7,P6,v6,x,Rt(7,x)[0] if x==x else np.nan,tag))
