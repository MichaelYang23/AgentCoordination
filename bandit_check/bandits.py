"""Learn-while-doing ("bandit") agents for the same market and the same benchmark W.

Two budget-accounting worlds are used so that every comparison is
apples-to-apples with the never-learning benchmark W(B) of the paper:

World A  -- the paper's own accounting.  Any open-loop plan, when committed,
            must spend the current wallet in expectation under the belief held
            at commitment.  W commits once (t=0); the paper's ETC commits twice
            (t=0 and the hand-off).  The learn-while-doing agent below
            re-commits every period with its updated posterior and real wallet
            (certainty-equivalent re-pacing, "CE").  A hybrid first probes for
            tau periods at b^I and then runs CE.

World B  -- ex-ante accounting: only E[total spend] <= B is required (the
            standard fluid / Lagrangian relaxation used for budgeted bandits).
            W is unchanged (an open-loop agent has a single history).  Here we
            can compute the Bayes-optimal adaptive policy exactly by dynamic
            programming over (periods left, posterior log-odds), plus a myopic
            Bayesian bidder (CE) and Thompson sampling (TS).  The ETC protocol is
            also re-solved under the same ex-ante accounting.
"""
import math

import numpy as np
from numba import njit, prange
from scipy.interpolate import PchipInterpolator

from core import qbar, dqbar_db, pace_bid, sigmoid


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
@njit(cache=True)
def _interp_row(row, x, x0, h, n):
    t = (x - x0) / h
    if t <= 0.0:
        return row[0]
    if t >= n - 1:
        return row[n - 1]
    i = int(t)
    f = t - i
    return row[i] * (1.0 - f) + row[i + 1] * f


@njit(cache=True)
def _interp_col(U, beta, il, hb, Nb):
    if beta <= 0.0:
        return 0.0
    tb = beta / hb
    if tb >= Nb - 1:
        return U[Nb - 1, il]
    ib = int(tb)
    fb = tb - ib
    return U[ib, il] * (1.0 - fb) + U[ib + 1, il] * fb


@njit(cache=True)
def _interp2(U, beta, l, hb, Nb, lmin, hl, Nl):
    if beta <= 0.0:
        return 0.0
    tb = beta / hb
    if tb >= Nb - 1:
        tb = Nb - 1 - 1e-12
    ib = int(tb)
    fb = tb - ib
    tl = (l - lmin) / hl
    if tl <= 0.0:
        il = 0
        fl = 0.0
    elif tl >= Nl - 1:
        il = Nl - 2
        fl = 1.0
    else:
        il = int(tl)
        fl = tl - il
    v0 = U[ib, il] * (1.0 - fl) + U[ib, il + 1] * fl
    v1 = U[ib + 1, il] * (1.0 - fl) + U[ib + 1, il + 1] * fl
    return v0 * (1.0 - fb) + v1 * fb


def belief_grid(thL, thH, pi0, target_h=0.05, span=13.0):
    """Log-odds grid centred at logit(pi0) that contains the b^I probing lattice."""
    delta = 0.5 * math.log(thH / thL)
    m = max(1, int(round(delta / target_h)))
    hl = delta / m
    J = int(math.ceil((span + abs(math.log(pi0 / (1 - pi0)))) / hl))
    return hl, J, m


