"""Explainer figures.

1. fig_agents_explained.png: what the paper's ETC team and the learn-while-doing (CE) agent do in one
   simulated campaign (same random auction draws for both), against the no-learning benchmark W.
2. fig_agreement_summary.png: how often learning moves the planner's split in the same direction under
   each design (K = 100 factorial sweep, inside the paper's two regimes R1+R2), overall and by r.
"""
import csv
import math
import os

import numpy as np

from matplotlib.ticker import NullFormatter

from core import pace_bid, etc_exact_curve_capped
import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

thL, thH, pi0, K, B = 0.5, 8.0, 0.5, 100, 150.0
bI = math.sqrt(thL * thH)
GRAY = "#898781"
PMIN = 1e-5                                        # belief axis limits (log-odds scale)
SAME, ZERO, OPP = "#2a78d6", "#d3d1c9", "#e34948"   # diverging pair: blue <-> red, neutral gray


def q(theta, b):
    return b / (b + theta)


def update(pi, b, win):
    qh, ql = q(thH, b), q(thL, b)
    lh, ll = (qh, ql) if win else (1.0 - qh, 1.0 - ql)
    return pi * lh / (pi * lh + (1.0 - pi) * ll)


def simulate(theta, U, tau):
    """Bids b_t (t = 1..K) and beliefs after t auctions (t = 0..K) for W, ETC and CE."""
    out = {}
    b0 = pace_bid(pi0, B / K, thL, thH)
    out["W"] = (np.full(K, b0), np.full(K + 1, pi0))
    # ETC: probing agent bids b^I for tau auctions, then the exploitation agent commits to one paced bid
    bids, pis, pi, w = [], [pi0], pi0, 0
    for t in range(tau):
        win = U[t] < q(theta, bI)
        pi = update(pi, bI, win)
        w += int(win)
        bids.append(bI)
        pis.append(pi)
    bE = pace_bid(pi, (B - w * bI) / (K - tau), thL, thH)
    bids += [bE] * (K - tau)
    pis += [pi] * (K - tau)
    out["ETC"] = (np.array(bids), np.array(pis))
    # CE: after every auction update the belief and re-pace the remaining (real) wallet
    bids, pis, pi, R = [], [pi0], pi0, B
    for t in range(K):
        b = pace_bid(pi, R / (K - t), thL, thH) if R > 1e-9 else 0.0
        b = min(b, R)
        win = b > 0 and U[t] < q(theta, b)
        if b > 0:
            pi = update(pi, b, win)
        if win:
            R -= b
        bids.append(b)
        pis.append(pi)
    out["CE"] = (np.array(bids), np.array(pis))
    return out, w


