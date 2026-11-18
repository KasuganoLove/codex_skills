#!/usr/bin/env python3
"""Compile an existing TeX figure and export review artifacts. No topology validation.

Usage: compile_figure.py SOURCE.tex OUTPUT_DIR [--width-mm 178] [--svg] [--inspect]
Dependencies: one TeX engine plus PyMuPDF (fitz). No network or installation steps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from tex_environment import prepare_tex_environment


def atomic_json(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def warning(check, message, **data):
    return {"level": "WARN", "check": check, "message": message, **data}


def geometry(page, target_mm, min_font):
    bounds = page.rect
    native_mm = bounds.width * 25.4 / 72
    scale = target_mm / native_mm if target_mm else 1.0
    fonts = []
    small = []
    spans = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["text"].strip():
                    spans.append(span)
                    size = span["size"] * scale
                    fonts.append(size)
                    if size < min_font:
                        small.append({"text": span["text"][:100], "estimated_pt": round(size, 2)})
    boxes = []
    for entry in page.get_bboxlog():
        kind, box = entry[:2]
        if kind != "ignore-text" and all(abs(x) < 1e8 for x in box):
            boxes.append(box)
    content = None
    warnings = []
    if boxes:
        content = [min(b[0] for b in boxes), min(b[1] for b in boxes),
                   max(b[2] for b in boxes), max(b[3] for b in boxes)]
        if (content[0] < bounds.x0 - 1 or content[1] < bounds.y0 - 1 or
                content[2] > bounds.x1 + 1 or content[3] > bounds.y1 + 1):
            warnings.append(warning("content-outside-page", "Drawing bounds exceed the visible page; inspect for clipping."))
    else:
        warnings.append(warning("empty-page", "No text, image, or drawing bounds detected."))
    if not spans:
        warnings.append(warning("text-not-measurable", "No extractable text spans; assess labels visually."))
    if small:
        warnings.append(warning("small-text", f"{len(small)} text spans are estimated below {min_font:g} pt at the requested width.", samples=small[:12]))
    ratio = max(bounds.width / bounds.height, bounds.height / bounds.width)
    if ratio > 4:
        warnings.append(warning("extreme-aspect-ratio", "Aspect ratio exceeds 4:1; check layout at the target paper width."))
    return {"width_mm": round(native_mm, 3), "height_mm": round(bounds.height * 25.4 / 72, 3),
            "content_bbox_pt": content, "target_width_mm": target_mm,
            "font_scale_estimate": round(scale, 5),
            "minimum_estimated_font_pt": round(min(fonts), 2) if fonts else None,
            "text_span_count": len(spans), "warnings": warnings}


def inspect_upstream(source, pdf, timeout):
    script = Path(__file__).resolve().parent / "vendor/tikz_inspector/quality-report.py"
    result = {"status": "unavailable", "coverage": "Heuristic only; upstream catches internal exceptions. Empty findings do not prove correctness.", "warnings": []}
    if not script.is_file():
        result["error"] = "Vendored inspector is missing."
        return result
    try:
        run = subprocess.run([sys.executable, str(script), str(source), str(pdf)],
                             cwd=source.parent, capture_output=True, text=True,
                             errors="replace", timeout=timeout)
        result["returncode"] = run.returncode
        if run.returncode:
            raise RuntimeError(f"Inspector failed: {run.stderr[-1500:]}")
        match = re.search(r"--- JSON ---\s*\n(.*)", run.stdout, re.S)
        if not match:
            raise RuntimeError("Inspector did not return a JSON findings list.")
        findings = json.loads(match.group(1))
        if not isinstance(findings, list) or not all(isinstance(x, dict) for x in findings):
            raise RuntimeError("Inspector findings have an unexpected schema.")
        result.update(status="completed-heuristic", warnings=findings)
    except (OSError, subprocess.TimeoutExpired, ValueError, RuntimeError) as error:
        result.update(status="failed", error=str(error))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--engine", choices=["auto", "pdflatex", "xelatex", "lualatex"], default="auto")
    parser.add_argument("--width-mm", type=float, help="Estimate label size when included at this width; does not resize the figure.")
    parser.add_argument("--min-font-pt", type=float, default=7)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--timeout", type=int, default=120, help="Maximum seconds per compilation pass.")
    parser.add_argument("--svg", action="store_true", help="Export SVG with text converted to paths.")
    parser.add_argument("--inspect", action="store_true", help="Run vendored upstream quality heuristics; never a pass/fail gate.")
    args = parser.parse_args()
    if args.width_mm is not None and args.width_mm <= 0:
        parser.error("--width-mm must be positive")
    if not 36 <= args.dpi <= 600 or args.timeout <= 0 or args.min_font_pt <= 0:
        parser.error("Use 36 <= dpi <= 600 and positive timeout/min-font-pt")
    source = args.source.expanduser().resolve()
    out = args.output_dir.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    stem = source.stem
    report_path = out / f"{stem}.report.json"
    # Previous successful exports are preserved, but are never counted as this run's outputs.
    previous = sorted(str(p) for p in out.glob(stem + "*") if p.suffix in {".pdf", ".png", ".svg"})
    report = {"source": str(source), "started_at": datetime.now(timezone.utc).isoformat(),
              "compile_success": False, "export_success": False, "outputs": [],
              "previous_artifacts_retained": previous, "passes": [], "warnings": [],
              "topology_review": "not-performed", "visual_review": "not-performed",
              "font_estimate_note": "PDF text span sizes scaled to requested inclusion width; math scripts may legitimately be smaller."}
    atomic_json(report_path, report)
    build = None
    exitcode = 1
    try:
        if source.suffix.lower() != ".tex" or not source.is_file():
            raise RuntimeError("SOURCE must be an existing .tex file.")
        raw = source.read_bytes()
        report["source_sha256"] = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8")
        engines = [args.engine] if args.engine != "auto" else (
            ["xelatex", "lualatex"] if re.search(r"fontspec|xeCJK|ctex", text) else
            ["pdflatex", "xelatex", "lualatex"])
        engine = next((shutil.which(e) for e in engines if shutil.which(e)), None)
        if not engine:
            raise RuntimeError("No suitable TeX engine found. Available choices: pdflatex, xelatex, lualatex.")
        report["engine"] = engine
        try:
            import fitz
        except ImportError as error:
            raise RuntimeError("PyMuPDF (fitz) is required for PNG and PDF diagnostics.") from error
        build = Path(tempfile.mkdtemp(prefix=".figure-build-", dir=out))
        report["build_directory"] = str(build)
        tex_env, adjustments = prepare_tex_environment(engine, build / "tex-runtime")
        report["environment_adjustments"] = adjustments
        # Fixed ASCII jobname handles spaces and Unicode in input/output paths.
        cmd = [engine, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", "-jobname=figure", f"-output-directory={build}", str(source)]
        report["command"] = cmd
        for index in range(1, 3):
            log_path = out / f"{stem}.pass{index}.log"
            try:
                run = subprocess.run(cmd, cwd=source.parent, env=tex_env, capture_output=True, text=True,
                                     errors="replace", timeout=args.timeout)
                log_path.write_text(run.stdout + "\n" + run.stderr, encoding="utf-8")
                report["passes"].append({"pass": index, "returncode": run.returncode, "log": str(log_path)})
                if run.returncode:
                    raise RuntimeError(f"TeX compilation pass {index} failed; see {log_path.name}.")
            except subprocess.TimeoutExpired as error:
                partial = (error.stdout or b"")
                if isinstance(partial, bytes):
                    partial = partial.decode("utf-8", errors="replace")
                log_path.write_text(partial + "\nCOMPILATION TIMEOUT\n", encoding="utf-8")
                report["passes"].append({"pass": index, "timeout": True, "log": str(log_path)})
                raise RuntimeError(f"TeX compilation exceeded {args.timeout} seconds.") from error
        pdf = build / "figure.pdf"
        tex_warnings = re.findall(r"(?:LaTeX|Package \S+|Class \S+|pdfTeX) Warning:[^\n]+|(?:Over|Under)full \\[hv]box[^\n]+|Missing character:[^\n]+", run.stdout + run.stderr)
        if tex_warnings:
            report["warnings"].append(warning("tex-warnings", "TeX emitted warnings; review the complete pass log.", samples=list(dict.fromkeys(tex_warnings))[:20]))
        if not pdf.is_file() or not pdf.stat().st_size:
            raise RuntimeError("TeX returned success but no fresh nonempty PDF exists.")
        with fitz.open(pdf) as doc:
            if not len(doc):
                raise RuntimeError("Compiled PDF contains no pages.")
            report["compile_success"] = True
            report["page_count"] = len(doc)
            report["pages"] = []
            if len(doc) != 1:
                report["warnings"].append(warning("multiple-pages", "Expected a standalone single-page figure; review each exported page."))
            exports = [(pdf, out / f"{stem}.pdf")]
            for index, page in enumerate(doc):
                report["pages"].append(geometry(page, args.width_mm, args.min_font_pt))
                suffix = "" if len(doc) == 1 else f"-p{index + 1}"
                png = build / f"figure{suffix}.png"
                page.get_pixmap(dpi=args.dpi, alpha=False).save(png)
                exports.append((png, out / f"{stem}{suffix}.png"))
                if args.svg:
                    svg = build / f"figure{suffix}.svg"
                    svg.write_text(page.get_svg_image(text_as_path=True), encoding="utf-8")
                    exports.append((svg, out / f"{stem}{suffix}.svg"))
            report["svg_text"] = "outlined paths; edit labels in TeX source" if args.svg else None
        if args.inspect:
            report["upstream_inspection"] = inspect_upstream(source, pdf, min(args.timeout, 60))
            if report["upstream_inspection"]["status"] != "completed-heuristic":
                report["warnings"].append(warning("inspector-unavailable", "Optional upstream inspection failed or is unavailable; review its status."))
        # Publish only freshly generated outputs, after complete rendering.
        for src, dest in exports:
            tmp = dest.with_suffix(dest.suffix + ".tmp")
            shutil.copyfile(src, tmp)
            os.replace(tmp, dest)
            report["outputs"].append(str(dest))
        report["export_success"] = True
        report["output_sha256"] = {str(dest): hashlib.sha256(dest.read_bytes()).hexdigest() for _, dest in exports}
        exitcode = 0
    except Exception as error:
        report["error"] = str(error)
    finally:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        atomic_json(report_path, report)
        if build and exitcode == 0:
            shutil.rmtree(build)
            report.pop("build_directory", None)
            atomic_json(report_path, report)
    print(json.dumps({"compile_success": report["compile_success"], "export_success": report["export_success"],
                      "report": str(report_path), "outputs": report["outputs"], "error": report.get("error")}, ensure_ascii=False))
    return exitcode


if __name__ == "__main__":
    sys.exit(main())
