"""
output.py

Output generation pipeline.

Purpose
-------
Coordinates the generation of all exported artifacts produced by the
Zemax Optical Analysis Toolkit.

Responsibilities
----------------
For each analysis type, dataset (when applicable), and wavelength:

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
    tuple[
        AnalysisType,
        str | None,
        float,
    ],
    list[OpticalCase],
]:
    """
    Group optical cases by

        Analysis Type
            └── Dataset
                    └── Wavelength
    """

    grouped: dict[
        tuple[
            AnalysisType,
            str | None,
            float,
        ],
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if (
            optical_case.analysis_type is None
            or optical_case.wavelength_um is None
        ):
            continue

        grouped[
            (
                optical_case.analysis_type,
                optical_case.dataset,
                optical_case.wavelength_um,
            )
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

    Group by Dataset
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
        (
            analysis_type,
            _dataset,
            _wavelength_um,
        ),
        grouped_cases_list,
    ) in grouped_cases.items():

        export_csv(
            grouped_cases_list,
        )

        export_excel(
            grouped_cases_list,
        )

        plot_generator = PLOT_GENERATORS.get(
            analysis_type
        )

        if plot_generator is not None:

            plot_generator(
                grouped_cases_list,
            )