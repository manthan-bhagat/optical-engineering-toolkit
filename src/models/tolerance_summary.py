"""
Tolerance study summary model.

This module defines the metadata and configuration describing a Zemax
tolerance analysis. It corresponds to the study summary section located near
the beginning of the tolerance report.

The class contains only descriptive information about how the tolerance study
was performed. It does not include any analysis results.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ToleranceSummary:
    """
    General information describing a tolerance study.

    Attributes
    ----------
    lens_file
        Path to the Zemax lens file used for the analysis.

    title
        Lens title recorded in the Zemax report.

    date
        Date on which the tolerance analysis was performed.

    units
        Linear units used throughout the report.

    criterion
        Performance criterion evaluated during tolerance analysis.

    mode
        Zemax tolerance analysis mode.

    sampling
        Sampling density used during ray tracing.

    optimization_cycles
        Optimization cycle setting used for compensator optimization.

    nominal_criterion
        Nominal value of the selected performance criterion.

    test_wavelength
        Wavelength used during tolerance analysis, in micrometers.

    compensator
        Human-readable description of the optimization compensator.

    compensator_min
        Minimum allowable compensator value.

    compensator_max
        Maximum allowable compensator value.
    """

    lens_file: str

    title: str

    date: str

    units: str

    criterion: str

    mode: str

    sampling: int

    optimization_cycles: str

    nominal_criterion: float

    test_wavelength: float

    compensator: str

    compensator_min: float

    compensator_max: float