# PlotNeuralNet backend

Use this backend for spatial feature hierarchies, CNNs and U-Nets. Use the flat
TikZ templates for attention internals and dense training/loss branches.

## Generate the bundled examples

Resolve `SKILL_ROOT` to this skill's actual directory. Run:

```bash
python "$SKILL_ROOT/assets/plotneuralnet/generate_examples.py" \
  --out-dir "$OUTPUT_DIR" --example all
```

The command writes `unet_3d.tex`, `cnn_3d.tex`, `layers/`, and
`PLOTNEURALNET-LICENSE` into the output directory. Compile from that directory
with the skill's build helper or `pdflatex -halt-on-error -interaction=nonstopmode
-no-shell-escape unet_3d.tex`. Run for CNN similarly. Keep `layers/` beside the
TeX source when delivering or moving it. Python is only needed to regenerate the
starting template; the generated TeX can be edited and compiled independently.

`--example unet` and `--example cnn` select one example. The generator imports
the original upstream `pycore.tikzeng` and uses the upstream Box drawing macros.
The upstream API has legacy escape-string SyntaxWarnings on Python 3.12; these
do not prevent generation. Do not interpret them as successful TeX compilation.

## Template contracts

| Template | Meaning | Adaptation rules |
| --- | --- | --- |
| `unet_3d.tex` | Generic three-resolution U-Net; input/output 3×128×128; channels 32/64/128; same-padded 3×3 convolutions; two max-pools; transposed-convolution upsampling; channel concatenation skips | Keep copy branches connected to concatenation circles, not addition circles. After changing resolutions/channels, recalculate each concat input and following decoder convolution. Update every shape label. |
| `cnn_3d.tex` | Generic 3-layer encoder; input 3×128×128; 32/64/128 channels; 3×3 kernels with p=1; strides 1/2/2 | Recalculate H/W from kernel, padding, stride and dilation. Drawing dimensions are schematic and must never be interpreted as numeric dimensions. |

Preserve semantic node IDs (`enc1`, `enc2`, `bottom`, `cat1`, `cat2`, `dec1`,
`dec2`, `out`, or `c1`–`c3`) when editing existing figures. Keep all tensor labels
in C×H×W order. Use solid directed arrows for main data flow and dashed orange
arrows for copy/skip paths. Avoid identifying this generic U-Net with the original
2015 valid-convolution U-Net, which used cropping and different sizes.

The examples are editable starting points, not automatic model tracers. Replace
their example architecture from the user's actual code/description before
claiming that a figure represents their model. The spatial sizes are explicitly
labelled; block widths/heights use schematic values for legibility.

## Pinned upstream and modifications

Source: [HarisIqbal88/PlotNeuralNet](https://github.com/HarisIqbal88/PlotNeuralNet),
commit `e96bc852189c2089dd500527a0a01a5a36e8977e`.
All upstream files listed below were fetched as text from immutable raw URLs of
the form `https://raw.githubusercontent.com/HarisIqbal88/PlotNeuralNet/e96bc852189c2089dd500527a0a01a5a36e8977e/<path>`.

| File | Upstream Git blob |
| --- | --- |
| `LICENSE` | `914f9771afab2dfb21557d400fd0a78fff4b01c9` |
| `layers/Ball.sty` | `b5fa719f3e5ae0c294fa572b84595f938129898d` |
| `layers/Box.sty` | `38818a87fa8aadeaddc723fe1f6abbfd486f321b` |
| `layers/RightBandedBox.sty` | `7d74a514df8dac6512214f566ee07b46f31eb074` |
| `layers/init.tex` | `9a9b3eb09d9c616a1fb06dd6a608f3369df4b1da` |
| `pycore/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `pycore/blocks.py` | `82c2c2a8260877f3274616cb4d459f8bfa534a36` |
| `pycore/tikzeng.py` | `8e988c449c3733c73b96b9f8630beda874adcddf` |

The layer/API source and MIT notice are retained verbatim (including the empty
Python package marker). `generate_examples.py` is a new integration/example
generator: it changes palette, topology layout, labels and arrow conventions at
the call site, without changing upstream implementation. Retain the bundled MIT
notice with reused substantial source. No compiled `.pyc` files are included.

## Environment

Need a complete LaTeX installation with the `pdflatex` format, `standalone`,
`import`, PGF/TikZ and `amsmath`. Executable discovery alone is insufficient:
verify package lookup and an actual compile. Render the resulting PDF and inspect
labels/arrows at the target paper width before describing it as publication-ready.
