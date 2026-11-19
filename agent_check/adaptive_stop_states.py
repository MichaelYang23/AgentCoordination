# Stop-or-continue decision of the sequential stopping rule at B=100, state by state
# (pilots done, passes): belief, value if the team stops, value if it continues.
from functools import lru_cache
from agent_model import model
M_=model(); ne,nh,pi0,s=M_['ne'],M_['nh'],M_['pi0'],M_['s']
qL,qH=0.8,0.2; B=100.0; Tmax=24
def G(pi,B,me,mh): return M_['solve'](pi,B,me,mh)[0]
def post(t,w):
    a=pi0*qH**w*(1-qH)**(t-w); b=(1-pi0)*qL**w*(1-qL)**(t-w); return a/(a+b)
@lru_cache(None)
def U(t,w):
    p=post(t,w); stop=w+G(p,B-t*s,ne-t,nh)
    if t>=Tmax: return stop,stop,stop
    pp=p*qH+(1-p)*qL
    cont=pp*U(t+1,w+1)[0]+(1-pp)*U(t+1,w)[0]
    return max(stop,cont),stop,cont
print("state (pilots done, passes): belief P(strict), value if stop, value if continue, decision")
for t in range(0,9):
    for w in range(t+1):
        v,st,co=U(t,w)
        print("  t=%d w=%d  belief=%.3f  stop=%.3f  cont=%.3f  %s"%(t,w,post(t,w),st,co,"CONTINUE" if co>st+1e-12 else "stop"))
