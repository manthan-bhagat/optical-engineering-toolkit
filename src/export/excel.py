"""
excel.py

Excel exporter for optical analysis results.

Purpose
-------
Exports a collection of OpticalCase objects belonging to a single
analysis type and wavelength to an Excel workbook.

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

from src.plotting.paths import get_excel_path

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_excel(
    cases: Iterable[OpticalCase],
    sheet_name: str = "Results",
) -> None:
    """
    Export optical analysis results to an Excel workbook.

    Parameters
    ----------
    cases
        Optical cases belonging to a single analysis type and
        wavelength.

    sheet_name
        Name of the worksheet.
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

    output_file = get_excel_path(
        analysis_type,
        wavelength_um,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------
    # Export to Excel.
    # -------------------------------------------------------------

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl",
    ) as writer:

        dataframe.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
        )

        worksheet = writer.sheets[
            sheet_name
        ]

        # ---------------------------------------------------------
        # Freeze the header row.
        # ---------------------------------------------------------

        worksheet.freeze_panes = "A2"

        # ---------------------------------------------------------
        # Auto-size all columns.
        # ---------------------------------------------------------

        for column_cells in worksheet.columns:

            length = max(
                len(str(cell.value))
                if cell.value is not None
                else 0
                for cell in column_cells
            )

            worksheet.column_dimensions[
                column_cells[0].column_letter
            ].width = max(
                length + 2,
                12,
            )