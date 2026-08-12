"""
Root-sum-square (RSS) performance estimate model.

This module defines the RSS performance estimate reported by the Zemax
tolerance analysis. The estimate predicts the expected degradation of the
selected performance criterion due to the combined effect of all specified
tolerances.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RSSEstimate:
    """
    Root-sum-square (RSS) performance estimate.

    Attributes
    ----------
    nominal
        Nominal value of the selected performance criterion.

    estimated_change
        Estimated change in the performance criterion obtained using the
        root-sum-square method.

    estimated_value
        Estimated performance criterion after applying the RSS estimate.
    """

    nominal: float

    estimated_change: float

    estimated_value: float