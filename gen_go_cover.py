"""Generate a Go-language themed blog cover image.
Style: dark tech theme (#0a0e27 base) with Go's signature cyan accents,
terminal/code aesthetic -- NOT the AI-frontier neural network look.
Output: D:/hermes/priblog/source/img/cover-go.png (1024x576, 16:9)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np
from matplotlib import font_manager as fm

# Register a CJK-capable font (SimHei) so Chinese glyphs render.
CJK_FONT = "C:/Windows/Fonts/simhei.ttf"
if __import__("os").path.exists(CJK_FONT):
    fm.fontManager.addfont(CJK_FONT)
    cjk_name = fm.FontProperties(fname=CJK_FONT).get_name()
else:
    cjk_name = "DejaVu Sans"

W, H = 1024, 576
BG = "#0a0e27"
CYAN = "#00ADD8"      # Go's official brand cyan
LIGHT_CYAN = "#5DCFF0"
DARK_PANEL = "#10153a"
WHITE = "#e8f0ff"
DIM = "#6b7ba8"

fig, ax = plt.subplots(figsize=(W/100, H/100), dpi=100)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# subtle circuit-grid background dots
for x in np.arange(0, W, 48):
    for y in np.arange(0, H, 48):
        ax.plot(x, y, ".", color=CYAN, markersize=1.2, alpha=0.10)

# top accent bar (Go flag vibe)
ax.add_patch(Rectangle((0, 0), W, 8, facecolor=CYAN, edgecolor="none", alpha=0.9))

# main terminal panel
panel = FancyBboxPatch((70, 150), W-140, H-230,
                       boxstyle="round,pad=0.02,rounding_size=18",
                       linewidth=1.5, edgecolor=CYAN, facecolor=DARK_PANEL, alpha=0.92)
ax.add_patch(panel)

# terminal title bar
ax.add_patch(Rectangle((70, 468), W-140, 34, facecolor="#0d1230", edgecolor="none"))
for c in ["#ff5f56", "#ffbd2e", "#27c93f"]:
    ax.add_patch(Circle((96, 485), 7, facecolor=c, edgecolor="none"))
ax.text(120, 486, "go run evolution.go", color=DIM, fontsize=13,
        fontfamily="monospace", va="center")

# code lines with Go syntax highlighting
code_lines = [
    ("package ", DIM, "main"),
    ("", None, ""),
    ("func ", LIGHT_CYAN, "Sum[T "),
    ("~int | ~float64", CYAN, ""),
    ("] ", WHITE, "{"),
    ("    ", DIM, "var total T"),
    ("    ", DIM, "for _, v := range vals {"),
    ("        ", DIM, "total += v"),
    ("    ", DIM, "}"),
    ("    ", DIM, "return total"),
    ("}", WHITE, ""),
]
y = 430
line_h = 26
for prefix, pcolor, rest in code_lines:
    if not prefix and not rest:
        y -= line_h * 0.5
        continue
    ax.text(110, y, prefix, color=pcolor or WHITE, fontsize=14,
            fontfamily="monospace", va="center")
    if rest:
        ax.text(110 + len(prefix) * 8.2, y, rest, color=WHITE, fontsize=14,
                fontfamily="monospace", va="center")
    y -= line_h

# big title text (top area)
fp_title = fm.FontProperties(fname=CJK_FONT)
ax.text(W/2, 512, "Go 语言十年演进史", color=WHITE, fontsize=40,
        ha="center", va="center", weight="bold", fontproperties=fp_title)

# subtitle with version badge
ax.add_patch(FancyBboxPatch((W/2-130, 96), 260, 44,
                            boxstyle="round,pad=0.03,rounding_size=12",
                            linewidth=1.2, edgecolor=CYAN, facecolor=CYAN, alpha=0.15))
fp_sub = fm.FontProperties(fname=CJK_FONT)
ax.text(W/2, 118, "从诞生到 Go 1.24 的蜕变之路", color=LIGHT_CYAN, fontsize=19,
        ha="center", va="center", weight="bold", fontproperties=fp_sub)

# decorative concurrency arrows bottom-right
for i, dx in enumerate([0, 60, 120]):
    ax.annotate("", xy=(W-110+dx, 60), xytext=(W-150+dx, 60),
                arrowprops=dict(arrowstyle="->", color=CYAN, lw=2.5, alpha=0.5-i*0.12))

# thin bottom accent line
ax.add_patch(Rectangle((0, H-8), W, 8, facecolor=LIGHT_CYAN, edgecolor="none", alpha=0.7))

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig("D:/hermes/priblog/source/img/cover-go.png", dpi=100,
            facecolor=BG, bbox_inches="tight", pad_inches=0)
print("WROTE cover-go.png")
