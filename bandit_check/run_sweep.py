"""Parameter sweep: does the sign of the allocation shift agree between the
paper's ETC team and learn-while-doing (bandit) agents?

Usage:  python run_sweep.py            (all configs; curves cached in results/cache)
"""
import csv
import os
import sys
import time

import numpy as np

from agents import compute_curves
from analysis import shifts, agreement, regime_boundaries

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CACHE = os.path.join(RES, "cache")
os.makedirs(CACHE, exist_ok=True)

THL = 0.5
KEYS = ["etc_exact", "etc_smooth", "etc_adapt", "ce_A", "probe_ce_A", "opt_B", "ts_B", "etc_B"]
VRATIOS = (1.25, 1.5, 2.0, 3.0, 4.0)


def configs():
    out = []
    for thH in (2.0, 4.0, 8.0, 16.0, 32.0):
        for pi0 in (0.2, 0.35, 0.5, 0.65, 0.8):
            out.append((thH, pi0, 100))
    for K in (50, 200):
        for thH in (4.0, 8.0, 16.0):
            for pi0 in (0.35, 0.5, 0.65):
                out.append((thH, pi0, K))
    return out


def tol(T):
    return 0.1 + 0.001 * T


def main():
    rows = []
    t0 = time.time()
    cfgs = configs()
    only = sys.argv[1:]  # optional filter "thH,pi0,K"
    for i, (thH, pi0, K) in enumerate(cfgs):
        if only and "%g,%g,%d" % (thH, pi0, K) not in only:
            continue
        Bmax = 12.0 * K * max(1.0, (thH / 8.0) ** 0.5)
        print("[%5.0fs] config %d/%d  thH=%g pi0=%g K=%d  Bmax=%g" % (time.time() - t0, i + 1, len(cfgs), thH, pi0, K, Bmax), flush=True)
        C = compute_curves(THL, thH, pi0, K, Bmax, h=0.1, hb=0.1, which=KEYS, verbose=False, cache_dir=CACHE,
                           hl_B=0.04, nbg=48, n_fine=300)
        Ts = np.arange(0.2 * K, Bmax + 1e-9, K / 100.0)
        for v in VRATIOS:
            S = shifts(C, KEYS, Ts, v, 1.0)
            np.savez_compressed(os.path.join(CACHE, "shift_thH%g_pi%g_K%d_v%g.npz" % (thH, pi0, K, v)), **S)
            tl = tol(Ts)
            for ref in ("etc_smooth", "etc_exact"):
                b_ref = regime_boundaries(Ts, S[ref], 0.0)
                for k in KEYS:
                    if k == ref:
                        continue
                    a = sign_agree(S[ref], S[k], tl)
                    rows.append({"thH": thH, "pi0": pi0, "K": K, "v": v, "ref": ref, "agent": k, **a,
                                 "ref_boundaries": ";".join("%g:%+d>%+d" % b for b in regime_boundaries(Ts, S[ref], 0.0)),
                                 "agent_boundaries": ";".join("%g:%+d>%+d" % b for b in regime_boundaries(Ts, S[k], 0.0))})
        write(rows)
    print("done in %.0fs" % (time.time() - t0))


def sign_agree(ref, other, tl):
    sa = np.sign(ref)
    sa[np.abs(ref) < tl] = 0
    sb = np.sign(other)
    sb[np.abs(other) < tl] = 0
    nz = sa != 0
    both_nz = nz & (sb != 0)
    return {
        "agree_all": float(np.mean(sa == sb)),
        "agree_ref_nonzero": float(np.mean(sa[nz] == sb[nz])) if nz.any() else float("nan"),
        "agree_both_nonzero": float(np.mean(sa[both_nz] == sb[both_nz])) if both_nz.any() else float("nan"),
        "n": int(sa.size),
        "n_ref_pos": int(np.sum(sa > 0)),
        "n_ref_neg": int(np.sum(sa < 0)),
        "n_opposite": int(np.sum(sa * sb < 0)),
        "n_ref0_other_nz": int(np.sum((sa == 0) & (sb != 0))),
        "n_ref_nz_other0": int(np.sum((sa != 0) & (sb == 0))),
    }


def write(rows):
    if not rows:
        return
    with open(os.path.join(RES, "sweep_agreement.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
