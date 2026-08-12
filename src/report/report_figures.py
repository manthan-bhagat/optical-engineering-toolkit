"""
report_figures.py

Publication-quality report figure generation.

Purpose
-------
Generates publication-quality figures from the canonical summary table.

For every configured report metric, two figures are produced

• All-field figure
• Summary figure

The plotting implementation is delegated to report.figures while
engineering reference curves are supplied by report.reference.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    REPORT_FIGURES,
    ENGINEERING_WAVELENGTH_UM,
)

from src.report.common import (
    build_summary_series,
    build_field_series,
    build_wavelength_series,
    build_engineering_summary_series,
)


from src.models.analysis_type import (
    AnalysisType,
)


from src.report.figures import (
    save_figure,
)

from src.report.reference import (
    get_reference_series,
    get_engineering_reference_series,
)

from src.report.report_paths import (
    get_report_figure_path,
)

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _get_x_column(
    analysis_type: AnalysisType,
) -> str:
    """
    Return the plotting X-axis column.
    """

    if analysis_type == AnalysisType.BASELINE:

        return "Wavelength (µm)"

    if analysis_type == AnalysisType.THERMAL:

        return "Temperature (°C)"

    if analysis_type == AnalysisType.MONTE_CARLO:

        return "Statistical Case"

    raise ValueError(
        f"Unsupported analysis type: {analysis_type}"
    )


def _get_x_label(
    analysis_type: AnalysisType,
) -> str:
    """
    Return the plotting X-axis label.
    """

    if analysis_type == AnalysisType.BASELINE:

        return "Wavelength (nm)"

    if analysis_type == AnalysisType.THERMAL:

        return "Temperature (°C)"

    if analysis_type == AnalysisType.MONTE_CARLO:

        return "Representative Trial"

    raise ValueError(
        f"Unsupported analysis type: {analysis_type}"
    )


def _build_reference_series(
    analysis_type: AnalysisType,
    output_name: str,
    summary,
):
    """
    Build engineering reference curves for a figure.

    Reference curves are currently available only for wavelength-based
    baseline figures.

    Thermal and Monte Carlo figures use temperature and representative
    trial as their X-axis respectively, so wavelength-based theoretical
    references are not applicable.
    """

    if analysis_type != AnalysisType.BASELINE:

        return None

    return get_reference_series(
        output_name,
        summary["Wavelength (µm)"],
    )


def _convert_series_x_to_nm(
    series: list[dict] | None,
) -> list[dict] | None:
    """
    Convert wavelength-based X coordinates from µm to nm.

    Used only for baseline publication figures.
    """

    if series is None:
        return None

    converted = []

    for curve in series:

        curve = curve.copy()

        curve["x"] = [
            value * 1000.0
            for value in curve["x"]
        ]

        converted.append(
            curve,
        )

    return converted


def _export_metric_figures(
    analysis_type: AnalysisType,
    summary,
    output_name: str,
    metric_column: str,
    title: str,
    ylabel: str,
    legend_title: str,
    xlabel: str,
    x_column: str,
    suffix: str = "",
) -> None:
    """
    Export every report figure associated with a single metric.
    """

    reference_series = _build_reference_series(
        analysis_type,
        output_name,
        summary,
    )

    summary_series = build_summary_series(
        summary,
        x_column=x_column,
        y_column=metric_column,
    )

    if analysis_type == AnalysisType.BASELINE:
        summary_series = _convert_series_x_to_nm(
            summary_series,
        )

        reference_series = _convert_series_x_to_nm(
            reference_series,
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    save_figure(
        series=summary_series,
        reference_series=reference_series,
        output_file=get_report_figure_path(
            analysis_type,
            f"{output_name}{suffix}",
            "summary",
        ),
        xlabel=xlabel,
        ylabel=ylabel,
        title=f"Summary of {title}",
    )

    # =========================================================
    # BASELINE
    # =========================================================

    if analysis_type == AnalysisType.BASELINE:
        field_series = build_field_series(
            summary,
            x_column=x_column,
            y_column=metric_column,
        )

        field_series = _convert_series_x_to_nm(
            field_series,
        )

        save_figure(
            series=field_series,
            reference_series=reference_series,
            output_file=get_report_figure_path(
                analysis_type,
                f"{output_name}{suffix}",
                "field",
            ),
            xlabel=xlabel,
            ylabel=ylabel,
            title=f"{title} Across Wavelength",
            legend_title=legend_title,
        )

        return

    # =========================================================
    # THERMAL / MONTE CARLO
    # =========================================================

    engineering_reference_series = None

    if analysis_type != AnalysisType.BASELINE:
        engineering_reference_series = (
            get_engineering_reference_series(
                output_name,
                summary[x_column],
            )
        )

    # ---------------------------------------------------------
    # Field Averaged
    # ---------------------------------------------------------

    for aggregation in (
        "mean",
        "min",
        "std",
        "max",
    ):

        save_figure(
            series=build_field_series(
                summary,
                x_column=x_column,
                y_column=metric_column,
                statistic=aggregation,
            ),
            reference_series=None,
            output_file=get_report_figure_path(
                analysis_type,
                f"{output_name}{suffix}",
                "field_averaged",
                aggregation,
            ),
            xlabel=xlabel,
            ylabel=ylabel,
            title=(
                f"{title}\n"
                f"({aggregation.title()} Across All Wavelengths)"
            ),
            legend_title=legend_title,
        )

    # ---------------------------------------------------------
    # Wavelength Averaged
    # ---------------------------------------------------------

    for aggregation in (
        "mean",
        "min",
        "std",
        "max",
    ):

        save_figure(
            series=build_wavelength_series(
                summary,
                x_column=x_column,
                y_column=metric_column,
                statistic=aggregation,
            ),
            reference_series=(
                None
                if aggregation == "std"
                else engineering_reference_series
            ),
            output_file=get_report_figure_path(
                analysis_type,
                f"{output_name}{suffix}",
                "wavelength_averaged",
                aggregation,
            ),
            xlabel=xlabel,
            ylabel=ylabel,
            title=(
                f"{title}\n"
                f"({aggregation.title()} Across All Field Positions)"
            ),
            legend_title="Wavelength",
        )

    # ---------------------------------------------------------
    # Engineering Validation
    # ---------------------------------------------------------

    engineering_series = (
        build_engineering_summary_series(
            summary,
            wavelength_um=ENGINEERING_WAVELENGTH_UM,
            x_column=x_column,
            y_column=metric_column,
        )
    )

    if not engineering_series:
        return

    engineering_reference_series = (
        get_engineering_reference_series(
            output_name,
            engineering_series[0]["x"],
        )
    )

    save_figure(
        series=engineering_series,
        reference_series=engineering_reference_series,
        output_file=get_report_figure_path(
            analysis_type,
            f"{output_name}{suffix}",
            "engineering",
        ),
        xlabel=xlabel,
        ylabel=ylabel,
        title=(
            f"{title}\n"
            f"(Engineering Validation at "
            f"{ENGINEERING_WAVELENGTH_UM * 1000:.0f} nm)"
        ),
        legend_title="Statistics",
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def export_report_figures(
    analysis_type: AnalysisType,
    summary,
) -> None:
    """
    Export every publication-quality report figure.
    """

    x_column = _get_x_column(
        analysis_type,
    )

    xlabel = _get_x_label(
        analysis_type,
    )

    # -------------------------------------------------------------
    # Thermal analyses are exported separately for every dataset.
    # -------------------------------------------------------------

    if analysis_type == AnalysisType.THERMAL:

        datasets = sorted(
            summary["Dataset"].unique()
        )

    else:

        datasets = [None]

    # -------------------------------------------------------------
    # Export figures.
    # -------------------------------------------------------------

    for dataset in datasets:

        if dataset is None:

            plot_summary = summary

            suffix = ""

        else:

            plot_summary = (
                summary[
                    summary["Dataset"] == dataset
                ]
                .copy()
            )

            suffix = (
                "_"
                + dataset.lower()
            )

        for output_name, metadata in REPORT_FIGURES.items():
            _export_metric_figures(
                analysis_type=analysis_type,
                summary=plot_summary,
                output_name=output_name,
                metric_column=metadata["column"],
                title=metadata["title"],
                ylabel=metadata["ylabel"],
                legend_title=metadata["legend"],
                xlabel=xlabel,
                x_column=x_column,
                suffix=suffix,
            )