"""
Tolerance analysis pipeline.
"""

from __future__ import annotations

from pathlib import Path

from src.export.tolerance_csv import export_tolerance_csv
from src.export.tolerance_excel import export_tolerance_excel
from src.parsers.tolerance import ToleranceParser
from src.plotting.tolerance import generate_plots


INPUT_FILE = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "input"
    / "tolerance-analysis-result.txt"
)


def run() -> None:
    """
    Execute the complete tolerance analysis pipeline.
    """

    study = ToleranceParser().parse(
        INPUT_FILE,
    )

    export_tolerance_csv(
        study,
    )

    export_tolerance_excel(
        study,
    )

    generate_plots(
        study,
    )


if __name__ == "__main__":
    run()