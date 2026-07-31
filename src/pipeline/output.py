"""
output.py

Output generation pipeline.

Purpose
-------
Coordinates the generation of all exported artifacts produced by the
Zemax Optical Analysis Toolkit.

Responsibilities
----------------
For each analysis type and wavelength:

- Export CSV results
- Export Excel results
- Generate engineering plots

This module is responsible only for orchestration. It does not know the
directory structure or output filenames; those responsibilities belong
to export, plotting, and paths modules.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from collections import defaultdict
from typing import Callable, Iterable

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.export.csv import export_csv
from src.export.excel import export_excel

from src.models.analysis_type import AnalysisType
from src.models.optical_case import OpticalCase

from src.plotting.thermal import generate_thermal_plots

# ---------------------------------------------------------------------
# Plot Generator Registry
# ---------------------------------------------------------------------

PLOT_GENERATORS: dict[
    AnalysisType,
    Callable[[Iterable[OpticalCase]], None],
] = {
    AnalysisType.THERMAL: generate_thermal_plots,
}

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _group_cases(
    cases: Iterable[OpticalCase],
) -> dict[
    AnalysisType,
    dict[float, list[OpticalCase]],
]:
    """
    Group optical cases by

        Analysis Type
            └── Wavelength
    """

    grouped: dict[
        AnalysisType,
        dict[float, list[OpticalCase]],
    ] = defaultdict(
        lambda: defaultdict(list)
    )

    for optical_case in cases:

        if (
            optical_case.analysis_type is None
            or optical_case.wavelength_um is None
        ):
            continue

        grouped[
            optical_case.analysis_type
        ][
            optical_case.wavelength_um
        ].append(
            optical_case
        )

    return grouped


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_outputs(
    cases: Iterable[OpticalCase],
) -> None:
    """
    Generate every exported artifact.

    Workflow
    --------

    Cases
        ↓

    Group by Analysis Type
        ↓

    Group by Wavelength
        ↓

    CSV
    Excel
    Figures
    """

    grouped_cases = _group_cases(
        cases
    )

    for (
        analysis_type,
        wavelength_groups,
    ) in grouped_cases.items():

        plot_generator = PLOT_GENERATORS.get(
            analysis_type
        )

        for wavelength_cases in wavelength_groups.values():

            export_csv(
                wavelength_cases,
            )

            export_excel(
                wavelength_cases,
            )

            if plot_generator is not None:

                plot_generator(
                    wavelength_cases,
                )