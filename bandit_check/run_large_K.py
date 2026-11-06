"""Verification of Propositions 1-2: per-period learning premium as K grows (K = 50..400),
compared with the large-horizon limits VPI, Psi_ETC and Phi; allocation shifts in the limit."""
import glob
import json
import math
import os
import time

import numpy as np
from scipy.optimize import brentq

from core import (W_curve, etc_exact_curve_capped, etc_smooth_curve, etc_adaptive_curve, g_rate_prime)
from bandits import belief_grid, ce_worldA
from limit_theory import (vpi, psi_etc_curve, concave_envelope_curve, max_belief_curvature, min_belief_curvature,
                          first_positive)
from allocation import solve_allocation
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")
OUT = os.path.join(RES, "large_K")
os.makedirs(OUT, exist_ok=True)

thL, thH, pi0 = 0.5, 8.0, 0.5
KS = [50, 100, 200, 400]
RHO_MAX = 12.0
t0 = time.time()


def log(msg):
    print("[%6.0fs] %s" % (time.time() - t0, msg), flush=True)


# --------------------------------------------------------------- 1. limit functions
rhos = np.round(np.arange(0.005, RHO_MAX + 1e-9, 0.005), 6)
g0, vp, psi, ptau = psi_etc_curve(rhos, thL, thH, pi0, 80)
rc = rhos[::2]
phi = concave_envelope_curve(rc, thL, thH, pi0, 401)
curv = max_belief_curvature(rc, thL, thH, 401)
curv_min = min_belief_curvature(rc, thL, thH, 401)
rho_far = np.geomspace(RHO_MAX, 1e4, 200)          # convexity well beyond the plotted range
curv_min_far = min_belief_curvature(rho_far, thL, thH, 401)
not_convex = np.where(curv_min <= 0)[0]
rho1_root = brentq(lambda r: vpi(r, thL, thH, pi0), 0.3, 0.6, xtol=1e-10)
dr = 1e-5
vpi_slope = (vpi(rho1_root + dr, thL, thH, pi0) - vpi(rho1_root - dr, thL, thH, pi0)) / (2 * dr)
g_slope = g_rate_prime(pi0, rho1_root, thL, thH)
c1 = math.sqrt(pi0 / thH + (1 - pi0) / thL) - pi0 / math.sqrt(thH) - (1 - pi0) / math.sqrt(thL)
thr = {
    "rho_concave_until": float(rc[np.where(curv >= 0)[0][0]]) if (curv >= 0).any() else None,
    "rho0_any_information_helps": first_positive(rc, phi, 1e-9),
    "rho_ETC_entry": first_positive(rhos, psi, 1e-9),
    "rho_PI_perfect_information_helps": first_positive(rhos, vp, 0.0),
    "rho_convex_from": float(rc[not_convex[-1] + 1]) if not_convex.size else float(rc[0]),
    "convex_up_to_1e4": bool((curv_min_far > 0).all()),
    "rho1_VPI_root": round(rho1_root, 5),
    "kink_VPI_slope": round(vpi_slope, 5),
    "kink_g_rho": round(g_slope, 5),
    "kink_ratio_jump": round(1.0 + vpi_slope / g_slope, 4),
    "small_rho_VPI_over_sqrt_rho_at_1e-4": round(vpi(1e-4, thL, thH, pi0) / 1e-2, 4),
    "small_rho_theory_minus_c1": round(-c1, 4),
    "large_rho_rho2_VPI_at_3000": round(3000.0 ** 2 * vpi(3000.0, thL, thH, pi0), 3),
    "large_rho_theory_Var_theta": pi0 * (1 - pi0) * (thH - thL) ** 2,
    "max_Phi_minus_max_VPI_0": round(float(np.max(phi - np.maximum(np.interp(rc, rhos, vp), 0.0))), 5),
    "rho_at_max_Phi_gap": float(rc[np.argmax(phi - np.maximum(np.interp(rc, rhos, vp), 0.0))]),
}
log("thresholds: %s" % thr)
np.savez_compressed(os.path.join(OUT, "limit_functions.npz"), rhos=rhos, g0=g0, vpi=vp, psi=psi, ptau=ptau,
                    rho_coarse=rc, phi=phi, curv=curv, curv_min=curv_min)

