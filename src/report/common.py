"""
common.py

Shared utilities for statistical report generation.

Purpose
-------
Provides common helpers used by every reporting stage.

Responsibilities
----------------
- Locate report output directories.
- Load exported results tables.
- Write CSV and Excel files.
- Apply common thermal and Monte Carlo formatting.
- Sort report rows consistently.
- Build publication plotting series.

This module intentionally contains no statistical calculations.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import pandas as pd

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    MONTE_CARLO_DATASET_ORDER,
    THERMAL_REPORT_RANGE_NAMES,
    FIELD_COLORS,
    REPORT_WAVELENGTH_COLORS,
)

# ---------------------------------------------------------------------
# Public Helpers
# ---------------------------------------------------------------------


def load_results_table(
    path: Path,
) -> pd.DataFrame:
    """
    Load an exported results table.
    """

    return pd.read_csv(
        path,
    )


def save_csv(
    dataframe: pd.DataFrame,
    path: Path,
) -> None:
    """
    Save a CSV report.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        path,
        index=False,
    )


def save_excel(
    dataframe: pd.DataFrame,
    path: Path,
) -> None:
    """
    Save an Excel report.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_excel(
        path,
        index=False,
    )


def format_thermal_ranges(
    dataframe: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Replace internal thermal dataset names with report names.
    """

    dataframe = dataframe.copy()

    dataframe[column] = (
        dataframe[column]
        .astype(str)
        .str.lower()
        .map(
            THERMAL_REPORT_RANGE_NAMES,
        )
        .fillna(
            dataframe[column],
        )
    )

    return dataframe


