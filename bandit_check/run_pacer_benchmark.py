"""Alternative benchmark: a no-learning agent that ALSO re-paces on its real wallet
(belief frozen at the prior).  Learning = Bayesian updating on top of the same
pacing rule.  Does learning still move the split in the same direction?"""
import os

import numpy as np

from core import W_curve
from bandits import belief_grid, ce_worldA
from agents import compute_curves
from allocation import solve_allocation
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")

thL, thH, pi0, K = 0.5, 8.0, 0.5, 100
Bmax, hb = 2000.0, 0.1
hl, J, m = belief_grid(thL, thH, pi0, target_h=0.05)
Nb = int(round(Bmax / hb)) + 1
grid = np.arange(Nb) * hb
learn, _ = ce_worldA(thL, thH, pi0, K, hb, Nb, hl, J, m, 0, True)
frozen, _ = ce_worldA(thL, thH, pi0, K, hb, Nb, hl, J, m, 0, False)
W = W_curve(np.maximum(grid, 1e-9), thL, thH, pi0, K)
W[0] = 0.0
pacer = frozen                                      # the benchmark is the frozen-belief pacer itself
learnS = np.maximum(learn, pacer)                   # planner may switch Bayesian updating off

R = learnS - pacer
print("premium of Bayesian updating over a wallet-pacing benchmark:")
for B in (20, 40, 60, 100, 150, 250, 400, 1000, 2000):
    i = int(round(B / hb)) if B < Bmax else Nb - 1
    print("  B=%5d  pacer-W=%+.3f  CE-pacer=%+.3f  (CE-W=%+.3f)" % (B, pacer[i] - W[i], learn[i] - pacer[i], learn[i] - W[i]))
pos = np.where(learn - pacer > 1e-4)[0]
print("Bayesian updating pays (vs pacer) from B =", grid[pos[0]] if pos.size else None)

C = compute_curves(thL, thH, pi0, K, 4000.0, h=0.1, hb=0.1, cache_dir=CACHE)
Ts = np.arange(20, 1990, 1.0)
rows = []
for T in Ts:
    aP = solve_allocation(grid, pacer, T, 2.0, 1.0)
    aL = solve_allocation(grid, learnS, T, 2.0, 1.0)
    aE = solve_allocation(C["grid"], C["W"], T, 2.0, 1.0)
    aX = solve_allocation(C["grid"], C["etc_smooth"], T, 2.0, 1.0)
    rows.append((T, aL - aP, aX - aE))
rows = np.array(rows)
tl = 0.1 + 0.001 * rows[:, 0]
s1 = np.sign(rows[:, 1]); s1[np.abs(rows[:, 1]) < tl] = 0
s2 = np.sign(rows[:, 2]); s2[np.abs(rows[:, 2]) < tl] = 0
print("\nshift (learning vs pacer benchmark) vs paper ETC shift (vs W):")
for T in (60, 84, 100, 150, 185, 200, 250, 300, 400, 600, 1000, 1500, 1900):
    i = int(np.argmin(np.abs(rows[:, 0] - T)))
    print("  T=%5d  Bayes-on-pacer %+7.3f   ETC %+7.3f" % (T, rows[i, 1], rows[i, 2]))
print("sign agreement over T in [20, 1990): %.3f, opposite %.3f" % (np.mean(s1 == s2), np.mean(s1 * s2 < 0)))
np.savetxt(os.path.join(RES, "pacer_benchmark_shift.csv"), rows, delimiter=",",
           header="T,shift_bayes_vs_pacer,shift_etc_vs_W", comments="", fmt="%.5g")

ps.setup()
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
ax = axes[0]
ax.plot(grid[10:], (learn - pacer)[10:], color=ps.COLORS["ce_A"], label="Bayesian updating vs frozen-belief pacer")
ax.plot(C["grid"][10:], (C["etc_smooth"] - C["W"])[10:], color=ps.COLORS["etc_smooth"], label="ETC vs W (paper)")
ps.zero_line(ax)
ax.set_xscale("log")
ax.set_xlabel("Team budget B")
ax.set_ylabel("Learning premium")
ax.set_title("Benchmark that also paces on its wallet")
ax.legend(loc="lower right", fontsize=8)
ax = axes[1]
ax.plot(rows[:, 0], rows[:, 1], color=ps.COLORS["ce_A"], label="Bayesian updating vs pacer")
ax.plot(rows[:, 0], rows[:, 2], color=ps.COLORS["etc_smooth"], label="ETC vs W (paper)")
ps.zero_line(ax)
ax.set_xlabel("Total budget T")
ax.set_ylabel("a − a^benchmark   (v1/v2 = 2)")
ax.set_title("Allocation shift")
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_pacer_benchmark.png"), dpi=170)