# --------------------------------------------------------------- 2. finite-K curves
curves = {}
for K in KS:
    path = os.path.join(OUT, "curves_K%d.npz" % K)
    if os.path.exists(path):
        curves[K] = dict(np.load(path))
        log("K=%d loaded" % K)
        continue
    cached = glob.glob(os.path.join(CACHE, "v2_thL0.5_thH8_pi0.5_K%d_B*_h0.1_hb0.1_hlB0.04.npz" % K))
    if cached:
        d = np.load(cached[0])
        C = {k: d[k] for k in ("grid", "W", "etc_exact", "etc_smooth", "etc_adapt", "ce_A", "ce_A_raw")}
        log("K=%d from sweep cache" % K)
    else:
        Bmax = RHO_MAX * K
        h = 0.2
        grid = np.arange(0.0, Bmax + 0.5 * h, h)
        gpos = np.maximum(grid, 1e-9)
        C = {"grid": grid}
        C["W"] = W_curve(gpos, thL, thH, pi0, K)
        C["W"][0] = 0.0
        g1 = np.arange(1.0, Bmax + 0.5, 1.0)
        v1, _ = etc_exact_curve_capped(g1, thL, thH, pi0, K, 150)
        C["etc_exact"] = np.maximum(np.interp(grid, np.concatenate(([0.0], g1)), np.concatenate(([0.0], v1))), C["W"])
        log("K=%d etc_exact" % K)
        g2 = np.arange(0.5, Bmax + 0.25, 0.5)
        v2, _ = etc_smooth_curve(g2, thL, thH, pi0, K, 600, 200.0)
        C["etc_smooth"] = np.maximum(np.interp(grid, np.concatenate(([0.0], g2)), np.concatenate(([0.0], v2))), C["W"])
        log("K=%d etc_smooth" % K)
        g4 = np.arange(4.0, Bmax + 2.0, 4.0)
        v4, _ = etc_adaptive_curve(g4, thL, thH, pi0, K)
        C["etc_adapt"] = np.maximum(np.interp(grid, np.concatenate(([0.0], g4)), np.concatenate(([0.0], v4))), C["W"])
        log("K=%d etc_adapt" % K)
        hl, J, m = belief_grid(thL, thH, pi0, target_h=0.05)
        Nb = int(round(Bmax / h)) + 1
        Vce, _ = ce_worldA(thL, thH, pi0, K, h, Nb, hl, J, m, 0, True)
        C["ce_A_raw"] = np.interp(grid, np.arange(Nb) * h, Vce)
        C["ce_A"] = np.maximum(C["ce_A_raw"], C["W"])
        log("K=%d learn-while-doing DP (Nb=%d)" % (K, Nb))
    np.savez_compressed(path, **C)
    curves[K] = C

# --------------------------------------------------------------- 3. table at selected budgets
RT = [0.2, 0.3, 0.45, 0.5, 0.6, 0.8, 1.0, 1.5, 2.5, 4.0, 6.0, 10.0]
lim = {
    "psi": lambda r: float(np.interp(r, rhos, psi)),
    "vpi": lambda r: float(np.interp(r, rhos, vp)),
    "phi": lambda r: float(np.interp(r, rc, phi)),
}


def prem(K, key, r):
    C = curves[K]
    B = r * K
    return (np.interp(B, C["grid"], C[key]) - np.interp(B, C["grid"], C["W"])) / K


table = []
taus = {}
for K in KS:
    Bs = np.array([r * K for r in RT])
    _, tt = etc_exact_curve_capped(Bs, thL, thH, pi0, K, 150)
    taus[K] = [int(x) for x in tt]
for r in RT:
    row = {"rho": r, "VPI": lim["vpi"](r), "Psi_ETC": lim["psi"](r), "Phi": lim["phi"](r)}
    for key in ("etc_exact", "etc_smooth", "etc_adapt", "ce_A_raw", "ce_A"):
        row[key] = [float(prem(K, key, r)) for K in KS]
    table.append(row)

lines = []
lines.append("thresholds (per-period budget rho = B/K): " + json.dumps(thr))
lines.append("\nper-period learning premium (V - W)/K, K = %s" % KS)
lines.append("%5s %8s %8s %8s | %-34s | %-34s | %-34s" % ("rho", "VPI", "Psi_ETC", "Phi", "ETC exact", "learn-while-doing (always on)", "ETC adaptive stopping"))
for row in table:
    f = lambda v: " ".join("%8.5f" % x for x in v)
    lines.append("%5.2f %8.5f %8.5f %8.5f | %s | %s | %s" % (row["rho"], row["VPI"], row["Psi_ETC"], row["Phi"],
                                                             f(row["etc_exact"]), f(row["ce_A_raw"]), f(row["etc_adapt"])))
lines.append("\nlearning cost in impressions, K * (limit - premium/K): ETC exact vs Psi_ETC, learn-while-doing vs VPI")
for row in table:
    if row["rho"] < 0.6:
        continue
    ce = [K * (row["VPI"] - x) for K, x in zip(KS, row["ce_A_raw"])]
    et = [K * (row["Psi_ETC"] - x) for K, x in zip(KS, row["etc_exact"])]
    lines.append("rho=%5.2f  ETC: %s   learn-while-doing: %s" % (row["rho"], " ".join("%6.3f" % x for x in et),
                                                                  " ".join("%6.3f" % x for x in ce)))
lines.append("\noptimal probing length tau*_K of exact ETC (columns K = %s)" % KS)
for i, r in enumerate(RT):
    lines.append("rho=%5.2f  tau* = %s   tau*/K = %s" % (r, [taus[K][i] for K in KS],
                                                        ["%.3f" % (taus[K][i] / K) for K in KS]))