def figure_agents():
    _, taus = etc_exact_curve_capped(np.array([B]), thL, thH, pi0, K, 150)
    tau = int(taus[0])
    # first seed whose probe outcome is typical in both markets (posterior on the correct side after tau probes)
    for seed in range(1000):
        U = np.random.default_rng(seed).random(K)
        hard, wh = simulate(thH, U, tau)
        easy, we = simulate(thL, U, tau)
        if hard["ETC"][1][tau] > 0.8 and easy["ETC"][1][tau] < 0.2:
            break
    t_bid = np.arange(1, K + 1)
    t_pi = np.arange(0, K + 1)
    style = {
        "W": dict(color=GRAY, lw=1.5, ls=(0, (4, 2.5)), label="No learning (W): bid from the prior, never updates"),
        "ETC": dict(color=ps.COLORS["etc_smooth"], lw=2.0,
                    label="ETC team (paper): probe %d auctions at fixed bid $b^I$=%.0f, then commit to one bid" % (tau, bI)),
        "CE": dict(color=ps.COLORS["ce_A"], lw=2.0,
                   label="Learn-while-doing (CE): update belief and re-pace the wallet after every auction"),
    }
    ps.setup()
    fig, axes = plt.subplots(2, 2, figsize=(12, 6.6), sharex=True, sharey="row")
    for c, (name, run, w) in enumerate((("Hard market (true $\\theta=\\theta_H$=8)", hard, wh),
                                        ("Easy market (true $\\theta=\\theta_L$=0.5)", easy, we))):
        axb, axp = axes[0, c], axes[1, c]
        for ax in (axb, axp):
            ax.axvspan(0.5, tau + 0.5, color=ps.COLORS["etc_smooth"], alpha=0.08, lw=0, zorder=0)
            ax.axvline(tau + 0.5, color=ps.COLORS["etc_smooth"], lw=0.9, ls=":", zorder=1)
        for key in ("W", "ETC", "CE"):
            bids, pis = run[key]
            axb.step(t_bid, bids, where="mid", zorder=3 if key != "W" else 2, **style[key])
            axp.plot(t_pi, np.clip(pis, PMIN, 1 - PMIN), zorder=3 if key != "W" else 2, **style[key])
        axb.set_title(name, loc="left")
        axb.text(tau / 2 + 0.5, 0.97, "probing\nagent", transform=axb.get_xaxis_transform(),
                 ha="center", va="top", fontsize=7.5, color=ps.INK2)
        axb.text(tau + 2.5, 0.97, "← pure learning   |   hand-off after %d probes (%d wins)  →  exploitation agent:\n"
                 "one fixed bid, no more learning" % (tau, w), transform=axb.get_xaxis_transform(),
                 ha="left", va="top", fontsize=8, color=ps.INK2)
        axp.set_yscale("logit")
        axp.set_ylim(PMIN, 1 - PMIN)
        axp.set_yticks([1e-4, 1e-2, 0.5, 0.99, 0.9999])
        axp.set_yticklabels(["0.0001", "0.01", "0.5", "0.99", "0.9999"])
        axp.yaxis.set_minor_formatter(NullFormatter())
        axp.set_xlabel("Auction t   (horizon K = %d, budget B = %.0f, prior Pr(hard) = %.1f)" % (K, B, pi0))
        pe = run["ETC"][1][tau]
        axp.annotate("ETC's belief is frozen at hand-off", (60, pe), xytext=(0, -16 if pe > 0.5 else 12),
                     textcoords="offset points", ha="center", va="center", fontsize=8, color=ps.INK2)
        axp.annotate("CE keeps learning", (35, 1 - PMIN if pe > 0.5 else PMIN), xytext=(0, -9 if pe > 0.5 else 9),
                     textcoords="offset points", ha="center", va="center", fontsize=8, color=ps.INK2)
    ce_bids = hard["CE"][0]
    axes[0, 0].annotate("CE re-paces what is left in the wallet:\nfew auctions left → higher bids", (K - 2, ce_bids[K - 3]),
                        xytext=(-150, 18), textcoords="offset points", ha="left", va="center", fontsize=8,
                        color=ps.INK2, arrowprops=dict(arrowstyle="-", color=ps.MUTED, lw=0.8))
    axes[0, 0].set_ylabel("Bid in auction t")
    axes[1, 0].set_ylabel("Belief Pr(market is hard)\n(log-odds scale)")
    ymax = max(max(r[k][0].max() for k in r) for r in (hard, easy))
    axes[0, 0].set_ylim(0, ymax * 1.32)
    axes[0, 0].set_xlim(0, K + 0.5)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=1, bbox_to_anchor=(0.5, 1.0), fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    path = os.path.join(RES, "fig_agents_explained.png")
    fig.savefig(path, dpi=170)
    print("seed", seed, "tau", tau, "probe wins (hard, easy)", wh, we, "->", path)


