"""
Canonical summary generation.

Purpose
-------
Builds the canonical summary table for an analysis type.

The canonical summary is created by collecting every optical results
table associated with an analysis and combining them into a single
dataset.

The summary preserves one row per optical case and performs no
statistical reduction. It serves as the canonical input for all
downstream reporting stages.

Pipeline
--------

Optical Results
        ↓
Canonical Summary
        ↓
Metric Tables
Report Tables
Report Figures

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

from src.models.analysis_type import (
    AnalysisType,
)

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


def _load_analysis_results(
    analysis_type: AnalysisType,
) -> pd.DataFrame:
    """
    Load every canonical optical results table associated with an
    analysis.

    Result tables are collected from the analysis output directory while
    excluding reporting artifacts.

    Returns
    -------
    pandas.DataFrame
        Combined canonical optical results.
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
            "Configuration",
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
    # Load optical results.
    # -------------------------------------------------------------

    summary = _load_analysis_results(
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