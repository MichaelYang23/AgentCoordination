"""Where do the full bandit (DP) and the decomposition agree?

Full bandit   = Bayes-optimal policy, solved by dynamic programming (ex-ante budget rule: expected total
                spend <= B); it learns and executes in every auction.
Decomposition = learn for tau auctions at the fixed probe bid b^I, then execute one bid chosen from the
                number of wins w. Two versions:
                  same rule   - re-solved under the ex-ante rule (key etc_B): isolates the structure;
                  paper's rule - the paper's (smoothed) model (key etc_smooth).

Two closeness measures, from the sweep caches (run_sweep.py; no new simulation):
  value of learning  ratio [V_dec(B) - W(B)] / [V_fb(B) - W(B)] at per-period budget rho = B/K;
  skewness           the planner's shift a - a^E of the senior budget at total budget per period t = T/K:
                     same direction and similar size (ratio in [1/2, 2]), same direction but size differs by
                     more than 2x, neither shifts, only one shifts, opposite directions.
Writes results/region_map_summary.txt, results/region_map.json and results/fig_region_map.png.
"""
import glob
import json
import math
import os
import re

import numpy as np
from matplotlib.patches import Patch

import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")

FB = "opt_B"
DEC = {"same": "etc_B", "paper": "etc_smooth"}
COLS = ["#d4302f", "#f0908e", "#e6e4de", "#86b6ef", "#256abf"]   # category 0..4, far -> close
VAL_LABELS = ["< 20% of the full bandit's", "20–50%", "learning adds < 0.5% for both", "50–80%", "≥ 80% (close)"]
SKEW_LABELS = ["opposite direction", "only one of them shifts", "neither shifts",
               "same direction, size differs > 2×", "same direction, similar size"]
NEGLIGIBLE = 0.005            # full bandit's learning value below 0.5% of W: nothing to compare
RHO = np.geomspace(0.05, 10.0, 55)   # the decomposition's lambda sweep under-covers the last ~5% of each
                                     # budget range (rho > ~11 when it ends at 12K), so stop at 10
T_EDGES = np.geomspace(0.2, 12.0, 49)
THH = [2, 4, 8, 16, 32]


def load_values():
    out = {}
    files = glob.glob(os.path.join(CACHE, "v2_thL0.5_thH*_hlB0.04.npz"))
    files += glob.glob(os.path.join(CACHE, "dp_thL0.5_thH*_hlB0.04.npz"))      # run_dp_largeK.py
    for f in files:
        m = re.search(r"thH(\d+)_pi([\d.]+)_K(\d+)_B", os.path.basename(f))
        thH, pi0, K = int(m.group(1)), float(m.group(2)), int(m.group(3))
        out[(thH, pi0, K)] = dict(np.load(f))
    return out


def value_categories(C, K):
    g = C["grid"]
    idx = np.clip(np.searchsorted(g, RHO * K), 0, g.size - 1)
    W = C["W"][idx]
    pf = C[FB][idx] - W
    res = {}
    for name, key in DEC.items():
        pd_ = np.maximum(C[key][idx] - W, 0.0)
        ratio = np.where(pf > 0, pd_ / np.where(pf > 0, pf, 1.0), np.nan)
        cat = np.select([ratio >= 0.8, ratio >= 0.5, ratio >= 0.2], [4, 3, 1], 0)
        cat = np.where(pf < NEGLIGIBLE * W, 2, cat)
        res[name] = (cat, np.clip(ratio, 0, 1))
    return res


def skew_point_categories(T, a_dec, a_fb):
    tol = 0.1 + 0.001 * T
    sd = np.where(np.abs(a_dec) < tol, 0, np.sign(a_dec))
    sf = np.where(np.abs(a_fb) < tol, 0, np.sign(a_fb))
    same = (sd == sf) & (sd != 0)
    r = np.divide(a_dec, a_fb, out=np.zeros_like(a_dec), where=np.abs(a_fb) > 0)
    cat = np.full(T.size, 1)
    cat[(sd == 0) & (sf == 0)] = 2
    cat[same] = 3
    cat[same & (r >= 0.5) & (r <= 2.0)] = 4
    cat[(sd * sf) < 0] = 0
    return cat


def load_shift(thH, pi0, K, v):
    for prefix in ("shift", "dpshift"):
        f = os.path.join(CACHE, "%s_thH%d_pi%s_K%d_v%s.npz" % (prefix, thH, ("%g" % pi0), K, ("%g" % v)))
        if os.path.exists(f):
            return np.load(f)
    return None


