"""
Compensator statistics model.

This module defines the statistical summary for a Zemax compensator produced
during Monte Carlo tolerance analysis.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CompensatorStatistics:
    """
    Statistical summary of a tolerance compensator.

    Attributes
    ----------
    name
        Human-readable compensator name reported by Zemax
        (e.g. "Thickness Surf 10").

    nominal
        Nominal compensator value.

    minimum
        Minimum compensator value observed during Monte Carlo analysis.

    maximum
        Maximum compensator value observed during Monte Carlo analysis.

    mean
        Mean compensator value.

    standard_deviation
        Standard deviation of the compensator value.
    """

    name: str

    nominal: float

    minimum: float

    maximum: float

    mean: float

    standard_deviation: float