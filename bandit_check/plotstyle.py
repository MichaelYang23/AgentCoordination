"""Shared matplotlib style: fixed categorical order, thin marks, recessive chrome."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#fcfcfb"

# entity -> colour (fixed, never re-assigned between figures)
COLORS = {
    "etc_smooth": "#2a78d6",   # blue
    "ce_A": "#eb6834",         # orange
    "opt_B": "#1baf7a",        # aqua
    "etc_exact": "#eda100",    # yellow
    "ts_B": "#e87ba4",         # magenta
    "etc_adapt": "#008300",    # green
    "etc_B": "#6250d6",        # violet
    "ce_B": "#e34948",         # red
    "ce_A_raw": "#eb6834",
    "probe_ce_A": "#eb6834",
}

LABELS = {
    "etc_exact": "ETC (paper, exact)",
    "etc_smooth": "ETC (paper, smoothed)",
    "etc_adapt": "ETC, adaptive stopping",
    "ce_A": "Learn-while-doing (CE), off-switch",
    "ce_A_raw": "Learn-while-doing (CE), always on",
    "probe_ce_A": "Probe then CE",
    "opt_B": "Bayes-optimal bandit (ex-ante)",
    "ts_B": "Thompson sampling (ex-ante)",
    "ce_B": "Myopic Bayesian (ex-ante)",
    "etc_B": "ETC re-solved (ex-ante)",
}


def setup():
    plt.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 9.5,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "lines.linewidth": 1.6,
        "font.family": "DejaVu Sans",
    })


def zero_line(ax, y=0.0):
    ax.axhline(y, color=AXIS, lw=0.9, zorder=1)
