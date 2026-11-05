"""Does letting the planner choose the probing bid (not just tau) bring ETC
closer to the learn-while-doing agent?  Same model, same accounting (World A)."""
import os
import sys

import numpy as np

from core import W_curve, etc_optbid_curve
from analysis import shifts
from agents import compute_curves
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")
KEYS = ["etc_exact", "etc_smooth", "etc_adapt", "ce_A", "probe_ce_A", "opt_B", "ts_B", "etc_B"]

configs = [(2.0, 0.5, 100), (4.0, 0.5, 100), (8.0, 0.5, 100), (16.0, 0.5, 100)]
if len(sys.argv) > 1:
    configs = [c for c in configs if "%g" % c[0] in sys.argv[1:]]

rows = []
curves = {}
for thH, pi0, K in configs:
    Bmax = 12.0 * K * max(1.0, (thH / 8.0) ** 0.5)
    C = compute_curves(0.5, thH, pi0, K, Bmax, h=0.1, hb=0.1, which=KEYS, verbose=False, cache_dir=CACHE,
                       hl_B=0.04, nbg=48, n_fine=300)
    grid = C["grid"]
    bI = np.sqrt(0.5 * thH)
    bids = bI * np.geomspace(0.25, 12.0, 28)
    Bs = np.arange(0.5, Bmax + 0.25, 0.5)
    V, tau, bp = etc_optbid_curve(Bs, bids, 0.5, thH, pi0, K, 60)
    v = np.interp(grid, np.concatenate(([0.0], Bs)), np.concatenate(([0.0], V)))
    C["etc_optbid"] = np.maximum(v, C["W"])
    curves[thH] = (C, Bs, tau, bp)
    Ts = np.arange(0.2 * K, Bmax + 1e-9, K / 100.0)
    S = shifts(C, ["etc_smooth", "etc_exact", "etc_optbid", "ce_A"], Ts, 2.0, 1.0)
    tl = 0.1 + 0.001 * Ts

    def sg(x):
        s = np.sign(x)
        s[np.abs(x) < tl] = 0
        return s
    for ref in ("etc_exact", "etc_optbid"):
        a, b = sg(S[ref]), sg(S["ce_A"])
        rows.append((thH, ref, float(np.mean(a == b)), float(np.mean(a * b < 0))))
    R = {k: C[k] - C["W"] for k in ("etc_exact", "etc_optbid", "ce_A")}
    print("thH=%g: premium max  ETC(b^I) %.3f@%.0f | ETC(opt bid) %.3f@%.0f | CE %.3f@%.0f" % (
        thH, *[x for k in ("etc_exact", "etc_optbid", "ce_A") for x in (R[k].max(), grid[np.argmax(R[k])])]))
    for B in (60, 100, 200, 400, 800):
        i = int(np.argmin(np.abs(Bs - B)))
        print("     B=%4d  ETC(opt bid): tau=%2d  bid=%.2f (b^I=%.2f)   premium %.3f vs CE %.3f vs ETC(b^I) %.3f" % (
            B, tau[i], bp[i], bI, np.interp(B, grid, R["etc_optbid"]), np.interp(B, grid, R["ce_A"]),
            np.interp(B, grid, R["etc_exact"])))
print("\nsign agreement with learn-while-doing CE (World A), v1/v2=2, all T in [0.2K, Bmax]:")
for thH, ref, ag, op in rows:
    print("  r=%4g  %-11s agree %.2f  opposite %.2f" % (thH / 0.5, ref, ag, op))

ps.setup()
fig, axes = plt.subplots(1, len(curves), figsize=(3.3 * len(curves), 3.3))
axes = np.atleast_1d(axes)
for ax, (thH, (C, Bs, tau, bp)) in zip(axes, curves.items()):
    g = C["grid"]
    for k, lab, col, ls in (("etc_exact", "ETC, probe bid b^I (paper)", ps.COLORS["etc_exact"], "-"),
                            ("etc_optbid", "ETC, probe bid chosen by planner", ps.COLORS["etc_B"], "-"),
                            ("ce_A", "Learn-while-doing (CE)", ps.COLORS["ce_A"], "-")):
        ax.plot(g[10:], (C[k] - C["W"])[10:], color=col, label=lab, ls=ls, lw=1.5)
    ps.zero_line(ax)
    ax.set_xscale("log")
    ax.set_title("r = %g" % (thH / 0.5), fontsize=10)
    ax.set_xlabel("Team budget B")
axes[0].set_ylabel("Learning premium V − W")
axes[0].legend(loc="upper left", fontsize=7)
fig.suptitle("Letting the planner choose the probing bid closes most of the gap (World A, pi0 = 0.5, K = 100)", fontsize=10.5)
fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_optbid_premium.png"), dpi=170)
np.savetxt(os.path.join(RES, "optbid_agreement.csv"), np.array([(t, 0 if r == "etc_exact" else 1, a, o) for t, r, a, o in rows]),
           delimiter=",", header="thH,ref_is_optbid,agree_with_ce_A,opposite", comments="", fmt="%.4g")
