#!/usr/bin/env python3
"""Report installed engines, figure packages and Python libraries; install nothing."""
import importlib.util
import json
import shutil
import subprocess
import sys
import os
from tex_environment import query

engines = {name: shutil.which(name) for name in ("pdflatex", "xelatex", "lualatex")}
packages = {}
kpsewhich = shutil.which("kpsewhich")
env = os.environ.copy()
recursive_lookup = False
if not query("article.cls", env):
    tree = query("--var-value=TEXMF", env)
    candidate = dict(env, TEXMF=tree.replace("!!", ""))
    if query("article.cls", candidate):
        env = candidate
        recursive_lookup = True
for name in ("article.cls", "standalone.cls", "tikz.sty", "amsmath.sty", "xcolor.sty", "import.sty"):
    if kpsewhich:
        try:
            found = subprocess.run([kpsewhich, name], env=env, capture_output=True, text=True, timeout=10)
            packages[name] = found.stdout.strip() if found.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            packages[name] = None
    else:
        packages[name] = None
python = {name: importlib.util.find_spec(name) is not None for name in ("fitz",)}
ready = any(engines.values()) and all(packages.values()) and all(python.values())
print(json.dumps({"ready_for_bundled_templates": ready, "engines": engines,
                  "requires_process_local_index_recovery": recursive_lookup,
                  "kpsewhich": kpsewhich, "tex_packages": packages, "python_modules": python,
                  "note": "Package availability is a preflight check; successful compilation and visual review are still required."}, indent=2))
sys.exit(0 if ready else 1)
