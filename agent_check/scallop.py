# Search over the evaluation fee c for a value at which the exact premium has two local maxima
# (a change of tau* between two branch peaks). Prints the peak of each branch for each c.
import numpy as np
from scipy.optimize import brentq
from agent_model import model

def analyse(c, taus=(5,6,7,8,9), lo=95.0, hi=165.0):
    M=model(c=c); ne,nh,pi0=M['ne'],M['nh'],M['pi0']
    def Rt(tau,B):
        v,vb=M['Vb'](tau,B); W,Wp=M['solve'](pi0,B,ne,nh); return v-W, vb-Wp
    peaks={}
    for tau in taus:
        f=lambda B:Rt(tau,B)[1]
        if f(lo)>0 and f(hi)<0:
            P=brentq(f,lo,hi,xtol=1e-10); peaks[tau]=(P,Rt(tau,P)[0])
    return M,Rt,peaks

if __name__=="__main__":
    for c in np.arange(0.20,0.81,0.04):
        M,Rt,peaks=analyse(c)
        best=max(peaks,key=lambda t:peaks[t][1])
        s="c=%.2f  "%c+"  ".join("tau=%d: peak at %.3f value %.6f"%(t,peaks[t][0],peaks[t][1]) for t in sorted(peaks))
        print(s,"| best tau",best)
