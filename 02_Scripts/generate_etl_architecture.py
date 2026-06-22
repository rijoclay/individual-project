# -*- coding: utf-8 -*-
"""
generate_etl_architecture.py — ETL Medallion Architecture Diagram (Bronze → Silver → Gold)
Professional style matching ERD: dark theme, clear flow arrows
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis("off")
fig.patch.set_facecolor("#FAFAFA")

# Colors
SRC_BG = "#E8F5E9"; SRC_HD = "#1B5E20"
BRONZE_BG = "#FFF3E0"; BRONZE_HD = "#E65100"
SILVER_BG = "#E3F2FD"; SILVER_HD = "#0D47A1"
GOLD_BG = "#FFF9C4";   GOLD_HD = "#F57F17"
OUT_BG = "#F3E5F5";    OUT_HD = "#4A148C"
ARROW_C = "#455A64"

def draw_box(ax, x, y, w, h, hd_color, bg_color, title, lines, hd_fs=9, fs=7.5):
    box = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                  facecolor=bg_color, edgecolor="#B0BEC5", linewidth=1.2)
    ax.add_patch(box)
    ax.add_patch(mpatches.FancyBboxPatch((x, y+h-0.38), w, 0.38,
                  boxstyle="round,pad=0.04", facecolor=hd_color, edgecolor="none"))
    ax.text(x+w/2, y+h-0.19, title, ha="center", va="center",
            fontsize=hd_fs, fontweight="bold", color="white", family="sans-serif")
    for i, ln in enumerate(lines):
        ax.text(x+w/2, y+h-0.58-i*0.22, ln, ha="center", va="center",
                fontsize=fs, color="#212121", family="sans-serif")

def arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_C, lw=2, shrinkA=5, shrinkB=5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.18, label, ha="center", va="bottom",
                fontsize=7, color="#616161", style="italic", family="sans-serif")

# ── Title ──
ax.text(7, 6.7, "ETL Medallion Architecture — Data Flow Diagram",
        ha="center", va="center", fontsize=14, fontweight="bold",
        color="#212121", family="sans-serif")

# ── Data Sources ──
src_x, src_y, src_w, src_h = 0.2, 1.8, 2.0, 3.8
draw_box(ax, src_x, src_y, src_w, src_h, SRC_HD, SRC_BG,
         "DATA SOURCES", [
             "S1: CSV Dataset",
             "   5,500 records",
             "S2: JSON Benchmarks",
             "   11 industries",
             "S3: Logs CSV",
             "   5,500 rows",
             "S4: OpenAlex API",
             "   25 papers",
         ], fs=7)

# ── Bronze Layer ──
br_x, br_y, br_w, br_h = 3.0, 2.5, 2.2, 2.5
draw_box(ax, br_x, br_y, br_w, br_h, BRONZE_HD, BRONZE_BG,
         "BRONZE LAYER", [
             "Raw Ingestion",
             "• Parquet format",
             "• Schema enforcement",
             "• Metadata (src, ts)",
             "• 4 partitioned dirs",
         ], fs=7.5)

# ── Silver Layer ──
sv_x, sv_y, sv_w, sv_h = 6.0, 2.5, 2.2, 2.5
draw_box(ax, sv_x, sv_y, sv_w, sv_h, SILVER_HD, SILVER_BG,
         "SILVER LAYER", [
             "Cleansing & Enrich",
             "• Dedup (Record_ID)",
             "• Median imputation",
             "• Derived columns",
             "• NLP contextual map",
             "• 5,500 clean records",
         ], fs=7.5)

# ── Gold Layer ──
gl_x, gl_y, gl_w, gl_h = 9.0, 2.5, 2.2, 2.5
draw_box(ax, gl_x, gl_y, gl_w, gl_h, GOLD_HD, GOLD_BG,
         "GOLD LAYER", [
             "Analytics & ML",
             "• K-Means (k=3)",
             "  Sil=0.5276",
             "• LogReg (multiclass)",
             "  Acc=55.44%",
             "• Feature isolation",
         ], fs=7.5)

# ── Output / Data Marts ──
out_x, out_y, out_w, out_h = 11.9, 2.2, 1.9, 3.0
draw_box(ax, out_x, out_y, out_w, out_h, OUT_HD, OUT_BG,
         "OUTPUT", [
             "ai_enriched",
             "industry_summary",
             "cluster_profile",
             "models/lr_export",
             "charts (.png)",
         ], fs=7.5)

# ── Arrows ──
arrow(ax, src_x+src_w, src_y+src_h/2, br_x, br_y+br_h/2)
arrow(ax, br_x+br_w, br_y+br_h/2, sv_x, sv_y+sv_h/2)
arrow(ax, sv_x+sv_w, sv_y+sv_h/2, gl_x, gl_y+gl_h/2)
arrow(ax, gl_x+gl_w, gl_y+gl_h/2, out_x, out_y+out_h/2)

# ── Layer Labels Below ──
labels = [
    (src_x+src_w/2, 1.4, "Ingest",  SRC_HD),
    (br_x+br_w/2, 1.4, "Raw Store", BRONZE_HD),
    (sv_x+sv_w/2, 1.4, "Cleanse",  SILVER_HD),
    (gl_x+gl_w/2, 1.4, "Analyse",  GOLD_HD),
    (out_x+out_w/2, 1.4, "Deliver", OUT_HD),
]
for lx, ly, lt, lc in labels:
    ax.text(lx, ly, lt, ha="center", va="center", fontsize=8,
            fontweight="bold", color=lc, family="sans-serif")

# ── Legend ──
legend_items = [
    (SRC_HD, "Source"), (BRONZE_HD, "Bronze"), (SILVER_HD, "Silver"),
    (GOLD_HD, "Gold"), (OUT_HD, "Output"),
]
for i, (c, lbl) in enumerate(legend_items):
    bx = 4.2 + i*1.4
    ax.add_patch(mpatches.FancyBboxPatch((bx, 0.35), 0.25, 0.25,
                 boxstyle="round,pad=0.02", facecolor=c, edgecolor="#9E9E9E"))
    ax.text(bx+0.35, 0.47, lbl, fontsize=7.5, va="center", color="#424242", family="sans-serif")

plt.tight_layout(pad=0.5)
OUT = r"C:\Users\richa\Documents\Sem.6\DatEng_Individual_Project\individual_project_2\06_Visualization\etl_architecture.png"
plt.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="#FAFAFA")
plt.close()
print(f"ETL Architecture saved to: {OUT}")
