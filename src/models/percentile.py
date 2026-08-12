"""
Monte Carlo percentile model.

This module defines a single percentile reported by the Zemax Monte Carlo
tolerance analysis.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Percentile:
    """
    Monte Carlo percentile.

    Attributes
    ----------
    percentage
        Percentile level expressed as a percentage
        (e.g. 2, 10, 50, 90, 98).

    criterion
        Value of the performance criterion corresponding to the percentile.
    """

    percentage: int

    criterion: float