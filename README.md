# sales-dashboard
Interactive sales performance dashboard with the five key visualizations,Filters out albums without chart positions, Dynamically calculates performance tiers, Uses color scales to enhance data representation
# Sales Performance Dashboard

## Overview
This is an interactive dashboard for analyzing sales/chart performance data using Python, Dash, and Plotly.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sales-performance-dashboard.git
cd sales-performance-dashboard
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

```bash
python app.py
```

Then open a web browser and navigate to `http://127.0.0.1:8050/`

## Usage
1. Click on the upload area
2. Select a JSON file with the following structure:
```json
[
  {
    "album": "Album Name",
    "year": 2000,
    "US_peak_chart_post": 10
  }
]
```

## Features
- Line Chart: Chart Performance Over Time
- Bar Chart: Album Release Frequency
- Scatter Plot: Year vs Chart Position
- Heatmap: Year vs Chart Performance
- Treemap: Album Performance Distribution

## Troubleshooting
- Ensure you have the latest version of Python
- Check that all dependencies are installed correctly
- Verify the JSON file format matches the expected structure