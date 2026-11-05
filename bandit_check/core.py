"""Core primitives of the single-team model (Yang, Zhu & Mookerjee).

Market state theta in {thL, thH}, prior pi0 = P(theta = thH).
Win probability q_theta(b) = b / (b + theta); a win costs b (first price).
Budget B, horizon K (one auction per period).

Everything here is the paper's model ("World A" accounting): whenever an
agent commits to an open-loop plan it must spend its wallet in expectation
under the belief it holds at the moment of commitment.

Functions are numba-jitted scalars so that the bandit dynamic programs in
bandits.py can call them inside tight loops.
"""
import math

import numpy as np
from numba import njit, prange


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------
@njit(cache=True)
def qbar(pi, b, thL, thH):
    """Predictive win probability at belief pi = P(thH)."""
    return pi * b / (b + thH) + (1.0 - pi) * b / (b + thL)


@njit(cache=True)
def dqbar_db(pi, b, thL, thH):
    return pi * thH / (b + thH) ** 2 + (1.0 - pi) * thL / (b + thL) ** 2


@njit(cache=True)
def pace_bid(pi, rho, thL, thH):
    """Unique b >= 0 with b * qbar(pi, b) = rho (per-period expected spend).

    f(b) = b*qbar - rho is increasing and convex, so Newton started at a point
    with f >= 0 (b0 = rho + thH) decreases monotonically to the root.
    """
    if rho <= 0.0:
        return 0.0
    b = rho + thH
    for _ in range(300):
        aH = b + thH
        aL = b + thL
        f = pi * b * b / aH + (1.0 - pi) * b * b / aL - rho
        fp = pi * (b * b + 2.0 * b * thH) / (aH * aH) + (1.0 - pi) * (b * b + 2.0 * b * thL) / (aL * aL)
        step = f / fp
        nb = b - step
        if nb <= 0.0:
            nb = 0.5 * b
        if abs(step) <= 1e-15 * (1.0 + b):
            b = nb
            break
        b = nb
    return b


@njit(cache=True)
def g_rate(pi, rho, thL, thH):
    """Win rate bought per period with expected spend rho at belief pi."""
    if rho <= 0.0:
        return 0.0
    b = pace_bid(pi, rho, thL, thH)
    return qbar(pi, b, thL, thH)


@njit(cache=True)
def g_rate_prime(pi, rho, thL, thH):
    """d g / d rho  = qbar_b / (qbar + b qbar_b)."""
    if rho <= 0.0:
        return np.inf
    b = pace_bid(pi, rho, thL, thH)
    qb = dqbar_db(pi, b, thL, thH)
    return qb / (qbar(pi, b, thL, thH) + b * qb)


@njit(cache=True)
def sigmoid(x):
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


# ---------------------------------------------------------------------------
# benchmark W (never learns) -- identical in every accounting regime
# ---------------------------------------------------------------------------
@njit(cache=True, parallel=True)
def W_curve(Bs, thL, thH, pi0, K):
    out = np.empty(Bs.size)
    for i in prange(Bs.size):
        out[i] = K * g_rate(pi0, Bs[i] / K, thL, thH)
    return out


@njit(cache=True, parallel=True)
def Wprime_curve(Bs, thL, thH, pi0, K):
    out = np.empty(Bs.size)
    for i in prange(Bs.size):
        out[i] = g_rate_prime(pi0, Bs[i] / K, thL, thH)
    return out


# ---------------------------------------------------------------------------
# paper's exact ETC: integer tau committed up front, binomial w
# ---------------------------------------------------------------------------
@njit(cache=True)
def etc_exact_tau_values(B, thL, thH, pi0, K):
    """Return array V(tau) for tau = 0..tau_max (tau*b^I <= B, tau <= K-1)."""
    bI = math.sqrt(thL * thH)
    r = thH / thL
    sr = math.sqrt(r)
    pL = sr / (1.0 + sr)   # q_{thL}(b^I)
    pH = 1.0 / (1.0 + sr)  # q_{thH}(b^I)
    tmax = int(math.floor(B / bI + 1e-12))
    if tmax > K - 1:
        tmax = K - 1
    if tmax < 0:
        tmax = 0
    out = np.empty(tmax + 1)
    lk0 = math.log(pi0 / (1.0 - pi0))
    lr = math.log(r)
    for tau in range(tmax + 1):
        tot = 0.0
        for w in range(tau + 1):
            lc = math.lgamma(tau + 1.0) - math.lgamma(w + 1.0) - math.lgamma(tau - w + 1.0)
            PwL = math.exp(lc + w * math.log(pL) + (tau - w) * math.log(1.0 - pL))
            PwH = math.exp(lc + w * math.log(pH) + (tau - w) * math.log(1.0 - pH))
            Pw = pi0 * PwH + (1.0 - pi0) * PwL
            if Pw <= 0.0:
                continue
            lpost = lk0 + 0.5 * (tau - 2.0 * w) * lr
            pi = sigmoid(lpost)
            rem = B - w * bI
            if rem < 0.0:
                rem = 0.0
            val = w + (K - tau) * g_rate(pi, rem / (K - tau), thL, thH)
            tot += Pw * val
        out[tau] = tot
    return out


