"""
tolerance.py

Tolerance analysis plotting.

Purpose
-------
Generate all engineering figures associated with a Zemax tolerance analysis.

This module contains no plotting implementation itself. Instead it converts
the parsed ToleranceStudy into generic statistical plots provided by
plotting.statistical.

All Zemax criterion values are converted from millimetres to microns before
plotting so that engineering figures are presented in the same units used
throughout the toolkit outputs.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from collections import defaultdict

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.tolerance_study import ToleranceStudy

from src.plotting.paths import (
    get_tolerance_figure_path,
)

from src.plotting.statistical import (
    plot_bar,
    plot_cdf,
    plot_histogram,
    plot_horizontal_bar,
)

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

MM_TO_UM = 1000.0


def _um(value: float) -> float:
    """
    Convert millimetres to microns.
    """

    return value * MM_TO_UM


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_plots(
    study: ToleranceStudy,
) -> None:
    """
    Generate every tolerance analysis figure.
    """

    plot_sensitivity_ranking(
        study,
    )

    plot_worst_offenders(
        study,
    )

    plot_monte_carlo_histogram(
        study,
    )

    plot_percentiles(
        study,
    )

    plot_component_contributions(
        study,
    )

    plot_monte_carlo_cdf(
        study,
    )


# ---------------------------------------------------------------------
# Sensitivity Ranking
# ---------------------------------------------------------------------


def plot_sensitivity_ranking(
    study: ToleranceStudy,
) -> None:
    """
    Plot sensitivity ranking.
    """

    results = sorted(
        study.sensitivities,
        key=lambda result: max(
            abs(result.minimum_change),
            abs(result.maximum_change),
        ),
        reverse=True,
    )

    labels = [
        f"{result.component} ({result.mnemonic}{result.surface})"
        for result in results
    ]

    values = [
        _um(
            max(
                abs(result.minimum_change),
                abs(result.maximum_change),
            )
        )
        for result in results
    ]

    plot_horizontal_bar(
        labels,
        values,
        xlabel="Absolute Criterion Change (µm)",
        ylabel="Tolerance Operand",
        title="Tolerance Sensitivity Ranking",
        output_file=get_tolerance_figure_path(
            "sensitivity_ranking.png",
        ),
    )


# ---------------------------------------------------------------------
# Worst Offenders
# ---------------------------------------------------------------------


def plot_worst_offenders(
    study: ToleranceStudy,
) -> None:
    """
    Plot worst offenders.
    """

    labels = [
        f"{offender.mnemonic}{offender.surface}"
        for offender in study.worst_offenders
    ]

    values = [
        _um(offender.change)
        for offender in study.worst_offenders
    ]

    plot_horizontal_bar(
        labels,
        values,
        xlabel="Criterion Change (µm)",
        ylabel="Tolerance Operand",
        title="Worst Tolerance Offenders",
        output_file=get_tolerance_figure_path(
            "worst_offenders.png",
        ),
    )


# ---------------------------------------------------------------------
# Monte Carlo Histogram
# ---------------------------------------------------------------------


def plot_monte_carlo_histogram(
    study: ToleranceStudy,
) -> None:
    """
    Plot Monte Carlo histogram.
    """

    plot_histogram(
        [_um(value) for value in study.monte_carlo.criterion_values],
        bins=40,
        xlabel="Criterion Value (µm)",
        ylabel="Number of Trials",
        title="Monte Carlo Criterion Distribution",
        output_file=get_tolerance_figure_path(
            "monte_carlo_histogram.png",
        ),
    )


# ---------------------------------------------------------------------
# Monte Carlo Cumulative Distribution
# ---------------------------------------------------------------------


def plot_monte_carlo_cdf(
    study: ToleranceStudy,
) -> None:
    """
    Plot Monte Carlo cumulative distribution.
    """

    plot_cdf(
        [_um(value) for value in study.monte_carlo.criterion_values],
        xlabel="Criterion Value (µm)",
        ylabel="Cumulative Probability",
        title="Monte Carlo Criterion Cumulative Distribution",
        output_file=get_tolerance_figure_path(
            "monte_carlo_cdf.png",
        ),
    )


# ---------------------------------------------------------------------
# Percentiles
# ---------------------------------------------------------------------


def plot_percentiles(
    study: ToleranceStudy,
) -> None:
    """
    Plot percentile statistics.
    """

    labels = [
        f"{percentile.percentage}%"
        for percentile in study.percentiles
    ]

    values = [
        _um(percentile.criterion)
        for percentile in study.percentiles
    ]

    plot_bar(
        labels,
        values,
        xlabel="Percentile",
        ylabel="Criterion Value (µm)",
        title="Monte Carlo Percentiles",
        output_file=get_tolerance_figure_path(
            "percentiles.png",
        ),
    )


# ---------------------------------------------------------------------
# Component Contributions
# ---------------------------------------------------------------------


def plot_component_contributions(
    study: ToleranceStudy,
) -> None:
    """
    Plot accumulated sensitivity contribution per optical component.
    """

    contributions = defaultdict(float)

    for result in study.sensitivities:

        contributions[result.component] += _um(
            max(
                abs(result.minimum_change),
                abs(result.maximum_change),
            )
        )

    ranking = sorted(
        contributions.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    labels = [
        component
        for component, _ in ranking
    ]

    values = [
        contribution
        for _, contribution in ranking
    ]

    plot_horizontal_bar(
        labels,
        values,
        xlabel="Total Criterion Change (µm)",
        ylabel="Optical Component",
        title="Component Contribution Ranking",
        output_file=get_tolerance_figure_path(
            "component_contributions.png",
        ),
    )