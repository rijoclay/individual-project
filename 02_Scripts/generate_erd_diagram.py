import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Setup
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

# Colors
BLUE = '#2E4057'
LIGHT_BLUE = '#4A90D9'
GRAY = '#8B8B8B'
WHITE = '#FFFFFF'
LIGHT_GRAY = '#F0F0F0'
RED_ACCENT = '#E74C3C'
GREEN_ACCENT = '#27AE60'

def draw_table(ax, x, y, width, height, title, columns, color=BLUE, is_fact=False):
    """Draw a professional table box."""
    # Main box
    rect = FancyBboxPatch((x, y), width, height, 
                           boxstyle="round,pad=0.05",
                           facecolor=WHITE, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    
    # Title bar
    title_rect = FancyBboxPatch((x, y + height - 0.6), width, 0.6,
                                 boxstyle="round,pad=0.05",
                                 facecolor=color, edgecolor=color, linewidth=2)
    ax.add_patch(title_rect)
    
    # Title text
    ax.text(x + width/2, y + height - 0.3, title, 
            ha='center', va='center', fontsize=11, fontweight='bold', color=WHITE)
    
    # Columns
    col_height = (height - 0.6) / len(columns)
    for i, (col_name, col_type) in enumerate(columns):
        col_y = y + height - 0.6 - (i + 1) * col_height
        ax.text(x + 0.15, col_y + col_height/2, col_name, 
                ha='left', va='center', fontsize=9, fontweight='bold')
        ax.text(x + width - 0.15, col_y + col_height/2, col_type, 
                ha='right', va='center', fontsize=8, color=GRAY, style='italic')
        
        # Separator line
        if i < len(columns) - 1:
            ax.plot([x, x + width], [col_y, col_y], '-', color=LIGHT_GRAY, linewidth=0.5)

def draw_relationship(ax, start, end, label="", color=GRAY):
    """Draw relationship line between tables."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5, 
                               connectionstyle="arc3,rad=0"))
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y + 0.1, label, ha='center', va='bottom', 
                fontsize=7, color=GRAY, style='italic')

# Draw Fact Table (center)
fact_cols = [
    ("fact_id", "PK"),
    ("org_key", "FK"),
    ("agent_key", "FK"),
    ("research_key", "FK"),
    ("task_success_rate", "DOUBLE"),
    ("productivity_improvement", "DOUBLE"),
    ("leadership_trust_score", "DOUBLE"),
    ("response_time_seconds", "DOUBLE"),
    ("complexity_score", "DOUBLE"),
    ("cpu_utilization_percent", "DOUBLE"),
    ("memory_per_message_mb", "DOUBLE")
]

draw_table(ax, 4.5, 3, 5, 6.5, "Fact_AI_Deployment", fact_cols, color=RED_ACCENT, is_fact=True)

# Draw Dimension 1: Organization (left)
org_cols = [
    ("org_key", "PK"),
    ("record_id", "STRING"),
    ("organization_name", "STRING"),
    ("industry", "STRING"),
    ("organization_size", "STRING"),
    ("ai_maturity_level", "STRING")
]

draw_table(ax, 0.5, 4.5, 3.5, 5, "Dim_Organization", org_cols, color=BLUE)

# Draw Dimension 2: Agent (right)
agent_cols = [
    ("agent_key", "PK"),
    ("agent_type", "STRING"),
    ("use_case_area", "STRING"),
    ("agent_autonomy_level", "STRING"),
    ("decision_making_type", "STRING"),
    ("context_awareness_score", "DOUBLE")
]

draw_table(ax, 10, 4.5, 3.5, 5, "Dim_Agent", agent_cols, color=BLUE)

# Draw Dimension 3: Research (bottom)
research_cols = [
    ("research_key", "PK"),
    ("openalex_paper_id", "STRING"),
    ("title", "STRING"),
    ("citation_count", "INT"),
    ("publication_year", "INT"),
    ("mapped_business_sector", "STRING")
]

draw_table(ax, 4.5, 0.2, 5, 2.3, "Dim_Research_Context", research_cols, color=BLUE)

# Draw relationships
draw_relationship(ax, (4.0, 7.0), (4.5, 7.0), "1:N")
draw_relationship(ax, (9.5, 7.0), (10.0, 7.0), "1:N")
draw_relationship(ax, (7.0, 3.0), (7.0, 2.5), "1:N")

# Title
ax.text(7, 9.5, "Star Schema ERD: Agentic AI Performance Analytics", 
        ha='center', va='center', fontsize=16, fontweight='bold', color=BLUE)
ax.text(7, 9.1, "Gold Layer - Data Warehouse Schema", 
        ha='center', va='center', fontsize=10, color=GRAY, style='italic')

# Legend
legend_elements = [
    mpatches.Patch(facecolor=RED_ACCENT, edgecolor=RED_ACCENT, label='Fact Table'),
    mpatches.Patch(facecolor=BLUE, edgecolor=BLUE, label='Dimension Table'),
    mpatches.Patch(facecolor=WHITE, edgecolor=GRAY, label='Primary Key (PK)'),
    mpatches.Patch(facecolor=WHITE, edgecolor=GRAY, label='Foreign Key (FK)')
]
ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)

plt.tight_layout()
plt.savefig(r"C:\Users\richa\Documents\Sem.6\DatEng_Individual_Project\individual_project_2\06_Visualization\star_schema_erd.png", 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("ERD diagram saved successfully!")
