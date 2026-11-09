"""n teams: who gains budget when the teams can learn? (Proposition 5)

Large-K limit under the paper's budget rule (baseline, where the limit premium is max{VPI, 0}): the per-period
value of a team is L = max{g0, G} with g0 = g(pi0; .) (no learning) and G = pi0 g(1; .) + (1 - pi0) g(0; .)
(state known). Both are strictly concave, so for every assignment of modes (learn / not) the planner's problem is
concave; enumerating the 2^n assignments gives the exact optimum. Proposition 5(c): team i gains budget iff
R_i > kappa, with R_i = (mode derivative / g0')(benchmark budget) and kappa = lambda_L / lambda_E.
Finite K = 100 (paper's smoothed ETC, slides version): exact optimum on a 0.5 grid by max-plus convolution.
Writes results/n_teams_summary.txt and results/fig_n_teams.png.
"""
import itertools
import os

import numpy as np

from core import g_rate, g_rate_prime
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
thL, thH, pi0 = 0.5, 8.0, 0.5
V = np.array([3.0, 2.0, 1.0])                      # senior -> junior
TEAM_COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]

# ------------------------------------------------------------------ limit objects on a fine grid
RHO = np.concatenate(([1e-6], np.geomspace(1e-4, 40.0, 6000)))
g0 = np.array([g_rate(pi0, r, thL, thH) for r in RHO])
G = np.array([pi0 * g_rate(1.0, r, thL, thH) + (1 - pi0) * g_rate(0.0, r, thL, thH) for r in RHO])
d0 = np.array([g_rate_prime(pi0, r, thL, thH) for r in RHO])
dG = np.array([pi0 * g_rate_prime(1.0, r, thL, thH) + (1 - pi0) * g_rate_prime(0.0, r, thL, thH) for r in RHO])
RHO1 = float(RHO[np.where(G > g0)[0][0]])
VAL = {0: g0, 1: G}
DER = {0: d0, 1: dG}


def alloc_at(lam, modes):
    """alpha_i solving v_i * mode_i'(alpha_i) = lam (derivatives are strictly decreasing)."""
    out = np.empty(len(modes))
    for i, m in enumerate(modes):
        target = lam / V[i]
        out[i] = np.interp(-target, -DER[m], RHO)          # -DER is increasing in rho
    return out


def solve(t, modes):
    lo, hi = 1e-6, 1e6
    for _ in range(200):
        lam = np.sqrt(lo * hi)
        if alloc_at(lam, modes).sum() > t:
            lo = lam
        else:
            hi = lam
    lam = np.sqrt(lo * hi)
    a = alloc_at(lam, modes)
    val = sum(V[i] * np.interp(a[i], RHO, VAL[m]) for i, m in enumerate(modes))
    return a, lam, val


def limit_problem(t):
    aE, lamE, _ = solve(t, (0,) * len(V))
    best = None
    for modes in itertools.product((0, 1), repeat=len(V)):
        a, lam, val = solve(t, modes)
        if best is None or val > best[2] + 1e-12:
            best = (a, lam, val, modes)
    aL, lamL, _, modes = best
    learners = tuple(int(x > RHO1) for x in aL)
    R = np.array([np.interp(aE[i], RHO, DER[m] / d0) for i, m in enumerate(modes)])
    return aE, aL, lamE, lamL, modes, learners, R


def finite_K_problem(Vc, grid, T):
    """Exact 3-team optimum on the grid by max-plus convolution: H2(s) = max v1 V(a1) + v2 V(s - a1)."""
    n = int(round(T / (grid[1] - grid[0])))
    f1, f2, f3 = V[0] * Vc[: n + 1], V[1] * Vc[: n + 1], V[2] * Vc[: n + 1]
    H2 = np.empty(n + 1)
    A1 = np.empty(n + 1, dtype=int)
    for s in range(n + 1):
        vals = f1[: s + 1] + f2[s::-1]
        k = int(np.argmax(vals))
        H2[s], A1[s] = vals[k], k
    tot = f3[: n + 1] + H2[n::-1]
    k3 = int(np.argmax(tot))
    s = n - k3
    k1 = A1[s]
    k2 = s - k1
    return np.array([k1, k2, k3]) * (grid[1] - grid[0])


def robustness():
    """Other value vectors and four teams (limit): sign-rule violations and whether the marginal learner loses."""
    global V
    out = ["\nRobustness (limit): sign-rule violations; does the marginal learner ever lose budget?;"
           " share of t with non-learners losing (kappa > 1) / with some higher learner losing"]
    keepV = V.copy()
    for vv in ((3.0, 2.0, 1.0), (4.0, 2.0, 1.0), (2.0, 1.5, 1.0), (1.5, 1.2, 1.0), (4.0, 3.0, 2.0, 1.0)):
        V = np.array(vv)
        viol = mlose = nl_lose = hl_lose = cnt = 0
        for t in np.round(np.arange(0.3, 12.0001, 0.02), 4):
            aE, aL, lamE, lamL, modes, learners, R = limit_problem(t)
            kappa = lamL / lamE
            d = aL - aE
            for i in range(len(V)):
                if abs(d[i]) > 1e-6 and np.sign(d[i]) != np.sign(R[i] - kappa):
                    viol += 1
            k = sum(learners)
            if k > 0:
                cnt += 1
                if d[k - 1] < -1e-6:
                    mlose += 1
                if k < len(V) and np.any(d[k:] < -1e-6):
                    nl_lose += 1
                if k > 1 and np.any(d[: k - 1] < -1e-6):
                    hl_lose += 1
        out.append("  v=%s: violations %d; marginal learner loses at %d of %d t with learners; non-learners lose"
                   " %.0f%%; a higher learner loses %.0f%%" % (vv, viol, mlose, cnt, 100 * nl_lose / max(cnt, 1),
                                                              100 * hl_lose / max(cnt, 1)))
    V = keepV
    return out


