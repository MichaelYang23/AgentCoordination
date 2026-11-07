"""Do the decomposition and the full bandit (DP) converge as the horizon K grows?

Both under the ex-ante budget rule, pi0 = 0.5, r = 8, 16, 32 (thH = 4, 8, 16), K = 50, 100, 200, 400.
Top row: per-period value of learning (V - W)/K against rho = B/K. Bottom row: per-period allocation shift
(a - a^E)/K against t = T/K (v1/v2 = 2). Dashed: the K -> infinity limit (state known from the start,
ex-ante rule), which both must approach. Reads the caches of run_sweep.py and run_dp_largeK.py.
Writes results/fig_dp_convergence.png and results/dp_convergence_summary.txt.
"""
import glob
import os
import re

import numpy as np

from allocation import solve_allocation
from core import W_curve
from limit_theory import exante_full_info
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")
THL, PI0, V1, V2 = 0.5, 0.5, 2.0, 1.0
THH = [4, 8, 16]
KS = [50, 100, 200, 400]
BLUES = {50: "#86b6ef", 100: "#3987e5", 200: "#256abf", 400: "#104281"}      # decomposition, light -> dark
ORANGE = {50: "#f5b08f", 100: "#eb6834", 200: "#c4511f", 400: "#8f3a15"}     # full bandit, light -> dark


def load(thH, K):
    for pat in ("v2_thL0.5_thH%d_pi0.5_K%d_B*_h0.1_hb0.1_hlB0.04.npz", "dp_thL0.5_thH%d_pi0.5_K%d_B*_h0.1_hlB0.04.npz"):
        f = glob.glob(os.path.join(CACHE, pat % (thH, K)))
        if f:
            C = dict(np.load(f[0]))
            for prefix in ("shift", "dpshift"):
                g = os.path.join(CACHE, "%s_thH%d_pi0.5_K%d_v2.npz" % (prefix, thH, K))
                if os.path.exists(g):
                    return C, dict(np.load(g))
    return None, None


def switches(t, s, tol):
    sg = np.where(np.abs(s) < tol, 0, np.sign(s))
    return [(round(float(t[i]), 2), int(sg[i - 1]), int(sg[i])) for i in range(1, t.size) if sg[i] != sg[i - 1]]


def first_balanced(t, s, tol):
    """First t at which the shift is negative after having been positive."""
    sg = np.where(np.abs(s) < tol, 0, np.sign(s))
    pos = np.where(sg > 0)[0]
    if pos.size == 0:
        return None
    neg = np.where((sg < 0) & (np.arange(sg.size) > pos[0]))[0]
    return round(float(t[neg[0]]), 2) if neg.size else None


def main():
    ps.setup()
    fig, axes = plt.subplots(2, len(THH), figsize=(15, 7.6))
    lines = ["Decomposition vs full bandit (DP), ex-ante budget rule, pi0 = 0.5, v1/v2 = 2"]
    grid = np.round(np.arange(0, 12.0 + 1e-9, 0.002), 6)
    ts = np.round(np.arange(0.2, 12.0 + 1e-9, 0.01), 4)
    for j, thH in enumerate(THH):
        r = int(thH / THL)
        L = exante_full_info(grid, THL, thH, PI0)
        Wl = W_curve(np.maximum(grid, 1e-12), THL, thH, PI0, 1)
        Wl[0] = 0.0
        lim_sh = np.array([solve_allocation(grid, L, t, V1, V2) - solve_allocation(grid, Wl, t, V1, V2) for t in ts])
        lim_sw = first_balanced(ts, lim_sh, 1e-4 + 0.001 * ts)
        axv, axs = axes[0, j], axes[1, j]
        m = (grid >= 0.05) & (grid <= 10)
        axv.plot(grid[m], (L - Wl)[m], color=ps.INK, lw=1.6, ls=(0, (4, 2)), label="limit K → ∞", zorder=5)
        axs.plot(ts, lim_sh, color=ps.INK, lw=1.6, ls=(0, (4, 2)), zorder=5)
        lines.append("\nr = %d   limit (K -> inf): switch to 'more balanced' at t = %s" % (r, lim_sw))
        for K in KS:
            C, S = load(thH, K)
            if C is None:
                continue
            g = C["grid"]
            rho = g / K
            mm = (rho >= 0.05) & (rho <= 10)   # edge artifact of the decomposition beyond ~11
            for key, col, lab in (("etc_B", BLUES[K], "decomposition"), ("opt_B", ORANGE[K], "full bandit (DP)")):
                axv.plot(rho[mm], ((C[key] - C["W"]) / K)[mm], color=col, lw=1.4,
                         label="%s, K = %d" % (lab, K))
                tt = S["T"] / K
                axs.plot(tt, S[key] / K, color=col, lw=1.2)
            tol = 0.1 + 0.001 * S["T"]
            sw_d, sw_f = first_balanced(S["T"] / K, S["etc_B"], tol), first_balanced(S["T"] / K, S["opt_B"], tol)
            at = {}
            for x in (1.0, 2.5, 5.0, 10.0):
                i = int(np.argmin(np.abs(rho - x)))
                at[x] = ((C["etc_B"][i] - C["W"][i]) / K, (C["opt_B"][i] - C["W"][i]) / K)
            il = {x: int(np.argmin(np.abs(grid - x))) for x in at}
            lines.append("  K=%3d  switch t: decomposition %s, full bandit %s  |  per-period value of learning "
                         "(dec / full bandit / limit) at rho=1: %.4f/%.4f/%.4f  2.5: %.4f/%.4f/%.4f  "
                         "5: %.4f/%.4f/%.4f  10: %.4f/%.4f/%.4f"
                         % ((K, sw_d, sw_f) + tuple(v for x in at for v in (at[x][0], at[x][1],
                                                                            (L - Wl)[il[x]]))))
        axv.set_xscale("log")
        axv.set_xlim(0.05, 10)
        ps.zero_line(axv)
        axv.set_title("r = %d" % r, loc="left")
        axv.set_xlabel("Team budget per period ρ = B/K (log)")
        axs.set_xscale("log")
        axs.set_xlim(0.2, 12)
        ps.zero_line(axs)
        axs.set_xlabel("Total budget per period t = T/K (log)")
    axes[0, 0].set_ylabel("Value of learning per period (V − W)/K")
    axes[1, 0].set_ylabel("Senior budget shift per period (a − a^E)/K")
    h, lab = axes[0, 1].get_legend_handles_labels()
    order = [0] + [1 + 2 * i for i in range(len(KS))] + [2 + 2 * i for i in range(len(KS))]
    fig.legend([h[i] for i in order if i < len(h)], [lab[i] for i in order if i < len(lab)], loc="upper center",
               ncol=5, fontsize=8.5, bbox_to_anchor=(0.5, 1.0))
    fig.text(0.5, 0.004, "π0 = 0.5, θ_L = 0.5, v1/v2 = 2. Both under the ex-ante budget rule. Blue: decomposition "
             "(learn τ at b^I, then a w-contingent bid); orange: full bandit by dynamic programming; dashed: K → ∞.",
             ha="center", va="bottom", fontsize=8, color=ps.MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.88))
    fig.savefig(os.path.join(RES, "fig_dp_convergence.png"), dpi=170)
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(RES, "dp_convergence_summary.txt"), "w") as f:
        f.write(txt + "\n")
    print("-> results/fig_dp_convergence.png")


if __name__ == "__main__":
    main()
