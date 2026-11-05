"""Summarise the sweep: sign agreement of the allocation shift, by agent and region."""
import glob
import os
import re

import numpy as np

import plotstyle as ps
from plotstyle import plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")
AG = ["etc_exact", "etc_adapt", "ce_A", "opt_B", "ts_B", "etc_B"]


def tol(T):
    return 0.1 + 0.001 * T


def sgn(x, T):
    s = np.sign(x)
    s[np.abs(x) < tol(T)] = 0
    return s


def first_switch(T, s):
    """First T at which the sign becomes negative after having been >= 0 (skewed->balanced)."""
    sg = sgn(s, T)
    neg = np.where(sg < 0)[0]
    return float(T[neg[0]]) if neg.size else np.nan


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(CACHE, "shift_thH*_pi*_K*_v*.npz"))):
        m = re.search(r"shift_thH([\d.]+)_pi([\d.]+)_K(\d+)_v([\d.]+)\.npz", f)
        thH, pi0, K, v = float(m.group(1)), float(m.group(2)), int(m.group(3)), float(m.group(4))
        d = dict(np.load(f))
        rows.append(((thH, pi0, K, v), d))
    return rows


def agree(ref, oth, T, mask):
    a, b = sgn(ref, T)[mask], sgn(oth, T)[mask]
    nz = a != 0
    return (np.mean(a == b), np.mean(a[nz] == b[nz]) if nz.any() else np.nan, np.mean(a * b < 0))


def etc_regimes(T, ref):
    """Label each T by the reference (ETC) regime:
    0 = no shift below entry, 1 = low-T 'more skewed' (before first negative),
    2 = 'more balanced' (first to last negative), 3 = tail (after last negative)."""
    s = sgn(ref, T)
    lab = np.zeros(T.size, int)
    nz = np.where(s != 0)[0]
    if nz.size == 0:
        return lab
    neg = np.where(s < 0)[0]
    if neg.size == 0:
        lab[nz[0]:] = 1
        return lab
    lab[nz[0]:neg[0]] = 1
    lab[neg[0]:neg[-1] + 1] = 2
    lab[neg[-1] + 1:] = 3
    return lab


def regime_table(data, ref, agents):
    out = {}
    for k in agents:
        acc = {r: [0, 0, 0] for r in (0, 1, 2, 3)}  # agree, opposite, total
        for c, d in data:
            T = d["T"]
            lab = etc_regimes(T, d[ref])
            a, b = sgn(d[ref], T), sgn(d[k], T)
            for r in acc:
                m = lab == r
                acc[r][0] += int(np.sum(a[m] == b[m]))
                acc[r][1] += int(np.sum(a[m] * b[m] < 0))
                acc[r][2] += int(m.sum())
        out[k] = acc
    return out


