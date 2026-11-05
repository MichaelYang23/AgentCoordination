"""Allocation shifts, marginal-value ratios and sign agreement between agents."""
import numpy as np

from allocation import solve_allocation


def derivative(grid, V, step=1.0):
    """Central difference with a fixed budget step (robust to grid noise)."""
    up = np.interp(grid + 0.5 * step, grid, V)
    dn = np.interp(np.maximum(grid - 0.5 * step, 0.0), grid, V)
    width = (grid + 0.5 * step) - np.maximum(grid - 0.5 * step, 0.0)
    return (up - dn) / width


def ratio(grid, V, W, step=1.0):
    return derivative(grid, V, step) / derivative(grid, W, step)


def shifts(curves, keys, Ts, v1, v2):
    grid = curves["grid"]
    W = curves["W"]
    aE = np.array([solve_allocation(grid, W, T, v1, v2) for T in Ts])
    out = {"T": np.asarray(Ts, float), "aE": aE}
    for k in keys:
        aX = np.array([solve_allocation(grid, curves[k], T, v1, v2) for T in Ts])
        out[k] = aX - aE
    return out


def sign_with_tol(x, tol):
    s = np.sign(x)
    s[np.abs(x) < tol] = 0
    return s


def agreement(ref, other, tol=0.25):
    """Fraction of T at which sign(shift) agrees.

    Returns dict with: overall agreement, agreement where the reference shift is
    non-zero, and counts by category.
    """
    a = sign_with_tol(ref, tol)
    b = sign_with_tol(other, tol)
    nz = a != 0
    res = {
        "agree_all": float(np.mean(a == b)),
        "agree_ref_nonzero": float(np.mean(a[nz] == b[nz])) if nz.any() else np.nan,
        "n": int(a.size),
        "n_ref_nonzero": int(nz.sum()),
        "ref+ other-": int(np.sum((a > 0) & (b < 0))),
        "ref- other+": int(np.sum((a < 0) & (b > 0))),
        "ref0 other!=0": int(np.sum((a == 0) & (b != 0))),
        "ref!=0 other0": int(np.sum((a != 0) & (b == 0))),
    }
    return res


def regime_boundaries(T, s, tol=0.25):
    """List of (T where sign changes, from, to)."""
    sg = sign_with_tol(s, tol)
    out = []
    for i in range(1, sg.size):
        if sg[i] != sg[i - 1]:
            out.append((float(T[i]), int(sg[i - 1]), int(sg[i])))
    return out
