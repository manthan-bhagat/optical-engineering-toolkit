"""
Tolerance sensitivity result model.

This module defines the result of a single tolerance sensitivity evaluation.
Each instance corresponds to one row in the Zemax Sensitivity Analysis table.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SensitivityResult:
    """
    Sensitivity analysis result for a single tolerance operand.

    Attributes
    ----------
    component
        Optical component to which the tolerance belongs
        (e.g. Primary Mirror, Secondary Mirror).

    description
        Human-readable tolerance description reported by Zemax.

    mnemonic
        Zemax tolerance mnemonic (e.g. TRAD, TTHI, TSDX).

    surface
        Surface number associated with the tolerance.

    minimum_value
        Minimum tolerance value evaluated.

    minimum_criterion
        Criterion value obtained at the minimum tolerance.

    minimum_change
        Change in criterion relative to the nominal design.

    maximum_value
        Maximum tolerance value evaluated.

    maximum_criterion
        Criterion value obtained at the maximum tolerance.

    maximum_change
        Change in criterion relative to the nominal design.
    """

    component: str

    description: str

    mnemonic: str

    surface: int

    minimum_value: float

    minimum_criterion: float

    minimum_change: float

    maximum_value: float

    maximum_criterion: float

    maximum_change: float