def figure_agreement():
    rows = list(csv.DictReader(open(os.path.join(RES, "sweep_regime_agreement.csv"))))
    rows = [r for r in rows if int(r["K"]) == 100 and int(r["regime"]) in (1, 2)]
    comps = [("ce_A", "Learn-while-doing (CE)\nvs. ETC"),
             ("etc_exact", "Benchmark: the paper's exact ETC\nvs. its smoothed ETC"),
             ("opt_B", "Bayes-optimal bandit (ex-ante budget)\nvs. ETC")]

    def pooled(agent, r=None):
        sel = [x for x in rows if x["agent"] == agent and (r is None or float(x["r"]) == r)]
        n = np.array([float(x["n_T"]) for x in sel])
        same = np.array([float(x["share_same_sign"]) for x in sel])
        opp = np.array([float(x["share_opposite_sign"]) for x in sel])
        return (n * same).sum() / n.sum(), (n * opp).sum() / n.sum()

    ps.setup()
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(12.5, 4.4), gridspec_kw={"width_ratios": [1.2, 1]})
    ys = np.arange(len(comps))[::-1]
    for y, (agent, lab) in zip(ys, comps):
        s, o = pooled(agent)
        z = 1.0 - s - o
        left = 0.0
        for val, col, txt in ((s, SAME, "same direction"), (z, ZERO, "one side ≈ 0"), (o, OPP, "opposite")):
            axa.barh(y, val, left=left, height=0.56, color=col, edgecolor=ps.SURFACE, linewidth=2,
                     label=txt if y == ys[0] else None)
            left += val
        axa.text(s / 2, y, "%.0f%%" % (100 * s), ha="center", va="center", fontsize=9.5, color="white",
                 fontweight="bold")
        axa.text(1.012, y, "opposite %.0f%%" % (100 * o), ha="left", va="center", fontsize=8.5, color=ps.INK2)
        print("%-10s same %.3f  opposite %.3f" % (agent, s, o))
    axa.set_yticks(ys)
    axa.set_yticklabels([lab for _, lab in comps], fontsize=8.8)
    axa.tick_params(axis="y", labelcolor=ps.INK2)
    axa.set_xlim(0, 1.0)
    axa.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    axa.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    axa.grid(axis="y", visible=False)
    axa.set_xlabel("Share of budget levels T inside the paper's two regimes\n"
                   "(125 scenarios: 25 markets × 5 value ratios, K = 100)")
    axa.set_title("Does learning move the split in the same direction?", loc="left")
    axa.legend(loc="upper center", bbox_to_anchor=(0.45, -0.3), ncol=3, fontsize=8.5)

    rs = [4.0, 8.0, 16.0, 32.0, 64.0]
    for agent, lab in comps:
        vals = [pooled(agent, r)[0] for r in rs]
        short = {"ce_A": "CE vs ETC", "etc_exact": "exact vs smoothed ETC", "opt_B": "Bayes-optimal (ex-ante) vs ETC"}[agent]
        axb.plot(rs, vals, color=ps.COLORS[agent], lw=2.0, marker="o", ms=7, mec=ps.SURFACE, mew=1.5, label=short)
        anchor, off, ha = {"ce_A": ((4.0, vals[0]), (9, -4), "left"),
                           "etc_exact": ((8.0, vals[1]), (8, -9), "left"),
                           "opt_B": ((32.0, vals[3]), (0, -13), "center")}[agent]
        axb.annotate(short, anchor, xytext=off, textcoords="offset points", fontsize=8.5, color=ps.INK2,
                     va="center", ha=ha)
        print("%-10s by r: %s" % (agent, " ".join("%.2f" % v for v in vals)))
    lk = math.log(100)
    share = [lk / (100 * math.log((1 + math.sqrt(r)) / (2 * r ** 0.25))) for r in rs]
    axb.set_xscale("log", base=2)
    axb.set_xticks(rs)
    axb.set_xticklabels(["%d\n(%.0f%%)" % (r, 100 * s) for r, s in zip(rs, share)])
    axb.minorticks_off()
    axb.set_ylim(0, 1.05)
    axb.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    axb.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    axb.set_xlabel("State separation $r=\\theta_H/\\theta_L$\n(in brackets: probes needed to learn the state / K)")
    axb.set_ylabel("Same direction")
    axb.set_title("Agreement by state separation r", loc="left")
    axb.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    path = os.path.join(RES, "fig_agreement_summary.png")
    fig.savefig(path, dpi=170)
    print("->", path)


if __name__ == "__main__":
    figure_agents()
    figure_agreement()
