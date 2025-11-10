"""
Architecture Diagram Generator for AutoPipelineAI
Creates a comprehensive visual representation of the system architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# Define colors
color_ui = '#E3F2FD'  # Light blue
color_mode = '#FFF3E0'  # Light orange
color_core = '#E8F5E9'  # Light green
color_storage = '#F3E5F5'  # Light purple
color_llm = '#FFEBEE'  # Light red
color_agent = '#E0F2F1'  # Light teal

# Title
title = ax.text(10, 13.5, 'AutoPipelineAI v0.3.0 - System Architecture',
                ha='center', va='center', fontsize=24, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))

# Subtitle
subtitle = ax.text(10, 12.8, 'LLM-Driven Agentic Framework for Autonomous ETL and DataOps',
                   ha='center', va='center', fontsize=14, style='italic')

# ==================== Layer 1: User Interface ====================
ui_box = FancyBboxPatch((1, 11), 18, 1.2, boxstyle="round,pad=0.1",
                        edgecolor='#1976D2', facecolor=color_ui, linewidth=2)
ax.add_patch(ui_box)
ax.text(10, 11.6, 'User Interface Layer', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#1565C0')
ax.text(10, 11.2, 'Streamlit Web Application | Interactive Dashboard | Real-time Updates',
        ha='center', va='center', fontsize=10, style='italic')

# ==================== Layer 2: Mode Selection ====================
mode_y = 9.5
mode_height = 1.0

# Mode router box
router_box = FancyBboxPatch((8, mode_y), 4, mode_height, boxstyle="round,pad=0.1",
                           edgecolor='#F57C00', facecolor=color_mode, linewidth=2)
ax.add_patch(router_box)
ax.text(10, mode_y + 0.5, 'Mode Router\n& Dispatcher', ha='center', va='center',
        fontsize=11, fontweight='bold')

# ==================== Layer 3: Operational Modes ====================
modes_y = 7.5
mode_width = 3.2
mode_spacing = 0.3

modes = [
    {'name': 'Manual\nMode', 'icon': '📊', 'x': 1},
    {'name': 'LLM\nMode', 'icon': '🧠', 'x': 4.5},
    {'name': 'Agent\nMode', 'icon': '🤝', 'x': 8},
    {'name': 'PDF\nMode', 'icon': '📄', 'x': 11.5},
    {'name': 'Database\nMode', 'icon': '🗄️', 'x': 15}
]

for mode in modes:
    box = FancyBboxPatch((mode['x'], modes_y), mode_width, 1.2,
                         boxstyle="round,pad=0.08",
                         edgecolor='#F57C00', facecolor=color_mode, linewidth=1.5)
    ax.add_patch(box)
    ax.text(mode['x'] + mode_width/2, modes_y + 0.8, mode['icon'],
            ha='center', va='center', fontsize=16)
    ax.text(mode['x'] + mode_width/2, modes_y + 0.35, mode['name'],
            ha='center', va='center', fontsize=9, fontweight='bold')

# ==================== Layer 4: Core Modules ====================
modules_y = 5
module_height = 1.5

# ETL Module
etl_box = FancyBboxPatch((0.5, modules_y), 3, module_height,
                         boxstyle="round,pad=0.1",
                         edgecolor='#388E3C', facecolor=color_core, linewidth=2)
ax.add_patch(etl_box)
ax.text(2, modules_y + 1.1, 'ETL Module', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#2E7D32')
ax.text(2, modules_y + 0.7, 'Data Loading', ha='center', va='center', fontsize=8)
ax.text(2, modules_y + 0.4, 'Transformation', ha='center', va='center', fontsize=8)
ax.text(2, modules_y + 0.1, 'Schema Validation', ha='center', va='center', fontsize=8)

# Ollama Client
ollama_box = FancyBboxPatch((4, modules_y), 3, module_height,
                           boxstyle="round,pad=0.1",
                           edgecolor='#D32F2F', facecolor=color_llm, linewidth=2)
ax.add_patch(ollama_box)
ax.text(5.5, modules_y + 1.1, 'Ollama Client', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#C62828')
ax.text(5.5, modules_y + 0.7, 'llama3, mistral, phi3', ha='center', va='center', fontsize=8)
ax.text(5.5, modules_y + 0.4, 'Prompt Templates', ha='center', va='center', fontsize=8)
ax.text(5.5, modules_y + 0.1, 'Code Executor', ha='center', va='center', fontsize=8)

# Agent Orchestrator
agent_box = FancyBboxPatch((7.5, modules_y), 3.5, module_height,
                          boxstyle="round,pad=0.1",
                          edgecolor='#00897B', facecolor=color_agent, linewidth=2)
ax.add_patch(agent_box)
ax.text(9.25, modules_y + 1.1, 'Agent Orchestrator', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#00796B')
ax.text(9.25, modules_y + 0.7, '• ETL Agent', ha='center', va='center', fontsize=8)
ax.text(9.25, modules_y + 0.4, '• Query Agent', ha='center', va='center', fontsize=8)
ax.text(9.25, modules_y + 0.1, '• Profiling Agent', ha='center', va='center', fontsize=8)

# PDF Extractor
pdf_box = FancyBboxPatch((11.5, modules_y), 3, module_height,
                        boxstyle="round,pad=0.1",
                        edgecolor='#7B1FA2', facecolor=color_storage, linewidth=2)
ax.add_patch(pdf_box)
ax.text(13, modules_y + 1.1, 'PDF Extractor', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#6A1B9A')
ax.text(13, modules_y + 0.7, 'Text & Tables', ha='center', va='center', fontsize=8)
ax.text(13, modules_y + 0.4, 'NER Processor', ha='center', va='center', fontsize=8)
ax.text(13, modules_y + 0.1, 'Entity Extraction', ha='center', va='center', fontsize=8)

# Database Handlers
db_box = FancyBboxPatch((15, modules_y), 3, module_height,
                       boxstyle="round,pad=0.1",
                       edgecolor='#1976D2', facecolor=color_ui, linewidth=2)
ax.add_patch(db_box)
ax.text(16.5, modules_y + 1.1, 'DB Handlers', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#1565C0')
ax.text(16.5, modules_y + 0.7, 'DuckDB', ha='center', va='center', fontsize=8)
ax.text(16.5, modules_y + 0.4, 'SQLite', ha='center', va='center', fontsize=8)
ax.text(16.5, modules_y + 0.1, 'SQL Interface', ha='center', va='center', fontsize=8)

# ==================== Layer 5: Support Services ====================
support_y = 2.5
support_height = 1.8

# Cache Manager
cache_box = FancyBboxPatch((1, support_y), 4, support_height,
                          boxstyle="round,pad=0.1",
                          edgecolor='#F57C00', facecolor='#FFF8E1', linewidth=2)
ax.add_patch(cache_box)
ax.text(3, support_y + 1.4, 'Cache Manager', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#EF6C00')
ax.text(3, support_y + 1.0, '💾 Memory Cache', ha='center', va='center', fontsize=9)
ax.text(3, support_y + 0.6, '💿 Disk Cache', ha='center', va='center', fontsize=9)
ax.text(3, support_y + 0.2, 'TTL Management', ha='center', va='center', fontsize=8)

# Memory Store
memory_box = FancyBboxPatch((5.5, support_y), 4, support_height,
                           boxstyle="round,pad=0.1",
                           edgecolor='#7B1FA2', facecolor='#F3E5F5', linewidth=2)
ax.add_patch(memory_box)
ax.text(7.5, support_y + 1.4, 'Memory Store', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#6A1B9A')
ax.text(7.5, support_y + 1.0, '💬 Conversation History', ha='center', va='center', fontsize=9)
ax.text(7.5, support_y + 0.6, '📦 Session State', ha='center', va='center', fontsize=9)
ax.text(7.5, support_y + 0.2, 'Context Management', ha='center', va='center', fontsize=8)

# Configuration
config_box = FancyBboxPatch((10, support_y), 4, support_height,
                           boxstyle="round,pad=0.1",
                           edgecolor='#388E3C', facecolor='#E8F5E9', linewidth=2)
ax.add_patch(config_box)
ax.text(12, support_y + 1.4, 'Configuration', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#2E7D32')
ax.text(12, support_y + 1.0, '⚙️ Environment Variables', ha='center', va='center', fontsize=9)
ax.text(12, support_y + 0.6, '📁 Directory Setup', ha='center', va='center', fontsize=9)
ax.text(12, support_y + 0.2, 'Settings Management', ha='center', va='center', fontsize=8)

# Security
security_box = FancyBboxPatch((14.5, support_y), 4, support_height,
                             boxstyle="round,pad=0.1",
                             edgecolor='#D32F2F', facecolor='#FFEBEE', linewidth=2)
ax.add_patch(security_box)
ax.text(16.5, support_y + 1.4, 'Security Layer', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#C62828')
ax.text(16.5, support_y + 1.0, '🔒 Code Sandbox', ha='center', va='center', fontsize=9)
ax.text(16.5, support_y + 0.6, '✅ Safety Checks', ha='center', va='center', fontsize=9)
ax.text(16.5, support_y + 0.2, 'Module Whitelist', ha='center', va='center', fontsize=8)

# ==================== Layer 6: Data Storage ====================
storage_y = 0.3
storage_width = 3.5

storages = [
    {'name': 'DuckDB\nAnalytics', 'x': 1, 'color': '#1976D2'},
    {'name': 'SQLite\nStorage', 'x': 5, 'color': '#388E3C'},
    {'name': 'Parquet\nFiles', 'x': 9, 'color': '#F57C00'},
    {'name': 'CSV\nFiles', 'x': 13, 'color': '#7B1FA2'},
]

for storage in storages:
    box = FancyBboxPatch((storage['x'], storage_y), storage_width, 1.2,
                         boxstyle="round,pad=0.08",
                         edgecolor=storage['color'], facecolor=color_storage,
                         linewidth=2, linestyle='--')
    ax.add_patch(box)
    ax.text(storage['x'] + storage_width/2, storage_y + 0.6, storage['name'],
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=storage['color'])

# ==================== Arrows / Data Flow ====================

# UI to Mode Router
arrow1 = FancyArrowPatch((10, 11), (10, 10.5),
                        arrowstyle='->', mutation_scale=20, linewidth=2,
                        color='#1976D2')
ax.add_patch(arrow1)

# Mode Router to Modes
for mode in modes:
    x_pos = mode['x'] + mode_width/2
    arrow = FancyArrowPatch((10, mode_y + mode_height), (x_pos, modes_y + 1.2),
                           arrowstyle='->', mutation_scale=15, linewidth=1.5,
                           color='#F57C00', linestyle='--', alpha=0.6)
    ax.add_patch(arrow)

# Modes to Core Modules (selected examples)
# Manual to ETL
arrow_m1 = FancyArrowPatch((2.5, modes_y), (2, modules_y + module_height),
                          arrowstyle='->', mutation_scale=15, linewidth=1.5,
                          color='#388E3C', alpha=0.7)
ax.add_patch(arrow_m1)

# LLM to Ollama
arrow_m2 = FancyArrowPatch((6, modes_y), (5.5, modules_y + module_height),
                          arrowstyle='->', mutation_scale=15, linewidth=1.5,
                          color='#D32F2F', alpha=0.7)
ax.add_patch(arrow_m2)

# Agent to Orchestrator
arrow_m3 = FancyArrowPatch((9.5, modes_y), (9.25, modules_y + module_height),
                          arrowstyle='->', mutation_scale=15, linewidth=1.5,
                          color='#00897B', alpha=0.7)
ax.add_patch(arrow_m3)

# PDF to Extractor
arrow_m4 = FancyArrowPatch((13, modes_y), (13, modules_y + module_height),
                          arrowstyle='->', mutation_scale=15, linewidth=1.5,
                          color='#7B1FA2', alpha=0.7)
ax.add_patch(arrow_m4)

# DB to Handlers
arrow_m5 = FancyArrowPatch((16.5, modes_y), (16.5, modules_y + module_height),
                          arrowstyle='->', mutation_scale=15, linewidth=1.5,
                          color='#1976D2', alpha=0.7)
ax.add_patch(arrow_m5)

# Core to Support (bidirectional)
arrow_s1 = FancyArrowPatch((3, modules_y), (3, support_y + support_height),
                          arrowstyle='<->', mutation_scale=15, linewidth=1.5,
                          color='#F57C00', linestyle=':', alpha=0.5)
ax.add_patch(arrow_s1)

arrow_s2 = FancyArrowPatch((7.5, modules_y), (7.5, support_y + support_height),
                          arrowstyle='<->', mutation_scale=15, linewidth=1.5,
                          color='#7B1FA2', linestyle=':', alpha=0.5)
ax.add_patch(arrow_s2)

# Support to Storage
arrow_st1 = FancyArrowPatch((2.5, support_y), (2.5, storage_y + 1.2),
                           arrowstyle='->', mutation_scale=15, linewidth=1.5,
                           color='#1976D2', alpha=0.6)
ax.add_patch(arrow_st1)

arrow_st2 = FancyArrowPatch((16.5, modules_y), (16.5, storage_y + 1.2),
                           arrowstyle='->', mutation_scale=15, linewidth=1.5,
                           color='#1976D2', alpha=0.6)
ax.add_patch(arrow_st2)

# ==================== Legend ====================
legend_elements = [
    mlines.Line2D([0], [0], color='#1976D2', linewidth=2, linestyle='-',
                  label='Direct Data Flow'),
    mlines.Line2D([0], [0], color='#F57C00', linewidth=2, linestyle='--',
                  label='Request Flow'),
    mlines.Line2D([0], [0], color='#7B1FA2', linewidth=2, linestyle=':',
                  label='Bidirectional'),
    mpatches.Patch(facecolor=color_ui, edgecolor='#1976D2', label='User Interface'),
    mpatches.Patch(facecolor=color_mode, edgecolor='#F57C00', label='Modes'),
    mpatches.Patch(facecolor=color_core, edgecolor='#388E3C', label='Core Modules'),
    mpatches.Patch(facecolor=color_llm, edgecolor='#D32F2F', label='LLM Services'),
    mpatches.Patch(facecolor=color_agent, edgecolor='#00897B', label='Agents'),
    mpatches.Patch(facecolor=color_storage, edgecolor='#7B1FA2', label='Storage'),
]

legend = ax.legend(handles=legend_elements, loc='upper left',
                  bbox_to_anchor=(0.01, 0.18), fontsize=9,
                  framealpha=0.9, title='Legend', title_fontsize=10)

# ==================== Footer ====================
footer_text = (
    'AutoPipelineAI v0.3.0 | Built with Python, Streamlit, LangChain, CrewAI, Ollama | '
    '100% Local & Private | Open Source (MIT License)'
)
ax.text(10, 0.05, footer_text, ha='center', va='bottom',
        fontsize=8, style='italic', color='gray')

# Key Features Box
features_text = (
    "🔒 100% Local Execution | 🤖 Multi-Agent System | 🧠 Natural Language Interface | "
    "📄 PDF Intelligence | 🗄️ High-Performance DB | ⚡ Safe Code Execution"
)
features_box = FancyBboxPatch((0.2, 12.2), 19.6, 0.4, boxstyle="round,pad=0.05",
                             edgecolor='gray', facecolor='lightyellow',
                             linewidth=1, linestyle='--', alpha=0.7)
ax.add_patch(features_box)
ax.text(10, 12.4, features_text, ha='center', va='center',
        fontsize=9, fontweight='bold', color='#424242')

# Save the figure
plt.tight_layout()
plt.savefig('architecture_diagram.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('architecture_diagram.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')

print("✅ Architecture diagram created successfully!")
print("📁 Saved as:")
print("   - architecture_diagram.png (high resolution)")
print("   - architecture_diagram.pdf (vector format)")
print("\n🎨 Diagram includes:")
print("   • 6 architectural layers")
print("   • 5 operational modes")
print("   • 10+ core components")
print("   • Data flow arrows")
print("   • Color-coded modules")
print("   • Comprehensive legend")
