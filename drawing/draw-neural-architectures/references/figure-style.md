# Figure style and export

Choose the visual grammar by what the reader needs to follow:

| Structure | Useful representation | Evidence to retain |
| --- | --- | --- |
| Convolutional VAE / multiscale encoder–decoder | Feature-map planes or volumes for stages; enlarge a convolution/residual unit when its internals matter | Spatial sizes and channels where verified; state when drawn scale/thickness is schematic |
| Transformer / DiT / multimodal attention | Planar computation graph with distinct streams and internal operations | Actual Q/K/V sources, attention and MLP paths, norm, modulation, gates and residual routes only where present |
| Mixed or compared models | End-to-end overview plus selected module expansions using the appropriate grammar for each | Consistent comparison labels while preserving different stream layouts, conditioning and block designs |

Choose the number and depth of panels from the explanation, not a fixed quota per model. A block name alone is insufficient when the question concerns its computation; a local operator question need not expand the entire network. Inspect relevant primary figures for hierarchy, grouping and reading order without copying their unverified structure.

Default to white, dark text, muted blue computation, green conditioning, orange merge/resize, and one stronger accent for user-identified contributions. These are reversible defaults. Add labels/patterns so color is not the only encoding.

Keep short labels inside boxes and shapes outside. Give arrows routing lanes. Use consistent panel labels and local legends; preserve names and tensor/condition interfaces between overview and enlarged blocks.

Use actual manuscript column/text width if known. Otherwise state an approximate target such as 170 mm for a wide figure, to revisit when the venue is known. Prefer rearrangement/two panels over shrinking text. Aim for effective text near 8–10 pt, about 7 pt as a warning threshold rather than a claimed venue rule. The compiler's width-based scale estimate supplements visual inspection. Never assume universal conference widths.

Export tightly bounded vector PDF with margin. PNG is a preview, normally 180–240 dpi and higher on request. SVG may outline text; retain .tex as authoritative source. Include relative assets and license notices. Avoid absolute installed-skill paths in deliverable .tex.

For Chinese use XeLaTeX with an available CJK font and verify glyphs. Match publication fonts against the actual manuscript class/style where possible; retain editable vectors.
