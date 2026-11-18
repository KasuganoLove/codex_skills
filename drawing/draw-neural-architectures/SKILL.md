---
name: draw-neural-architectures
description: Draw and revise editable publication figures for deep-learning architectures and methods from model descriptions, code, or papers. Use for CNN, U-Net, multiscale feature maps, Transformer, attention, DiT, diffusion/flow training and inference diagrams, neural-network architecture figures, 深度学习结构图 or 论文方法框架图. Reuse curated TikZ and original PlotNeuralNet resources, verify topology, compile, and visually inspect. Use scientific-figure-making for numeric experiment plots; do not use for generic websites, decorative image generation, or paper reading without a requested figure.
---

# Draw neural architectures

Produce a clear model figure with editable source, vector PDF and PNG preview. Use planar TikZ by default and original PlotNeuralNet when spatial scale/channel structure benefits from 3D boxes. Treat bundled models as generic examples, never as evidence of the user's architecture.

## Start with structure

1. Read the supplied description, current code/forward method, or cited paper and relevant figures. Fetch named public repositories through GitHub when available. Distinguish implemented behavior, paper claims and proposed additions. Do not execute arbitrary model code merely to draw it.
2. Record a compact architecture note alongside the figure: inputs/outputs; modules and repeat counts; connections; add versus concatenate; verified shapes; condition injection; training-only elements; source/version; unresolved assumptions. For a simple specified model, a few lines suffice.
3. Read [architecture-checks.md](references/architecture-checks.md). Check shape consistency and algorithm/time conventions before layout. Ask only when missing information changes scientific meaning and cannot be recovered from sources. Default reversible layout choices independently. Never fabricate dimensions or exact internals; use symbolic shapes or an explicitly abstract module.
4. Choose the visual grammar and overview/detail split with [figure-style.md](references/figure-style.md), then select or compose template primitives. When the user supplies figure references or the model family is unfamiliar, inspect a small relevant set of original paper/official technical-report figures. Separate borrowed presentation choices from source-verified topology; examples guide clarity and depth, not a ceiling or a mandatory architecture. Build a new skeleton when existing templates would misrepresent the method.

## Choose resources on demand

| Need | Resource |
| --- | --- |
| CNN / U-Net, spatial resolution and channels | [plotneuralnet.md](references/plotneuralnet.md), `assets/plotneuralnet/` |
| Transformer and cross-attention | [tikz-templates.md](references/tikz-templates.md), `assets/tikz/transformer-cross-attention.tex` |
| Conditional flow training and inference | Same reference, `assets/tikz/conditional-flow.tex` |
| Generic conditioned transformer/DiT block | Same reference, `assets/tikz/dit-block.tex` |
| Style, target width, submission export | [figure-style.md](references/figure-style.md) |
| Compiler, environment recovery, diagnostic limits | [rendering.md](references/rendering.md) |

Read only the relevant template and reference. Preserve upstream provenance/license files. Fetch additional templates at recorded revisions and verify their own dependencies/licenses; a parent license does not automatically cover third-party assets. See bundled source records in the resource references.

## Make the figure

1. Copy templates and dependencies into the figure's work directory. Do not edit installed assets during ordinary drawing. Retain relative imports and include every required layer macro, image and style in the final source package. Planar templates stay standalone-compilable.
2. Use meaningful stable node names. Put tunable labels, counts, spacing and colors in an obvious parameter section. Preserve structural invariants when changing counts; changing displayed repeat text alone does not change connectivity.
3. Default to white, muted module fills, dark readable text and one accent for the proposed component. Use solid forward-data arrows and distinguish conditioning/training-only paths with labels or dash styles. Include a legend when needed.
4. For a detailed architecture explanation, pair the end-to-end path with an expansion of the block that answers the reader's question, even when the overview is not crowded. Use matched names and an explicit expansion link; choose panels or separate figures as needed. Give residual/skip routes their own lanes. Use repeated blocks marked ×N only when source evidence supports it.
5. Use the manuscript language (English by default for an English paper). For Chinese labels use XeLaTeX and available CJK fonts; verify glyphs rather than silently transliterating.

## Compile and inspect

Use the bundled compiler as documented in [rendering.md](references/rendering.md). Check actual classes/packages as well as executable presence. Reuse available dependencies and resolve routine local setup within the user's authorization. Avoid blanket confirmation steps for reversible fixes. If compilation remains unavailable, preserve source and report the missing dependency; never claim a compiled result.

After successful compilation:

1. Inspect PNG at full size and intended manuscript width. Check labels, edges, arrowheads, titles, bounds, symbols and hierarchy.
2. Treat automatic warnings as heuristics. Detector failure is an unavailable check, not a pass; clean output does not prove topology/aesthetics. Review inherited template issues too. Distinguish intended crossings from missing junctions.
3. Reconcile visible modules/edges and formulas against the architecture note. Check concat/add, residuals, Q/K/V sources, masks, time direction, conditioning and losses. Confirm that each expanded block has the same inputs, outputs and conditions as its overview node; no detail may appear solely because the reference figure or template contains it.
4. Fix actual problems, recompile and inspect affected output. Stop when relevant checks pass; repeat only for new changes or concerns.

## Deliver

- Provide editable `.tex` and required source resources, vector `.pdf`, and `.png`. Include generator `.py` when applicable. Provide SVG when useful/requested; state if labels are outlined.
- Supply a brief architecture description/alt text and remaining assumptions. Say whether compilation and visual inspection occurred; do not equate compilation with scientific validation.
- Save user deliverables with the current Library workflow unless they belong to an existing Git-backed project or the user specifies another destination. Keep intermediate builds in scratch. Do not modify this skill during ordinary drawing.
- Adapt dimensions to the actual venue template. Describe styles as personal/venue-compatible, never official conference architecture templates without evidence.

## Maintain the collection

Add templates for recurring needs or explicit requests. Record origin/version/license, editing constraints and dependencies. Compile and visually inspect before calling additions validated. Keep the collection bounded and searchable. Skill maintenance uses skill-creator; do not silently install every finished figure as a template.