@njit(cache=True, parallel=True)
def etc_exact_curve(Bs, thL, thH, pi0, K):
    V = np.empty(Bs.size)
    tau = np.empty(Bs.size)
    for i in prange(Bs.size):
        vals = etc_exact_tau_values(Bs[i], thL, thH, pi0, K)
        j = np.argmax(vals)
        V[i] = vals[j]
        tau[i] = j
    return V, tau


# ---------------------------------------------------------------------------
# ETC with a planner-chosen probing bid (still learn-then-exploit; w remains a
# sufficient statistic, only the two log-likelihood steps become asymmetric)
# ---------------------------------------------------------------------------
@njit(cache=True)
def etc_bid_value(B, bp, tau, thL, thH, pi0, K):
    qL = bp / (bp + thL)
    qH = bp / (bp + thH)
    lw = math.log(qH / qL)
    ll = math.log((1.0 - qH) / (1.0 - qL))
    lk0 = math.log(pi0 / (1.0 - pi0))
    tot = 0.0
    for w in range(tau + 1):
        lc = math.lgamma(tau + 1.0) - math.lgamma(w + 1.0) - math.lgamma(tau - w + 1.0)
        PwL = math.exp(lc + w * math.log(qL) + (tau - w) * math.log(1.0 - qL))
        PwH = math.exp(lc + w * math.log(qH) + (tau - w) * math.log(1.0 - qH))
        Pw = pi0 * PwH + (1.0 - pi0) * PwL
        if Pw <= 0.0:
            continue
        pi = sigmoid(lk0 + w * lw + (tau - w) * ll)
        rem = B - w * bp
        if rem < 0.0:
            rem = 0.0
        tot += Pw * (w + (K - tau) * g_rate(pi, rem / (K - tau), thL, thH))
    return tot


@njit(cache=True, parallel=True)
def etc_optbid_curve(Bs, bids, thL, thH, pi0, K, tau_cap):
    V = np.empty(Bs.size)
    TB = np.empty(Bs.size)
    BP = np.empty(Bs.size)
    for i in prange(Bs.size):
        B = Bs[i]
        best = K * g_rate(pi0, B / K, thL, thH)
        bt = 0.0
        bb = 0.0
        for j in range(bids.size):
            bp = bids[j]
            tmax = int(math.floor(B / bp + 1e-12))
            if tmax > K - 1:
                tmax = K - 1
            if tmax > tau_cap:
                tmax = tau_cap
            for tau in range(1, tmax + 1):
                v = etc_bid_value(B, bp, tau, thL, thH, pi0, K)
                if v > best:
                    best = v
                    bt = tau
                    bb = bp
        V[i] = best
        TB[i] = bt
        BP[i] = bb
    return V, TB, BP


# ---------------------------------------------------------------------------
# paper's smoothed ETC (average path, continuous tau)
# ---------------------------------------------------------------------------
@njit(cache=True)
def smooth_value(tau, B, thL, thH, pi0, K):
    bI = math.sqrt(thL * thH)
    r = thH / thL
    sr = math.sqrt(r)
    pL = sr / (1.0 + sr)
    pH = 1.0 / (1.0 + sr)
    sL = bI * pL
    sH = bI * pH
    c = 0.5 * (sr - 1.0) / (sr + 1.0) * math.log(r)
    lk0 = math.log(pi0 / (1.0 - pi0))
    piH = sigmoid(lk0 + c * tau)   # belief on the theta_H average path
    piL = sigmoid(lk0 - c * tau)   # belief on the theta_L average path
    n = K - tau
    remH = B - tau * sH
    remL = B - tau * sL
    if remL < 0.0:
        remL = 0.0
    if remH < 0.0:
        remH = 0.0
    bH = pace_bid(piH, remH / n, thL, thH)
    bL = pace_bid(piL, remL / n, thL, thH)
    vH = tau * pH + n * bH / (bH + thH)
    vL = tau * pL + n * bL / (bL + thL)
    return pi0 * vH + (1.0 - pi0) * vL


