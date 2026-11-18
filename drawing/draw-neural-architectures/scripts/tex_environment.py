"""Process-local recovery for installed TeX trees with missing indexes/formats.

No packages are installed and no system configuration is changed. Repairs are
limited to pdflatex; other engines use their normal installed configuration.
"""
import os
from pathlib import Path
import shutil
import subprocess


def query(argument, env):
    kpse = shutil.which("kpsewhich")
    if not kpse:
        return ""
    try:
        run = subprocess.run([kpse, argument], env=env, capture_output=True,
                             text=True, timeout=15)
        return run.stdout.strip() if run.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def prepare_tex_environment(engine, cache):
    env = os.environ.copy()
    changes = []
    if not query("article.cls", env):
        tree = query("--var-value=TEXMF", env)
        if "!!" in tree:
            candidate = dict(env, TEXMF=tree.replace("!!", ""))
            if query("article.cls", candidate):
                env = candidate
                changes.append("Use recursive TeX tree lookup because installed indexes are missing.")
    if Path(engine).name != "pdflatex" or not query("article.cls", env):
        return env, changes
    cache.mkdir(parents=True, exist_ok=True)
    env["TEXFORMATS"] = str(cache) + "//:" + env.get("TEXFORMATS", "")
    env["TEXFONTMAPS"] = str(cache) + "//:" + env.get("TEXFONTMAPS", "")
    if not query("pdflatex.fmt", env):
        pdftex = shutil.which("pdftex")
        if not pdftex:
            raise RuntimeError("pdflatex format is absent and pdftex is unavailable to rebuild it.")
        cmd = [pdftex, "-ini", "-etex", "-no-shell-escape", "-halt-on-error",
               "-interaction=nonstopmode", "-jobname=pdflatex", "-progname=pdflatex", "pdflatex.ini"]
        run = subprocess.run(cmd, cwd=cache, env=env, capture_output=True,
                             text=True, errors="replace", timeout=90)
        (cache / "format-build.log").write_text(run.stdout + "\n" + run.stderr, encoding="utf-8")
        if run.returncode or not (cache / "pdflatex.fmt").is_file():
            raise RuntimeError(f"Unable to build installed pdflatex format; see {cache / 'format-build.log'}")
        changes.append("Built pdflatex format from installed sources in a local build cache.")
    if not query("pdftex.map", env):
        roots = [Path(query("--var-value=TEXMFDIST", env)), Path("/usr/share/texmf")]
        maps = []
        for root in roots:
            maps.extend(root.glob("fonts/map/dvips/amsfonts/*.map"))
            maps.extend(root.glob("fonts/map/dvips/lm/lm.map"))
        maps = sorted(set(maps))
        if maps:
            (cache / "pdftex.map").write_text("\n".join(p.read_text(errors="replace") for p in maps), encoding="utf-8")
            changes.append("Built local AMS/Latin Modern font map from installed map fragments; inspect embedding for other font families.")
    return env, changes
