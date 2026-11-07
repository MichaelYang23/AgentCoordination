"""Full bandit (DP) vs decomposition at longer horizons, for the region map.

r = 8, 16, 32 (thH = 4, 8, 16), pi0 = 0.5, K = 200 and 400. Only the curves the comparison needs are computed:
W, the full bandit (Bayes-optimal policy by dynamic programming, key opt_B), the decomposition re-solved under
the same budget rule (etc_B) and the paper's decomposition (etc_smooth). Files use their own prefixes (dp_,
dpshift_), so the earlier sweep scripts, which expect every agent, never pick them up.

Usage:  python run_dp_largeK.py [thH,K ...]      (default: all five new configurations)
"""
import os
import sys
import time

import numpy as np

from agents import compute_curves
from analysis import shifts

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "results", "cache")
KEYS = ["etc_smooth", "opt_B", "etc_B"]
VRATIOS = (1.25, 1.5, 2.0, 3.0, 4.0)
CONFIGS = [(4.0, 200), (16.0, 200), (8.0, 400), (4.0, 400), (16.0, 400)]
PI0 = 0.5
TAU_CAP_B = 60


def main():
    t0 = time.time()
    only = sys.argv[1:]
    for thH, K in CONFIGS:
        if only and "%g,%d" % (thH, K) not in only:
            continue
        Bmax = 12.0 * K * max(1.0, (thH / 8.0) ** 0.5)
        path = os.path.join(CACHE, "dp_thL0.5_thH%g_pi%g_K%d_B%d_h0.1_hlB0.04.npz" % (thH, PI0, K, Bmax))
        print("[%6.0fs] thH=%g (r=%g) K=%d Bmax=%.0f" % (time.time() - t0, thH, thH / 0.5, K, Bmax), flush=True)
        if os.path.exists(path):
            C = dict(np.load(path))
        else:
            C = compute_curves(0.5, thH, PI0, K, Bmax, h=0.1, hb=0.1, which=KEYS, verbose=True, cache_dir=None,
                               hl_B=0.04, nbg=48, n_fine=300, tau_cap_B=TAU_CAP_B)
            np.savez_compressed(path, **C)
        print("[%6.0fs]   max optimal tau: same rule %d (cap %d), paper %.1f"
              % (time.time() - t0, C["etc_B_tau"].max(), min(K - 1, TAU_CAP_B), C["etc_smooth_tau"].max()), flush=True)
        Ts = np.arange(0.2 * K, Bmax + 1e-9, K / 100.0)
        for v in VRATIOS:
            S = shifts(C, KEYS, Ts, v, 1.0)
            np.savez_compressed(os.path.join(CACHE, "dpshift_thH%g_pi%g_K%d_v%g.npz" % (thH, PI0, K, v)), **S)
        print("[%6.0fs]   shifts done" % (time.time() - t0), flush=True)
    print("done in %.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
