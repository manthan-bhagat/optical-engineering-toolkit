"""
Tolerance Excel export.

This module exports a parsed Zemax tolerance study to a single Excel workbook.
Each logical section of the tolerance report is written to its own worksheet.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from src.models.tolerance_study import ToleranceStudy

from src.export.tolerance_row_builder import (
    build_summary_row,
    build_field_row,
    build_sensitivity_row,
    build_worst_offender_row,
    build_rss_row,
    build_monte_carlo_row,
    build_compensator_row,
    build_percentile_row,
)


OUTPUT_FILE = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "output"
    / "tolerance"
    / "tolerance_analysis.xlsx"
)


def export_tolerance_excel(
    study: ToleranceStudy,
    output_file: Path | None = None,
) -> None:
    """
    Export a tolerance study to an Excel workbook.

    Parameters
    ----------
    study
        Parsed tolerance study.

    output_file
        Destination workbook.
    """

    path = output_file or OUTPUT_FILE

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    workbook = Workbook()

    #
    # Remove default worksheet.
    #
    workbook.remove(workbook.active)

    _write_sheet(
        workbook,
        "Summary",
        [build_summary_row(study.summary)],
    )

    _write_sheet(
        workbook,
        "Fields",
        [
            build_field_row(field)
            for field in study.fields
        ],
    )

    _write_sheet(
        workbook,
        "Sensitivities",
        [
            build_sensitivity_row(result)
            for result in study.sensitivities
        ],
    )

    _write_sheet(
        workbook,
        "Worst Offenders",
        [
            build_worst_offender_row(result)
            for result in study.worst_offenders
        ],
    )

    _write_sheet(
        workbook,
        "RSS",
        [
            build_rss_row(study.rss),
        ],
    )

    _write_sheet(
        workbook,
        "Monte Carlo",
        [
            build_monte_carlo_row(
                study.monte_carlo,
            )
        ],
    )

    _write_sheet(
        workbook,
        "Compensators",
        [
            build_compensator_row(result)
            for result in study.compensators
        ],
    )

    _write_sheet(
        workbook,
        "Percentiles",
        [
            build_percentile_row(result)
            for result in study.percentiles
        ],
    )

    workbook.save(path)


def _write_sheet(
    workbook: Workbook,
    name: str,
    rows: list[dict[str, object]],
) -> None:
    """
    Write one worksheet.

    Parameters
    ----------
    workbook
        Workbook being constructed.

    name
        Worksheet name.

    rows
        Table rows.
    """

    worksheet = workbook.create_sheet(title=name)

    if not rows:
        return

    headers = list(rows[0].keys())

    worksheet.append(headers)

    for row in rows:

        worksheet.append(
            [
                row[column]
                for column in headers
            ]
        )