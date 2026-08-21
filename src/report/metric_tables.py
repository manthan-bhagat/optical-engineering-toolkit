"""
metric_tables.py

Metric table generation.

Purpose
-------
Generates one statistical table for each report metric from the
canonical summary table.

Baseline analyses produce configuration-, wavelength-, and
field-dependent metric tables.

Thermal and Monte Carlo analyses additionally produce grouped
statistical summaries.

Each table is exported as

- CSV
- Excel
- LaTeX longtable

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

from src.config import (
    REPORT_METRICS,
    THERMAL_REPORT_GROUP_COLUMN,
    MONTE_CARLO_REPORT_GROUP_COLUMN,
    THERMAL_PRIMARY_DATASET,
    MONTE_CARLO_PRIMARY_DATASET,
)

from src.models.analysis_type import AnalysisType

from src.report.common import (
    format_thermal_ranges,
    save_csv,
    save_excel,
    sort_montecarlo_datasets,
)

from src.report.latex import (
    save_longtable,
)

from src.report.report_paths import (
    get_metric_csv_path,
    get_metric_excel_path,
    get_metric_tex_path,
    get_selected_metric_csv_path,
    get_selected_metric_excel_path,
    get_selected_metric_tex_path,
)

from src.report.statistics import (
    calculate_summary_statistics,
)


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _generate_baseline_metric_table(
    summary: pd.DataFrame,
    metric_column: str,
) -> pd.DataFrame:
    """
    Generate a configuration-dependent baseline metric table.

    The baseline analysis contains one nominal value for every

    - configuration
    - wavelength
    - field

    No statistical aggregation is performed.
    """

    columns = [
        column
        for column in (
            "Configuration",
            "Wavelength (µm)",
            "Field",
            metric_column,
        )
        if column in summary.columns
    ]

    sort_columns = [
        column
        for column in (
            "Configuration",
            "Wavelength (µm)",
            "Field",
        )
        if column in columns
    ]

    return (
        summary[columns]
        .sort_values(
            by=sort_columns,
        )
        .reset_index(
            drop=True,
        )
    )


def _generate_statistical_metric_table(
    analysis_type: AnalysisType,
    summary: pd.DataFrame,
    metric_column: str,
) -> tuple[pd.DataFrame, str, str]:
    """
    Generate grouped statistical metric tables for thermal and
    Monte Carlo analyses.
    """

    if analysis_type == AnalysisType.THERMAL:

        group_column = (
            THERMAL_REPORT_GROUP_COLUMN
        )

        selected_dataset = (
            THERMAL_PRIMARY_DATASET
        )

    elif analysis_type == AnalysisType.MONTE_CARLO:

        group_column = (
            MONTE_CARLO_REPORT_GROUP_COLUMN
        )

        selected_dataset = (
            MONTE_CARLO_PRIMARY_DATASET
        )

    else:

        raise ValueError(
            f"Unsupported analysis type: {analysis_type}"
        )

    metric_table = calculate_summary_statistics(
        dataframe=summary,
        group_columns=[
            "Wavelength (µm)",
            group_column,
        ],
        metric_column=metric_column,
    )

    if analysis_type == AnalysisType.THERMAL:

        metric_table = format_thermal_ranges(
            metric_table,
            group_column,
        )

    else:

        metric_table = sort_montecarlo_datasets(
            metric_table,
            group_column,
        )

    return (
        metric_table,
        group_column,
        selected_dataset,
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_metric_tables(
    analysis_type: AnalysisType,
    summary: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Generate metric tables from a canonical summary.

    Parameters
    ----------
    analysis_type
        Analysis type.

    summary
        Canonical summary table.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Generated metric tables keyed by output name.
    """

    metric_tables: dict[
        str,
        pd.DataFrame,
    ] = {}

    # -------------------------------------------------------------
    # Generate every metric table.
    # -------------------------------------------------------------

    for (
        output_name,
        report_title,
        metric_column,
    ) in REPORT_METRICS:

        # ---------------------------------------------------------
        # Build metric table.
        # ---------------------------------------------------------

        if analysis_type == AnalysisType.BASELINE:

            metric_table = (
                _generate_baseline_metric_table(
                    summary,
                    metric_column,
                )
            )

        else:

            (
                metric_table,
                group_column,
                selected_dataset,
            ) = _generate_statistical_metric_table(
                analysis_type,
                summary,
                metric_column,
            )

        # ---------------------------------------------------------
        # Export complete metric table.
        # ---------------------------------------------------------

        save_csv(
            metric_table,
            get_metric_csv_path(
                analysis_type,
                output_name,
            ),
        )

        save_excel(
            metric_table,
            get_metric_excel_path(
                analysis_type,
                output_name,
            ),
        )

        save_longtable(
            dataframe=metric_table,
            output_path=get_metric_tex_path(
                analysis_type,
                output_name,
            ),
            caption=report_title,
            label=f"tab:{output_name}",
        )

        # ---------------------------------------------------------
        # Baseline exports end here.
        # ---------------------------------------------------------

        if analysis_type == AnalysisType.BASELINE:

            metric_tables[
                output_name
            ] = metric_table

            continue

        # ---------------------------------------------------------
        # Export selected dataset.
        # ---------------------------------------------------------

        selected_metric_table = (
            metric_table[
                metric_table[
                    group_column
                ]
                == selected_dataset
            ]
            .reset_index(
                drop=True,
            )
        )

        save_csv(
            selected_metric_table,
            get_selected_metric_csv_path(
                analysis_type,
                output_name,
            ),
        )

        save_excel(
            selected_metric_table,
            get_selected_metric_excel_path(
                analysis_type,
                output_name,
            ),
        )

        save_longtable(
            dataframe=selected_metric_table,
            output_path=get_selected_metric_tex_path(
                analysis_type,
                output_name,
            ),
            caption=(
                f"{report_title} "
                f"({selected_dataset})"
            ),
            label=f"tab:{output_name}_selected",
        )

        metric_tables[
            output_name
        ] = metric_table

    return metric_tables