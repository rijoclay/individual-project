# -*- coding: utf-8 -*-
"""
generate_erd.py — Generates a highly professional Star Schema ERD for the Proposal.
Fact table: Red
Dimension tables: Blue
Lines: Orthogonal/clean connections.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIZ_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '06_Visualization'))
ERD_PATH = os.path.join(VIZ_DIR, 'star_schema_erd.png')

# Colors
COLOR_FACT_HEAD = '#B71C1C'   # Dark Red
COLOR_FACT_BODY = '#FFEBEE'   # Light Red
COLOR_DIM_HEAD  = '#01579B'   # Dark Blue
COLOR_DIM_BODY  = '#E1F5FE'   # Light Blue
TEXT_LIGHT      = '#FFFFFF'
TEXT_DARK       = '#000000'

def draw_table(ax, x, y, width, title, cols, is_fact=False):
    head_color = COLOR_FACT_HEAD if is_fact else COLOR_DIM_HEAD
    body_color = COLOR_FACT_BODY if is_fact else COLOR_DIM_BODY
    
    # Calculate height based on columns
    row_h = 0.4
    head_h = 0.6
    total_h = head_h + (len(cols) * row_h)
    
    # Draw body
    body = patches.Rectangle((x, y - total_h), width, total_h, 
                             linewidth=1, edgecolor='#757575', facecolor=body_color, zorder=2)
    ax.add_patch(body)
    
    # Draw header
    head = patches.Rectangle((x, y - head_h), width, head_h, 
                             linewidth=1, edgecolor='#757575', facecolor=head_color, zorder=2)
    ax.add_patch(head)
    
    # Header text
    ax.text(x + width/2, y - head_h/2, title, 
            color=TEXT_LIGHT, fontweight='bold', fontsize=10, 
            ha='center', va='center', fontfamily='sans-serif', zorder=3)
    
    # Columns text
    for i, col in enumerate(cols):
        is_pk_fk = "(PK)" in col or "(FK)" in col
        fw = 'bold' if is_pk_fk else 'normal'
        ax.text(x + 0.2, y - head_h - (i * row_h) - (row_h/2), col, 
                color=TEXT_DARK, fontweight=fw, fontsize=9, 
                ha='left', va='center', fontfamily='monospace', zorder=3)
                
    # Return connection points (center-left, center-right, top-center, bottom-center)
    return {
        'left': (x, y - total_h/2),
        'right': (x + width, y - total_h/2),
        'top': (x + width/2, y),
        'bottom': (x + width/2, y - total_h)
    }

def draw_line(ax, p1, p2, label=""):
    # Draw orthogonal line (elbow)
    mid_x = (p1[0] + p2[0]) / 2
    
    x_coords = [p1[0], mid_x, mid_x, p2[0]]
    y_coords = [p1[1], p1[1], p2[1], p2[1]]
    
    ax.plot(x_coords, y_coords, color='#424242', linewidth=1.5, zorder=1, linestyle='--')
    
    if label:
        ax.text(mid_x, (p1[1] + p2[1])/2, label, 
                backgroundcolor='white', color='#424242', fontsize=8,
                ha='center', va='center', zorder=4)

def main():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # ── FACT ──
    fact_cols = [
        "Record_ID (PK)",
        "Organization_ID (FK)",
        "Agent_Config_ID (FK)",
        "Research_Topic_ID (FK)",
        "Task_Success_Rate",
        "Productivity_Improvement",
        "Complexity_Score",
        "Leadership_Trust_Score",
        "Response_Time_Seconds",
        "Memory_Per_Message_MB",
        "CPU_Utilization_Percent",
        "Ingestion_Timestamp"
    ]
    f_pts = draw_table(ax, 6, 8.5, 4.0, "Fact_AI_Deployment", fact_cols, is_fact=True)
    
    # ── DIM 1: Organization ──
    dim1_cols = [
        "Organization_ID (PK)",
        "Organization_Name",
        "Industry",
        "Organization_Size",
        "AI_Maturity_Level"
    ]
    d1_pts = draw_table(ax, 0.5, 7.5, 3.5, "Dim_Organization", dim1_cols)
    
    # ── DIM 2: Agent Config ──
    dim2_cols = [
        "Agent_Config_ID (PK)",
        "Agent_Type",
        "Use_Case_Area",
        "Agent_Autonomy_Level",
        "Decision_Making_Type",
        "Context_Awareness_Score"
    ]
    d2_pts = draw_table(ax, 12, 7.5, 3.8, "Dim_Agent", dim2_cols)
    
    # ── DIM 3: Research Context ──
    dim3_cols = [
        "Research_Topic_ID (PK)",
        "Mapped_Business_Sector",
        "Avg_Citation_Count",
        "Paper_Count",
        "Top_Keywords"
    ]
    d3_pts = draw_table(ax, 6.25, 2.5, 3.5, "Dim_Research_Context", dim3_cols)
    
    # Connections
    draw_line(ax, d1_pts['right'], f_pts['left'], "1 : N")
    draw_line(ax, d2_pts['left'], f_pts['right'], "1 : N")
    
    # Vertical line for Dim3
    ax.plot([8, 8], [d3_pts['top'][1], f_pts['bottom'][1]], color='#424242', linewidth=1.5, zorder=1, linestyle='--')
    ax.text(8, (d3_pts['top'][1] + f_pts['bottom'][1])/2, "1 : N", 
            backgroundcolor='white', color='#424242', fontsize=8, ha='center', va='center', zorder=4)

    plt.title("Lakehouse Star Schema: Agentic AI Telemetry", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    os.makedirs(VIZ_DIR, exist_ok=True)
    plt.savefig(ERD_PATH, bbox_inches='tight', dpi=300)
    print(f"ERD saved to: {ERD_PATH}")

if __name__ == "__main__":
    main()
