"""
report_tables.py

Thesis report table generation.

Purpose
-------
Generates the final report-ready tables used in the thesis.

Unlike metric tables, report tables are generated directly from the
canonical summary so that all statistics are computed from the original
measurements rather than from previously aggregated values.

Each report table is exported as

- CSV
- Excel
- LaTeX longtable

Responsibilities
----------------
- Calculate report statistics directly from the canonical summary.
- Round numerical values for presentation.
- Export CSV, Excel and LaTeX report tables.

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
    CSV_DECIMALS,
    REPORT_METRICS,
    THERMAL_REPORT_GROUP_COLUMN,
    MONTE_CARLO_REPORT_GROUP_COLUMN,
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
    get_report_csv_path,
    get_report_excel_path,
    get_report_tex_path,
)

from src.report.statistics import (
    calculate_summary_statistics,
)

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _generate_baseline_report_table(
    summary: pd.DataFrame,
    metric_column: str,
) -> pd.DataFrame:
    """
    Generate a baseline report table.

    The baseline report summarizes the optical performance at each
    wavelength by computing statistics across every field.
    """

    return (
        calculate_summary_statistics(
            dataframe=summary,
            group_columns=[
                "Wavelength (µm)",
            ],
            metric_column=metric_column,
        )
        .sort_values(
            "Wavelength (µm)",
        )
        .reset_index(
            drop=True,
        )
    )


def _generate_statistical_report_table(
    analysis_type: AnalysisType,
    summary: pd.DataFrame,
    metric_column: str,
) -> pd.DataFrame:
    """
    Generate a statistical report table for thermal or Monte Carlo
    analyses.
    """

    if analysis_type == AnalysisType.THERMAL:

        group_column = (
            THERMAL_REPORT_GROUP_COLUMN
        )

    elif analysis_type == AnalysisType.MONTE_CARLO:

        group_column = (
            MONTE_CARLO_REPORT_GROUP_COLUMN
        )

    else:

        raise ValueError(
            f"Unsupported analysis type: "
            f"{analysis_type}"
        )

    report_table = (
        calculate_summary_statistics(
            dataframe=summary,
            group_columns=[
                group_column,
            ],
            metric_column=metric_column,
        )
    )

    if analysis_type == AnalysisType.THERMAL:

        report_table = (
            format_thermal_ranges(
                report_table,
                group_column,
            )
        )

    else:

        report_table = (
            sort_montecarlo_datasets(
                report_table,
                group_column,
            )
        )

    return report_table


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def export_report_tables(
    analysis_type: AnalysisType,
    summary: pd.DataFrame,
) -> None:
    """
    Generate thesis-ready report tables.

    Parameters
    ----------
    analysis_type
        Analysis type.

    summary
        Canonical summary table.
    """

    for (
        output_name,
        report_title,
        metric_column,
    ) in REPORT_METRICS:

        # ---------------------------------------------------------
        # Build report table.
        # ---------------------------------------------------------

        if analysis_type == AnalysisType.BASELINE:

            report_table = (
                _generate_baseline_report_table(
                    summary,
                    metric_column,
                )
            )

        else:

            report_table = (
                _generate_statistical_report_table(
                    analysis_type,
                    summary,
                    metric_column,
                )
            )

        # ---------------------------------------------------------
        # Presentation formatting.
        # ---------------------------------------------------------

        numeric_columns = (
            report_table
            .select_dtypes(
                include="number",
            )
            .columns
        )

        report_table[
            numeric_columns
        ] = (
            report_table[
                numeric_columns
            ]
            .round(
                CSV_DECIMALS,
            )
        )

        # ---------------------------------------------------------
        # Export.
        # ---------------------------------------------------------

        save_csv(
            report_table,
            get_report_csv_path(
                analysis_type,
                output_name,
            ),
        )

        save_excel(
            report_table,
            get_report_excel_path(
                analysis_type,
                output_name,
            ),
        )

        save_longtable(
            dataframe=report_table,
            output_path=get_report_tex_path(
                analysis_type,
                output_name,
            ),
            caption=report_title,
            label=f"tab:{output_name}_report",
        )