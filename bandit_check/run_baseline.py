"""Baseline deep-dive: theta_L=1/2, theta_H=8, K=100, pi0=1/2, v1/v2=2."""
import json
import os

import numpy as np

from agents import compute_curves
from analysis import ratio, shifts, agreement, regime_boundaries
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")
os.makedirs(CACHE, exist_ok=True)

thL, thH, pi0, K = 0.5, 8.0, 0.5, 100
Bmax = 4000.0

print("computing curves ...", flush=True)
C = compute_curves(thL, thH, pi0, K, Bmax, h=0.1, hb=0.1, cache_dir=CACHE)
grid, W = C["grid"], C["W"]

keysA = ["etc_exact", "etc_smooth", "etc_adapt", "ce_A", "probe_ce_A"]
keysB = ["opt_B", "ce_B", "ts_B", "etc_B"]
keys = keysA + keysB

# ---------------------------------------------------------------- single team
summary = {}
for k in keys + ["ce_A_raw"]:
    R = C[k] - W
    pos = np.where(R > 1e-6)[0]
    neg = np.where(R < -1e-6)[0]
    summary[k] = {
        "premium_max": float(np.nanmax(R)),
        "B_at_premium_max": float(grid[np.nanargmax(R)]),
        "first_B_positive": float(grid[pos[0]]) if pos.size else None,
        "last_B_positive": float(grid[pos[-1]]) if pos.size else None,
        "min_premium": float(np.nanmin(R)),
        "R_at": {str(b): float(np.interp(b, grid, R)) for b in (20, 40, 57, 60, 80, 100, 150, 250, 400, 1000, 2000, 3000, 4000)},
    }
    print("%-12s premium max %.3f at B=%7.1f | positive on [%s, %s] | min %.3f" % (
        k, summary[k]["premium_max"], summary[k]["B_at_premium_max"], summary[k]["first_B_positive"],
        summary[k]["last_B_positive"], summary[k]["min_premium"]))

print("\nvalue gap to the Bayes-optimal bandit (ex-ante) at selected B:")
for b in (60, 100, 150, 250, 400, 1000):
    print("  B=%5d  W=%.3f  ETC=%.3f  CE_A=%.3f  opt_B=%.3f  TS_B=%.3f  ETC_B=%.3f" % (
        b, *[np.interp(b, grid, C[k]) for k in ("W", "etc_smooth", "ce_A", "opt_B", "ts_B", "etc_B")]))

# ---------------------------------------------------------------- allocation
Ts = np.concatenate((np.arange(20, 1000, 1.0), np.arange(1000, 3901, 10.0)))
S = shifts(C, keys, Ts, 2.0, 1.0)
np.savez_compressed(os.path.join(RES, "baseline_shifts.npz"), **S)

print("\nshift a^X - a^E at v1/v2=2:")
hdr = "%7s" % "T" + "".join("%11s" % k[:10] for k in keys)
print(hdr)
for T in (60, 84, 100, 150, 184, 185, 200, 250, 300, 400, 600, 800, 1000, 1500, 2000, 3000, 3900):
    i = int(np.argmin(np.abs(S["T"] - T)))
    print("%7d" % S["T"][i] + "".join("%11.3f" % S[k][i] for k in keys))

print("\nvalue of re-optimising the split given learning, F_X(a^X) - F_X(a^E) (weighted impressions):")
from allocation import objective  # noqa: E402
print("%7s" % "T" + "".join("%11s" % k[:10] for k in keys))
gains = {}
for T in (100, 150, 250, 400, 600, 1000, 1500, 2000, 2500, 3000, 3900):
    i = int(np.argmin(np.abs(S["T"] - T)))
    row = "%7d" % S["T"][i]
    for k in keys:
        aE = S["aE"][i]
        aX = aE + S[k][i]
        g = objective(grid, C[k], S["T"][i], 2.0, 1.0, aX) - objective(grid, C[k], S["T"][i], 2.0, 1.0, aE)
        gains.setdefault(k, {})[str(T)] = float(g)
        row += "%11.4f" % g
    print(row)

