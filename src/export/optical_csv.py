"""
optical_csv.py

CSV exporter for optical analysis results.

Purpose
-------
Exports a collection of OpticalCase objects belonging to a single
analysis grouping to a CSV file.

If a CSV already exists, newly generated values are merged into the
existing table. Previously exported values remain unless replaced by
newly computed non-null values.

The output location is determined automatically using the centralized
path utilities.

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

from src.plotting.paths import get_csv_path

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_csv(
    cases: Iterable[OpticalCase],
) -> None:
    """
    Export optical analysis results to a CSV file.

    Parameters
    ----------
    cases
        Optical cases belonging to a single analysis grouping.

    Notes
    -----
    Each OpticalCase is flattened into a single table row using the
    shared row builder.

    If a previous CSV export exists, newly generated values are merged
    into the existing table so that running individual processing
    pipelines updates only the corresponding columns.
    """

    cases = validate_export_cases(
        cases
    )

    # -------------------------------------------------------------
    # Convert optical cases into flat table rows.
    # -------------------------------------------------------------

    rows = [
        build_case_row(optical_case)
        for optical_case in cases
    ]

    # -------------------------------------------------------------
    # Build the DataFrame using the project-wide column order.
    # -------------------------------------------------------------

    dataframe = pd.DataFrame(
        rows,
        columns=RESULT_COLUMNS,
    )

    # -------------------------------------------------------------
    # Determine the output location.
    # -------------------------------------------------------------

    representative_case = cases[0]

    output_file = get_csv_path(
        representative_case,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------
    # Load existing export, if present.
    # -------------------------------------------------------------

    existing_dataframe = None

    if output_file.exists():

        existing_dataframe = pd.read_csv(
            output_file
        )

    # -------------------------------------------------------------
    # Merge newly generated results.
    # -------------------------------------------------------------

    dataframe = merge_export_table(
        existing=existing_dataframe,
        new=dataframe,
    )

    # -------------------------------------------------------------
    # Export to CSV.
    # -------------------------------------------------------------

    dataframe.to_csv(
        output_file,
        index=False,
    )