"""
Tolerance analysis model.

This module defines engineering quantities derived from a parsed Zemax
tolerance study. The analysis aggregates sensitivity statistics, component
contributions, Monte Carlo yield estimates and histogram data for export and
visualization.

The class intentionally contains only derived quantities. The original parsed
report remains available through ``ToleranceStudy``.
"""

from dataclasses import dataclass

from src.models.sensitivity_result import SensitivityResult


@dataclass(slots=True)
class ToleranceAnalysis:
    """
    Derived engineering analysis of a tolerance study.

    Attributes
    ----------
    strongest_positive
        Tolerance producing the largest increase in the selected performance
        criterion.

    strongest_negative
        Tolerance producing the largest decrease in the selected performance
        criterion.

    absolute_ranking
        Sensitivity results ranked by absolute change in the performance
        criterion.

    component_contributions
        Total absolute contribution of each optical component to the overall
        performance degradation.

    rss_degradation
        Percentage degradation predicted by the RSS estimate.

    monte_carlo_yield
        Estimated manufacturing yield for the selected acceptance criterion.

    histogram_bins
        Histogram bin edges used for Monte Carlo visualization.

    histogram_counts
        Number of Monte Carlo samples in each histogram bin.
    """

    strongest_positive: SensitivityResult

    strongest_negative: SensitivityResult

    absolute_ranking: list[SensitivityResult]

    component_contributions: dict[str, float]

    rss_degradation: float

    monte_carlo_yield: float

    histogram_bins: list[float]

    histogram_counts: list[int]