# ---------------------------------------------------------------------------
# World A: certainty-equivalent re-pacing with a real wallet (+ probe hybrid)
# ---------------------------------------------------------------------------
@njit(cache=True, parallel=True)
def ce_worldA(thL, thH, pi0, K, hb, Nb, hl, J, m, tau_cap, learn):
    """Backward induction over (periods left n, wallet beta, log-odds l).

    learn=False freezes the belief at pi0 (re-pacing on the wallet only).
    Returns (V_CE(B) on the wallet grid, hybrid[tau, B]) where hybrid[tau] is
    the value of probing tau periods at b^I and then running CE.
    """
    l0 = math.log(pi0 / (1.0 - pi0))
    Nl = 2 * J + 1
    lmin = l0 - J * hl
    bI = math.sqrt(thL * thH)
    sr = math.sqrt(thH / thL)
    pL = sr / (1.0 + sr)
    pH = 1.0 / (1.0 + sr)
    Uprev = np.zeros((Nb, Nl))
    Ucur = np.zeros((Nb, Nl))
    hybrid = np.full((tau_cap + 1, Nb), np.nan)
    for n in range(1, K + 1):
        for ib in prange(Nb):
            beta = ib * hb
            for il in range(Nl):
                if ib == 0:
                    Ucur[ib, il] = 0.0
                    continue
                l = lmin + il * hl
                pi = sigmoid(l)
                b = pace_bid(pi, beta / n, thL, thH)
                q = qbar(pi, b, thL, thH)
                if learn:
                    lw = l + math.log((b + thL) / (b + thH))
                    ll = l + math.log(thH * (b + thL) / (thL * (b + thH)))
                else:
                    lw = l
                    ll = l
                vw = _interp2(Uprev, beta - b, lw, hb, Nb, lmin, hl, Nl)
                vl = _interp_row(Uprev[ib], ll, lmin, hl, Nl)
                Ucur[ib, il] = q * (1.0 + vw) + (1.0 - q) * vl
        for ib in prange(Nb):
            for il in range(Nl):
                Uprev[ib, il] = Ucur[ib, il]
        tau = K - n
        if learn and tau <= tau_cap:
            for ib in prange(Nb):
                B = ib * hb
                if tau * bI > B + 1e-9:
                    continue
                tot = 0.0
                for w in range(tau + 1):
                    lc = math.lgamma(tau + 1.0) - math.lgamma(w + 1.0) - math.lgamma(tau - w + 1.0)
                    PwL = math.exp(lc + w * math.log(pL) + (tau - w) * math.log(1.0 - pL))
                    PwH = math.exp(lc + w * math.log(pH) + (tau - w) * math.log(1.0 - pH))
                    Pw = pi0 * PwH + (1.0 - pi0) * PwL
                    il = J + (tau - 2 * w) * m
                    if il < 0:
                        il = 0
                    if il > Nl - 1:
                        il = Nl - 1
                    tot += Pw * (w + _interp_col(Uprev, B - w * bI, il, hb, Nb))
                hybrid[tau, ib] = tot
    out = np.empty(Nb)
    for ib in range(Nb):
        out[ib] = Uprev[ib, J]
    return out, hybrid


# ---------------------------------------------------------------------------
# World B: ex-ante budget, Lagrangian dynamic programs over (n, log-odds)
# ---------------------------------------------------------------------------
@njit(cache=True)
def myopic_bid(pi, lam, thL, thH):
    """argmax_b qbar(pi,b)(1 - lam b); the objective is strictly concave on [0,1/lam]."""
    lo = 0.0
    hi = 1.0 / lam
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        d = dqbar_db(pi, mid, thL, thH) * (1.0 - lam * mid) - lam * qbar(pi, mid, thL, thH)
        if d > 0.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-14 * (1.0 + hi):
            break
    return 0.5 * (lo + hi)


@njit(cache=True)
def known_bid(th, lam):
    return -th + math.sqrt(th * th + th / lam)


@njit(cache=True)
def _lag_step_value(b, pi, l, lam, U, lmin, hl, Nl, thL, thH):
    q = qbar(pi, b, thL, thH)
    lw = l + math.log((b + thL) / (b + thH))
    ll = l + math.log(thH * (b + thL) / (thL * (b + thH)))
    return q * (1.0 - lam * b + _interp_row(U, lw, lmin, hl, Nl)) + (1.0 - q) * _interp_row(U, ll, lmin, hl, Nl)


