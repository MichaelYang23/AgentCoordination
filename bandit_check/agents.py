"""Compute V_X(B) on a common uniform budget grid for every agent type X."""
import os
import time

import numpy as np

from core import W_curve, etc_exact_curve, etc_smooth_curve, etc_adaptive_curve
from bandits import (belief_grid, ce_worldA, lag_sweep, etc_exante_sweep,
                     curve_to_grid, curve_to_grid_hermite, lam_targets)

AGENTS = {
    # key: (label, world)
    "etc_exact": ("ETC, integer tau (paper exact)", "A"),
    "etc_smooth": ("ETC, smoothed (paper approx.)", "A"),
    "etc_adapt": ("ETC, adaptive stopping", "A"),
    "ce_A": ("Learn-while-doing CE, planner may switch off", "A"),
    "ce_A_raw": ("Learn-while-doing CE, always on", "A"),
    "probe_ce_A": ("Probe at b^I then CE (best tau)", "A"),
    "opt_B": ("Bayes-optimal adaptive bandit", "B"),
    "ts_B": ("Thompson sampling", "B"),
    "ce_B": ("Myopic Bayesian (CE)", "B"),
    "etc_B": ("ETC re-solved, ex-ante budget", "B"),
}


def _coarse_then_interp(fn, grid, step):
    g2 = np.arange(0.0, grid[-1] + step, step)
    g2[0] = 1e-9
    v, _ = fn(g2)
    g2[0] = 0.0
    v[0] = 0.0
    return np.interp(grid, g2, v)


def compute_curves(thL, thH, pi0, K, Bmax, h=0.1, hb=0.1, hl_A=0.05, hl_B=0.02,
                   which=None, verbose=True, cache_dir=None, nbg=80, n_fine=700, tau_cap_B=None):
    tag = "v2_thL%.3g_thH%.3g_pi%.3g_K%d_B%d_h%.3g_hb%.3g_hlB%.3g" % (thL, thH, pi0, K, Bmax, h, hb, hl_B)
    if cache_dir is not None:
        path = os.path.join(cache_dir, tag + ".npz")
        if os.path.exists(path):
            d = np.load(path)
            return {k: d[k] for k in d.files}
    which = which or list(AGENTS)
    grid = np.arange(0.0, Bmax + 0.5 * h, h)
    out = {"grid": grid}
    gpos = np.maximum(grid, 1e-9)
    out["W"] = W_curve(gpos, thL, thH, pi0, K)
    out["W"][0] = 0.0
    t0 = time.time()

    def log(msg):
        if verbose:
            print("   [%6.1fs] %s" % (time.time() - t0, msg), flush=True)

    # V >= W is exact for every agent below that can replicate the benchmark
    # (tau = 0 / stop at once / optimal policies); the floor only removes
    # interpolation error near B = 0 where V ~ sqrt(B).
    if "etc_exact" in which:
        v = _coarse_then_interp(lambda g: etc_exact_curve(g, thL, thH, pi0, K), grid, max(h, 0.25))
        out["etc_exact"] = np.maximum(v, out["W"])
        log("etc_exact")
    if "etc_smooth" in which:
        v, tau = etc_smooth_curve(gpos, thL, thH, pi0, K, 600, 1e9)
        v[0] = 0.0
        out["etc_smooth"] = v
        out["etc_smooth_tau"] = tau
        log("etc_smooth")
    if "etc_adapt" in which:
        v = _coarse_then_interp(lambda g: etc_adaptive_curve(g, thL, thH, pi0, K), grid, max(h, 0.25))
        out["etc_adapt"] = np.maximum(v, out["W"])
        log("etc_adapt")
    if any(k in which for k in ("ce_A", "ce_A_raw", "probe_ce_A")):
        hl, J, m = belief_grid(thL, thH, pi0, target_h=hl_A)
        Nb = int(round(Bmax / hb)) + 1
        tau_cap = min(K - 1, 30)
        V, hyb = ce_worldA(thL, thH, pi0, K, hb, Nb, hl, J, m, tau_cap, True)
        bgrid = np.arange(Nb) * hb
        ce = np.interp(grid, bgrid, V)
        out["ce_A_raw"] = ce
        out["ce_A"] = np.maximum(ce, out["W"])
        best = np.nanmax(np.where(np.isnan(hyb), -np.inf, hyb), axis=0)
        out["probe_ce_A"] = np.maximum(np.interp(grid, bgrid, best), out["W"])
        out["probe_ce_A_tau"] = np.interp(grid, bgrid, np.argmax(np.where(np.isnan(hyb), -np.inf, hyb), axis=0).astype(float))
        log("ce_A (Nb=%d, Nl=%d)" % (Nb, 2 * J + 1))
    hl, J, _ = belief_grid(thL, thH, pi0, target_h=hl_B)
    for key, kind in (("ts_B", 1), ("ce_B", 0), ("opt_B", 2)):
        if key in which:
            lams = lam_targets(lambda L: lag_sweep(thL, thH, pi0, K, L, hl, J, kind, nbg)[1], Bmax, n_fine=n_fine)
            N, S = lag_sweep(thL, thH, pi0, K, lams, hl, J, kind, nbg)
            if kind == 2:
                v = curve_to_grid_hermite(S, N, lams, grid)
            else:
                v = curve_to_grid(S, N, grid)
            out[key] = np.maximum(v, out["W"]) if kind in (0, 2) else v
            out[key + "_lam"] = np.interp(grid, np.sort(S), lams[np.argsort(S)])
            log(key + " (%d multipliers)" % lams.size)
    if "etc_B" in which:
        tau_cap = min(K - 1, 40 if tau_cap_B is None else tau_cap_B)
        lams = lam_targets(lambda L: etc_exante_sweep(thL, thH, pi0, K, L, 0)[1][:, 0], Bmax, n_fine=n_fine)
        N, S = etc_exante_sweep(thL, thH, pi0, K, lams, tau_cap)
        best = np.full(grid.size, -np.inf)
        btau = np.zeros(grid.size)
        for tau in range(tau_cap + 1):
            v = curve_to_grid_hermite(S[:, tau], N[:, tau], lams, grid)
            v = np.where(np.isnan(v), -np.inf, v)
            better = v > best + 1e-12
            btau[better] = tau
            best = np.maximum(best, v)
        out["etc_B"] = np.maximum(best, out["W"])
        out["etc_B_tau"] = btau
        log("etc_B")
    if cache_dir is not None:
        np.savez_compressed(os.path.join(cache_dir, tag + ".npz"), **out)
    return out
