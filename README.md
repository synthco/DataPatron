# Analysis of Ukrainian support among posts on Reddit

The project explores Reddit activity to measure attitudes toward Ukraine. It cleans raw dumps, inspects engagement metrics, and visualizes how scores, comments, timing, and content types relate to support signals.

## Quick start
- Python 3.10+ recommended.
- Create an isolated environment and install dependencies:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- Place the CSV data into `data/` (paths are referenced directly in the notebooks).

## Running notebooks or scripts
- Launch Jupyter and open the analysis notebook:
  ```bash
  source .venv/bin/activate
  jupyter lab notebooks/ucsq_analysis.ipynb
  ```
- The loading utilities in `notebooks/Loading/` can be run as plain Python scripts (e.g., `python notebooks/Loading/to_csv.py`) once data paths are updated for your environment.

## Environment and dependencies
- Core stack: pandas, seaborn, matplotlib, numpy (see `requirements.txt` for the full list).
- Optional: Jupyter Lab/Notebook for interactive exploration.
- OS-agnostic; tested locally with Python 3.10.

## Dataset
- Source link: _TBD — add dataset URL here once finalized._

## Files and folder structure
- `notebooks/` — primary analysis notebooks, including `ucsq_analysis.ipynb`.
- `notebooks/Loading/` — helper scripts for converting `.zst` dumps to CSV and initializing a SQLite dump.
- `data/` — local storage for CSVs and generated artifacts (not versioned).
- `loadpipe/` — archived CLI for syncing with Google Drive; currently frozen and not used in this research.
- `requirements.txt` — Python dependencies for the analysis workflow.

## Notes
- Keep secrets and large data files out of version control; `.gitignore` already covers common cases.
