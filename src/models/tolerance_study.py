"""
Tolerance study aggregate model.

This module defines the top-level container representing one complete Zemax
tolerance analysis report.

The parser constructs a single ``ToleranceStudy`` instance, which aggregates
all sections extracted from the report. Downstream analysis, export and
plotting modules operate exclusively on this object.

The class intentionally contains no parsing or analysis logic. It is a pure
data model.
"""

from dataclasses import dataclass

from src.models.compensator_statistics import CompensatorStatistics
from src.models.monte_carlo_statistics import MonteCarloStatistics
from src.models.percentile import Percentile
from src.models.rss_estimate import RSSEstimate
from src.models.sensitivity_result import SensitivityResult
from src.models.tolerance_field import ToleranceField
from src.models.tolerance_summary import ToleranceSummary
from src.models.worst_offender import WorstOffender


@dataclass(slots=True)
class ToleranceStudy:
    """
    Complete Zemax tolerance analysis study.

    A single instance represents one tolerance analysis report and aggregates
    every parsed section contained within it.

    Attributes
    ----------
    summary
        General study metadata and analysis settings.

    fields
        Field definitions used during the tolerance analysis.

    sensitivities
        Complete sensitivity analysis results.

    worst_offenders
        Ranked list of the most significant tolerance contributors.

    rss
        Root-sum-square performance estimate.

    monte_carlo
        Monte Carlo statistical summary.

    compensators
        Statistics for all optimization compensators.

    percentiles
        Monte Carlo percentile statistics.
    """

    summary: ToleranceSummary

    fields: list[ToleranceField]

    sensitivities: list[SensitivityResult]

    worst_offenders: list[WorstOffender]

    rss: RSSEstimate

    monte_carlo: MonteCarloStatistics

    compensators: list[CompensatorStatistics]

    percentiles: list[Percentile]