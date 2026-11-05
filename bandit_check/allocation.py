"""Two-team allocation: max_a v1*V(a) + v2*V(T-a) on a uniform budget grid."""
import numpy as np


def objective(grid, V, T, v1, v2, a):
    return v1 * np.interp(a, grid, V) + v2 * np.interp(T - a, grid, V)


def solve_allocation(grid, V, T, v1, v2, return_value=False):
    """Global argmax on the grid (step h) followed by a parabolic refinement.

    grid must be uniform, start at 0 and extend to at least T.
    Returns the senior team's budget a (and optionally the objective value).
    """
    h = grid[1] - grid[0]
    n = int(np.floor(T / h + 1e-9))
    a = np.arange(n + 1) * h
    if abs(n * h - T) < 1e-7 * max(1.0, T) and n < V.size:
        F = v1 * V[: n + 1] + v2 * V[n::-1]          # fast path: T on the grid
    else:
        F = objective(grid, V, T, v1, v2, a)
    k = int(np.argmax(F))
    a_star, F_star = a[k], F[k]
    if 0 < k < n:
        f0, f1, f2 = F[k - 1], F[k], F[k + 1]
        den = f0 - 2 * f1 + f2
        if den < 0:
            delta = 0.5 * (f0 - f2) / den
            if abs(delta) <= 1.0:
                a_star = a[k] + delta * h
                F_star = objective(grid, V, T, v1, v2, a_star)
    if return_value:
        return a_star, F_star
    return a_star


def shift_curve(grid, V, W, Ts, v1, v2):
    """a^X - a^E for each total budget T."""
    out = np.empty(len(Ts))
    aE = np.empty(len(Ts))
    for i, T in enumerate(Ts):
        e = solve_allocation(grid, W, T, v1, v2)
        x = solve_allocation(grid, V, T, v1, v2)
        out[i] = x - e
        aE[i] = e
    return out, aE
