# 科研绘图技能

把本页链接发给本地 Codex 或能访问此仓库的 Agent，即可让它安装下面两套技能。日常维护和更新都使用同一个链接。

| 技能 | 什么时候用 | 主要产物 |
| --- | --- | --- |
| [draw-neural-architectures](./draw-neural-architectures/SKILL.md) | 从论文或 forward 画模型总览，展开 CNN、Transformer、DiT 或 Flow 模块，核对残差和条件注入 | 可编辑 TeX、矢量 PDF、PNG 预览；含 TikZ 和 PlotNeuralNet 模板 |
| [scientific-figure-making](./scientific-figure-making/SKILL.md) | 用已有实验数据画消融曲线、分组柱状图、热图和多面板图 | Matplotlib 绘图代码、矢量图和位图；含配色、数值编码和排版规范 |

## 复制这句话给 Agent

> 请从 https://github.com/KasuganoLove/codex_skills/tree/main/drawing 安装两套科研绘图技能，按本页的安装步骤保留两个完整技能目录。检查是否能发现两套技能，并用附带的 DiT 示例验证 PDF 和 PNG 导出。

仓库为私有时，目标环境需要已授权的 GitHub 连接或具有读取权限的本地 Git 凭据。

## 安装步骤

1. 获取仓库默认分支。已登录 GitHub CLI 的环境可运行 `gh repo clone KasuganoLove/codex_skills`。已有本地副本时，在仓库中运行 `git pull --ff-only`。
2. 从 `drawing/` 取出表中的两个子目录，各自保留顶层 `SKILL.md` 及内部模板、脚本和参考文件。
3. 按目标环境放置两个目录：

   | 目标 | 安装位置 |
   | --- | --- |
   | 本地 Codex，所有项目共用 | 用户主目录的 `.agents/skills/` |
   | 本地 Codex，仅当前项目 | 项目根目录的 `.agents/skills/` |
   | 其他支持 Agent Skills 的客户端 | 该客户端配置的技能目录 |
   | 可读取项目文件的通用 Agent | 在项目里保留 `drawing/`，在项目指令中注明“绘制架构图或结果图时，先读 drawing/ 中对应技能的 SKILL.md，按其相对路径加载模板和脚本” |

在 macOS、Linux 或 WSL 上，可以**从克隆的仓库根目录**执行下列命令进行 Codex 用户级安装。使用符号链接后，更新仓库即可同步技能。若已有同名目录，先核对来源，保留本地改动。

```bash
mkdir -p "$HOME/.agents/skills"
for name in draw-neural-architectures scientific-figure-making; do
  dest="$HOME/.agents/skills/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "已存在，请核对来源：$dest"
  else
    ln -s "$PWD/drawing/$name" "$dest"
  fi
done
```

Windows 也可以把两个技能文件夹复制到 `%USERPROFILE%\.agents\skills\`。以后更新时，在拉取新版本后同步复制。Codex 中输入 `$` 查看两个技能名，若列表未刷新，重启会话。

## 验证绘图环境

架构图使用 Python 3、PyMuPDF 和 TeX Live 或 MiKTeX。LaTeX 组件包含 standalone、TikZ/PGF 和 import 等，中文标签另需 XeLaTeX 和中文字体。结果图使用 Python 3 和 Matplotlib。安装技能目录后，可在自己的 Python 环境中用 `python -m pip install pymupdf matplotlib` 补齐 Python 依赖。

以下命令从仓库根目录执行，将示例输出到临时目录：

```bash
skill_dir=./drawing/draw-neural-architectures
out_dir="$(mktemp -d)"
python "$skill_dir/scripts/check_env.py"
python "$skill_dir/scripts/compile_figure.py" "$skill_dir/assets/tikz/dit-block.tex" "$out_dir" --width-mm 170
python -c "import matplotlib; print(matplotlib.__version__)"
echo "$out_dir"
```

在输出目录打开 `dit-block.pdf` 和 `dit-block.png` 即可核对渲染。日常使用时把成图和可编辑源码保存到目标项目指定的目录，例如 `figures/`。

## 使用示例

- `$draw-neural-architectures 读取这个仓库的 forward，画一张模型总览，再展开条件注入的 DiT block。核对残差和张量形状，导出 TeX、PDF 和 PNG。`
- `$scientific-figure-making 读取 ablation.csv，以推理步数为横轴，分面展示 PSNR 和 LPIPS。保留各自单位，导出 Python 源码、PDF 和 PNG。`

模板、第三方脚本的来源与许可保存在各技能的 references、assets 和 scripts/vendor 下。