print("\nsign agreement with the paper's smoothed ETC (|shift| < 0.1 + 0.001 T counts as zero):")
agree = {}
for ref in ("etc_smooth", "etc_exact"):
    for k in keys:
        if k == ref:
            continue
        a = agreement(S[ref], S[k], tol=0.1 + 0.001 * S["T"])
        agree[ref + "__" + k] = a
        if ref == "etc_smooth":
            print("  %-12s all=%.3f  where ETC!=0: %.3f   %s" % (k, a["agree_all"], a["agree_ref_nonzero"],
                  {kk: v for kk, v in a.items() if kk.startswith("ref")}))
print("\nregime boundaries (T, from-sign, to-sign):")
bounds = {k: regime_boundaries(S["T"], S[k], tol=0.1 + 0.001 * S["T"]) for k in keys}
for k in keys:
    print("  %-12s %s" % (k, bounds[k]))

with open(os.path.join(RES, "baseline_summary.json"), "w") as f:
    json.dump({"single_team": summary, "agreement": agree, "boundaries": bounds, "reallocation_gain": gains}, f, indent=1)

# ---------------------------------------------------------------- figures
ps.setup()
fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
ax = axes[0]
for k in ("etc_exact", "etc_smooth", "etc_adapt", "ce_A_raw"):
    ax.plot(grid[1:], (C[k] - W)[1:], color=ps.COLORS[k], lw=1.6 if k != "ce_A_raw" else 1.8,
            ls="-" if k not in ("etc_exact",) else (0, (4, 2)), label=ps.LABELS[k])
ax.set_xscale("log")
ax.set_xlim(10, 4000)
ax.set_ylim(-2.0, 3.6)
ps.zero_line(ax)
ax.set_title("World A: the paper's budget accounting")
ax.set_xlabel("Team budget B (log scale)")
ax.set_ylabel("Learning premium  V(B) − W(B)")
ax.legend(loc="upper left")
ax = axes[1]
for k in ("opt_B", "ts_B", "etc_B", "etc_smooth"):
    ax.plot(grid[1:], (C[k] - W)[1:], color=ps.COLORS[k], label=ps.LABELS[k],
            ls="-" if k != "etc_smooth" else (0, (1.5, 1.5)))
ax.set_xscale("log")
ax.set_xlim(10, 4000)
ps.zero_line(ax)
ax.set_title("World B: ex-ante budget (no cross-state subsidy loss)")
ax.set_xlabel("Team budget B (log scale)")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_baseline_premium.png"), dpi=170)

fig, ax = plt.subplots(figsize=(7.2, 3.9))
for k in ("etc_smooth", "ce_A", "opt_B", "ts_B", "etc_B"):
    rr = ratio(grid, C[k], W, step=2.0)
    m = grid > 3
    ax.plot(grid[m], rr[m], color=ps.COLORS[k], label=ps.LABELS[k])
ax.set_xscale("log")
ax.set_xlim(10, 4000)
ax.set_ylim(0.8, 1.5)
ps.zero_line(ax, 1.0)
ax.set_title("Marginal-value ratio V'(B)/W'(B) — the object Theorem 1 reads")
ax.set_xlabel("Team budget B (log scale)")
ax.set_ylabel("V'(B) / W'(B)")
ax.legend(loc="upper right", ncol=1)
fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_baseline_ratio.png"), dpi=170)

fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
for ax, lim in zip(axes, ((20, 1000), (20, 3900))):
    for k in ("etc_smooth", "ce_A", "opt_B", "ts_B", "etc_B"):
        ax.plot(S["T"], S[k], color=ps.COLORS[k], label=ps.LABELS[k], lw=1.5)
    ps.zero_line(ax)
    ax.set_xlim(*lim)
    ax.set_xlabel("Total budget T")
    if lim[1] > 1000:
        ax.set_xscale("log")
        ax.set_title("Same, full range (log T)")
    else:
        ax.set_title("Shift of the senior budget  a^X − a^E   (v1/v2 = 2)")
        ax.set_ylabel("a^X − a^E   (>0: more skewed)")
axes[0].legend(loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_baseline_shift.png"), dpi=170)
print("figures written")