def sort_montecarlo_datasets(
    dataframe: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Sort Monte Carlo datasets using the canonical ordering.

    The dataset column remains an ordered categorical so that the
    canonical Monte Carlo ordering is preserved through subsequent
    grouping and plotting operations.
    """

    dataframe = dataframe.copy()

    dataframe[column] = pd.Categorical(
        dataframe[column],
        categories=MONTE_CARLO_DATASET_ORDER,
        ordered=True,
    )

    return (
        dataframe
        .sort_values(
            column,
        )
        .reset_index(
            drop=True,
        )
    )


# ---------------------------------------------------------------------
# Figure Helpers
# ---------------------------------------------------------------------


def _aggregate(
    dataframe: pd.DataFrame,
    *,
    group_columns: str | list[str],
    value_column: str,
    aggregation: str,
) -> pd.DataFrame:
    """
    Aggregate a metric using the requested statistical operation.

    Parameters
    ----------
    dataframe
        Source table.

    group_columns
        Grouping column(s).

    value_column
        Metric column.

    aggregation
        One of

        - mean
        - min
        - max

    Returns
    -------
    pandas.DataFrame
        Aggregated table.
    """

    if isinstance(
        group_columns,
        str,
    ):

        group_columns = [
            group_columns,
        ]

    if aggregation not in (
        "mean",
        "min",
        "std",
        "max",
    ):

        raise ValueError(
            f"Unsupported aggregation "
            f"'{aggregation}'."
        )

    return (
        dataframe
        .groupby(
            group_columns,
            sort=True,
            observed=True,
        )[value_column]
        .agg(
            aggregation,
        )
        .reset_index()
    )


def build_summary_series(
    dataframe: pd.DataFrame,
    *,
    x_column: str,
    y_column: str,
) -> list[dict]:
    """
    Build publication summary curves.

    Baseline
        X = Wavelength

        Collapse:
            • Field

    Thermal / Monte Carlo
        X = Temperature / Representative Trial

        Collapse:
            • Wavelength
            • Field

    Returns
    -------
    list[dict]
        Three curves

        - Min
        - Mean
        - Max
    """

    if x_column == "Statistical Case":
        dataframe = sort_montecarlo_datasets(
            dataframe,
            x_column,
        )

    grouped = (
        dataframe
        .groupby(
            x_column,
            sort=True,
            observed=True,
        )[y_column]
        .agg(
            [
                "min",
                "mean",
                "std",
                "max",
            ]
        )
        .reset_index()
    )

    x = grouped[x_column]

    return [

        {
            "label": "Min",
            "x": x,
            "y": grouped["min"],
        },

        {
            "label": "Mean",
            "x": x,
            "y": grouped["mean"],
            "std": grouped["std"],
        },

        {
            "label": "Max",
            "x": x,
            "y": grouped["max"],
        },

    ]

def build_wavelength_series(
    dataframe: pd.DataFrame,
    *,
    x_column: str,
    y_column: str,
    statistic: str = "mean",
) -> list[dict]:
    """
    Build wavelength curves.

    One curve is generated for every wavelength.

    Baseline
        Not applicable.

    Thermal / Monte Carlo

        X = Temperature / Representative Trial

        Curves = Wavelength

        Each point is computed across every field using

        - min
        - mean
        - max

    Parameters
    ----------
    dataframe
        Canonical summary table.

    x_column
        Temperature or Representative Trial.

    y_column
        Metric column.

    statistic
        Aggregation across field.

        Supported values

        - "min"
        - "mean"
        - "max"

    Returns
    -------
    list[dict]
        Plotting series.
    """

    if x_column == "Wavelength (µm)":

        return []

    series: list[dict] = []

    grouped = list(
        dataframe.groupby(
            "Wavelength (µm)",
            sort=True,
        )
    )

    for index, (wavelength, table) in enumerate(grouped):
        if x_column == "Statistical Case":
            table = sort_montecarlo_datasets(
                table,
                x_column,
            )

        plot_table = _aggregate(
            table,
            group_columns=x_column,
            value_column=y_column,
            aggregation=statistic,
        )

        series.append(
            {
                "label": f"{wavelength * 1000:.1f} nm",
                "color": REPORT_WAVELENGTH_COLORS[index],
                "x": plot_table[x_column],
                "y": plot_table[y_column],
            }
        )

    return series


def build_field_series(
    dataframe: pd.DataFrame,
    *,
    x_column: str,
    y_column: str,
    statistic: str = "mean",
) -> list[dict]:
    """
    Build field curves.

    One curve is generated for every field.

    Baseline

        X = Wavelength

        No averaging is performed.

    Thermal / Monte Carlo

        X = Temperature / Representative Trial

        Curves = Field

        Each point is computed across every wavelength using

        - min
        - mean
        - max

    Parameters
    ----------
    dataframe
        Canonical summary table.

    x_column
        Plot X-axis.

    y_column
        Metric column.

    statistic
        Aggregation across wavelength.

        Supported values

        - "min"
        - "mean"
        - "max"

    Returns
    -------
    list[dict]
        Plotting series.
    """

    if "Field" not in dataframe.columns:

        return []

    series: list[dict] = []

    grouped = list(
        dataframe.groupby(
            "Field",
            sort=True,
        )
    )

    for index, (field, table) in enumerate(grouped):

        #
        # Baseline
        #

        if x_column == "Wavelength (µm)":

            plot_table = table.sort_values(
                x_column,
            )

        #
        # Thermal / Monte Carlo
        #

        else:
            if x_column == "Statistical Case":
                table = sort_montecarlo_datasets(
                    table,
                    x_column,
                )

            plot_table = _aggregate(
                table,
                group_columns=x_column,
                value_column=y_column,
                aggregation=statistic,
            )

        series.append(
            {
                "label": f"Field {field}",
                "color": FIELD_COLORS[index],
                "x": plot_table[x_column],
                "y": plot_table[y_column],
            }
        )

    return series


def build_engineering_summary_series(
    dataframe: pd.DataFrame,
    *,
    wavelength_um: float,
    x_column: str,
    y_column: str,
) -> list[dict]:
    """
    Build engineering validation summary curves.

    A single engineering wavelength is selected, after which statistics
    are computed across every field.

    Thermal
        X = Temperature

    Monte Carlo
        X = Representative Trial

    Collapse
        • Field

    Statistics
        • Min
        • Mean
        • Std
        • Max

    Parameters
    ----------
    dataframe
        Canonical summary table.

    wavelength_um
        Engineering wavelength used for validation.

    x_column
        Plot X-axis.

    y_column
        Metric column.

    Returns
    -------
    list[dict]
        Three plotting series

        - Min
        - Mean
        - Max

        The Mean series contains the standard deviation for plotting the
        uncertainty band.
    """

    if x_column == "Wavelength (µm)":

        return []

    dataframe = dataframe[
        dataframe["Wavelength (µm)"] == wavelength_um
    ]

    if x_column == "Statistical Case":
        dataframe = sort_montecarlo_datasets(
            dataframe,
            x_column,
        )

    grouped = (
        dataframe
        .groupby(
            x_column,
            sort=True,
            observed=True,
        )[y_column]
        .agg(
            [
                "min",
                "mean",
                "std",
                "max",
            ]
        )
        .reset_index()
    )

    x = grouped[x_column]

    return [

        {
            "label": "Min",
            "x": x,
            "y": grouped["min"],
        },

        {
            "label": "Mean",
            "x": x,
            "y": grouped["mean"],
            "std": grouped["std"],
        },

        {
            "label": "Max",
            "x": x,
            "y": grouped["max"],
        },

    ]