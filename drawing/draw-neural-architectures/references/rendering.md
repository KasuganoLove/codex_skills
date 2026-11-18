# Compile and review

Resolve `SKILL_ROOT` to the installed directory containing SKILL.md. Do not hard-code an installation ID or past scratch path. Use a writable output directory outside the installed skill.

```bash
python "$SKILL_ROOT/scripts/check_env.py"
python "$SKILL_ROOT/scripts/compile_figure.py" figure.tex ./rendered --width-mm 170 --inspect
# Optional vector SVG; its text is outlined, not editable as text:
python "$SKILL_ROOT/scripts/compile_figure.py" figure.tex ./rendered --svg
```

The compiler runs two bounded passes in a fresh build directory, disables shell escape, uses the source directory for relative imports, and exports PDF/PNG with JSON diagnostics. It does not alter the source or resize the figure. `--width-mm` estimates text size at the eventual inclusion width. Choose the intended width based on the manuscript, not a universal conference default.

Read `<name>.report.json`: compilation, export, available inspector checks, previous artifacts, and unresolved reviews are distinct. A nonzero run or `compile_success=false` cannot deliver an old PDF as a new result. Old successful files may remain; use only outputs listed for the current successful run. The report records source hash; after editing, recompile. Inspect PNG with an image viewer and review topology separately; automated JSON deliberately starts those reviews as not performed.

Dependencies: Python + PyMuPDF; a supported TeX engine and required LaTeX packages (at least article, standalone and TikZ). The optional vendored quality reporter additionally uses available PDF support. It is a heuristic warning source, not a complete 15-sensor certification. Its provenance/license are under `scripts/vendor/tikz_inspector/`. An empty warning list does not prove the detector examined all layout features.

Some environments have TeX binaries/packages but missing file indexes, format caches or font maps. The bundled helper can search existing system TeX trees without index-only lookup and locally generate a missing pdfLaTeX format/font map in the build directory. This changes only process environment and local build files; it does not install packages globally. It must not hide absent packages. Engine-specific features or XeLaTeX/LuaLaTeX cache recovery may require additional setup; report actual results.

Options include `--engine auto|pdflatex|xelatex|lualatex`, `--dpi`, `--timeout`, `--min-font-pt`, `--inspect`, `--svg`. Run `--help` for current flags. For CJK source use an appropriate engine/font and inspect actual characters. Do not claim CJK is supported merely because a binary exists.

Copy complete source resources into the user's deliverable folder. For PlotNeuralNet, its generator copies the required layers relative to the generated .tex; keep that layers directory. If delivering editable Python, also include its needed pycore/layers and license. Keep cache/log files out of the final source folder unless requested for debugging.
