"""
Tolerance export row builders.

This module converts tolerance study models into dictionaries suitable for
CSV and Excel export.

Each function is responsible for one logical table contained within the Zemax
tolerance report.
"""

from __future__ import annotations

from src.models.compensator_statistics import CompensatorStatistics
from src.models.monte_carlo_statistics import MonteCarloStatistics
from src.models.percentile import Percentile
from src.models.rss_estimate import RSSEstimate
from src.models.sensitivity_result import SensitivityResult
from src.models.tolerance_field import ToleranceField
from src.models.tolerance_summary import ToleranceSummary
from src.models.worst_offender import WorstOffender


MM_TO_UM = 1000.0


def _um(value: float) -> float:
    """
    Convert millimetres to microns.
    """

    return value * MM_TO_UM


def build_summary_row(
    summary: ToleranceSummary,
) -> dict[str, object]:
    """
    Build the summary export row.
    """

    return {
        "Criterion": summary.criterion,
        "Mode": summary.mode,
        "Sampling": summary.sampling,
        "Optimization Cycles": summary.optimization_cycles,
        "Nominal Criterion (µm)": _um(summary.nominal_criterion),
        "Test Wavelength": summary.test_wavelength,
        "Units": "µm",
    }


def build_field_row(
    field: ToleranceField,
) -> dict[str, object]:
    """
    Build one field definition row.
    """

    return {
        "Field": field.index,
        "X Field": field.x_field,
        "Y Field": field.y_field,
        "Weight": field.weight,
        "VDX": field.vdx,
        "VDY": field.vdy,
        "VCX": field.vcx,
        "VCY": field.vcy,
    }


def build_sensitivity_row(
    result: SensitivityResult,
) -> dict[str, object]:
    """
    Build one sensitivity analysis row.
    """

    return {
        "Component": result.component,
        "Description": result.description,
        "Mnemonic": result.mnemonic,
        "Surface": result.surface,
        "Minimum Value (µm)": _um(result.minimum_value),
        "Minimum Criterion (µm)": _um(result.minimum_criterion),
        "Minimum Change (µm)": _um(result.minimum_change),
        "Maximum Value (µm)": _um(result.maximum_value),
        "Maximum Criterion (µm)": _um(result.maximum_criterion),
        "Maximum Change (µm)": _um(result.maximum_change),
    }


def build_worst_offender_row(
    offender: WorstOffender,
) -> dict[str, object]:
    """
    Build one worst offender row.
    """

    return {
        "Rank": offender.rank,
        "Mnemonic": offender.mnemonic,
        "Surface": offender.surface,
        "Value (µm)": _um(offender.value),
        "Criterion (µm)": _um(offender.criterion),
        "Change (µm)": _um(offender.change),
    }


def build_rss_row(
    rss: RSSEstimate,
) -> dict[str, object]:
    """
    Build the RSS estimate row.
    """

    return {
        "Nominal (µm)": _um(rss.nominal),
        "Estimated Change (µm)": _um(rss.estimated_change),
        "Estimated Value (µm)": _um(rss.estimated_value),
    }


def build_monte_carlo_row(
    statistics: MonteCarloStatistics,
) -> dict[str, object]:
    """
    Build the Monte Carlo summary row.
    """

    return {
        "Trials": statistics.trials,
        "Distribution": statistics.distribution,
        "Nominal (µm)": _um(statistics.nominal),
        "Best (µm)": _um(statistics.best),
        "Best Trial": statistics.best_trial,
        "Worst (µm)": _um(statistics.worst),
        "Worst Trial": statistics.worst_trial,
        "Mean (µm)": _um(statistics.mean),
        "Standard Deviation (µm)": _um(statistics.standard_deviation),
    }


def build_compensator_row(
    compensator: CompensatorStatistics,
) -> dict[str, object]:
    """
    Build one compensator statistics row.
    """

    return {
        "Name": compensator.name,
        "Nominal (µm)": _um(compensator.nominal),
        "Minimum (µm)": _um(compensator.minimum),
        "Maximum (µm)": _um(compensator.maximum),
        "Mean (µm)": _um(compensator.mean),
        "Standard Deviation (µm)": _um(compensator.standard_deviation),
    }


def build_percentile_row(
    percentile: Percentile,
) -> dict[str, object]:
    """
    Build one percentile row.
    """

    return {
        "Percentile": percentile.percentage,
        "Criterion (µm)": _um(percentile.criterion),
    }