@njit(cache=True)
def _lag_optimal_one(thL, thH, pi0, K, lam, hl, J, nbg):
    """Bayes-optimal adaptive bidder for multiplier lam. Returns (wins, spend)."""
    l0 = math.log(pi0 / (1.0 - pi0))
    Nl = 2 * J + 1
    lmin = l0 - J * hl
    U = np.zeros(Nl)
    N = np.zeros(Nl)
    S = np.zeros(Nl)
    Un = np.zeros(Nl)
    Nn = np.zeros(Nl)
    Sn = np.zeros(Nl)
    lbmin = math.log(1e-7 * thL)
    lbmax = math.log(1.0 / lam)
    step = (lbmax - lbmin) / (nbg - 1)
    gr = 0.5 * (math.sqrt(5.0) - 1.0)
    for n in range(1, K + 1):
        for il in range(Nl):
            l = lmin + il * hl
            pi = sigmoid(l)
            best = U[il]          # b = 0: skip the auction, keep belief
            lbest = -1e300
            for k in range(nbg):
                lb = lbmin + k * step
                v = _lag_step_value(math.exp(lb), pi, l, lam, U, lmin, hl, Nl, thL, thH)
                if v > best:
                    best = v
                    lbest = lb
            if lbest > -1e299:
                a = lbest - step
                c = lbest + step
                x1 = c - gr * (c - a)
                x2 = a + gr * (c - a)
                f1 = _lag_step_value(math.exp(x1), pi, l, lam, U, lmin, hl, Nl, thL, thH)
                f2 = _lag_step_value(math.exp(x2), pi, l, lam, U, lmin, hl, Nl, thL, thH)
                for _ in range(50):
                    if f1 > f2:
                        c = x2
                        x2 = x1
                        f2 = f1
                        x1 = c - gr * (c - a)
                        f1 = _lag_step_value(math.exp(x1), pi, l, lam, U, lmin, hl, Nl, thL, thH)
                    else:
                        a = x1
                        x1 = x2
                        f1 = f2
                        x2 = a + gr * (c - a)
                        f2 = _lag_step_value(math.exp(x2), pi, l, lam, U, lmin, hl, Nl, thL, thH)
                xm = 0.5 * (a + c)
                fm = _lag_step_value(math.exp(xm), pi, l, lam, U, lmin, hl, Nl, thL, thH)
                if fm > best:
                    best = fm
                    lbest = xm
            if lbest > -1e299:
                b = math.exp(lbest)
                q = qbar(pi, b, thL, thH)
                lw = l + math.log((b + thL) / (b + thH))
                ll = l + math.log(thH * (b + thL) / (thL * (b + thH)))
                Un[il] = best
                Nn[il] = q * (1.0 + _interp_row(N, lw, lmin, hl, Nl)) + (1.0 - q) * _interp_row(N, ll, lmin, hl, Nl)
                Sn[il] = q * (b + _interp_row(S, lw, lmin, hl, Nl)) + (1.0 - q) * _interp_row(S, ll, lmin, hl, Nl)
            else:
                Un[il] = U[il]
                Nn[il] = N[il]
                Sn[il] = S[il]
        for il in range(Nl):
            U[il] = Un[il]
            N[il] = Nn[il]
            S[il] = Sn[il]
    return N[J], S[J]


@njit(cache=True)
def _lag_policy_one(thL, thH, pi0, K, lam, hl, J, kind):
    """Policy evaluation. kind 0 = myopic Bayesian (CE), kind 1 = Thompson sampling."""
    l0 = math.log(pi0 / (1.0 - pi0))
    Nl = 2 * J + 1
    lmin = l0 - J * hl
    N = np.zeros(Nl)
    S = np.zeros(Nl)
    Nn = np.zeros(Nl)
    Sn = np.zeros(Nl)
    bHk = known_bid(thH, lam)
    bLk = known_bid(thL, lam)
    for n in range(1, K + 1):
        for il in range(Nl):
            l = lmin + il * hl
            pi = sigmoid(l)
            if kind == 0:
                nb = 1
            else:
                nb = 2
            accN = 0.0
            accS = 0.0
            for j in range(nb):
                if kind == 0:
                    b = myopic_bid(pi, lam, thL, thH)
                    wgt = 1.0
                else:
                    if j == 0:
                        b = bHk
                        wgt = pi
                    else:
                        b = bLk
                        wgt = 1.0 - pi
                q = qbar(pi, b, thL, thH)
                lw = l + math.log((b + thL) / (b + thH))
                ll = l + math.log(thH * (b + thL) / (thL * (b + thH)))
                accN += wgt * (q * (1.0 + _interp_row(N, lw, lmin, hl, Nl)) + (1.0 - q) * _interp_row(N, ll, lmin, hl, Nl))
                accS += wgt * (q * (b + _interp_row(S, lw, lmin, hl, Nl)) + (1.0 - q) * _interp_row(S, ll, lmin, hl, Nl))
            Nn[il] = accN
            Sn[il] = accS
        for il in range(Nl):
            N[il] = Nn[il]
            S[il] = Sn[il]
    return N[J], S[J]


