# Planar neural architecture templates

Use the bundled source under `assets/tikz/`. Copy a selected `.tex` and its applicable license into the figure's source directory before editing. Each `.tex` is standalone and embeds its palette and styles; no network fetch is needed at generation time. Use the parent skill's compile helper, then inspect its PNG at final manuscript width.

## Template selection and invariants

| File | Use | Edit points | Preserve or explicitly revise |
|---|---|---|---|
| `transformer-cross-attention.tex` | Post-norm encoder–decoder with causal decoder self-attention | `encCount`, `decCount`, `colSep`, `boxWidth`, input labels, colors | Encoder memory owns cross-attention K,V; decoder state owns Q. Every residual taps its sublayer input. Encoder and decoder repetitions are independent. Shifting target tokens and causal masking are required for this autoregressive example. |
| `conditional-flow.tex` | Generic paired conditional rectified-flow training and iterative inference | `boxW`, `gapX`, `conditionLabel`, model label, solver description | Noise at t=0, clean target at t=1; x_t=(1-t)z+t x_HQ; target u=x_HQ-z; same sample defines interpolant and target. Loss is an expectation over paired data, noise and time. c is fixed during inference; solver repeatedly queries v_theta. |
| `dit-block.tex` | Generic pre-norm conditioned Transformer block | `rowSep`, `conditionText`, module names, widths, colors | Two residuals, each bypassing the complete normalization/attention or normalization/FFN branch. Condition arrows are abstract. This is NOT an exact DiT, adaLN-Zero, SD3, Flux or joint-attention implementation. |
| `encoder-decoder.tex` | Compact input → encoder → latent → decoder → output overview | Top `def` block controls sizes, gaps and labels | Encoder narrows toward latent; decoder widens away. This diagram abstracts away skips, losses and internal layers. |

Choose the post-norm Transformer only when it matches the actual model. Pre-norm requires moving the normalization ahead of each sublayer and preserving residual taps. For encoder-only remove the decoder and head, then route memory to the requested output. For decoder-only remove encoder and cross-attention, then reconnect the remaining decoder residual sequence; keep causal masking only if the target task requires it.

For an exact DiT-like model, inspect code/paper for patch embedding/unpatchify, condition encoder, adaptive-normalization shift/scale, residual gates, attention type and final modulation. Expand the generic block from that evidence. Never infer these details from the name “DiT.”

The RF template assumes data and noise share the same space and dimensionality. For latent-space restoration, add verified encoder/decoder components. For noisy-LQ initialization, residual-field paths, opposite time conventions or a different target parameterization, revise the interpolation equation, target, initial state, solver direction and legend together. The generic RF template does not assert the user's RRF method or any unpublished architecture.

All node names are semantic edit anchors. When adding branches, preserve these anchors or update every referring edge. Width/spacing changes can expose overlaps: recompilation and raster inspection are mandatory after adaptation. Template-inherited warnings are not automatically exempt from review.

## Sources and modifications

Sources inspected 2026-11-08 and pinned; no upstream Skill instructions are installed as runtime policy.

- `haiyichen001/tikz-figure-skill`, revision `5952e18631600aa46de91ea7653f92ae6697d774`:
  - https://github.com/haiyichen001/tikz-figure-skill/blob/5952e18631600aa46de91ea7653f92ae6697d774/references/templates/transformer.tex
  - https://github.com/haiyichen001/tikz-figure-skill/blob/5952e18631600aa46de91ea7653f92ae6697d774/LICENSE
  - MIT copyright notice retained in `assets/tikz/LICENSE-tikz-figure-skill-MIT.txt`.
  - `transformer-cross-attention.tex` reuses the layer/style idiom and academic palette, with reworked compact layout, explicit embedding labels, directed residual flow, Q/K/V ownership and post-norm topology. `dit-block.tex` reuses adapted layer styles and adds a deliberately generic pre-norm conditioned block. These are locally adapted templates, not verbatim upstream examples.
- `opentikz/opentikz`, revision `359befbf8e8af7ce08e7e387b2c2a198e0ca735d`:
  - https://github.com/opentikz/opentikz/blob/359befbf8e8af7ce08e7e387b2c2a198e0ca735d/templates/encoder-decoder/template.tex
  - https://github.com/opentikz/opentikz/blob/359befbf8e8af7ce08e7e387b2c2a198e0ca735d/templates/flowchart/template.tex
  - https://github.com/opentikz/opentikz/blob/359befbf8e8af7ce08e7e387b2c2a198e0ca735d/LICENSE-CONTENT
  - CC0 text retained in `assets/tikz/LICENSE-OpenTikZ-CC0.txt`.
  - `encoder-decoder.tex` is a verbatim copy of the graphic source. `conditional-flow.tex` adapts the flowchart's palette and process/flow styles, with new paired conditional RF topology and equations.

The local examples establish drawable, editable structural patterns, not venue certification. Match final dimensions/fonts against the actual paper template. Record any material assumptions and remaining semantic uncertainty with the produced figure.
