# ETC (number of pilot tasks fixed in advance) versus sequential stopping (decide after each verdict).
# Same pilot tasks (easy, probe effort, cost s each), same 0/1 verdicts. Only the stopping rule differs.
import numpy as np
from functools import lru_cache
from agent_model import model
M_=model(); ne,nh,pi0,s=M_['ne'],M_['nh'],M_['pi0'],M_['s']
qL,qH=0.8,0.2
def G(pi,B,me,mh): return M_['solve'](pi,B,me,mh)[0]
def post(t,w):
    a=pi0*qH**w*(1-qH)**(t-w); b=(1-pi0)*qL**w*(1-qL)**(t-w); return a/(a+b)
def seq(B,Tmax=24):
    @lru_cache(None)
    def U(t,w):
        p=post(t,w); stop=w+G(p,B-t*s,ne-t,nh)
        if t>=Tmax or B-(t+1)*s<0: return stop,0.0
        pp=p*qH+(1-p)*qL
        cont=pp*U(t+1,w+1)[0]+(1-pp)*U(t+1,w)[0]
        return (cont,1.0) if cont>stop+1e-12 else (stop,0.0)
    # expected number of pilot tasks and distribution of the stopping time under the optimal rule
    dist={}
    def walk(t,w,pr):
        if U(t,w)[1]==0.0: dist[t]=dist.get(t,0)+pr; return
        p=post(t,w); pp=p*qH+(1-p)*qL
        walk(t+1,w+1,pr*pp); walk(t+1,w,pr*(1-pp))
    walk(0,0,1.0)
    return U(0,0)[0],dist
print("    B      W     ETC premium (tau*)   sequential premium   gain   E[pilots]  range of stopping times")
for B in [30,60,100,150,250,400]:
    W=G(pi0,B,ne,nh)
    e=max(((M_['Vb'](t,B)[0],t) for t in range(0,16)))
    v,dist=seq(B)
    En=sum(t*p for t,p in dist.items())
    print(" %5g %6.2f    %6.3f (%d)           %6.3f           %5.3f   %5.2f     %d..%d"%(B,W,e[0]-W,e[1],v-W,v-e[0],En,min(dist),max(dist)))
v,dist=seq(100.0)
print("\nB=100 stopping-time distribution:",{t:round(p,3) for t,p in sorted(dist.items()) if p>5e-4})
