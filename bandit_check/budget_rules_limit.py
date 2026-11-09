"""Large-horizon limit of the learning premium and of the two-team split under three budget rules.

A  paper's rule   every commitment spends the wallet in expectation under the agent's current belief.
                  Benchmark g0 = g(pi0; .); a team that learns the state earns G = pi0 g_H + (1 - pi0) g_L,
                  so the limit value is max{g0, G} (Proposition 1 at the baseline).
B  ex-ante rule   expected total spend <= B for every policy. Benchmark g0; learning teams earn the ex-ante
                  full-information value L (Proposition 3).
H  hard budget    realised spend <= B on every path. A team that knows the state earns G (it cannot move budget
                  across states). A constant bid that never adapts runs out of money early in the easy market:
                  W_hard(rho) = max_b sum_theta pi_theta min{q_theta(b), rho / b}.

Checks reported: G >= W_hard (information never hurts under a hard budget), W_hard <= g0 (the paper's benchmark
earns more than any non-adaptive bidder could under a hard budget, because it overspends in the easy market),
and L >= max{g0, G}. Two teams with v1/v2 = 2. Writes results/budget_rules_limit.txt.
"""
import math
import os
import sys

import numpy as np

from allocation import solve_allocation
from core import g_rate, pace_bid, qbar
from limit_theory import exante_full_info

HERE = os.path.dirname(os.path.abspath(__file__))
thL, pi0, v1, v2 = 0.5, 0.5, 2.0, 1.0


def w_hard(rho, thH):
    """max over constant bids of the fluid value when bidding stops once the budget is gone."""
    bL, bH = pace_bid(0.0, rho, thL, thH), pace_bid(1.0, rho, thL, thH)      # bids that exactly exhaust in each state
    h = lambda b: pi0 * min(b / (b + thH), rho / b) + (1 - pi0) * min(b / (b + thL), rho / b)
    cands = [bL, bH]
    den = math.sqrt(pi0 * thH) - math.sqrt((1 - pi0) * rho)                   # stationary point on [bL, bH]
    if den > 0:
        b = thH * math.sqrt((1 - pi0) * rho) / den
        if bL < b < bH:
            cands.append(b)
    return max(h(b) for b in cands)


def run(thH, out):
    grid = np.round(np.arange(0.0, 14.0 + 1e-9, 0.002), 6)
    gp = np.maximum(grid, 1e-12)
    g0 = np.array([g_rate(pi0, r, thL, thH) for r in gp])
    G = np.array([pi0 * g_rate(1.0, r, thL, thH) + (1 - pi0) * g_rate(0.0, r, thL, thH) for r in gp])
    L = exante_full_info(gp, thL, thH, pi0)
    Wh = np.array([w_hard(r, thH) for r in gp])
    for a in (g0, G, L, Wh):
        a[0] = 0.0
    b0 = pace_bid(pi0, 1.0, thL, thH)
    out.append("r = %g:  checks  G >= W_hard: %s   W_hard <= g0: %s   L >= max(g0, G): %s" % (
        thH / thL, bool(np.all(G >= Wh - 1e-9)), bool(np.all(Wh <= g0 + 1e-9)), bool(np.all(L >= np.maximum(g0, G) - 1e-9))))
    out.append("  at rho = 1 the paper's benchmark spends %.2f per period in the easy market and %.2f in the hard one"
               % (b0 * b0 / (b0 + thL), b0 * b0 / (b0 + thH)))
    out.append("  learning premium, %% of the benchmark value   rho:  " + "  ".join("%5.1f" % x for x in (0.2, 0.5, 1, 2.5, 5, 10)))
    worlds = (("A paper", g0, np.maximum(g0, G)), ("B ex-ante", g0, L), ("H hard", Wh, G))
    for name, W, V in worlds:
        idx = [int(np.argmin(np.abs(grid - x))) for x in (0.2, 0.5, 1, 2.5, 5, 10)]
        out.append("    %-10s                                      " % name + "  ".join("%5.2f" % (100 * (V[i] - W[i]) / W[i]) for i in idx))
    ts = np.round(np.arange(0.2, 12.0 + 1e-9, 0.02), 4)
    for name, W, V in worlds:
        sh, gain = [], []
        for t in ts:
            aE, aL = solve_allocation(grid, W, t, v1, v2), solve_allocation(grid, V, t, v1, v2)
            F = lambda a: v1 * np.interp(a, grid, V) + v2 * np.interp(t - a, grid, V)
            sh.append(aL - aE)
            gain.append((F(aL) - F(aE)) / F(aL))
        sh, gain = np.array(sh), np.array(gain)
        sg = np.where(np.abs(sh) < 0.002 * ts, 0, np.sign(sh))
        ch = [(float(ts[i]), int(sg[i - 1]), int(sg[i])) for i in range(1, ts.size) if sg[i] != sg[i - 1]]
        out.append("  %-10s two teams: sign changes of the shift (t, from, to) %s" % (name, ch[:6]))
        out.append("             shift / t at t = 0.6, 1, 2, 4, 8: %s ; gain from the learning-aware split: max %.3f%% of value"
                   % (" ".join("%+.3f" % (sh[int(np.argmin(np.abs(ts - x)))] / x) for x in (0.6, 1, 2, 4, 8)), 100 * gain.max()))


if __name__ == "__main__":
    out = ["Large-horizon limit under three budget rules (thL = 0.5, pi0 = 0.5, v1/v2 = 2); |shift| < 0.2% of t counted as 0"]
    for thH in (4.0, 8.0, 16.0, 32.0):
        run(thH, out)
        out.append("")
    txt = "\n".join(out)
    print(txt)
    with open(os.path.join(HERE, "results", "budget_rules_limit.txt"), "w") as f:
        f.write(txt + "\n")
