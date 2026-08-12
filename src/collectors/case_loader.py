"""
case_loader.py

Discovery and loading of Zemax optical analysis cases.

Purpose
-------
This module scans the project input directory and creates an
OpticalCase object for every analysis case discovered.

Only case metadata is populated here.

No Zemax parsing or optical analysis is performed.

The returned OpticalCase objects are later populated by the individual
parsers and analysis modules.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.collectors.monte_carlo import (
    load_montecarlo_cases,
)

from src.collectors.thermal import (
    load_thermal_cases,
)

from src.models.optical_case import OpticalCase

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def load_cases(
    input_directory: str | Path,
) -> list[OpticalCase]:
    """
    Discover all optical analysis cases contained within an input
    directory.
    """

    input_directory = Path(
        input_directory
    )

    if not input_directory.exists():

        raise FileNotFoundError(
            f"Input directory does not exist: "
            f"{input_directory}"
        )

    cases: list[
        OpticalCase
    ] = []

    # -------------------------------------------------------------
    # Thermal Analyses
    # -------------------------------------------------------------

    thermal_directory = (
        input_directory
        / "thermal"
    )

    if thermal_directory.exists():

        cases.extend(
            load_thermal_cases(
                thermal_directory
            )
        )

    # -------------------------------------------------------------
    # Monte Carlo Analyses
    # -------------------------------------------------------------

    montecarlo_directory = (
        input_directory
        / "monte-carlo"
    )

    if montecarlo_directory.exists():

        cases.extend(
            load_montecarlo_cases(
                montecarlo_directory
            )
        )

    # -------------------------------------------------------------
    # Future Analyses
    # -------------------------------------------------------------

    #
    # tolerance_directory = (
    #     input_directory
    #     / "tolerance"
    # )
    #
    # if tolerance_directory.exists():
    #
    #     cases.extend(
    #         load_tolerance_cases(
    #             tolerance_directory
    #         )
    #     )

    return cases