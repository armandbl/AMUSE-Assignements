"""Load the planet-survival results CSV for visualisation."""

import csv
from pathlib import Path

DATADIR = Path(__file__).resolve().parents[1] / "reference"
RESULTS_CSV = DATADIR / "planet_survival_results.csv"


def load_data():
    """Return the results CSV as a list of rows (each a list of strings).

    The first row is the header.
    """
    with RESULTS_CSV.open(newline="", encoding="utf-8") as stream:
        return list(csv.reader(stream))
