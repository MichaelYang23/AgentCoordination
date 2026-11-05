"""Exact allocation for concave value functions in World B.

For the Bayes-optimal bandit and for W, V'(B) equals the Lagrange multiplier
lambda (envelope theorem; both are concave under the ex-ante constraint).
The planner's FOC v1 V'(a) = v2 V'(T-a) is then v1*lam1 = v2*lam2 = mu, so
  a(mu) = S(mu/v1),  T(mu) = S(mu/v1) + S(mu/v2)
traces the optimal allocation exactly, with no interpolation of V.
"""
import numpy as np

from core import qbar
from bandits import belief_grid, lag_sweep, myopic_bid

thL, thH, pi0, K = 0.5, 8.0, 0.5, 100
v1, v2 = 2.0, 1.0


def S_W(lam):
    b = np.array([myopic_bid(pi0, l, thL, thH) for l in lam])
    return K * b * np.array([qbar(pi0, x, thL, thH) for x in b])


hl, J, _ = belief_grid(thL, thH, pi0, target_h=0.02)
mus = np.exp(np.linspace(np.log(2e-3), np.log(30.0), 500))
lam1, lam2 = mus / v1, mus / v2
_, S1 = lag_sweep(thL, thH, pi0, K, lam1, hl, J, 2, 80)
_, S2 = lag_sweep(thL, thH, pi0, K, lam2, hl, J, 2, 80)
T_opt, a_opt = S1 + S2, S1
T_W, a_W = S_W(lam1) + S_W(lam2), S_W(lam1)
o1, o2 = np.argsort(T_opt), np.argsort(T_W)
print("monotone S(lambda)?", np.all(np.diff(S1[np.argsort(lam1)]) <= 1e-9))
print("   T    a^E      a^opt   shift (exact parametric)")
rows = []
for T in (40, 60, 84, 100, 150, 185, 200, 250, 275, 300, 400, 600, 1000, 2000):
    aE = np.interp(T, T_W[o2], a_W[o2])
    aO = np.interp(T, T_opt[o1], a_opt[o1])
    rows.append((T, aE, aO, aO - aE))
    print("%5d  %8.3f  %8.3f  %+.3f" % (T, aE, aO, aO - aE))

d = np.load("results/baseline_shifts.npz")
print("\ncompare with grid method (opt_B column of the baseline):")
for T, aE, aO, s in rows:
    i = int(np.argmin(np.abs(d["T"] - T)))
    print("T=%5d exact %+.3f   grid %+.3f" % (T, s, d["opt_B"][i]))
