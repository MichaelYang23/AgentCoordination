"""Reproduce numbers reported in the slides / paper to validate core.py."""
import numpy as np

from core import (W_curve, etc_exact_tau_values, etc_exact_curve, etc_smooth_curve,
                  etc_adaptive_curve, Wprime_curve)
from allocation import solve_allocation

thL, thH, pi0, K = 0.5, 8.0, 0.5, 100

print("--- B = 57 (slide 'A short experiment can lose value') ---")
v = etc_exact_tau_values(57.0, thL, thH, pi0, K)
print("W(57)        = %.5f   (slide: 43.30105)" % W_curve(np.array([57.0]), thL, thH, pi0, K)[0])
print("V(tau=0)     = %.5f" % v[0])
print("V(tau=1)     = %.5f   (slide: 43.28944)" % v[1])
print("V(tau=2)     = %.5f   (slide: 43.32796)" % v[2])
print("argmax tau   =", int(np.argmax(v)), " tau_max =", len(v) - 1, "(slide: 28)")

Bs = np.arange(1.0, 3001.0, 1.0)
W = W_curve(Bs, thL, thH, pi0, K)
Vx, tx = etc_exact_curve(Bs, thL, thH, pi0, K)
R = Vx - W
learn = np.where(tx > 0)[0]
print("\n--- exact ETC ---")
print("B1 (first B with tau*>0) =", Bs[learn[0]], " tau there =", tx[learn[0]], "(paper: 56, jumps to 2)")
print("B2 (last B with tau*>0)  =", Bs[learn[-1]], "(paper: ~2300)")
print("max premium = %.3f at B = %g (paper: ~1.9 at ~224)" % (R.max(), Bs[np.argmax(R)]))
print("max tau* = %g at B = %g (paper: 10 around 150)" % (tx.max(), Bs[np.argmax(tx)]))

print("\n--- smoothed ETC ---")
Bf = np.arange(0.5, 3000.0, 0.5)
Wf = W_curve(Bf, thL, thH, pi0, K)
Vs, ts = etc_smooth_curve(Bf, thL, thH, pi0, K)
Rs = Vs - Wf
ls = np.where(ts > 0)[0]
print("B1 =", Bf[ls[0]], " tau at entry = %.2f (paper: 59, 4.7)" % ts[ls[0]])
print("B2 =", Bf[ls[-1]], "(paper: 2683)")
print("max premium = %.3f at B = %g" % (Rs.max(), Bf[np.argmax(Rs)]))
Vp = np.gradient(Vs, Bf)
Wp = Wprime_curve(Bf, thL, thH, pi0, K)
ratio = Vp / Wp
inside = (Bf > Bf[ls[0]] + 1) & (Bf < Bf[ls[-1]] - 1)
print("peak ratio V'/W' = %.3f (paper 1.22)" % ratio[inside].max())
# Bhat: first B above B1 where ratio <= 1
idx = np.where(inside & (ratio <= 1.0))[0]
print("Bhat = %g (paper ~256)" % Bf[idx[0]])
print("tau* peak at B = %g (paper ~123)" % Bf[np.argmax(ts)])
mn = np.argmin(np.where(inside, ratio, 9))
print("ratio minimum %.3f at B = %g (paper 0.89 at ~990)" % (ratio[mn], Bf[mn]))

print("\n--- allocation with smoothed ETC, v1/v2 = 2 (slides summary-table.csv) ---")
grid = np.arange(0.0, 1500.0001, 0.05)
Wg = W_curve(np.maximum(grid, 1e-9), thL, thH, pi0, K)
Vg, _ = etc_smooth_curve(np.maximum(grid, 1e-9), thL, thH, pi0, K)
for T, aE_ref, aL_ref in [(150, 101.5743, 106.4313), (184, 124.4836, 129.1553), (185, 125.1580, 121.7490),
                          (200, 135.2764, 131.3001), (250, 169.0152, 163.2889), (400, 269.8063, 260.3311)]:
    aE = solve_allocation(grid, Wg, T, 2.0, 1.0)
    aL = solve_allocation(grid, Vg, T, 2.0, 1.0)
    print("T=%4d  aE=%.3f (ref %.3f)  aL=%.3f (ref %.3f)  shift=%+.3f" % (T, aE, aE_ref, aL, aL_ref, aL - aE))

print("\n--- adaptive-stopping ETC (draft/DP.tex) ---")
Va, Ea = etc_adaptive_curve(Bs[:600], thL, thH, pi0, K)
Ra = Va - W[:600]
la = np.where(Ra > 1e-10)[0]
print("first B with positive premium =", Bs[la[0]], "(DP draft: threshold 47/48)")
print("max premium = %.3f at B = %g (DP draft: 2.13 at 250)" % (Ra.max(), Bs[np.argmax(Ra)]))