@njit(cache=True)
def _etc_exante_one(thL, thH, pi0, K, lam, tau_cap):
    """ETC re-solved under ex-ante accounting: probe tau at b^I, then a
    w-contingent constant bid; one multiplier for all histories."""
    bI = math.sqrt(thL * thH)
    r = thH / thL
    sr = math.sqrt(r)
    pL = sr / (1.0 + sr)
    pH = 1.0 / (1.0 + sr)
    lk0 = math.log(pi0 / (1.0 - pi0))
    lr = math.log(r)
    N = np.zeros(tau_cap + 1)
    S = np.zeros(tau_cap + 1)
    for tau in range(tau_cap + 1):
        n = K - tau
        for w in range(tau + 1):
            lc = math.lgamma(tau + 1.0) - math.lgamma(w + 1.0) - math.lgamma(tau - w + 1.0)
            PwL = math.exp(lc + w * math.log(pL) + (tau - w) * math.log(1.0 - pL))
            PwH = math.exp(lc + w * math.log(pH) + (tau - w) * math.log(1.0 - pH))
            Pw = pi0 * PwH + (1.0 - pi0) * PwL
            pi = sigmoid(lk0 + 0.5 * (tau - 2.0 * w) * lr)
            b = myopic_bid(pi, lam, thL, thH)
            q = qbar(pi, b, thL, thH)
            N[tau] += Pw * (w + n * q)
            S[tau] += Pw * (w * bI + n * b * q)
    return N, S


@njit(cache=True, parallel=True)
def lag_sweep(thL, thH, pi0, K, lams, hl, J, kind, nbg):
    """kind: 0 CE-myopic, 1 TS, 2 Bayes-optimal."""
    Ns = np.empty(lams.size)
    Ss = np.empty(lams.size)
    for i in prange(lams.size):
        if kind == 2:
            a, b = _lag_optimal_one(thL, thH, pi0, K, lams[i], hl, J, nbg)
        else:
            a, b = _lag_policy_one(thL, thH, pi0, K, lams[i], hl, J, kind)
        Ns[i] = a
        Ss[i] = b
    return Ns, Ss


@njit(cache=True, parallel=True)
def etc_exante_sweep(thL, thH, pi0, K, lams, tau_cap):
    Ns = np.empty((lams.size, tau_cap + 1))
    Ss = np.empty((lams.size, tau_cap + 1))
    for i in prange(lams.size):
        a, b = _etc_exante_one(thL, thH, pi0, K, lams[i], tau_cap)
        Ns[i, :] = a
        Ss[i, :] = b
    return Ns, Ss


# ---------------------------------------------------------------------------
# turning (spend, wins) parametric curves into V(B) on a budget grid
# ---------------------------------------------------------------------------
def curve_to_grid(S, N, grid):
    """V(B) on grid from parametric points (S(lam), N(lam)); NaN outside range."""
    o = np.argsort(S)
    S = S[o]
    N = N[o]
    keep = np.concatenate(([True], np.diff(S) > 1e-12))
    S, N = S[keep], N[keep]
    # spend 0 <-> wins 0
    if S[0] > 1e-9:
        S = np.concatenate(([0.0], S))
        N = np.concatenate(([0.0], N))
    f = PchipInterpolator(S, N, extrapolate=False)
    return f(grid)


def curve_to_grid_hermite(S, N, lam, grid):
    """Same as curve_to_grid but uses the exact slope dV/dB = lam (valid for
    policies that are optimal for their Lagrangian, e.g. Bayes-optimal, ETC_B)."""
    from scipy.interpolate import CubicHermiteSpline
    o = np.argsort(S)
    S, N, lam = S[o], N[o], lam[o]
    keep = np.concatenate(([True], np.diff(S) > 1e-9))
    S, N, lam = S[keep], N[keep], lam[keep]
    f = CubicHermiteSpline(S, N, lam, extrapolate=False)
    out = f(grid)
    lo = grid < S[0]
    if lo.any():  # below the smallest computed spend: PCHIP through (0,0)
        g = PchipInterpolator(np.concatenate(([0.0], S[:3])), np.concatenate(([0.0], N[:3])))
        out[lo] = g(grid[lo])
    return out


def lam_targets(spend_fn, Bmax, n_coarse=120, n_fine=700, lam_lo=1e-6, lam_hi=200.0):
    """Two-pass choice of multipliers so that spends are ~uniform on [0, Bmax]."""
    lams = np.exp(np.linspace(np.log(lam_lo), np.log(lam_hi), n_coarse))
    S = spend_fn(lams)
    o = np.argsort(S)
    S, L = S[o], np.log(lams[o])
    targets = np.concatenate((np.geomspace(0.02, 5.0, 60), np.geomspace(5.0, Bmax * 1.02, n_fine // 2),
                              np.linspace(5.0, Bmax * 1.02, n_fine - n_fine // 2)))
    lt = np.interp(targets, S, L)
    return np.unique(np.exp(lt))
