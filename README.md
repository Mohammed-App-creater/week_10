# Project Name

## Overview
Brief description of the project

## Project Structure
├── .github/workflows/ # GitHub Actions workflows
├── data/ # Data directory
│ ├── raw/ # Raw, immutable data
│ └── processed/ # Cleaned, analysis-ready data
├── notebooks/ # Jupyter notebooks for exploration
├── src/ # Source code
├── dashboard/ # Dashboard application
├── tests/ # Unit tests
├── models/ # Trained models
├── reports/ # Generated reports
│ └── figures/ # Generated figures
├── requirements.txt # Python dependencies
└── README.md # This file

text

## Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Streamlit Dashboard (Task 5)
To launch the interactive dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard provides:
- **Overview**: Key metrics and summaries.
- **Trends**: Interactive analysis of historical Access and Usage data.
- **Forecasts**: Future projections (2025-2027) with scenario analysis.
- **Inclusion Projections**: Progress tracking towards the 60% national target.

### Notebooks
Explore the logic in `notebooks/` for data processing and modeling tasks.

License
Your license here
