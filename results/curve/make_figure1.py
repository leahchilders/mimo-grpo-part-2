"""Figure 1 of the article (held-out score during training, two ways), from the CSVs in this repo.

    python results/curve/make_figure1.py

Inputs (all in this repo):
  results/curve/eval_points.csv       7 held-out evals: mean over all 928 pieces + its 95% bootstrap CI
  results/curve/among_valid_ci.csv    mean among the pieces that got a score + a descriptive 95% bootstrap CI
  results/headline/reference_lines.csv  random notes 2 and 3 voices, canon among valid (Part 1)
Outputs (next to this script): figure1_{light,dark}.{png,svg}. The article's PNGs are media/img/held-out-score-*.png.
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

evals = list(csv.DictReader(open(os.path.join(HERE, "eval_points.csv"))))
esteps = [int(r["step"]) for r in evals]
emean = [float(r["mean_all"]) for r in evals]
elo = [float(r["mean_all_ci_lo"]) for r in evals]
ehi = [float(r["mean_all_ci_hi"]) for r in evals]
av = list(csv.DictReader(open(os.path.join(HERE, "among_valid_ci.csv"))))
assert [int(r["step"]) for r in av] == esteps
vmean = [float(r["mean_among_valid"]) for r in av]
vlo = [float(r["ci_lo"]) for r in av]
vhi = [float(r["ci_hi"]) for r in av]
ref = {r["line"]: float(r["value"]) for r in csv.DictReader(open(os.path.join(ROOT, "results/headline/reference_lines.csv")))}

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781", grid="#e1e0d9",
                  axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", ref="#6f6e69", band=0.18),
    "dark": dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781", grid="#2c2c2a",
                 axis="#383835", s1="#3987e5", s2="#d95926", ref="#a3a29a", band=0.28),
}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "svg.fonttype": "path"})
DASH = (0, (4, 3))


def frame(t, ylabel, ylim, yticks, right=0.69):
    fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=200)
    fig.patch.set_facecolor(t["surface"])
    ax.set_facecolor(t["surface"])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(t["axis"])
    ax.tick_params(colors=t["muted"], length=0, labelsize=11)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y:.2f}" for y in yticks])
    ax.set_ylim(*ylim)
    ax.set_xlim(-6, 306)
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300])
    ax.grid(axis="y", color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Training step", color=t["ink2"], fontsize=11.5)
    ax.set_ylabel(ylabel, color=t["ink2"], fontsize=11.5)
    fig.subplots_adjust(left=0.10, right=right, top=0.96, bottom=0.12)
    return fig, ax


def refline(ax, t, y, label, color=None, dy=0.0, style=DASH, lw=1.2):
    ax.axhline(y, color=color or t["ref"], linewidth=lw, linestyle=style, zorder=1)
    ax.annotate(label, xy=(1.0, y), xycoords=("axes fraction", "data"), xytext=(8, dy),
                textcoords="offset points", va="center", ha="left", color=t["ink2"], fontsize=10.5,
                linespacing=1.15)


def series(ax, t, color, ys, lo, hi, label=None):
    ax.fill_between(esteps, lo, hi, color=color, alpha=t["band"], linewidth=0, zorder=2)
    ax.plot(esteps, ys, color=color, linewidth=2, zorder=3, label=label, marker="o", markersize=0)
    ax.scatter(esteps, ys, s=40, color=color, edgecolor=t["surface"], linewidth=2, zorder=4)


def val(ax, t, x, y, text, xytext, color, bold=False, ha="center", va="center"):
    """Value label at `xytext` (data coords) with a thin arrow, in the series colour, to the point (x, y)."""
    ax.annotate(text, xy=(x, y), xytext=xytext, textcoords="data", ha=ha, va=va, color=t["ink"], fontsize=11,
                fontweight="bold" if bold else "normal", zorder=6,
                arrowprops=dict(arrowstyle="-|>,head_length=0.45,head_width=0.22", color=color, lw=1.2,
                                shrinkA=3, shrinkB=6, connectionstyle="arc3,rad=0"))


for mode, t in THEMES.items():
    fig, ax = frame(t, "Mean MiMo score", (0.55, 0.85), [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85])
    series(ax, t, t["s1"], emean, elo, ehi, label="All test pieces (rejected pieces score 0)")
    series(ax, t, t["s2"], vmean, vlo, vhi, label="Test pieces that got a score")
    r3, r2, cv = ref["random_notes_3_voices"], ref["random_notes_2_voices"], ref["canon_among_valid"]
    refline(ax, t, r3, f"Random notes,\n3 voices {r3:.3f}", dy=6)
    refline(ax, t, cv, f"Canonical composers,\npieces that got a score {cv:.3f}", color=t["ink2"], dy=-3,
            style=(0, (1, 2)), lw=1.6)
    refline(ax, t, r2, f"Random notes,\n2 voices {r2:.3f}")
    val(ax, t, 0, vmean[0], f"{vmean[0]:.3f}", (22, 0.772), t["s2"], ha="left")
    val(ax, t, 300, vmean[-1], f"{vmean[-1]:.3f}", (262, 0.838), t["s2"], bold=True, ha="right")
    val(ax, t, 0, emean[0], f"{emean[0]:.3f}", (24, 0.566), t["s1"], ha="left")
    val(ax, t, 300, emean[-1], f"{emean[-1]:.3f}", (262, 0.733), t["s1"], bold=True, ha="right")
    leg = ax.legend(loc="lower right", frameon=False, fontsize=10.5, handlelength=1.6, borderaxespad=0.3)
    for txt in leg.get_texts():
        txt.set_color(t["ink2"])
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(HERE, f"figure1_{mode}.{ext}"), facecolor=fig.get_facecolor())
    plt.close(fig)
print("wrote figure1_{light,dark}.{png,svg}")
