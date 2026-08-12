"""
baseline_csv.py

CSV exporter for the baseline optical analysis.

Purpose
-------
Exports the complete baseline optical dataset to a single CSV file.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from typing import Iterable

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import pandas as pd

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import RESULT_COLUMNS

from src.export.common import (
    merge_export_table,
    validate_export_cases,
)

from src.export.row_builder import build_case_row

from src.models.optical_case import OpticalCase

from src.plotting.paths import (
    get_baseline_csv_path,
)

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_baseline_csv(
    cases: Iterable[OpticalCase],
) -> None:
    """
    Export baseline optical analysis results to a CSV file.
    """

    cases = validate_export_cases(
        cases
    )

    rows = [
        build_case_row(optical_case)
        for optical_case in cases
    ]

    dataframe = pd.DataFrame(
        rows,
        columns=RESULT_COLUMNS,
    )

    output_file = get_baseline_csv_path()

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing_dataframe = None

    if output_file.exists():

        existing_dataframe = pd.read_csv(
            output_file
        )

    dataframe = merge_export_table(
        existing=existing_dataframe,
        new=dataframe,
    )

    dataframe.to_csv(
        output_file,
        index=False,
    )