"""Large-horizon limit objects for Propositions 1-2.

g(pi; rho)   per-period win rate when expected spend rho is paced at belief pi
VPI(rho)     value of free perfect information, per period
Psi_ETC(rho) best value of a binomial probing experiment at b^I (tau = 0, 1, ..., or
             tau = infinity), per period, net of g(pi0; rho)  -> limit of the paper's ETC
Phi(rho)     concave envelope of g(.; rho) at pi0 minus g(pi0; rho)  -> upper bound
"""
import math

import numpy as np
from numba import njit, prange

from core import g_rate, sigmoid


@njit(cache=True)
def vpi(rho, thL, thH, pi0):
    return pi0 * g_rate(1.0, rho, thL, thH) + (1.0 - pi0) * g_rate(0.0, rho, thL, thH) - g_rate(pi0, rho, thL, thH)


@njit(cache=True)
def binomial_experiment_value(rho, tau, thL, thH, pi0):
    """E[g(pi_tau(w); rho)] for tau probes at b^I = sqrt(thL thH) (prior-predictive w)."""
    r = thH / thL
    sr = math.sqrt(r)
    pL = sr / (1.0 + sr)
    pH = 1.0 / (1.0 + sr)
    lk0 = math.log(pi0 / (1.0 - pi0))
    lr = math.log(r)
    tot = 0.0
    for w in range(tau + 1):
        lc = math.lgamma(tau + 1.0) - math.lgamma(w + 1.0) - math.lgamma(tau - w + 1.0)
        PwL = math.exp(lc + w * math.log(pL) + (tau - w) * math.log(1.0 - pL))
        PwH = math.exp(lc + w * math.log(pH) + (tau - w) * math.log(1.0 - pH))
        Pw = pi0 * PwH + (1.0 - pi0) * PwL
        if Pw < 1e-300:
            continue
        tot += Pw * g_rate(sigmoid(lk0 + 0.5 * (tau - 2.0 * w) * lr), rho, thL, thH)
    return tot


@njit(cache=True, parallel=True)
def psi_etc_curve(rhos, thL, thH, pi0, tau_max):
    n = rhos.size
    g0 = np.empty(n)
    v = np.empty(n)
    best = np.empty(n)
    btau = np.empty(n)
    for i in prange(n):
        rho = rhos[i]
        base = g_rate(pi0, rho, thL, thH)
        g0[i] = base
        v[i] = vpi(rho, thL, thH, pi0)
        bb = 0.0
        bt = 0.0
        for tau in range(1, tau_max + 1):
            val = binomial_experiment_value(rho, tau, thL, thH, pi0) - base
            if val > bb:
                bb = val
                bt = tau
        if v[i] > bb:
            bb = v[i]
            bt = -1.0  # tau = infinity (full information)
        best[i] = bb
        btau[i] = bt
    return g0, v, best, btau


@njit(cache=True, parallel=True)
def concave_envelope_curve(rhos, thL, thH, pi0, npi):
    """Phi(rho) = cav_pi g(pi; rho) at pi0 minus g(pi0; rho) (two-point splits suffice in 1-D)."""
    n = rhos.size
    out = np.empty(n)
    grid = np.linspace(0.0, 1.0, npi)
    for i in prange(n):
        rho = rhos[i]
        gv = np.empty(npi)
        for k in range(npi):
            gv[k] = g_rate(grid[k], rho, thL, thH)
        base = g_rate(pi0, rho, thL, thH)
        best = base
        for a in range(npi):
            if grid[a] > pi0:
                break
            for b in range(npi - 1, -1, -1):
                if grid[b] < pi0:
                    break
                if grid[b] - grid[a] < 1e-12:
                    continue
                lam = (grid[b] - pi0) / (grid[b] - grid[a])
                val = lam * gv[a] + (1.0 - lam) * gv[b]
                if val > best:
                    best = val
        out[i] = best - base
    return out


@njit(cache=True, parallel=True)
def max_belief_curvature(rhos, thL, thH, npi):
    """max over pi of d^2 g / d pi^2 (finite differences); < 0 means g(.; rho) concave on [0,1]."""
    out = np.empty(rhos.size)
    h = 1.0 / (npi - 1)
    for i in prange(rhos.size):
        rho = rhos[i]
        mx = -1e300
        for k in range(1, npi - 1):
            p = k * h
            d2 = (g_rate(p + h, rho, thL, thH) - 2.0 * g_rate(p, rho, thL, thH) + g_rate(p - h, rho, thL, thH)) / (h * h)
            if d2 > mx:
                mx = d2
        out[i] = mx
    return out


@njit(cache=True, parallel=True)
def min_belief_curvature(rhos, thL, thH, npi):
    """min over pi of d^2 g / d pi^2 (finite differences); > 0 means g(.; rho) convex on [0,1]."""
    out = np.empty(rhos.size)
    h = 1.0 / (npi - 1)
    for i in prange(rhos.size):
        rho = rhos[i]
        mn = 1e300
        for k in range(1, npi - 1):
            p = k * h
            d2 = (g_rate(p + h, rho, thL, thH) - 2.0 * g_rate(p, rho, thL, thH) + g_rate(p - h, rho, thL, thH)) / (h * h)
            if d2 < mn:
                mn = d2
        out[i] = mn
    return out


def first_positive(x, y, tol=1e-12):
    idx = np.where(y > tol)[0]
    return float(x[idx[0]]) if idx.size else float("nan")


def exante_full_info(rhos, thL, thH, pi0, iters=120):
    """Per-period value when the state is known from the start under the ex-ante budget rule.

    The state-contingent spends (s_H, s_L) with pi0 s_H + (1 - pi0) s_L = rho maximise
    pi0 g(1; s_H) + (1 - pi0) g(0; s_L). With multiplier lam the bid in state theta maximises
    q_theta(b)(1 - lam b), i.e. b = -theta + sqrt(theta^2 + theta / lam); lam is found by bisection.
    This is the large-K limit of both the full bandit (DP) and the decomposition under the ex-ante rule.
    """
    rhos = np.asarray(rhos, float)
    lo = np.full(rhos.shape, 1e-12)
    hi = np.full(rhos.shape, 1e6)

    def at(lam):
        val, spend = 0.0, 0.0
        for th, p in ((thH, pi0), (thL, 1.0 - pi0)):
            b = -th + np.sqrt(th * th + th / lam)
            q = b / (b + th)
            val = val + p * q
            spend = spend + p * b * q
        return val, spend

    for _ in range(iters):
        lam = np.sqrt(lo * hi)
        _, s = at(lam)
        hi = np.where(s > rhos, hi, lam)
        lo = np.where(s > rhos, lam, lo)
    v, _ = at(np.sqrt(lo * hi))
    return np.where(rhos > 0, v, 0.0)
