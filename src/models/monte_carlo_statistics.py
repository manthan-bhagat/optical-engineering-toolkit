"""
Monte Carlo statistics model.

This module defines the statistical summary reported by the Zemax Monte Carlo
tolerance analysis.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MonteCarloStatistics:
    """
    Monte Carlo statistical summary.

    Attributes
    ----------
    trials
        Total number of Monte Carlo trials.

    distribution
        Initial probability distribution used for the tolerance analysis.

    nominal
        Nominal value of the selected performance criterion.

    best
        Best performance criterion obtained during the Monte Carlo analysis.

    best_trial
        Trial number corresponding to the best result.

    worst
        Worst performance criterion obtained during the Monte Carlo analysis.

    worst_trial
        Trial number corresponding to the worst result.

    mean
        Mean value of the performance criterion.

    standard_deviation
        Standard deviation of the performance criterion.
    """

    trials: int

    distribution: str

    nominal: float

    best: float

    best_trial: int

    worst: float

    worst_trial: int

    mean: float

    standard_deviation: float

    criterion_values: list[float]