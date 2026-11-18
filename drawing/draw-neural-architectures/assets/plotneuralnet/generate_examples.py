#!/usr/bin/env python3
"""Render editable PlotNeuralNet examples using the bundled upstream API/layers.

Run: python generate_examples.py --out-dir /absolute/output --example all
Then compile each .tex from that output directory. No network is needed.
"""
from pathlib import Path
import argparse
import shutil
import sys

sys.dont_write_bytecode = True
from pycore.tikzeng import to_head, to_end

ROOT = Path(__file__).resolve().parent

def preamble():
    return to_head('.') + r'''
\usepackage{amsmath}
\usetikzlibrary{calc}
\definecolor{feature}{HTML}{93BDD8}
\definecolor{bottleneck}{HTML}{B8A6D7}
\definecolor{edgeink}{HTML}{425466}
\definecolor{accent}{HTML}{DE9553}
\begin{document}
\begin{tikzpicture}[font=\sffamily\small,
 flow/.style={-Stealth,draw=edgeink,line width=0.8pt},
 skip/.style={-Stealth,draw=accent,dashed,line width=0.9pt},
 op/.style={draw=edgeink,fill=white,rounded corners=2pt,inner sep=5pt,align=center},
 tensor/.style={font=\sffamily\footnotesize,align=center},
 cat/.style={circle,draw=accent,fill=white,inner sep=2pt,font=\sffamily\footnotesize}]
'''

def box(name, x, y, size, color='feature'):
    # Feature sizes are written exactly. Drawing dimensions are schematic.
    return rf'''
\pic at ({x},{y},0) {{Box={{name={name},width=3,height={size},depth={size},
 fill={color},opacity=0.85,xlabel={{{{"",""}}}},caption=}}}};
'''

def unet():
    parts=[preamble()]
    for a in [('enc1',0,0,10),('enc2',0,-3.4,7),
              ('bottom',4.7,-6.4,5,'bottleneck'),
              ('dec2',9.6,-3.4,7),('dec1',9.6,0,10)]:
        parts.append(box(*a))
    parts.append(r'''
\node[tensor,anchor=east] (input) at (-1.1,0) {Input: $3\!\times\!128\!\times\!128$\\$2\!\times\!(3\!\times\!3)$ Conv + ReLU\\$32\!\times\!128\!\times\!128$};
\node[tensor,anchor=east] at (-1.1,-3.4) {Encoder 2\\$2\!\times\!(3\!\times\!3)$ Conv + ReLU\\$64\!\times\!64\!\times\!64$};
\node[tensor,anchor=north] at (5,-7.3) {Bottleneck: $128\!\times\!32\!\times\!32$\\$2\!\times\!(3\!\times\!3)$ Conv + ReLU};
\node[tensor,anchor=west] at (10.9,-3.4) {Decoder 2: $2\!\times\!$Conv + ReLU\\$128\to64$ channels\\$64\!\times\!64\!\times\!64$};
\node[tensor,anchor=west] at (10.9,0) {Decoder 1: $2\!\times\!$Conv + ReLU\\$64\to32$ channels\\$32\!\times\!128\!\times\!128$};
\draw[flow] (input.east) -- (enc1-west);
\node[cat] (cat2) at (8,-3.4) {$\Vert$};
\node[cat] (cat1) at (8,0) {$\Vert$};
\draw[flow] (enc1-south) -- node[right=3pt,font=\footnotesize] {$2\!\times\!2$ pool} (enc2-north);
\draw[flow] (enc2-south) -- (0.3,-6.4) -- node[above,font=\footnotesize] {$2\!\times\!2$ pool} (bottom-west);
\draw[flow] (bottom-east) -- (8,-6.4) -- node[right=3pt,font=\footnotesize,align=left] {up-conv $2\!\times\!2$\\$128\to64$} (cat2.south);
\draw[flow] (cat2.east) -- (dec2-west);
\draw[flow] (dec2-north) -- (9.9,-1.9) -- (8,-1.9) -- node[left=3pt,font=\footnotesize,align=right] {up-conv $2\!\times\!2$\\$64\to32$} (cat1.south);
\draw[flow] (cat1.east) -- (dec1-west);
\draw[skip] (enc2-east) -- node[above,font=\footnotesize] {copy $64\!\times\!64\!\times\!64$} (cat2.west);
\draw[skip] (enc1-east) -- node[above,font=\footnotesize] {copy $32\!\times\!128\!\times\!128$} (cat1.west);
\node[op] (out) at (9.9,2.3) {$1\!\times\!1$ Conv $32\to3$\\Output: $3\!\times\!128\!\times\!128$};
\draw[flow] (dec1-north) -- (out.south);
\node[font=\sffamily\bfseries\large] at (5,3.4) {Three-resolution U-Net};
\node[font=\sffamily\footnotesize,align=center] at (5,-8.6) {Generic example; same-padded convolutions; $C\!\times\!H\!\times\!W$ labels.\\$\Vert$: concatenate channels. Block dimensions are schematic.};
''')
    return ''.join(parts)+to_end()

def cnn():
    parts=[preamble()]
    for a in [('c1',0,0,10),('c2',3.6,0,7),('c3',7.2,0,5)]:
        parts.append(box(*a))
    parts.append(r'''
\node[font=\sffamily\bfseries\large] at (4,2.6) {Multiscale convolutional encoder};
\node[tensor,anchor=north] at (0.3,-1.7) {Conv $3\to32$, $3\!\times\!3$, $s=1$\\ReLU\\$32\!\times\!128\!\times\!128$};
\node[tensor,anchor=north] at (3.9,-1.7) {Conv $32\to64$, $3\!\times\!3$, $s=2$\\ReLU\\$64\!\times\!64\!\times\!64$};
\node[tensor,anchor=north] at (7.5,-1.7) {Conv $64\to128$, $3\!\times\!3$, $s=2$\\ReLU\\$128\!\times\!32\!\times\!32$};
\node[tensor,anchor=east] (input) at (-1.2,0) {Input\\$3\!\times\!128\!\times\!128$};
\draw[flow] (input.east) -- (c1-west);
\draw[flow] (c1-east) -- (c2-west);
\draw[flow] (c2-east) -- (c3-west);
\node[font=\sffamily\footnotesize,align=center] at (3.9,-3.5) {Generic example; padding $p=1$ for all convolutions.\\Tensor labels: $C\!\times\!H\!\times\!W$. Block dimensions are schematic.};
''')
    return ''.join(parts)+to_end()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',required=True,type=Path)
    parser.add_argument('--example',choices=['all','unet','cnn'],default='all')
    args=parser.parse_args()
    out=args.out_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'layers',out/'layers',dirs_exist_ok=True)
    shutil.copy2(ROOT/'LICENSE',out/'PLOTNEURALNET-LICENSE')
    for name, fn in [('unet',unet),('cnn',cnn)]:
        if args.example in ('all',name):
            target=out/f'{name}_3d.tex';target.write_text(fn(),encoding='utf-8');print(target)

if __name__=='__main__':
    main()