# --------------------------------------------------------------- 4. allocation in the limit
v1, v2 = 2.0, 1.0
tgrid = np.round(np.arange(0.3, 10.0001, 0.05), 4)
Lgrid = np.concatenate(([0.0], rhos))
L_W = np.concatenate(([0.0], g0))
L_etc = np.concatenate(([0.0], g0 + psi))
L_ce = np.concatenate(([0.0], g0 + np.maximum(vp, 0.0)))
alloc = {"t": tgrid}
alloc["limit_etc"] = np.array([solve_allocation(Lgrid, L_etc, t, v1, v2) - solve_allocation(Lgrid, L_W, t, v1, v2) for t in tgrid])
alloc["limit_ce"] = np.array([solve_allocation(Lgrid, L_ce, t, v1, v2) - solve_allocation(Lgrid, L_W, t, v1, v2) for t in tgrid])
for K in KS:
    C = curves[K]
    gK = C["grid"]
    for key in ("etc_exact", "ce_A"):
        sh = []
        for t in tgrid:
            T = t * K
            sh.append((solve_allocation(gK, C[key], T, v1, v2) - solve_allocation(gK, C["W"], T, v1, v2)) / K)
        alloc["%s_K%d" % (key, K)] = np.array(sh)
np.savez_compressed(os.path.join(OUT, "allocation_limit.npz"), **alloc)


def sign_changes(t, s, tol=2e-3):
    sg = np.sign(s)
    sg[np.abs(s) < tol] = 0
    out = []
    for i in range(1, sg.size):
        if sg[i] != sg[i - 1]:
            out.append((float(t[i]), int(sg[i - 1]), int(sg[i])))
    return out


lines.append("\nnormalized allocation shift (a^L - a^E)/K at v1/v2 = 2; sign switches (t = T/K, from, to):")
lines.append("  limit (ETC, Psi):              %s" % sign_changes(tgrid, alloc["limit_etc"]))
lines.append("  limit (learn-while-doing, VPI): %s" % sign_changes(tgrid, alloc["limit_ce"]))
for K in KS:
    lines.append("  K=%3d ETC exact:                %s" % (K, sign_changes(tgrid, alloc["etc_exact_K%d" % K])))
    lines.append("  K=%3d learn-while-doing:        %s" % (K, sign_changes(tgrid, alloc["ce_A_K%d" % K])))
for t in (1.0, 1.5, 2.5, 4.0, 6.0):
    i = int(np.argmin(np.abs(tgrid - t)))
    lines.append("  t=%.1f  ETC: %s -> limit %+.4f | CE: %s -> limit %+.4f" % (
        t, " ".join("%+.4f" % alloc["etc_exact_K%d" % K][i] for K in KS), alloc["limit_etc"][i],
        " ".join("%+.4f" % alloc["ce_A_K%d" % K][i] for K in KS), alloc["limit_ce"][i]))
txt = "\n".join(lines)
print(txt)
with open(os.path.join(OUT, "summary.txt"), "w") as f:
    f.write(txt + "\n")
with open(os.path.join(OUT, "summary.json"), "w") as f:
    json.dump({"thresholds": thr, "table": table, "tau_star": {str(k): v for k, v in taus.items()}, "K": KS}, f, indent=1)

# --------------------------------------------------------------- 5. figures
ps.setup()
blues = {50: "#86b6ef", 100: "#3987e5", 200: "#256abf", 400: "#104281"}
fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
for ax, key, limkey, title in ((axes[0], "etc_exact", "psi", "Paper's ETC (exact)"),
                               (axes[1], "ce_A_raw", "vpi", "Learn-while-doing (always on)")):
    for K in KS:
        C = curves[K]
        rr = C["grid"][1:] / K
        ax.plot(rr, (C[key] - C["W"])[1:] / K, color=blues[K], lw=1.4, label="K = %d" % K)
    yl = psi if limkey == "psi" else vp
    ax.plot(rhos, yl, color=ps.INK, lw=1.6, ls=(0, (4, 2)), label="limit (%s)" % ("Ψ" if limkey == "psi" else "VPI"))
    ps.zero_line(ax)
    ax.set_xscale("log")
    ax.set_xlim(0.1, 12)
    ax.set_ylim(-0.03, 0.032)
    ax.set_title(title)
    ax.set_xlabel("Per-period budget ρ = B/K (log scale)")
axes[0].set_ylabel("Per-period learning premium (V − W)/K")
axes[0].legend(loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_premium_convergence.png"), dpi=170)

fig, axes = plt.subplots(1, 2, figsize=(11, 3.7), sharey=True)
for ax, key, limkey, title in ((axes[0], "etc_exact", "limit_etc", "Paper's ETC (exact)"),
                               (axes[1], "ce_A", "limit_ce", "Learn-while-doing (planner may switch off)")):
    for K in KS:
        ax.plot(tgrid, alloc["%s_K%d" % (key, K)], color=blues[K], lw=1.3, label="K = %d" % K)
    ax.plot(tgrid, alloc[limkey], color=ps.INK, lw=1.6, ls=(0, (4, 2)), label="limit")
    ps.zero_line(ax)
    ax.set_xlim(0.3, 10)
    ax.set_title(title)
    ax.set_xlabel("Total budget per period t = T/K")
axes[0].set_ylabel("(a^L − a^E)/K   (v1/v2 = 2)")
axes[0].legend(loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_allocation_convergence.png"), dpi=170)
log("done")
