"""How much is at stake in the split, and what does planning with the decomposition cost?

Two teams, v1/v2 = 2, pi0 = 0.5. Ex-ante budget rule: teams are full bandits (Bayes-optimal DP, key opt_B);
the planner splits the budget using (i) the full-bandit value function, (ii) the no-learning value function W,
(iii) the decomposition's value function (etc_B). Reported as the maximum over total budgets T in [0.4K, 10K]:
  - the full bandit's learning premium, % of W (single team);
  - the gain from a learning-aware split over the learning-blind split, % of total value;
  - the loss from planning with the decomposition model when teams are full bandits, % of total value and
    % of the total gain from learning.
Also the paper's rule at K = 100 (teams = the paper's smoothed ETC): gain from the learning-aware split against
what learning itself adds. Reads the caches of run_baseline.py, run_sweep.py and run_dp_largeK.py.
Writes results/decision_stakes.txt.
"""
import glob
import os

import numpy as np

from allocation import objective, solve_allocation

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "results", "cache")
v1, v2 = 2.0, 1.0


def load(thH, K):
    for pat in ("v2_thL0.5_thH%d_pi0.5_K%d_B*_h0.1_hb0.1_hlB0.04.npz", "dp_thL0.5_thH%d_pi0.5_K%d_B*_h0.1_hlB0.04.npz"):
        f = glob.glob(os.path.join(CACHE, pat % (thH, K)))
        if f:
            return dict(np.load(f[0]))
    return None


def main():
    out = ["Ex-ante budget rule, teams = full bandit (DP), v1/v2 = 2, pi0 = 0.5; maxima over T in [0.4K, 10K]",
           " r    K | premium, % of W | gain: learning-aware vs learning-blind split, % of value |"
           " loss from planning with the decomposition: % of value (% of the gain from learning)"]
    for thH in (4, 8, 16):
        for K in (50, 100, 200, 400):
            C = load(thH, K)
            if C is None:
                continue
            gg, W, FB, D = C["grid"][::10], C["W"][::10], C["opt_B"][::10], C["etc_B"][::10]
            prem = np.max((FB[1:] - W[1:]) / W[1:])
            g_split, loss, loss_rel = [], [], []
            for T in np.arange(0.4 * K, 10.0 * K + 1e-9, K / 10.0):
                aE, aF, aD = (solve_allocation(gg, X, T, v1, v2) for X in (W, FB, D))
                F = lambda a: objective(gg, FB, T, v1, v2, a)
                FW = objective(gg, W, T, v1, v2, aE)
                g_split.append((F(aF) - F(aE)) / F(aF))
                loss.append((F(aF) - F(aD)) / F(aF))
                loss_rel.append((F(aF) - F(aD)) / max(F(aF) - FW, 1e-12))
            out.append("%2d  %4d | %5.2f | %6.3f | %6.3f (%.1f)" % (2 * thH, K, 100 * prem, 100 * max(g_split),
                                                                 100 * max(loss), 100 * max(loss_rel)))
    f = glob.glob(os.path.join(CACHE, "v2_thL0.5_thH8_pi0.5_K100_B4000_h0.1_hb0.1_hlB0.02.npz"))
    if f:
        C = dict(np.load(f[0]))
        g, W = C["grid"], C["W"]
        out.append("\nK = 100 baseline: budget from which learning pays, and the peak premium")
        for key in ("etc_smooth", "etc_exact", "ce_A", "etc_B", "opt_B"):
            p = C[key] - W
            pos = np.where(p > 1e-3)[0]
            i = int(np.argmax(p))
            out.append("  %-10s premium > 0.001 from B = %5.1f ; peak %.2f at B = %4.0f (%.1f%% of W)"
                       % (key, g[pos[0]], p[i], g[i], 100 * p[i] / W[i]))
        gg, Wc, E = g[::10], W[::10], C["etc_smooth"][::10]
        out.append("\nPaper's rule, K = 100, teams = the paper's smoothed ETC")
        for T in (100, 150, 250, 400, 1000):
            aE, aL = solve_allocation(gg, Wc, T, v1, v2), solve_allocation(gg, E, T, v1, v2)
            F = lambda a: objective(gg, E, T, v1, v2, a)
            out.append("  T = %4d  shift %+5.1f  learning-aware split adds %.3f%% of value ; learning itself adds %.2f%%"
                       % (T, aL - aE, 100 * (F(aL) - F(aE)) / F(aL),
                          100 * (F(aL) - objective(gg, Wc, T, v1, v2, aE)) / F(aL)))
    txt = "\n".join(out)
    print(txt)
    with open(os.path.join(HERE, "results", "decision_stakes.txt"), "w") as fh:
        fh.write(txt + "\n")


if __name__ == "__main__":
    main()
