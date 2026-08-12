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
from typing import Iterable

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.export.optical_csv import export_csv
from src.export.optical_excel import export_excel

from src.export.baseline_csv import (
    export_baseline_csv,
)

from src.export.baseline_excel import (
    export_baseline_excel,
)

from src.models.analysis_type import AnalysisType
from src.models.optical_case import OpticalCase

from src.plotting.monte_carlo import (
    generate_montecarlo_plots,
)

from src.plotting.thermal import (
    generate_thermal_plots,
)

from src.report.output import (
    generate_reports,
)

from src.plotting.baseline import (
    generate_baseline_plots,
)

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _get_baseline_cases(
    cases: Iterable[OpticalCase],
) -> list[OpticalCase]:
    """
    Return the baseline operating condition.

    The baseline corresponds to the reference thermal configuration
    (20 °C).
    """

    baseline_cases: list[OpticalCase] = []

    for optical_case in cases:

        if (
            optical_case.analysis_type != AnalysisType.THERMAL
            or optical_case.temperature_c is None
        ):
            continue

        if abs(
            optical_case.temperature_c - 20.0
        ) < 1e-6:

            baseline_cases.append(
                optical_case
            )

    return baseline_cases


def _group_thermal_cases(
    cases: Iterable[OpticalCase],
) -> dict[
    tuple[str, float],
    list[OpticalCase],
]:
    """
    Group thermal cases by

        Dataset
            └── Wavelength
    """

    grouped: dict[
        tuple[str, float],
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if (
            optical_case.analysis_type != AnalysisType.THERMAL
            or optical_case.dataset is None
            or optical_case.wavelength_um is None
        ):
            continue

        grouped[
            (
                optical_case.dataset,
                optical_case.wavelength_um,
            )
        ].append(
            optical_case
        )

    return grouped


def _group_montecarlo_cases(
    cases: Iterable[OpticalCase],
) -> dict[
    float,
    list[OpticalCase],
]:
    """
    Group Monte Carlo cases by wavelength.

    Representative trials remain within each group so they can be
    plotted against one another.
    """

    grouped: dict[
        float,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if (
            optical_case.analysis_type != AnalysisType.MONTE_CARLO
            or optical_case.wavelength_um is None
        ):
            continue

        grouped[
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
    """

    # -------------------------------------------------------------
    # Thermal
    # -------------------------------------------------------------

    thermal_groups = _group_thermal_cases(
        cases
    )

    for thermal_cases in thermal_groups.values():
        export_csv(
            thermal_cases,
        )

        export_excel(
            thermal_cases,
        )

        generate_thermal_plots(
            thermal_cases,
        )

        #
        # Reports require every thermal CSV to exist before the
        # canonical summary can be constructed.
        #
        if thermal_groups:
            generate_reports(
                AnalysisType.THERMAL,
            )

    # -------------------------------------------------------------
    # Baseline
    # -------------------------------------------------------------

    baseline_cases = _get_baseline_cases(
        cases
    )

    if baseline_cases:
        export_baseline_csv(
            baseline_cases,
        )

        export_baseline_excel(
            baseline_cases,
        )

        generate_baseline_plots(
            baseline_cases,
        )

    # -------------------------------------------------------------
    # Monte Carlo
    # -------------------------------------------------------------

    montecarlo_groups = _group_montecarlo_cases(
        cases
    )

    for montecarlo_cases in montecarlo_groups.values():
        export_csv(
            montecarlo_cases,
        )

        export_excel(
            montecarlo_cases,
        )

        generate_montecarlo_plots(
            montecarlo_cases,
        )

        #
        # Reports require every Monte Carlo CSV to exist before the
        # canonical summary can be constructed.
        #
        if montecarlo_groups:
            generate_reports(
                AnalysisType.MONTE_CARLO,
            )