"""Value of FREE perfect information under the two accountings.

World A (paper): after the signal the agent must spend its budget in
expectation under its new belief, so VPI_A(rho) = pi0 g(1;rho) + (1-pi0) g(0;rho)
- g(pi0;rho), per period.
World B (ex-ante): the informed agent may spend different amounts in the two
states as long as the prior-expected spend is rho.

Small-rho asymptotics (q ~ b/theta):  VPI_A / sqrt(rho) ->
  pi0/sqrt(thH) + (1-pi0)/sqrt(thL) - sqrt(pi0/thH + (1-pi0)/thL) < 0 (Jensen),
while VPI_B is second order.
"""
import math
import os

import numpy as np

from core import g_rate
from bandits import known_bid
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))


def vpi_A(rho, thL, thH, pi0):
    return pi0 * g_rate(1.0, rho, thL, thH) + (1 - pi0) * g_rate(0.0, rho, thL, thH) - g_rate(pi0, rho, thL, thH)


def vpi_B(rho, thL, thH, pi0):
    # find lambda s.t. prior-expected spend with state-known bids = rho
    def spend(lam):
        bH, bL = known_bid(thH, lam), known_bid(thL, lam)
        return pi0 * bH * bH / (bH + thH) + (1 - pi0) * bL * bL / (bL + thL)
    lo, hi = 1e-12, 1e6
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if spend(mid) > rho:
            lo = mid
        else:
            hi = mid
    lam = math.sqrt(lo * hi)
    bH, bL = known_bid(thH, lam), known_bid(thL, lam)
    wins = pi0 * bH / (bH + thH) + (1 - pi0) * bL / (bL + thL)
    return wins - g_rate(pi0, rho, thL, thH)


def crossing(f, lo=1e-4, hi=50.0):
    rs = np.geomspace(lo, hi, 4000)
    v = np.array([f(r) for r in rs])
    i = np.where((v[:-1] < 0) & (v[1:] >= 0))[0]
    return rs[i[0]] if i.size else np.nan


if __name__ == "__main__":
    rows = []
    for thH in (2.0, 4.0, 8.0, 16.0, 32.0):
        for pi0 in (0.2, 0.3, 0.5, 0.7, 0.8):
            thL = 0.5
            c = crossing(lambda r: vpi_A(r, thL, thH, pi0))
            lim = pi0 / math.sqrt(thH) + (1 - pi0) / math.sqrt(thL) - math.sqrt(pi0 / thH + (1 - pi0) / thL)
            rows.append((thH, pi0, c, lim))
            print("thH=%5.1f pi0=%.1f : free perfect info harmful for rho < %.3f   (small-rho slope %.4f)" % (thH, pi0, c, lim))
    ps.setup()
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    rs = np.geomspace(0.01, 40, 600)
    A = np.array([vpi_A(r, 0.5, 8.0, 0.5) for r in rs])
    B = np.array([vpi_B(r, 0.5, 8.0, 0.5) for r in rs])
    ax.plot(rs * 100, A * 100, color=ps.COLORS["etc_smooth"], label="Paper accounting (spend wallet under current belief)")
    ax.plot(rs * 100, B * 100, color=ps.COLORS["opt_B"], label="Ex-ante accounting")
    ps.zero_line(ax)
    ax.set_xscale("log")
    ax.set_xlabel("Team budget B = 100·rho (K = 100)")
    ax.set_ylabel("Value of free perfect information (impressions)")
    ax.set_title("Free information can hurt under the paper's accounting")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "results", "fig_free_information.png"), dpi=170)
    np.savetxt(os.path.join(HERE, "results", "free_information_threshold.csv"), np.array(rows),
               delimiter=",", header="thH,pi0,rho_threshold_A,small_rho_slope_A", comments="", fmt="%.6g")