def switch_point(T, s, K):
    """First t = T/K at which the shift turns from positive (more skewed) to negative (more balanced)."""
    tol = 0.1 + 0.001 * T
    sg = np.where(np.abs(s) < tol, 0, np.sign(s))
    pos = np.where(sg > 0)[0]
    if pos.size == 0:
        return None
    after = np.where((sg < 0) & (np.arange(sg.size) > pos[0]))[0]
    return round(float(T[after[0]] / K), 2) if after.size else None


def skew_categories(thH, pi0, K, v):
    S = load_shift(thH, pi0, K, v)
    T = S["T"]
    t = T / K
    res, pts = {}, {}
    for name, key in DEC.items():
        c = skew_point_categories(T, S[key], S[FB])
        pts[name] = c
        b = np.full(T_EDGES.size - 1, -1)
        for i in range(T_EDGES.size - 1):
            sel = (t >= T_EDGES[i]) & (t < T_EDGES[i + 1])
            if sel.any():
                b[i] = np.bincount(c[sel], minlength=5).argmax()
        res[name] = b
    return res, pts


def probe_share(r, K=100):
    return math.log(K) / (K * math.log((1 + math.sqrt(r)) / (2 * r ** 0.25)))


def intervals(x, mask):
    out, start = [], None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        if (not m or i == len(mask) - 1) and start is not None:
            end = i if m else i - 1
            out.append((round(float(x[start]), 2), round(float(x[end]), 2)))
            start = None
    return out


