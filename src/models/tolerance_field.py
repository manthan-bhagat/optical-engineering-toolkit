"""
Tolerance field model.

This module defines a single field used during a Zemax tolerance analysis.
Each field corresponds to one row in the field definition table contained
within the tolerance report.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ToleranceField:
    """
    Field definition used during tolerance analysis.

    Attributes
    ----------
    index
        Sequential field number.

    x_field
        X field coordinate (degrees).

    y_field
        Y field coordinate (degrees).

    weight
        Relative field weight.

    vdx
        VDX value reported by Zemax.

    vdy
        VDY value reported by Zemax.

    vcx
        VCX value reported by Zemax.

    vcy
        VCY value reported by Zemax.
    """

    index: int

    x_field: float

    y_field: float

    weight: float

    vdx: float

    vdy: float

    vcx: float

    vcy: float