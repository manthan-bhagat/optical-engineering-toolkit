"""
report_paths.py

Output path utilities for statistical reports.

Purpose
-------
Provides centralized path construction for the reporting pipeline.

Every report writer should obtain its output location through this
module instead of constructing filesystem paths directly.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    THERMAL_REPORT_OUTPUT_DIRECTORY,
    BASELINE_REPORT_OUTPUT_DIRECTORY,
    MONTE_CARLO_REPORT_OUTPUT_DIRECTORY,
    THERMAL_LATEX_OUTPUT_DIRECTORY,
    BASELINE_LATEX_OUTPUT_DIRECTORY,
    MONTE_CARLO_LATEX_OUTPUT_DIRECTORY,
    SUMMARY_DIRECTORY_NAME,
    METRICS_DIRECTORY_NAME,
    REPORT_DIRECTORY_NAME,
    LATEX_METRICS_DIRECTORY_NAME,
    LATEX_REPORT_DIRECTORY_NAME,
    SUMMARY_CSV_FILENAME,
    SUMMARY_EXCEL_FILENAME,
    LATEX_FILE_EXTENSION,
    THERMAL_OUTPUT_DIRECTORY,
    BASELINE_OUTPUT_DIRECTORY,
    MONTE_CARLO_OUTPUT_DIRECTORY,
)

from src.models.analysis_type import AnalysisType

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def get_analysis_output_directory(
    analysis_type: AnalysisType,
) -> Path:
    """
    Return the root optical output directory for an analysis type.
    """

    if analysis_type == AnalysisType.THERMAL:

        return THERMAL_OUTPUT_DIRECTORY

    if analysis_type == AnalysisType.BASELINE:

        return BASELINE_OUTPUT_DIRECTORY

    if analysis_type == AnalysisType.MONTE_CARLO:

        return MONTE_CARLO_OUTPUT_DIRECTORY

    raise ValueError(
        f"Unsupported analysis type: {analysis_type}"
    )


def _get_report_root(
    analysis_type: AnalysisType,
) -> Path:
    """
    Return the root report directory for an analysis type.
    """

    if analysis_type == AnalysisType.THERMAL:

        return THERMAL_REPORT_OUTPUT_DIRECTORY

    if analysis_type == AnalysisType.BASELINE:

        return BASELINE_REPORT_OUTPUT_DIRECTORY

    if analysis_type == AnalysisType.MONTE_CARLO:

        return MONTE_CARLO_REPORT_OUTPUT_DIRECTORY

    raise ValueError(
        f"Unsupported analysis type: {analysis_type}"
    )


def _get_latex_root(
    analysis_type: AnalysisType,
) -> Path:
    """
    Return the root LaTeX export directory for an analysis type.
    """

    if analysis_type == AnalysisType.THERMAL:

        return THERMAL_LATEX_OUTPUT_DIRECTORY

    if analysis_type == AnalysisType.BASELINE:

        return BASELINE_LATEX_OUTPUT_DIRECTORY

    if analysis_type == AnalysisType.MONTE_CARLO:

        return MONTE_CARLO_LATEX_OUTPUT_DIRECTORY

    raise ValueError(
        f"Unsupported analysis type: {analysis_type}"
    )


# ---------------------------------------------------------------------
# Summary Paths
# ---------------------------------------------------------------------


def get_summary_csv_path(
    analysis_type: AnalysisType,
) -> Path:
    """
    Return the summary CSV path.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / SUMMARY_DIRECTORY_NAME
        / SUMMARY_CSV_FILENAME
    )


def get_summary_excel_path(
    analysis_type: AnalysisType,
) -> Path:
    """
    Return the summary Excel path.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / SUMMARY_DIRECTORY_NAME
        / SUMMARY_EXCEL_FILENAME
    )


# ---------------------------------------------------------------------
# Metric Table Paths
# ---------------------------------------------------------------------


def get_metric_csv_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the CSV path for a complete metric table.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / METRICS_DIRECTORY_NAME
        / f"{metric_name}.csv"
    )


def get_metric_excel_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the Excel path for a complete metric table.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / METRICS_DIRECTORY_NAME
        / f"{metric_name}.xlsx"
    )


def get_metric_tex_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the LaTeX path for a complete metric table.
    """

    return (
        _get_latex_root(
            analysis_type,
        )
        / LATEX_METRICS_DIRECTORY_NAME
        / f"{metric_name}{LATEX_FILE_EXTENSION}"
    )


# ---------------------------------------------------------------------
# Selected Metric Table Paths
# ---------------------------------------------------------------------


def get_selected_metric_csv_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the CSV path for the selected-dataset metric table.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / METRICS_DIRECTORY_NAME
        / "selected"
        / f"{metric_name}.csv"
    )


def get_selected_metric_excel_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the Excel path for the selected-dataset metric table.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / METRICS_DIRECTORY_NAME
        / "selected"
        / f"{metric_name}.xlsx"
    )


def get_selected_metric_tex_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the LaTeX path for the selected-dataset metric table.
    """

    return (
        _get_latex_root(
            analysis_type,
        )
        / LATEX_METRICS_DIRECTORY_NAME
        / "selected"
        / f"{metric_name}{LATEX_FILE_EXTENSION}"
    )


# ---------------------------------------------------------------------
# Thesis Report Table Paths
# ---------------------------------------------------------------------


def get_report_csv_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the CSV path for a thesis report table.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / REPORT_DIRECTORY_NAME
        / f"{metric_name}.csv"
    )


def get_report_excel_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the Excel path for a thesis report table.
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / REPORT_DIRECTORY_NAME
        / f"{metric_name}.xlsx"
    )


def get_report_tex_path(
    analysis_type: AnalysisType,
    metric_name: str,
) -> Path:
    """
    Return the LaTeX path for a thesis report table.
    """

    return (
        _get_latex_root(
            analysis_type,
        )
        / LATEX_REPORT_DIRECTORY_NAME
        / f"{metric_name}{LATEX_FILE_EXTENSION}"
    )

# ---------------------------------------------------------------------
# Report Figure Paths
# ---------------------------------------------------------------------


def get_report_figure_path(
    analysis_type: AnalysisType,
    figure_name: str,
    *path_parts: str,
) -> Path:
    """
    Return the output path for a report figure.

    Parameters
    ----------
    analysis_type
        Analysis type.

    figure_name
        Figure filename without extension.

    *path_parts
        Optional nested subdirectories.

    Examples
    --------
    Summary figure

        figures/
            summary/
                psf.png

    Baseline field figure

        figures/
            field/
                psf.png

    Field-averaged figure

        figures/
            field_averaged/
                mean/
                    psf.png

    Wavelength-averaged figure

        figures/
            wavelength_averaged/
                max/
                    psf.png

    Engineering validation figure

        figures/
            engineering/
                psf.png
    """

    return (
        _get_report_root(
            analysis_type,
        )
        / "figures"
        / Path(*path_parts)
        / f"{figure_name}.pdf"
    )