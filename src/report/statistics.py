"""
statistics.py

Statistical summary utilities.

Purpose
-------
Provides common statistical aggregation routines used by the reporting
pipeline.

These functions are intentionally independent of any particular
analysis type. They operate purely on tabular data and are reused by
both thermal and Monte Carlo report generation.

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

from src.config import SUMMARY_STATISTICS

# ---------------------------------------------------------------------
# Public Functions
# ---------------------------------------------------------------------


def calculate_summary_statistics(
    dataframe: pd.DataFrame,
    group_columns: str | list[str],
    metric_column: str,
) -> pd.DataFrame:
    """
    Calculate summary statistics for a metric.

    Parameters
    ----------
    dataframe
        Source results table.

    group_columns
        Column(s) used for grouping.

        Examples
        --------
        Thermal metric tables

            [
                "Wavelength (µm)",
                "Temperature Range",
            ]

        Monte Carlo metric tables

            [
                "Wavelength (µm)",
                "Dataset",
            ]

        Thermal report tables

            [
                "Temperature Range",
            ]

        Monte Carlo report tables

            [
                "Dataset",
            ]

    metric_column
        Numerical metric to summarize.

    Returns
    -------
    pandas.DataFrame
        Grouping columns followed by

        Best
        Worst
        Mean
        Std. Dev.
    """

    if isinstance(
        group_columns,
        str,
    ):

        group_columns = [
            group_columns
        ]

    grouped = (
        dataframe
        .groupby(
            group_columns,
            sort=False,
        )[metric_column]
        .agg(
            [
                ("Min", "min"),
                ("Max", "max"),
                ("Mean", "mean"),
                ("Std. Dev.", "std"),
            ]
        )
        .reset_index()
    )

    # -------------------------------------------------------------
    # Ensure every expected statistic column exists.
    # -------------------------------------------------------------

    for statistic in SUMMARY_STATISTICS:

        if statistic not in grouped.columns:

            grouped[statistic] = pd.NA

    return grouped[
        [
            *group_columns,
            *SUMMARY_STATISTICS,
        ]
    ]