def main():
    lines = ["n = 3 teams, v = (3, 2, 1). Limit K -> inf, paper's budget rule, baseline (thL=0.5, thH=8, pi0=0.5);"
             " learning threshold rho1 = %.3f per period" % RHO1]
    ts = np.round(np.arange(0.3, 10.0001, 0.01), 4)
    res = [limit_problem(t) for t in ts]
    shifts = np.array([r[1] - r[0] for r in res])
    nlearn = np.array([sum(r[5]) for r in res])
    # check Proposition 5(c): sign(shift_i) = sign(R_i - kappa)
    bad = 0
    for t, (aE, aL, lamE, lamL, modes, learners, R) in zip(ts, res):
        kappa = lamL / lamE
        for i in range(len(V)):
            d = aL[i] - aE[i]
            if abs(d) > 1e-6 and np.sign(d) != np.sign(R[i] - kappa):
                bad += 1
        assert all(m == l for m, l in zip(modes, learners)), (t, modes, learners)
    lines.append("check 5(c) sign rule on %d t-values x 3 teams: %d violations" % (ts.size, bad))
    lines.append("modes agree with 'budget above rho1' at every t; learners always the top-k teams: %s"
                 % all(list(r[5]) == sorted(r[5], reverse=True) for r in res))
    for t in (0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
        i = int(np.argmin(np.abs(ts - t)))
        aE, aL, lamE, lamL, modes, learners, R = res[i]
        lines.append("  t=%.2f  learners %s  no learning %s -> learning %s  shift %s  R %s  kappa %.4f"
                     % (ts[i], learners, np.round(aE, 3), np.round(aL, 3), np.round(aL - aE, 3), np.round(R, 3),
                        lamL / lamE))
    # regimes
    for k in (1, 2, 3):
        sel = nlearn == k
        if sel.any():
            lines.append("  %d learner(s) for t in [%.2f, %.2f]" % (k, ts[sel].min(), ts[sel].max()))

    # ------------------------------------------------------------------ finite K = 100, smoothed ETC
    c = np.load(os.path.join(RES, "cache", "v2_thL0.5_thH8_pi0.5_K100_B4000_h0.1_hb0.1_hlB0.02.npz"))
    step = 5                                          # 0.5 budget units
    grid = c["grid"][::step]
    W, E = c["W"][::step], c["etc_smooth"][::step]
    lines.append("\nFinite K = 100, paper's smoothed ETC (slides), exact optimum on a 0.5 grid:")
    Ts = np.arange(30.0, 1000.0 + 1e-9, 5.0)
    fin = []
    for T in Ts:
        aE = finite_K_problem(W, grid, T)
        aL = finite_K_problem(E, grid, T)
        fin.append((aE, aL))
    for T in (150, 300, 500):
        i = int(np.argmin(np.abs(Ts - T)))
        aE, aL = fin[i]
        lines.append("  T=%d  no learning %s -> learning %s  shift %s" % (T, aE, aL, aL - aE))
    fshift = np.array([b - a for a, b in fin])

    lines += robustness()

    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(RES, "n_teams_summary.txt"), "w") as f:
        f.write(txt + "\n")

    # ------------------------------------------------------------------ figure
    ps.setup()
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4))
    ax = axes[0]
    shade = {1: "#eef4fc", 2: "#e1ecfa", 3: "#d2e3f8"}
    for k in (1, 2, 3):
        sel = nlearn == k
        if sel.any():
            ax.axvspan(ts[sel].min(), ts[sel].max(), color=shade[k], lw=0, zorder=0)
            ax.text(np.sqrt(ts[sel].min() * ts[sel].max()), 0.97, "%d learner%s" % (k, "" if k == 1 else "s"),
                    transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=8, color=ps.INK2)
    labels = ["team 1 (v = 3)", "team 2 (v = 2)", "team 3 (v = 1)"]
    for i in range(3):
        ax.plot(ts, shifts[:, i], color=TEAM_COLORS[i], lw=1.8, label=labels[i])
    ps.zero_line(ax)
    ax.set_xscale("log")
    ax.set_xlim(ts[0], ts[-1])
    ax.set_xlabel("Total budget per period t = T/K (log)")
    ax.set_ylabel("Budget shift per period  α^L − α^E")
    ax.set_title("Limit K → ∞ (Proposition 5)", loc="left")
    ax.legend(loc="lower left", fontsize=8.5)
    ax = axes[1]
    for i in range(3):
        ax.plot(Ts, fshift[:, i], color=TEAM_COLORS[i], lw=1.4, label=labels[i])
    ps.zero_line(ax)
    ax.set_xscale("log")
    ax.set_xlim(Ts[0], Ts[-1])
    ax.set_xlabel("Total budget T (log), K = 100")
    ax.set_ylabel("Budget shift  a^L − a^E")
    ax.set_title("Paper's model, K = 100 (smoothed ETC)", loc="left")
    fig.text(0.5, 0.005, "θ_L = 0.5, θ_H = 8, π0 = 0.5; three teams with values 3 : 2 : 1. Shaded (left): number of "
             "teams that learn at the optimum.", ha="center", va="bottom", fontsize=8, color=ps.MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(RES, "fig_n_teams.png"), dpi=170)
    print("-> results/fig_n_teams.png")


if __name__ == "__main__":
    main()
