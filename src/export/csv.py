"""
csv.py

CSV exporter for optical analysis results.

Purpose
-------
Exports a collection of OpticalCase objects belonging to a single
analysis type and wavelength to a CSV file.

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

from src.export.common import validate_export_cases
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
        Optical cases belonging to a single analysis type and
        wavelength.

    Notes
    -----
    Each OpticalCase is flattened into a single table row using the
    shared row builder. This guarantees that the CSV schema remains
    identical to the Excel export and any future tabular exporters.
    """

    (
        cases,
        analysis_type,
        wavelength_um,
    ) = validate_export_cases(
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

    output_file = get_csv_path(
        analysis_type,
        wavelength_um,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------
    # Export to CSV.
    # -------------------------------------------------------------

    dataframe.to_csv(
        output_file,
        index=False,
    )