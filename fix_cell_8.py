import json
import os

NOTEBOOK_PATH = r'C:\Users\yoga\code\10_Academy\week_10\notebooks\02_exploratory_data_analysis.ipynb'

# CELL 8: Updated to include 'target_indicator' definition
CODE_CELL_8 = [
    "# Figure 2: Access vs. Usage Trends with Event Overlay\n",
    "\n",
    "# 1. Prepare Access Data\n",
    "# Identify the primary access indicator (likely 'Account ownership')\n",
    "access_mask = (df['pillar'] == 'ACCESS') & (df['record_type'] == 'observation')\n",
    "access_vars = df[access_mask]['indicator'].unique()\n",
    "# DEFINE target_indicator for downstream compatibility (Cell 18)\n",
    "target_indicator = 'Account Ownership Rate' if 'Account Ownership Rate' in access_vars else access_vars[0]\n",
    "target_access = target_indicator\n",
    "\n",
    "access_df = df[\n",
    "    (df['pillar'] == 'ACCESS') & \n",
    "    (df['indicator'] == target_access) & \n",
    "    (df['record_type'] == 'observation')\n",
    "].copy()\n",
    "\n",
    "access_df['fiscal_year'] = pd.to_numeric(access_df['fiscal_year'], errors='coerce')\n",
    "access_df['value_numeric'] = pd.to_numeric(access_df['value_numeric'], errors='coerce')\n",
    "access_df = access_df.dropna(subset=['fiscal_year', 'value_numeric']).sort_values('fiscal_year')\n",
    "\n",
    "print(f\"Access Indicator: {target_access}\")\n",
    "print(f\"Access Data Points: {access_df.shape[0]}\")\n",
    "\n",
    "# 2. Prepare Usage Data\n",
    "usage_mask = (df['pillar'] == 'USAGE') & (df['record_type'] == 'observation')\n",
    "usage_df = df[usage_mask].copy()\n",
    "usage_df['fiscal_year'] = pd.to_numeric(usage_df['fiscal_year'], errors='coerce')\n",
    "usage_df['value_numeric'] = pd.to_numeric(usage_df['value_numeric'], errors='coerce')\n",
    "usage_df = usage_df.dropna(subset=['fiscal_year', 'value_numeric']).sort_values('fiscal_year')\n",
    "\n",
    "# Select a few key usage indicators for clarity\n",
    "top_usage = usage_df['indicator'].value_counts().head(3).index.tolist()\n",
    "usage_filtered = usage_df[usage_df['indicator'].isin(top_usage)]\n",
    "\n",
    "print(f\"Usage Indicators Selected: {top_usage}\")\n",
    "print(f\"Usage Data Points: {usage_filtered.shape[0]}\")\n",
    "\n",
    "# 3. Prepare Events Data\n",
    "events_df = df[df['record_type'] == 'event'].copy()\n",
    "events_df['fiscal_year'] = pd.to_numeric(events_df['fiscal_year'], errors='coerce')\n",
    "events_df = events_df.dropna(subset=['fiscal_year']).sort_values('fiscal_year')\n",
    "\n",
    "# 4. Plotting\n",
    "plt.figure(figsize=(14, 8))\n",
    "\n",
    "# Plot Usage first (so Access is on top if needed, or visually distinct)\n",
    "sns.lineplot(\n",
    "    data=usage_filtered, \n",
    "    x='fiscal_year', \n",
    "    y='value_numeric', \n",
    "    hue='indicator', \n",
    "    palette='viridis',\n",
    "    marker='s',\n",
    "    linestyle='--',\n",
    "    alpha=0.8\n",
    ")\n",
    "\n",
    "# Plot Access (Primary)\n",
    "sns.lineplot(\n",
    "    data=access_df, \n",
    "    x='fiscal_year', \n",
    "    y='value_numeric', \n",
    "    label=f'ACCESS: {target_access}', \n",
    "    color='navy', \n",
    "    linewidth=3, \n",
    "    marker='D',\n",
    "    markersize=8\n",
    ")\n",
    "\n",
    "# Add Events as Vertical Lines\n",
    "y_min, y_max = plt.ylim()\n",
    "for _, row in events_df.iterrows():\n",
    "    plt.axvline(x=row['fiscal_year'], color='red', linestyle=':', alpha=0.5, zorder=0)\n",
    "    plt.text(\n",
    "        row['fiscal_year'], \n",
    "        y_max * 0.95,\n",
    "        row['indicator'], # Event name stored in 'indicator' or 'original_text'\n",
    "        rotation=90, \n",
    "        va='top',\n",
    "        ha='right',\n",
    "        fontsize=8,\n",
    "        color='darkred'\n",
    "    )\n",
    "\n",
    "plt.title('Figure 2: Financial Access vs. Usage Trends with Key Events', fontsize=14)\n",
    "plt.xlabel('Fiscal Year', fontsize=12)\n",
    "plt.ylabel('Rate / Percentage (%)', fontsize=12)\n",
    "plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)\n",
    "plt.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
]

def update_cell_8():
    try:
        with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        idx = 8
        if idx < len(nb['cells']) and nb['cells'][idx]['cell_type'] == 'code':
            print(f"Updating Cell {idx} with 'target_indicator' definition...")
            nb['cells'][idx]['source'] = CODE_CELL_8
            nb['cells'][idx]['outputs'] = []
            
            with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=4)
            print("SUCCESS: Cell 8 updated.")
        else:
            print(f"ERROR: Cell {idx} not found or not a code cell.")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    update_cell_8()