@njit(cache=True)
def smooth_opt(B, thL, thH, pi0, K, ngrid, tau_cap):
    """Maximise smoothed value over tau in [0, tau_max(B)] (grid + golden refine)."""
    bI = math.sqrt(thL * thH)
    sr = math.sqrt(thH / thL)
    sL = bI * sr / (1.0 + sr)
    tmax = B / sL
    if tmax > K - 1e-6:
        tmax = K - 1e-6
    if tmax > tau_cap:
        tmax = tau_cap
    v0 = smooth_value(0.0, B, thL, thH, pi0, K)
    if tmax <= 0.0:
        return v0, 0.0
    best_v = v0
    best_t = 0.0
    h = tmax / ngrid
    for k in range(1, ngrid + 1):
        t = k * h
        v = smooth_value(t, B, thL, thH, pi0, K)
        if v > best_v:
            best_v = v
            best_t = t
    if best_t == 0.0:
        # check a tiny interior step (continuous entry)
        return best_v, 0.0
    a = best_t - h
    if a < 0.0:
        a = 0.0
    bnd = best_t + h
    if bnd > tmax:
        bnd = tmax
    gr = 0.5 * (math.sqrt(5.0) - 1.0)
    x1 = bnd - gr * (bnd - a)
    x2 = a + gr * (bnd - a)
    f1 = smooth_value(x1, B, thL, thH, pi0, K)
    f2 = smooth_value(x2, B, thL, thH, pi0, K)
    for _ in range(60):
        if f1 > f2:
            bnd = x2
            x2 = x1
            f2 = f1
            x1 = bnd - gr * (bnd - a)
            f1 = smooth_value(x1, B, thL, thH, pi0, K)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + gr * (bnd - a)
            f2 = smooth_value(x2, B, thL, thH, pi0, K)
    t = 0.5 * (a + bnd)
    v = smooth_value(t, B, thL, thH, pi0, K)
    if v > best_v:
        return v, t
    return best_v, best_t


@njit(cache=True, parallel=True)
def etc_smooth_curve(Bs, thL, thH, pi0, K, ngrid=600, tau_cap=1e9):
    V = np.empty(Bs.size)
    tau = np.empty(Bs.size)
    for i in prange(Bs.size):
        v, t = smooth_opt(Bs[i], thL, thH, pi0, K, ngrid, tau_cap)
        V[i] = v
        tau[i] = t
    return V, tau


# ---------------------------------------------------------------------------
# ETC with adaptive (history-dependent) stopping -- the DP in draft/DP.tex
# probe at b^I while affordable, stop when Bellman says so, then commit.
# ---------------------------------------------------------------------------
@njit(cache=True)
def etc_adaptive_value(B, thL, thH, pi0, K):
    bI = math.sqrt(thL * thH)
    r = thH / thL
    lr = math.log(r)
    lk0 = math.log(pi0 / (1.0 - pi0))
    Vn = np.zeros(K + 2)      # values at tau+1 (indexed by w)
    Vc = np.zeros(K + 2)
    ET = np.zeros(K + 2)      # expected number of probes (diagnostic)
    ETn = np.zeros(K + 2)
    for tau in range(K, -1, -1):
        for w in range(tau + 1):
            if tau == K:
                Vc[w] = 0.0
                ET[w] = 0.0
                continue
            pi = sigmoid(lk0 + 0.5 * (tau - 2.0 * w) * lr)
            rem = B - w * bI
            if rem < 0.0:
                rem = 0.0
            S = (K - tau) * g_rate(pi, rem / (K - tau), thL, thH)
            if rem >= bI - 1e-12:
                qq = qbar(pi, bI, thL, thH)
                C = qq * (1.0 + Vn[w + 1]) + (1.0 - qq) * Vn[w]
                if C > S:
                    Vc[w] = C
                    ET[w] = 1.0 + qq * ETn[w + 1] + (1.0 - qq) * ETn[w]
                    continue
            Vc[w] = S
            ET[w] = 0.0
        for w in range(tau + 1):
            Vn[w] = Vc[w]
            ETn[w] = ET[w]
    return Vn[0], ETn[0]


@njit(cache=True, parallel=True)
def etc_adaptive_curve(Bs, thL, thH, pi0, K):
    V = np.empty(Bs.size)
    T = np.empty(Bs.size)
    for i in prange(Bs.size):
        v, t = etc_adaptive_value(Bs[i], thL, thH, pi0, K)
        V[i] = v
        T[i] = t
    return V, T
