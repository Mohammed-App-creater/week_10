import json
import os

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Task 2: Exploratory Data Analysis (EDA) - Ethiopia Financial Inclusion\n",
    "\n",
    "## Objective\n",
    "Uncover patterns, drivers, gaps, and hypotheses to inform event impact modeling and forecasting. Focus on evidence-based, Ethiopia-specific, and policy-relevant analysis.\n",
    "\n",
    "## Steps\n",
    "1. **Dataset Overview**: Quality, gaps, and temporal coverage.\n",
    "2. **Access Analysis**: Account ownership trends vs. targets.\n",
    "3. **Usage Analysis**: Digital payments vs. access.\n",
    "4. **Infrastructure & Enablers**: Role of mobile and agent networks.\n",
    "5. **Event Timeline**: Impact of Telebirr, Safaricom, etc.\n",
    "6. **Correlations**: Relationships between infrastructure, access, and usage.\n",
    "7. **Key Insights**: Synthesis of findings.\n",
    "8. **Formulation**: Hypotheses for Task 3."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Imports\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "\n",
    "warnings.filterwarnings('ignore')\n",
    "pd.set_option('display.max_columns', None)\n",
    "plt.style.use('seaborn-v0_8-whitegrid')\n",
    "\n",
    "# Set file paths\n",
    "DATA_DIR = '../data/raw'\n",
    "MAIN_DATA_FILE = os.path.join(DATA_DIR, 'ethiopia_fi_unified_data.csv')\n",
    "REF_CODES_FILE = os.path.join(DATA_DIR, 'reference_codes.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1: Dataset Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load data\n",
    "try:\n",
    "    df = pd.read_csv(MAIN_DATA_FILE)\n",
    "    ref_codes = pd.read_csv(REF_CODES_FILE)\n",
    "    print(\"Data loaded successfully.\")\n",
    "except FileNotFoundError:\n",
    "    print(\"Error: Files not found. Check paths.\")\n",
    "\n",
    "# Basic info\n",
    "print(f\"Main Data Shape: {df.shape}\")\n",
    "print(f\"Columns: {df.columns.tolist()}\")\n",
    "df.head(3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Summary Tables\n",
    "\n",
    "# Counts by record_type\n",
    "print(\"\\n--- Counts by Record Type ---\")\n",
    "print(df['record_type'].value_counts())\n",
    "\n",
    "# Counts by Pillar\n",
    "print(\"\\n--- Counts by Pillar ---\")\n",
    "print(df['pillar'].value_counts())\n",
    "\n",
    "# Counts by Source Type\n",
    "print(\"\\n--- Counts by Source Type ---\")\n",
    "print(df['source_type'].value_counts())\n",
    "\n",
    "# Confidence Distribution\n",
    "print(\"\\n--- Confidence Levels ---\")\n",
    "print(df['confidence'].value_counts())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Temporal Coverage Visualization\n",
    "plt.figure(figsize=(15, 6))\n",
    "coverage = df.groupby(['indicator_name', 'year']).size().unstack(fill_value=0)\n",
    "sns.heatmap(coverage > 0, cmap='viridis', cbar=False, cbar_kws={'label': 'Data Present'})\n",
    "plt.title('Data Availability by Indicator and Year')\n",
    "plt.xlabel('Year')\n",
    "plt.ylabel('Indicator')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Data Quality & Gaps Assessment\n",
    "*Note: Observe the heatmap above for sparse rows.*\n",
    "- **Low Confidence Items**: [Analyze 'confidence' column]\n",
    "- **Missing Periods**: [Identify years with no data]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2: Access (Account Ownership) Analysis\n",
    "Focusing on the Global Findex Access definitions."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Filter for Account Ownership\n",
    "access_indicators = ['Account ownership (% age 15+)', 'Account Ownership Rate', 'ACC_OWNERSHIP'] # Adjust based on actual indicator names in CSV\n",
    "# Let's find the exact name dynamically to be safe\n",
    "acc_ownership_names = df[df['pillar'] == 'ACCESS']['indicator_name'].unique()\n",
    "print(f\"Access Indicators found: {acc_ownership_names}\")\n",
    "\n",
    "# Using the most likely main indicator for plot\n",
    "target_indicator = 'Account ownership (% age 15+)' # Placeholder, verify with print output\n",
    "if len(acc_ownership_names) > 0:\n",
    "    target_indicator = acc_ownership_names[0] # Take the first one if unsure, or specific string match\n",
    "\n",
    "access_df = df[(df['pillar'] == 'ACCESS') & (df['indicator_name'] == target_indicator) & (df['record_type']=='observation')].sort_values('year')\n",
    "\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.lineplot(data=access_df, x='year', y='value', marker='o')\n",
    "plt.title(f'{target_indicator} (2011-2024)')\n",
    "plt.ylabel('Percentage / Value')\n",
    "plt.grid(True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Calculate Growth Rates (CAGR or simple diff)\n",
    "if not access_df.empty:\n",
    "    access_df['prev_val'] = access_df['value'].shift(1)\n",
    "    access_df['prev_year'] = access_df['year'].shift(1)\n",
    "    access_df['pp_change'] = access_df['value'] - access_df['prev_val']\n",
    "    access_df['annualized_growth'] = access_df['pp_change'] / (access_df['year'] - access_df['prev_year'])\n",
    "    \n",
    "    print(\"Growth Analysis:\")\n",
    "    display(access_df[['year', 'value', 'pp_change', 'annualized_growth']])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2021-2024 Slowdown Discussion\n",
    "- **Observation**: [Add text after running]\n",
    "- **Hypothesis 1**: Saturation in urban centers?\n",
    "- **Hypothesis 2**: Definition of 'account' excl. some mobile wallets?\n",
    "- **Hypothesis 3**: Informality dominance?"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3: Usage (Digital Payments) Analysis\n",
    "Contrasting Access vs. Usage."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Identify Usage indicators\n",
    "usage_df = df[df['pillar'] == 'USAGE']\n",
    "print(\"Usage Indicators:\", usage_df['indicator_name'].unique())\n",
    "\n",
    "# Plotting standardized usage trends\n",
    "plt.figure(figsize=(12, 6))\n",
    "sns.lineplot(data=usage_df, x='year', y='value', hue='indicator_name', marker='o')\n",
    "plt.title('Digital Payment Usage Trends')\n",
    "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4: Infrastructure & Enablers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "infra_df = df[df['pillar'] == 'INFRASTRUCTURE']\n",
    "print(\"Infrastructure Indicators:\", infra_df['indicator_name'].unique())\n",
    "\n",
    "# Smartphone, Internet, Agent density\n",
    "selected_infra = [i for i in infra_df['indicator_name'].unique() if 'Mobile' in i or 'Agent' in i or 'Electricity' in i]\n",
    "\n",
    "plt.figure(figsize=(12, 6))\n",
    "sns.lineplot(data=infra_df[infra_df['indicator_name'].isin(selected_infra)], \n",
    "             x='year', y='value', hue='indicator_name', marker='s')\n",
    "plt.title('Key Infrastructure Enablers')\n",
    "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 5: Event Timeline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "events_df = df[df['record_type'] == 'event']\n",
    "print(\"Major Events:\")\n",
    "display(events_df[['year', 'event_date', 'indicator_name', 'value']].sort_values('event_date'))\n",
    "\n",
    "# Overlay plot\n",
    "plt.figure(figsize=(14, 7))\n",
    "# Plot Access again as base\n",
    "sns.lineplot(data=access_df, x='year', y='value', label='Access Rate', color='blue', linewidth=2)\n",
    "\n",
    "# Add vertical lines for events\n",
    "for _, row in events_df.iterrows():\n",
    "    plt.axvline(x=row['year'], color='red', linestyle='--', alpha=0.5)\n",
    "    plt.text(row['year'], 50, row['indicator_name'], rotation=90, va='center', fontsize=8)\n",
    "\n",
    "plt.title('Timeline of Policy & Market Events vs Access Rate')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 6: Correlation Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Pivot data for correlation\n",
    "pivot_df = df[df['record_type']=='observation'].pivot_table(index='year', columns='indicator_name', values='value')\n",
    "\n",
    "# Filter for columns with enough data points\n",
    "valid_cols = pivot_df.columns[pivot_df.count() > 3]\n",
    "corr_matrix = pivot_df[valid_cols].corr()\n",
    "\n",
    "plt.figure(figsize=(12, 10))\n",
    "sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1)\n",
    "plt.title('Correlation Matrix of Indicators')\n",
    "plt.show()\n",
    "\n",
    "# Top correlations with Access\n",
    "if target_indicator in corr_matrix.columns:\n",
    "    print(f\"Top correlations with {target_indicator}:\")\n",
    "    print(corr_matrix[target_indicator].sort_values(ascending=False).head(10))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 7: Key Insights Synthesis\n",
    "\n",
    "1. **Insight 1**: ...\n",
    "2. **Insight 2**: ...\n",
    "3. **Insight 3**: ...\n",
    "4. **Insight 4**: ...\n",
    "5. **Insight 5**: ..."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 8: Prepare for Task 3\n",
    "\n",
    "### Data Quality & Limitations\n",
    "- Limitation 1: ...\n",
    "- Limitation 2: ...\n",
    "\n",
    "### Hypotheses for Modeling\n",
    "- H1: ...\n",
    "- H2: ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open(r'c:\Users\yoga\code\10_Academy\week_10\notebooks\02_exploratory_data_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print("Notebook generated successfully.")
