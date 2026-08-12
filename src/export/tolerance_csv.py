"""
Tolerance CSV export.

This module exports a parsed Zemax tolerance study to a collection of CSV
files. Each logical section of the tolerance report is exported separately.
"""

from __future__ import annotations

from pathlib import Path
import csv

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


OUTPUT_DIRECTORY = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "output"
    / "tolerance"
)


def export_tolerance_csv(
    study: ToleranceStudy,
    output_directory: Path | None = None,
) -> None:
    """
    Export the tolerance study as CSV files.

    Parameters
    ----------
    study
        Parsed tolerance study.

    output_directory
        Destination directory.
    """

    directory = output_directory or OUTPUT_DIRECTORY

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_table(
        directory / "summary.csv",
        [build_summary_row(study.summary)],
    )

    _write_table(
        directory / "fields.csv",
        [
            build_field_row(field)
            for field in study.fields
        ],
    )

    _write_table(
        directory / "sensitivities.csv",
        [
            build_sensitivity_row(result)
            for result in study.sensitivities
        ],
    )

    _write_table(
        directory / "worst_offenders.csv",
        [
            build_worst_offender_row(result)
            for result in study.worst_offenders
        ],
    )

    _write_table(
        directory / "rss.csv",
        [build_rss_row(study.rss)],
    )

    _write_table(
        directory / "monte_carlo.csv",
        [build_monte_carlo_row(study.monte_carlo)],
    )

    _write_table(
        directory / "compensators.csv",
        [
            build_compensator_row(result)
            for result in study.compensators
        ],
    )

    _write_table(
        directory / "percentiles.csv",
        [
            build_percentile_row(result)
            for result in study.percentiles
        ],
    )


def _write_table(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    """
    Write a CSV table.

    Parameters
    ----------
    path
        Output CSV path.

    rows
        Rows to write.
    """

    if not rows:
        return

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )

        writer.writeheader()

        writer.writerows(rows)