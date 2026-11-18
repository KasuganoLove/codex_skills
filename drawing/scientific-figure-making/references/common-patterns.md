# Common Patterns for Publication Figures

These patterns are used across the repository for consistent, publication-ready figures. Apply them when building bar charts, multi-panel layouts, and print-safe graphics. Step-by-step flows that use many of these ideas are in [tutorials.md](tutorials.md); for chart types not covered there, use the closing section of that file and [demos.md](demos.md).

---

## Ultra-wide aspect for multi-metric panels

For 3-4 metrics or many categories in a single row, use a wide canvas so bars/labels don't crowd vertically.

- **Example:** `figsize=(45, 12)` or `(28, 6)`.
- **Rule:** Width often 3-4× height for comparison bars.
- **Why:** Lets the reader scan left-to-right without squinting; keeps y-axis and legend readable.

---

## Dedicated legend panel

When multiple curves or groups make the legend large, put it in its own subplot so it doesn't cover data.

- **Steps:**
  1. Create one extra subplot (e.g. last in the grid).
  2. Call `ax.set_axis_off()` on that axis.
  3. Build the legend on that axis (e.g. gather handles/labels from other axes and call `ax.legend(handles, labels)` there), or use a single legend that you place in the extra axis.
- **Result:** Data panels stay clean; legend is fully visible.

---

## Categorical bars without x-tick labels

When the x-axis is "method" or "condition" and the legend already identifies them, hide x ticks and rely on the legend/title.

- **Code:** `ax.set_xticks([])` or set tick labels to empty.
- **Use when:** Many methods across multiple metrics; names are in the legend or panel title.

---

## Dynamic y-axis scaling

Tighten y-limits to the relevant range so differences are visible instead of squashed.

- **Idea:** Use something like `data.min() - margin` to `data.max() + margin` (e.g. margin = small fraction of range or one std).
- **Avoid:** Fixed 0-100 when all values are in 85-95; use e.g. 80-100 instead.

---

## Bar edge and hatch for print-safe separation

Bars that differ only by fill can blur in grayscale. Use edges and optional hatching.

- **Edges:** `edgecolor='black'`, `linewidth=1.5`-`3` for clear separation.
- **Hatch:** Same color with different hatch (e.g. `'/'`, `'\\'`, `'.'`) for ablation or subgroups so they remain distinct in print.

---

## Semantic color mapping

Stick to the skill palette so "proposed vs baseline" is consistent across figures.

- **Blues:** Proposed method / key result.
- **Greens:** Improvements / positive variants.
- **Reds:** Baselines / contrasts / alternatives.
- **Neutral:** Reference or background categories.
- **Highlight:** Single callout only.

See [design-theory.md](design-theory.md) for the full palette and [api.md](api.md) for `PALETTE` and `DEFAULT_COLORS`.

## Numeric meaning before layout

- Record each panel's statistic, unit, comparison/reference, and observational unit from its current input table or code. Distinguish participant counts from repeated records; unresolved denominators remain unresolved. Plot supplied estimates without silently changing models, grouping, or sample inclusion.
- Keep coefficients and correlations on their own scales. Correlations lie in [-1, 1]; regression coefficients need not. Label units such as kg/year and the comparison explicitly. Use separate colorbars for different quantities; disclose any panel-specific magnitude normalization so equal-sized marks are not mistaken for equal effects across panels.
- Preserve zero, missing, empty-group, and not-estimable states. A genuine zero may have zero area; a missing estimate must be omitted or marked NA/NE, never filled with zero or a plausible-looking coefficient. Keep requested category labels with an honest unavailable marker when appropriate. Export the actual plotted values and their status.
- For signed quantities with meaningful zero, use a zero-centered diverging scale. Do not let a decorative palette override the statistic's sign, magnitude, or an explicit user-supplied legend.

## Magnitude encoded by area

When a square's **area** represents |v|, make its side proportional to sqrt(|v|), not |v|. For a grid cell with maximum half-side hmax and a positive reference magnitude s:

```python
half_side = hmax * np.sqrt(np.abs(values) / s)
```

Use s=1 for correlations and a stated common or per-panel reference for other statistics. For an all-zero panel, choose a finite positive fallback s (for example 1) and preserve zero sizes; for an all-missing panel, show an unavailable state instead of inventing a scale from data. Exclude or mark missing entries before creating patches. Use equal axis aspect for grid squares, and verify that the largest patch fits its cell.

Matplotlib scatter's `s` is already an area parameter in points squared: set it proportional to |v| directly. Do not apply the square-root transformation twice. Validate the intended encoding with two known magnitudes (for example .25 and 1 should have a 1:4 area ratio), sign reversal (same area, opposite color), zero, and missing values.

## Related files

- [SKILL.md](../SKILL.md) — When to load this skill
- [api.md](api.md) — `PALETTE`, helpers, validation
- [demos.md](demos.md) — Real scripts mirroring these patterns
- [design-theory.md](design-theory.md) — Visual and color theory
- [tutorials.md](tutorials.md) — Walkthroughs that apply these patterns
