"""Sanity checks and grid-convergence tests for bandits.py (baseline calibration)."""
import time

import numpy as np

from core import W_curve, Wprime_curve, etc_smooth_curve, etc_exact_curve
from bandits import (belief_grid, ce_worldA, lag_sweep, etc_exante_sweep, curve_to_grid, lam_targets)

thL, thH, pi0, K = 0.5, 8.0, 0.5, 100
Bchk = np.array([20.0, 57.0, 100.0, 150.0, 250.0, 400.0])
print("W at check points:", np.round(W_curve(Bchk, thL, thH, pi0, K), 4))

# ---------------- World B ----------------
hl, J, m = belief_grid(thL, thH, pi0, target_h=0.02)
print("belief grid hl=%.4f J=%d" % (hl, J))
t = time.time()
lams = np.exp(np.linspace(np.log(1e-4), np.log(20), 40))
N0, S0 = etc_exante_sweep(thL, thH, pi0, K, lams, 0)
Wp = W_curve(S0[:, 0], thL, thH, pi0, K)
print("ETC-exante tau=0 vs W: max |diff| = %.2e" % np.max(np.abs(N0[:, 0] - Wp)))
print("compile+run ETC exante %.1fs" % (time.time() - t))

for kind, name in [(0, "CE-myopic"), (1, "TS"), (2, "Bayes-optimal")]:
    t = time.time()
    N, S = lag_sweep(thL, thH, pi0, K, lams, hl, J, kind, 80)
    V = curve_to_grid(S, N, Bchk)
    print("%-14s V(B)-W(B) at %s = %s   (%.1fs)" % (name, Bchk, np.round(V - W_curve(Bchk, thL, thH, pi0, K), 4), time.time() - t))

# envelope check for the optimal policy: dV/dB == lambda
N, S = lag_sweep(thL, thH, pi0, K, lams, hl, J, 2, 80)
o = np.argsort(S)
dVdB = np.gradient(N[o], S[o])
print("Bayes-opt: lambda vs dN/dS (should match):")
for i in range(5, 40, 6):
    print("   S=%8.2f lam=%.5f  dN/dS=%.5f" % (S[o][i], lams[o][i], dVdB[i]))

# belief-grid convergence for the optimal policy
for tgt in [0.04, 0.02, 0.01]:
    hl2, J2, _ = belief_grid(thL, thH, pi0, target_h=tgt)
    N2, S2 = lag_sweep(thL, thH, pi0, K, lams, hl2, J2, 2, 80)
    print("hl=%.4f  V_opt-W at %s = %s" % (hl2, Bchk, np.round(curve_to_grid(S2, N2, Bchk) - W_curve(Bchk, thL, thH, pi0, K), 5)))

# ---------------- World A: CE with real wallet ----------------
for hb, tgt in [(0.2, 0.1), (0.1, 0.05), (0.05, 0.05), (0.1, 0.025)]:
    hlA, JA, mA = belief_grid(thL, thH, pi0, target_h=tgt)
    Bmax = 420.0
    Nb = int(round(Bmax / hb)) + 1
    t = time.time()
    V, hyb = ce_worldA(thL, thH, pi0, K, hb, Nb, hlA, JA, mA, 20, True)
    grid = np.arange(Nb) * hb
    Vc = np.interp(Bchk, grid, V)
    hy = np.nanmax(hyb, axis=0)
    Hc = np.interp(Bchk, grid, hy)
    print("hb=%.2f hl=%.4f: CE-W = %s | best(probe+CE)-W = %s  (%.1fs)" % (
        hb, hlA, np.round(Vc - W_curve(Bchk, thL, thH, pi0, K), 4), np.round(Hc - W_curve(Bchk, thL, thH, pi0, K), 4), time.time() - t))

# variance cost of re-pacing on a real wallet without learning
hlA, JA, mA = belief_grid(thL, thH, pi0, target_h=0.05)
Nb = int(round(420 / 0.1)) + 1
V0, _ = ce_worldA(thL, thH, pi0, K, 0.1, Nb, hlA, JA, mA, 0, False)
print("re-pacing on wallet, belief frozen at prior, minus W:", np.round(np.interp(Bchk, np.arange(Nb) * 0.1, V0) - W_curve(Bchk, thL, thH, pi0, K), 4))
