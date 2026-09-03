# Crime and Street Lighting Analysis App

A small Tkinter desktop application for entering or importing before-and-after crime counts and comparing them across dates and locations.

## Features

- manual data entry;
- CSV and Excel import;
- before-and-after bar charts;
- comparison across dates and locations;
- local CSV export.

## Input format

Imported files must contain:

| Column | Required | Description |
|---|---:|---|
| `date` | Yes | Observation date |
| `time` | No | Optional observation time |
| `location` | Yes | Location label |
| `before` | Yes | Crime count before lighting |
| `after` | Yes | Crime count after lighting |

No dataset is included. Records entered manually can be saved to `crime_data.csv`, which is ignored by Git.

## Installation

```bash
git clone https://github.com/zanax1990/CrimeLightingApp.git
cd CrimeLightingApp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.

Tkinter is part of the standard Python installation on Windows and macOS. Some Linux distributions require the separate `python3-tk` system package.

## Run

```bash
python app.py
```

## Limitations

The application visualizes supplied counts; it does not estimate the causal effect of street lighting on crime. It does not validate date formats or control for location, exposure time, reporting changes, or other confounders. Percent reduction is undefined when a supplied `before` count is zero.
