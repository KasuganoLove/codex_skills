# Tutorials: End-to-End Publication Figures

Implement the API described in [api.md](api.md) in your own code (constants, style, plot helpers, finalize). This repository does not currently ship a tracked shared Python module that defines `apply_publication_style`, `make_grouped_bar`, or the other helpers directly; their signatures and behavior are specified in [api.md](api.md) and should be implemented or adapted per project. For real-world scripts that follow this style, see [demos.md](demos.md) (links to the [figures4papers](https://github.com/ChenLiu-1996/figures4papers) `figure_*` folders).

If venue, approximate dimensions, or export formats are missing and they would change layout or DPI, ask before locking choices. For unattended scripts, set a non-interactive matplotlib backend (for example `matplotlib.use("Agg")`) before importing `pyplot`. Finish with `finalize_figure` as in [api.md](api.md).

---

## Tutorial 1: Grouped bar chart

**Goal:** One grouped bar chart: several series compared on the same categorical x-axis (metrics, conditions, tasks, or similar), optional value annotations, and export via `finalize_figure`.

**Checklist:**

- [ ] Load or define data: shared category list for the x-axis; one numeric array per series (each aligned with those categories); legend label per series.
- [ ] Call `apply_publication_style` with a style (e.g. `FigureStyle(font_size=24, axes_linewidth=3)` for a large panel).
- [ ] Create figure and one axis; widen `figsize` when there are many categories so ticks and labels stay readable.
- [ ] Call `make_grouped_bar(ax, categories, series, labels, ylabel="...", annotate=True)` (or `annotate=False` and use `annotate_bars` separately per [api.md](api.md)).
- [ ] Set y-limits to a range that fits the data (tighten when values sit in a narrow band).
- [ ] Call `finalize_figure(fig, "output/comparison", formats=["png", "pdf"], dpi=300)`.

**Example flow** (illustrative counts; implement helpers per [api.md](api.md)):

```python
import matplotlib.pyplot as plt

# Assume you have implemented: apply_publication_style, FigureStyle, make_grouped_bar, finalize_figure, PALETTE (see api.md)
apply_publication_style(FigureStyle(font_size=24, axes_linewidth=3))
fig, ax = plt.subplots(figsize=(16, 5))

categories = ["Metric A", "Metric B", "Metric C", "Metric D"]  # length K
series = [  # one list per series, each length K
    [0.92, 0.88, 0.85, 0.90],
    [0.85, 0.82, 0.88, 0.84],
    [0.78, 0.80, 0.82, 0.79],
]
labels = ["Ours", "Baseline X", "Baseline Y"]  # same length as series
make_grouped_bar(
    ax, categories, series, labels,
    ylabel="Score", colors=[PALETTE["blue_main"], PALETTE["green_3"], PALETTE["red_strong"]],
    annotate=True,
)
ax.set_ylim(0.7, 1.0)
finalize_figure(fig, "output/method_comparison", formats=["png", "pdf"], dpi=300)
```

---

## Tutorial 2: Multi-panel trend with shared legend

**Goal:** Two trend panels (e.g. train and validation curves) and a third panel used only for the legend.

**Checklist:**

- [ ] Apply style; create 1×3 subplots (or 2×2 with last axis for legend).
- [ ] Plot trends on the first axes; collect legend handles/labels from one of them.
- [ ] On the last axis, call `ax.set_axis_off()` and add a legend using the collected handles/labels.
- [ ] Set y-limits and titles on data panels.
- [ ] Call `finalize_figure`.

**Example flow** (implement helpers per [api.md](api.md)):

```python
import numpy as np
import matplotlib.pyplot as plt

apply_publication_style(FigureStyle(font_size=14, axes_linewidth=2))
fig, axes = create_subplots(1, 3, figsize=(14, 4))

x = np.linspace(0, 10, 50)
y1 = 0.5 + 0.4 * (1 - np.exp(-x / 3))
y2 = 0.45 + 0.35 * (1 - np.exp(-x / 4))
make_trend(axes[0], x, [y1, y2], ["Model A", "Model B"], ylabel="Loss", xlabel="Step")
axes[0].set_title("Training")
make_trend(axes[1], x, [y1 * 1.1, y2 * 1.05], ["Model A", "Model B"], ylabel="Loss", xlabel="Step")
axes[1].set_title("Validation")

# Legend-only panel
handles, labels = axes[0].get_legend_handles_labels()
axes[2].set_axis_off()
axes[2].legend(handles, labels, loc="center")

finalize_figure(fig, "output/trends", formats=["png", "pdf"], dpi=300)
```

---

## Tutorial 3: Heatmap with labels and colorbar

**Goal:** A correlation or score matrix with row/column labels and a colorbar.

**Checklist:**

- [ ] Apply style; create one axis.
- [ ] Establish whether the matrix is a correlation or another statistic; verify its units and range.
- [ ] Prepare 2D matrix and optional x_labels, y_labels. Preserve missing values.
- [ ] For correlations, use a zero-centered diverging colorbar over [-1, 1]. Use native Matplotlib when a helper does not expose the required normalization.
- [ ] Call `finalize_figure`.

**Example flow** (implement helpers per [api.md](api.md)):

```python
import numpy as np
import matplotlib.pyplot as plt

apply_publication_style(FigureStyle(font_size=12, axes_linewidth=2))
fig, ax = plt.subplots(figsize=(8, 6))
# Synthetic teaching data; replace with the user's verified data for a real figure.
rng = np.random.default_rng(42)
samples = rng.normal(size=(100, 5))
samples[:, 1] = 0.8 * samples[:, 0] + 0.2 * samples[:, 1]
samples[:, 2] = -0.6 * samples[:, 0] + 0.4 * samples[:, 2]
matrix = np.corrcoef(samples, rowvar=False)
labels = [f"F{i+1}" for i in range(5)]
im = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels)), labels)
ax.set_yticks(range(len(labels)), labels)
fig.colorbar(im, ax=ax, label="Pearson correlation")
finalize_figure(fig, "output/heatmap", formats=["png", "pdf"], dpi=300)
```

---

## Chart types beyond these walkthroughs

These tutorials cover grouped bars, multi-panel trends with a legend column, and heatmaps. For other house-style figures, open the closest match in [demos.md](demos.md), then align constants and `finalize_figure` with [api.md](api.md) and typography or export rules in [design-theory.md](design-theory.md).

- **Radar or polar comparisons:** `figure_VIGIL` (for example `plot_comparison_radar.py`).
- **Comparison or post-training line panels:** `figure_VIGIL`, `figure_ophthal_review`, or `figure_Cflows`, depending on layout.
- **Scatter-heavy or schematic panels:** `figure_Dispersion` and `figure_VIGIL` concept plots are good starting points.
- **Bar-style quantitative comparisons:** `figure_CellSpliceNet`, `figure_ImmunoStruct`, and `figure_Brainteaser`.
- **Heatmap-focused examples:** `figure_RNAGenScape`.

For more layout ideas (ultra-wide panels, legend-only axes, print-safe bars), see [common-patterns.md](common-patterns.md).

## Related files

- [SKILL.md](../SKILL.md) — When to load this skill
- [api.md](api.md) — API this tutorial assumes
- [demos.md](demos.md) — Production scripts in figures4papers
- [common-patterns.md](common-patterns.md) — Layout and print-safe details
- [design-theory.md](design-theory.md) — Why the style choices exist