def main():
    vals = load_values()
    summary, lines = {}, []

    # ---------------- baseline slice: pi0 = 0.5, K = 100, v1/v2 = 2
    vmap = {n: np.full((len(THH), RHO.size), np.nan) for n in DEC}
    smap = {n: np.full((len(THH), T_EDGES.size - 1), np.nan) for n in DEC}
    lines.append("Full bandit (DP) vs decomposition, pi0 = 0.5, K = 100 (skewness at v1/v2 = 2)")
    for i, thH in enumerate(THH):
        r = thH / 0.5
        vc = value_categories(vals[(thH, 0.5, 100)], 100)
        sc, sp = skew_categories(thH, 0.5, 100, 2.0)
        for n in DEC:
            vmap[n][i] = vc[n][0]
            smap[n][i] = np.where(sc[n] < 0, np.nan, sc[n])
            close = intervals(RHO, vc[n][0] == 4)
            agree = np.isin(sp[n], (3, 4)).mean()
            lines.append("  r=%2d (probes %3.0f%% of K)  %-5s  value of learning >= 80%% on rho in %s ;"
                         "  skewness same direction %.0f%% of T (similar size %.0f%%, opposite %.0f%%)"
                         % (r, 100 * probe_share(r), n, close, 100 * agree, 100 * (sp[n] == 4).mean(),
                            100 * (sp[n] == 0).mean()))
            summary.setdefault(n, {})["r%d" % r] = {"value_close_rho": close, "skew_same_dir": round(float(agree), 3)}

    # ---------------- all K = 100 configurations: shares by r, pi0, v1/v2
    def pooled(filter_fn):
        acc = {n: {"val": [], "skew": []} for n in DEC}
        for (thH, pi0, K), C in vals.items():
            if K != 100 or not filter_fn(thH, pi0, None):
                continue
            vc = value_categories(C, K)
            for n in DEC:
                acc[n]["val"].append(vc[n][0])
            for v in (1.25, 1.5, 2.0, 3.0, 4.0):
                if not filter_fn(thH, pi0, v):
                    continue
                _, sp = skew_categories(thH, pi0, K, v)
                for n in DEC:
                    acc[n]["skew"].append(sp[n])
        out = {}
        for n in DEC:
            vv = np.concatenate(acc[n]["val"])
            ss = np.concatenate(acc[n]["skew"])
            nonneg = vv != 2
            out[n] = (np.mean(vv[nonneg] == 4), np.mean(np.isin(vv[nonneg], (3, 4))),
                      np.mean(np.isin(ss, (3, 4))), np.mean(ss == 4), np.mean(ss == 0))
        return out

    lines.append("\nAll K = 100 configurations (value: share of budgets where learning is not negligible;"
                 " skewness: share of T points)")
    lines.append("  %-14s %-6s %10s %10s %12s %12s %10s" % ("group", "dec", "val>=80%", "val>=50%",
                                                          "skew same", "skew similar", "opposite"))
    groups = [("r=%d" % (thH * 2), (lambda th: (lambda a, b, c: a == th))(thH)) for thH in THH]
    groups += [("pi0=%g" % p, (lambda pp: (lambda a, b, c: b == pp))(p)) for p in (0.2, 0.35, 0.5, 0.65, 0.8)]
    groups += [("v1/v2=%g" % v, (lambda vv: (lambda a, b, c: c is None or c == vv))(v))
               for v in (1.25, 1.5, 2.0, 3.0, 4.0)]
    groups += [("all", lambda a, b, c: True)]
    for gname, fn in groups:
        res = pooled(fn)
        for n in DEC:
            a, b, c, d, e = res[n]
            lines.append("  %-14s %-6s %9.0f%% %9.0f%% %11.0f%% %11.0f%% %9.0f%%" % (gname, n, 100 * a, 100 * b,
                                                                                 100 * c, 100 * d, 100 * e))
            summary.setdefault("pooled", {}).setdefault(gname, {})[n] = [round(float(x), 3) for x in res[n]]

    # ---------------- horizon K: r = 8, 16, 32 at pi0 = 0.5, K = 50 ... 400
    KS = [50, 100, 200, 400]
    RS = [4, 8, 16]                        # thH; r = 2 thH
    kmap = {}
    lines.append("\nHorizon K (pi0 = 0.5). value: ratio at rho = 1, 2.5, 5, 10 and the rho-range with ratio >= 0.8;"
                 " skewness at v1/v2 = 2: same direction / similar size / opposite; switch point t (more skewed ->"
                 " more balanced) of the decomposition vs the full bandit")
    for thH in RS:
        for K in KS:
            if (thH, 0.5, K) not in vals or load_shift(thH, 0.5, K, 2.0) is None:
                continue
            vc = value_categories(vals[(thH, 0.5, K)], K)
            sc, sp = skew_categories(thH, 0.5, K, 2.0)
            S = load_shift(thH, 0.5, K, 2.0)
            for n in DEC:
                rr = [float(np.interp(math.log(x), np.log(RHO), vc[n][1])) for x in (1.0, 2.5, 5.0, 10.0)]
                close = intervals(RHO, vc[n][0] == 4)
                same = float(np.isin(sp[n], (3, 4)).mean())
                sim = float((sp[n] == 4).mean())
                opp = float((sp[n] == 0).mean())
                sw_d, sw_f = switch_point(S["T"], S[DEC[n]], K), switch_point(S["T"], S[FB], K)
                lines.append("  r=%2d K=%3d %-5s ratio %s  close rho %s  skew same %3.0f%% similar %3.0f%% opposite"
                             " %3.0f%%  switch t: dec %s vs full bandit %s"
                             % (2 * thH, K, n, " ".join("%.2f" % x for x in rr), close, 100 * same, 100 * sim,
                                100 * opp, sw_d, sw_f))
                summary.setdefault("K", {})["r%d_K%d_%s" % (2 * thH, K, n)] = {
                    "ratio_at_rho_1_2.5_5_10": [round(x, 3) for x in rr], "close_rho": close,
                    "skew_same": round(same, 3), "skew_similar": round(sim, 3), "skew_opposite": round(opp, 3),
                    "switch_dec": sw_d, "switch_full_bandit": sw_f}
            kmap[(thH, K)] = (vc["same"][0], np.where(sc["same"] < 0, np.nan, sc["same"]))

    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(RES, "region_map_summary.txt"), "w") as f:
        f.write(txt + "\n")
    with open(os.path.join(RES, "region_map.json"), "w") as f:
        json.dump(summary, f, indent=1)

    # ---------------- figure
    ps.setup()
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 7.4), sharey=True)
    titles = {"same": "Decomposition under the same budget rule as the DP",
              "paper": "Decomposition as in the paper (paper's budget rule)"}
    rho_edges = np.sqrt(RHO[1:] * RHO[:-1])
    rho_edges = np.concatenate(([RHO[0] ** 2 / rho_edges[0]], rho_edges, [RHO[-1] ** 2 / rho_edges[-1]]))
    for j, n in enumerate(("same", "paper")):
        for row, (data, edges) in enumerate(((vmap[n], rho_edges), (smap[n], T_EDGES))):
            ax = axes[row, j]
            for i in range(len(THH)):
                for k in range(data.shape[1]):
                    c = data[i, k]
                    if np.isnan(c):
                        continue
                    ax.fill_between([edges[k], edges[k + 1]], i - 0.4, i + 0.4, color=COLS[int(c)], lw=0)
            ax.set_xscale("log")
            ax.set_xlim(edges[0], edges[-1])
            ax.set_ylim(-0.6, len(THH) - 0.4)
            ax.grid(False)
            ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10] if row == 0 else [0.2, 0.5, 1, 2, 5, 10])
            ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"] if row == 0 else
                               ["0.2", "0.5", "1", "2", "5", "10"])
            ax.minorticks_off()
            if row == 0:
                ax.set_title(titles[n], loc="left")
                ax.set_xlabel("Team budget per period ρ = B/K")
            else:
                ax.set_xlabel("Total budget per period t = T/K   (senior value = 2 × junior)")
    for row in range(2):
        axes[row, 0].set_yticks(range(len(THH)))
        axes[row, 0].set_yticklabels(["r = %d  (%.0f%%)" % (2 * th, 100 * probe_share(2 * th)) for th in THH])
        axes[row, 0].set_ylabel(("Value of learning\n" if row == 0 else "Skewness of the split\n") +
                                "state separation r  (probes needed / K)")
    h1 = [Patch(color=COLS[c], label=VAL_LABELS[c]) for c in (4, 3, 2, 1, 0)]
    h2 = [Patch(color=COLS[c], label=SKEW_LABELS[c]) for c in (4, 3, 2, 1, 0)]
    fig.legend(handles=h1, loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=5, fontsize=8.5,
               title="Value of learning: decomposition as a share of the full bandit's", title_fontsize=9)
    fig.legend(handles=h2, loc="upper center", bbox_to_anchor=(0.5, 0.505), ncol=5, fontsize=8.5,
               title="Skewness: change of the senior budget, decomposition vs. full bandit", title_fontsize=9)
    fig.text(0.5, 0.004, "π0 = 0.5, K = 100, θ_L = 0.5. Full bandit = Bayes-optimal policy by dynamic programming "
             "(ex-ante budget rule). Summary over all π0, v1/v2 and K in results/region_map_summary.txt.",
             ha="center", va="bottom", fontsize=8, color=ps.MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.9), h_pad=6.0)
    fig.savefig(os.path.join(RES, "fig_region_map.png"), dpi=170)
    print("-> results/fig_region_map.png")

    fig, axes = plt.subplots(2, len(RS), figsize=(15, 6.6), sharey=True)
    for j, thH in enumerate(RS):
        for row, edges in enumerate((rho_edges, T_EDGES)):
            ax = axes[row, j]
            for i, K in enumerate(KS):
                if (thH, K) not in kmap:
                    continue
                data = kmap[(thH, K)][row]
                for k in range(data.size):
                    if np.isnan(data[k]):
                        continue
                    ax.fill_between([edges[k], edges[k + 1]], i - 0.4, i + 0.4, color=COLS[int(data[k])], lw=0)
            ax.set_xscale("log")
            ax.set_xlim(edges[0], edges[-1])
            ax.set_ylim(-0.6, len(KS) - 0.4)
            ax.grid(False)
            ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10] if row == 0 else [0.2, 0.5, 1, 2, 5, 10])
            ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"] if row == 0 else
                               ["0.2", "0.5", "1", "2", "5", "10"])
            ax.minorticks_off()
            if row == 0:
                ax.set_title("r = %d" % (2 * thH), loc="left")
                ax.set_xlabel("Team budget per period ρ = B/K")
            else:
                ax.set_xlabel("Total budget per period t = T/K   (v1/v2 = 2)")
        for row in range(2):
            axes[row, 0].set_yticks(range(len(KS)))
            axes[row, 0].set_yticklabels(["K = %d" % K for K in KS])
    axes[0, 0].set_ylabel("Value of learning\nhorizon K")
    axes[1, 0].set_ylabel("Skewness of the split\nhorizon K")
    fig.legend(handles=h1, loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=5, fontsize=8.5,
               title="Value of learning: decomposition as a share of the full bandit's", title_fontsize=9)
    fig.legend(handles=h2, loc="upper center", bbox_to_anchor=(0.5, 0.505), ncol=5, fontsize=8.5,
               title="Skewness: change of the senior budget, decomposition vs. full bandit", title_fontsize=9)
    fig.text(0.5, 0.004, "π0 = 0.5, θ_L = 0.5. Both under the same (ex-ante) budget rule; full bandit = Bayes-optimal "
             "policy by dynamic programming. Numbers in results/region_map_summary.txt.",
             ha="center", va="bottom", fontsize=8, color=ps.MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.9), h_pad=6.0)
    fig.savefig(os.path.join(RES, "fig_region_vs_K.png"), dpi=170)
    print("-> results/fig_region_vs_K.png")


if __name__ == "__main__":
    main()
