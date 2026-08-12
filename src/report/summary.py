"""
summary.py

Canonical summary generation.

Purpose
-------
Builds the master summary table for an analysis type.

For thermal and Monte Carlo analyses, the canonical summary is created
by combining every exported optical CSV into a single dataset.

For the baseline analysis, the canonical summary is generated directly
from the exported baseline results table, since the baseline already
contains every wavelength and field in a single file.

The summary table preserves one row per optical case and performs no
statistical reduction. It serves as the canonical input for all
downstream statistical reporting.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import pandas as pd

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.analysis_type import AnalysisType

from src.report.common import (
    load_results_table,
    save_csv,
    save_excel,
)

from src.report.report_paths import (
    get_analysis_output_directory,
    get_summary_csv_path,
    get_summary_excel_path,
)

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _load_multi_file_summary(
    analysis_type: AnalysisType,
) -> pd.DataFrame:
    """
    Build a canonical summary by concatenating every exported optical
    results table.

    Used for analyses whose results are distributed across multiple
    CSV files (e.g. Thermal and Monte Carlo).
    """

    analysis_directory = (
        get_analysis_output_directory(
            analysis_type,
        )
    )

    csv_files = sorted(

        path

        for path in analysis_directory.rglob(
            "*.csv"
        )

        if "reports" not in path.parts
    )

    tables: list[pd.DataFrame] = []

    for csv_file in csv_files:

        tables.append(
            load_results_table(
                csv_file,
            )
        )

    if not tables:

        return pd.DataFrame()

    return pd.concat(
        tables,
        ignore_index=True,
    )


def _load_baseline_summary() -> pd.DataFrame:
    """
    Load the canonical baseline results table.

    The baseline analysis exports a single results table containing all
    wavelengths and fields, so no concatenation is required.
    """

    analysis_directory = (
        get_analysis_output_directory(
            AnalysisType.BASELINE,
        )
    )

    results_file = (
        analysis_directory
        / "results.csv"
    )

    return load_results_table(
        results_file,
    )


def _sort_summary(
    summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply a consistent ordering to the canonical summary.
    """

    if summary.empty:

        return summary

    sort_columns = [

        column

        for column in (

            "Dataset",
            "Temperature (°C)",
            "Wavelength (µm)",
            "Field",
            "Statistical Case",
        )

        if column in summary.columns
    ]

    if sort_columns:

        summary = summary.sort_values(
            by=sort_columns,
        )

    return summary.reset_index(
        drop=True,
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_summary(
    analysis_type: AnalysisType,
) -> pd.DataFrame:
    """
    Build and export the canonical summary table.

    Parameters
    ----------
    analysis_type
        Analysis type to summarize.

    Returns
    -------
    pandas.DataFrame
        Canonical summary table.
    """

    # -------------------------------------------------------------
    # Load canonical results.
    # -------------------------------------------------------------

    if analysis_type == AnalysisType.BASELINE:

        summary = _load_baseline_summary()

    else:

        summary = _load_multi_file_summary(
            analysis_type,
        )

    # -------------------------------------------------------------
    # Apply consistent ordering.
    # -------------------------------------------------------------

    summary = _sort_summary(
        summary,
    )

    # -------------------------------------------------------------
    # Export.
    # -------------------------------------------------------------

    save_csv(
        summary,
        get_summary_csv_path(
            analysis_type,
        ),
    )

    save_excel(
        summary,
        get_summary_excel_path(
            analysis_type,
        ),
    )

    return summary