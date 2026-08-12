"""
baseline_excel.py

Excel exporter for the baseline optical analysis.

Purpose
-------
Exports the complete baseline optical dataset to a single Excel workbook.

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
    get_baseline_excel_path,
)

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_baseline_excel(
    cases: Iterable[OpticalCase],
    sheet_name: str = "Results",
) -> None:
    """
    Export baseline optical analysis results to an Excel workbook.
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

    output_file = get_baseline_excel_path()

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing_dataframe = None

    if output_file.exists():

        existing_dataframe = pd.read_excel(
            output_file,
            sheet_name=sheet_name,
        )

    dataframe = merge_export_table(
        existing=existing_dataframe,
        new=dataframe,
    )

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

        worksheet.freeze_panes = "A2"

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