def main():
    data = load()
    print("configs x value-ratios loaded:", len(data))
    regions = {"main (T/K in [0.2,4])": (0.2, 4.0), "upper (T/K in (4,12])": (4.0, 12.01), "all": (0.0, 1e9)}
    lines = []
    names = {0: "R0 no shift (nobody learns, low T)", 1: "R1 ETC more skewed (low T)",
             2: "R2 ETC more balanced", 3: "R3 tail (after ETC's last balanced T)"}
    for ref in ("etc_smooth", "etc_exact"):
        tab = regime_table(data, ref, [k for k in AG if k != ref])
        lines.append("\n=== agreement by ETC regime, reference %s (share of T with same sign / opposite sign) ===" % ref)
        lines.append("%-38s" % "regime" + "".join("%17s" % k for k in tab))
        for r in (0, 1, 2, 3):
            row = "%-38s" % names[r]
            for k in tab:
                ag, op, n = tab[k][r]
                row += "%17s" % ("%.2f / %.2f" % (ag / n, op / n) if n else "-")
            lines.append(row)
        row = "%-38s" % "R1+R2 (the paper's two regimes)"
        for k in tab:
            ag = tab[k][1][0] + tab[k][2][0]
            op = tab[k][1][1] + tab[k][2][1]
            n = tab[k][1][2] + tab[k][2][2]
            row += "%17s" % ("%.2f / %.2f" % (ag / n, op / n) if n else "-")
        lines.append(row)
        lines.append("%-38s" % "n(T points) per regime: " + ", ".join("R%d=%d" % (r, tab[list(tab)[0]][r][2]) for r in (0, 1, 2, 3)))
    # regime agreement by parameter for the key bandits
    for k in ("ce_A", "opt_B"):
        lines.append("\n=== %s vs etc_smooth: R1+R2 agreement by parameter ===" % k)
        for name, idx in (("thH", 0), ("pi0", 1), ("K", 2), ("v1/v2", 3)):
            vals = sorted(set(c[idx] for c, _ in data))
            row = "  by %-6s" % name
            for val in vals:
                sub = [(c, d) for c, d in data if c[idx] == val]
                t = regime_table(sub, "etc_smooth", [k])[k]
                ag = t[1][0] + t[2][0]
                n = t[1][2] + t[2][2]
                row += "  %g: %.2f" % (val, ag / n if n else np.nan)
            lines.append(row)
    for ref in ("etc_smooth", "etc_exact"):
        lines.append("\n=== reference: %s ===" % ref)
        for rname, (lo, hi) in regions.items():
            lines.append("-- region %s" % rname)
            lines.append("%-10s %10s %14s %10s" % ("agent", "agree_all", "agree|ref!=0", "opposite"))
            for k in AG:
                if k == ref:
                    continue
                A, Anz, Op, wts = [], [], [], []
                for (thH, pi0, K, v), d in data:
                    T = d["T"]
                    mask = (T / K >= lo) & (T / K <= hi)
                    if not mask.any():
                        continue
                    a, anz, op = agree(d[ref], d[k], T, mask)
                    A.append(a)
                    Anz.append(anz)
                    Op.append(op)
                lines.append("%-10s %10.3f %14.3f %10.3f" % (k, np.mean(A), np.nanmean(Anz), np.mean(Op)))
    # by parameter, main region, ref etc_smooth
    lines.append("\n=== main region, reference etc_smooth: agreement by parameter ===")
    for name, idx in (("thH", 0), ("pi0", 1), ("K", 2), ("v1/v2", 3)):
        vals = sorted(set(c[idx] for c, _ in data))
        lines.append("-- by %s" % name)
        lines.append("%8s" % name + "".join("%10s" % k for k in AG if k != "etc_smooth"))
        for val in vals:
            row = "%8g" % val
            for k in AG:
                if k == "etc_smooth":
                    continue
                A = []
                for c, d in data:
                    if c[idx] != val:
                        continue
                    T = d["T"]
                    mask = (T / c[2] >= 0.2) & (T / c[2] <= 4.0)
                    A.append(agree(d["etc_smooth"], d[k], T, mask)[0])
                row += "%10.3f" % np.mean(A)
            lines.append(row)
    # switch points
    lines.append("\n=== first T/K where the shift turns negative (skewed -> balanced), v1/v2 = 2 ===")
    lines.append("%6s %5s %4s" % ("thH", "pi0", "K") + "".join("%11s" % k for k in ["etc_smooth"] + AG))
    sw = []
    for (thH, pi0, K, v), d in data:
        if v != 2.0:
            continue
        T = d["T"]
        vals = [first_switch(T, d[k]) / K for k in ["etc_smooth"] + AG]
        sw.append(((thH, pi0, K), vals))
        lines.append("%6g %5g %4d" % (thH, pi0, K) + "".join("%11.2f" % x for x in vals))
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(RES, "sweep_summary.txt"), "w") as f:
        f.write(txt + "\n")

    # ---------------- figures ----------------
    ps.setup()
    # agreement heatmaps (K=100, v=2, main region) for CE_A and opt_B
    th_vals = sorted(set(c[0] for c, _ in data if c[2] == 100))
    pi_vals = sorted(set(c[1] for c, _ in data if c[2] == 100))
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    for ax, k in zip(axes, ("etc_exact", "ce_A", "opt_B")):
        M = np.full((len(pi_vals), len(th_vals)), np.nan)
        for (thH, pi0, K, v), d in data:
            if K != 100 or v != 2.0:
                continue
            T = d["T"]
            mask = (T / K >= 0.2) & (T / K <= 4.0)
            M[pi_vals.index(pi0), th_vals.index(thH)] = agree(d["etc_smooth"], d[k], T, mask)[0]
        im = ax.imshow(M, origin="lower", cmap="Blues", vmin=0.5, vmax=1.0, aspect="auto")
        for i in range(len(pi_vals)):
            for j in range(len(th_vals)):
                if not np.isnan(M[i, j]):
                    ax.text(j, i, "%.0f%%" % (100 * M[i, j]), ha="center", va="center", fontsize=8,
                            color="#ffffff" if M[i, j] > 0.8 else ps.INK)
        ax.set_xticks(range(len(th_vals)))
        ax.set_xticklabels(["%g" % (t / 0.5) for t in th_vals])
        ax.set_yticks(range(len(pi_vals)))
        ax.set_yticklabels(["%g" % p for p in pi_vals])
        ax.set_xlabel("separation r = thH/thL")
        ax.set_title(ps.LABELS[k], fontsize=9.5)
        ax.grid(False)
    axes[0].set_ylabel("prior pi0 = P(hard market)")
    fig.suptitle("Sign agreement with the paper's ETC (smoothed), T/K in [0.2, 4], K=100, v1/v2=2", fontsize=10.5)
    fig.colorbar(im, ax=axes, shrink=0.8, label="share of total budgets T with same sign")
    fig.savefig(os.path.join(RES, "fig_sweep_agreement_heatmap.png"), dpi=170, bbox_inches="tight")

    # small multiples: shift vs T/K across separations (pi0 = 0.5, K = 100, v = 2)
    sel = sorted([(c, d) for c, d in data if c[1] == 0.5 and c[2] == 100 and c[3] == 2.0], key=lambda x: x[0][0])
    if sel:
        fig, axes = plt.subplots(1, len(sel), figsize=(3.0 * len(sel), 3.3), sharey=False)
        axes = np.atleast_1d(axes)
        for ax, (c, d) in zip(axes, sel):
            T = d["T"]
            for k in ("etc_smooth", "ce_A", "opt_B"):
                ax.plot(T / c[2], d[k] / c[2] * 100, color=ps.COLORS[k], lw=1.4, label=ps.LABELS[k])
            ps.zero_line(ax)
            ax.set_xscale("log")
            ax.set_title("r = %g" % (c[0] / 0.5), fontsize=10)
            ax.set_xlabel("T / K")
        axes[0].set_ylabel("shift (a^X − a^E) / K  ×100")
        axes[0].legend(loc="lower left", fontsize=7)
        fig.suptitle("Allocation shift vs total budget, by state separation (pi0 = 0.5, K = 100, v1/v2 = 2)", fontsize=10.5)
        fig.tight_layout()
        fig.savefig(os.path.join(RES, "fig_sweep_shift_by_r.png"), dpi=170)

    # switch point comparison
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    ref = np.array([v[0] for _, v in sw])
    for j, k in enumerate(AG):
        if k in ("etc_exact", "ts_B"):
            continue
        y = np.array([v[j + 1] for _, v in sw])
        ax.scatter(ref, y, s=22, color=ps.COLORS[k], label=ps.LABELS[k], edgecolor=ps.SURFACE, linewidth=0.6, zorder=3)
    lim = [0, np.nanmax([np.nanmax([v[j] for _, v in sw]) for j in range(len(AG) + 1)]) * 1.05]
    ax.plot(lim, lim, color=ps.AXIS, lw=1, zorder=1)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("ETC (smoothed): T/K where learning starts to balance")
    ax.set_ylabel("Other agent: same switch point (T/K)")
    ax.set_title("Where 'more skewed' turns into 'more balanced'")
    ax.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    fig.savefig(os.path.join(RES, "fig_sweep_switch_points.png"), dpi=170)
    print("figures written")


if __name__ == "__main__":
    main()
