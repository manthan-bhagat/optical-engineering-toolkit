"""
Worst offender model.

This module defines a single entry from the Zemax "Worst Offenders" section.
Each instance represents one ranked tolerance operand contributing to the
largest degradation of the selected performance criterion.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class WorstOffender:
    """
    Worst offender entry.

    Attributes
    ----------
    rank
        Rank within the worst offender table.

    mnemonic
        Zemax tolerance mnemonic (e.g. TRAD, TSTX, TSDY).

    surface
        Surface number associated with the tolerance.

    value
        Tolerance value evaluated.

    criterion
        Resulting value of the performance criterion.

    change
        Change in the performance criterion relative to the nominal design.
    """

    rank: int

    mnemonic: str

    surface: int

    value: float

    criterion: float

    change: float