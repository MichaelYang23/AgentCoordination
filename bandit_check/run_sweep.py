"""Parameter sweep: does the sign of the allocation shift agree between the
paper's ETC team and learn-while-doing (bandit) agents?

Usage:  python run_sweep.py            (all configs; curves cached in results/cache)
"""
import os
import sys
import time

import numpy as np

from agents import compute_curves
from analysis import shifts

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
    for thH in (4.0, 8.0, 16.0):
        for pi0 in (0.35, 0.5, 0.65):
            out.append((thH, pi0, 50))
    # K=200 is slow; results scale with B/K, so only a matched subset is run
    for pi0 in (0.35, 0.5, 0.65):
        out.append((8.0, pi0, 200))
    return out


def main():
    """Compute V_X(B) for every agent and the allocation shifts a^X - a^E for each
    (configuration, value ratio, total budget); everything is cached in
    results/cache.  Agreement statistics are produced by summarize_sweep.py."""
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
    print("done in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
