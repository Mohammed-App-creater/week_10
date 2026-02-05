import json
import os

# Using absolute path for robustness as requested
NOTEBOOK_PATH = r'C:\Users\yoga\code\10_Academy\week_10\notebooks\02_exploratory_data_analysis.ipynb'

# ---------------------------------------------------------
# New Code Definitions
# ---------------------------------------------------------

# CELL 8: Figure 2 (Access vs Usage Trend Overlay)
CODE_CELL_8 = [
    "# Figure 2: Access vs. Usage Trends with Event Overlay\n",
    "\n",
    "# 1. Prepare Access Data\n",
    "# Identify the primary access indicator (likely 'Account ownership')\n",
    "access_mask = (df['pillar'] == 'ACCESS') & (df['record_type'] == 'observation')\n",
    "access_vars = df[access_mask]['indicator'].unique()\n",
    "target_access = 'Account Ownership Rate' if 'Account Ownership Rate' in access_vars else access_vars[0]\n",
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

# CELL 12: Figure 3 (Usage Trends Detailed)
CODE_CELL_12 = [
    "# Figure 3: Detailed Usage Indicators Trend\n",
    "\n",
    "# 1. Filter Usage Data\n",
    "usage_df = df[\n",
    "    (df['pillar'] == 'USAGE') & \n",
    "    (df['record_type'] == 'observation')\n",
    "].copy()\n",
    "\n",
    "usage_df['fiscal_year'] = pd.to_numeric(usage_df['fiscal_year'], errors='coerce')\n",
    "usage_df['value_numeric'] = pd.to_numeric(usage_df['value_numeric'], errors='coerce')\n",
    "usage_df = usage_df.dropna(subset=['fiscal_year', 'value_numeric']).sort_values('fiscal_year')\n",
    "\n",
    "print(f\"Total Usage Observations: {len(usage_df)}\")\n",
    "print(f\"Indicators: {usage_df['indicator'].unique()}\")\n",
    "\n",
    "# 2. Plot\n",
    "plt.figure(figsize=(14, 7))\n",
    "\n",
    "if not usage_df.empty:\n",
    "    sns.lineplot(\n",
    "        data=usage_df, \n",
    "        x='fiscal_year', \n",
    "        y='value_numeric', \n",
    "        hue='indicator', \n",
    "        marker='o', \n",
    "        palette='tab10',\n",
    "        linewidth=2\n",
    "    )\n",
    "    plt.title('Figure 3: Trends in Financial Usage Indicators', fontsize=14)\n",
    "    plt.xlabel('Fiscal Year', fontsize=12)\n",
    "    plt.ylabel('Percentage / Value', fontsize=12)\n",
    "    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')\n",
    "    plt.grid(True, alpha=0.3)\n",
    "else:\n",
    "    plt.text(0.5, 0.5, 'No Usage Data Available', ha='center', fontsize=14)\n",
    "    print(\"WARNING: No data available for Usage plot.\")\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
]

# CELL 14: Figure 4 (Infrastructure Enablers)
CODE_CELL_14 = [
    "# Figure 4: Infrastructure Enablers\n",
    "\n",
    "# 1. Filter Infrastructure Data\n",
    "# Broad search for infrastructure-related items if 'INFRASTRUCTURE' pillar isn't explicit\n",
    "infra_mask = (\n",
    "    (df['pillar'].isin(['INFRASTRUCTURE', 'ENABLER'])) | \n",
    "    (df['indicator'].str.contains('mobile|network|agent|bank', case=False, na=False))\n",
    ") & (df['record_type'] == 'observation')\n",
    "\n",
    "infra_df = df[infra_mask].copy()\n",
    "\n",
    "infra_df['fiscal_year'] = pd.to_numeric(infra_df['fiscal_year'], errors='coerce')\n",
    "infra_df['value_numeric'] = pd.to_numeric(infra_df['value_numeric'], errors='coerce')\n",
    "infra_df = infra_df.dropna(subset=['fiscal_year', 'value_numeric']).sort_values('fiscal_year')\n",
    "\n",
    "# Select a subset of diverse infrastructure indicators if too many\n",
    "unique_infra = infra_df['indicator'].unique()\n",
    "if len(unique_infra) > 6:\n",
    "    selected_infra = unique_infra[:6] # Take top 6 for readability\n",
    "    infra_df = infra_df[infra_df['indicator'].isin(selected_infra)]\n",
    "else:\n",
    "    selected_infra = unique_infra\n",
    "\n",
    "print(f\"Infrastructure Indicators Plotted: {selected_infra}\")\n",
    "\n",
    "# 2. Plot\n",
    "plt.figure(figsize=(14, 7))\n",
    "\n",
    "if not infra_df.empty:\n",
    "    sns.lineplot(\n",
    "        data=infra_df,\n",
    "        x='fiscal_year',\n",
    "        y='value_numeric',\n",
    "        hue='indicator',\n",
    "        style='indicator',\n",
    "        markers=True,\n",
    "        dashes=False,\n",
    "        palette='magma'\n",
    "    )\n",
    "    plt.title('Figure 4: Key Infrastructure & Enabler Trends', fontsize=14)\n",
    "    plt.xlabel('Fiscal Year')\n",
    "    plt.ylabel('Count / Percentage')\n",
    "    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')\n",
    "    plt.grid(True, alpha=0.3)\n",
    "else:\n",
    "    plt.text(0.5, 0.5, 'No Infrastructure Data Available', ha='center', fontsize=14)\n",
    "    print(\"WARNING: No Infrastructure data found.\")\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
]

# CELL 16: Figure 5 (Event Timeline) - Reusing logic from Cell 8 but focused on Events
CODE_CELL_16 = [
    "# Figure 5: Event Timeline Visualization\n",
    "\n",
    "# 1. Filter Events\n",
    "events_df = df[df['record_type'] == 'event'].copy()\n",
    "events_df['fiscal_year'] = pd.to_numeric(events_df['fiscal_year'], errors='coerce')\n",
    "events_df = events_df.dropna(subset=['fiscal_year']).sort_values('fiscal_year')\n",
    "\n",
    "print(f\"Events Found: {len(events_df)}\")\n",
    "\n",
    "# 2. Plot Overlay on Dummy Data or Access Data context\n",
    "plt.figure(figsize=(14, 6))\n",
    "\n",
    "# Determine year range\n",
    "min_year = events_df['fiscal_year'].min() - 1\n",
    "max_year = events_df['fiscal_year'].max() + 1\n",
    "\n",
    "# Setup canvas\n",
    "plt.xlim(min_year, max_year)\n",
    "plt.ylim(0, 10) # Arbitrary y-axis for timeline spacing\n",
    "plt.yticks([])\n",
    "\n",
    "# Plot events as stems\n",
    "import numpy as np\n",
    "# Stagger heights to key text legible\n",
    "heights = [2, 4, 6, 8, 3, 5, 7, 9] * (len(events_df) // 8 + 1)\n",
    "heights = heights[:len(events_df)]\n",
    "\n",
    "plt.vlines(x=events_df['fiscal_year'], ymin=0, ymax=heights, color='crimson', alpha=0.7, linewidth=2)\n",
    "plt.plot(events_df['fiscal_year'], np.zeros_like(events_df['fiscal_year']), '-k', linewidth=1) # Baseline\n",
    "\n",
    "# Add Labels\n",
    "for i, (idx, row) in enumerate(events_df.iterrows()):\n",
    "    plt.text(\n",
    "        row['fiscal_year'], \n",
    "        heights[i] + 0.2,\n",
    "        row['indicator'], # Event name\n",
    "        rotation=45, \n",
    "        ha='left',\n",
    "        va='bottom',\n",
    "        fontsize=9,\n",
    "        fontweight='bold'\n",
    "    )\n",
    "    # Add year marker\n",
    "    plt.text(\n",
    "        row['fiscal_year'], \n",
    "        -0.5,\n",
    "        str(int(row['fiscal_year'])),\n",
    "        ha='center',\n",
    "        fontsize=10\n",
    "    )\n",
    "\n",
    "plt.title('Figure 5: Timeline of Key Policy & Market Events', fontsize=14)\n",
    "plt.xlabel('Year')\n",
    "plt.grid(axis='x', alpha=0.2)\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
]

# ---------------------------------------------------------
# Execution
# ---------------------------------------------------------

def reconstruct_notebook():
    try:
        with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Verify valid notebook structure
        if 'cells' not in nb:
            raise ValueError("Invalid notebook JSON: 'cells' key missing")

        # Map logic to cell indices
        # NOTE: Indices 8, 12, 14, 16 are based on previous analysis. 
        # We verify valid indices before replacing.
        
        replacements = {
            8: CODE_CELL_8,
            12: CODE_CELL_12,
            14: CODE_CELL_14,
            16: CODE_CELL_16
        }

        changes_made = 0
        for idx, new_source in replacements.items():
            if idx < len(nb['cells']):
                # Verify it's a code cell
                if nb['cells'][idx]['cell_type'] == 'code':
                    print(f"Reconstructing Cell {idx}...")
                    nb['cells'][idx]['source'] = new_source
                    # Clear outputs to avoid Confusion
                    nb['cells'][idx]['outputs'] = []
                    nb['cells'][idx]['execution_count'] = None
                    changes_made += 1
                else:
                    print(f"Skipping Cell {idx}: Not a code cell (Type: {nb['cells'][idx]['cell_type']})")
            else:
                print(f"Skipping Cell {idx}: Index out of range")

        if changes_made > 0:
            with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=4)
            print(f"SUCCESS: Updated {changes_made} cells in {NOTEBOOK_PATH}")
        else:
            print("NO CHANGES: No valid cells identified for update.")

    except Exception as e:
        print(f"ERROR: Failed to reconstruct notebook. {str(e)}")

if __name__ == "__main__":
    reconstruct_notebook()
