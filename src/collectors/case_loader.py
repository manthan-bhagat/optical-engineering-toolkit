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

from src.config import (
    THERMAL_CASE_PREFIX,
    MONTE_CARLO_CASE_PREFIX,
)

from src.models.analysis_type import AnalysisType
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

    input_directory = Path(input_directory)

    if not input_directory.exists():
        raise FileNotFoundError(
            f"Input directory does not exist: {input_directory}"
        )

    cases: list[OpticalCase] = []

    # -------------------------------------------------------------
    # Thermal Analyses
    # -------------------------------------------------------------

    thermal_directory = (
        input_directory /
        "thermal"
    )

    if thermal_directory.exists():

        cases.extend(
            _load_thermal_cases(
                thermal_directory
            )
        )

    # -------------------------------------------------------------
    # Monte Carlo Analyses
    # -------------------------------------------------------------

    montecarlo_directory = (
        input_directory /
        "montecarlo"
    )

    if montecarlo_directory.exists():

        cases.extend(
            _load_montecarlo_cases(
                montecarlo_directory
            )
        )

    # -------------------------------------------------------------
    # Future Analyses
    # -------------------------------------------------------------

    tolerance_directory = (
        input_directory /
        "tolerance"
    )

    #
    # Future implementation
    #
    # if tolerance_directory.exists():
    #
    #     cases.extend(
    #         _load_tolerance_cases(
    #             tolerance_directory
    #         )
    #     )

    return cases

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _create_case(
    *,
    case_id: str,
    name: str,
    analysis_type: AnalysisType,
    case_directory: Path,
    dataset: str | None = None,
    wavelength_um: float | None = None,
    field_index: int | None = None,
    temperature_c: float | None = None,
    statistical_case: int | str | None = None,
) -> OpticalCase:
    """
    Construct an OpticalCase from discovered metadata.
    """

    return OpticalCase(
        case_id=case_id,
        name=name,
        analysis_type=analysis_type,
        case_directory=case_directory,
        dataset=dataset,
        wavelength_um=wavelength_um,
        field_index=field_index,
        temperature_c=temperature_c,
        statistical_case=statistical_case,
    )

# ---------------------------------------------------------------------
# Thermal
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Thermal
# ---------------------------------------------------------------------


def _load_thermal_cases(
    directory: Path,
) -> list[OpticalCase]:
    """
    Load thermal analysis cases.

    Expected directory layout

    thermal/
        dataset/
            wavelength/
                temperature/
                    field_x.xxxxxx/
                        psf.txt
                        mtf.txt
                        wavefront.txt
    """

    cases: list[OpticalCase] = []

    for dataset_directory in sorted(directory.iterdir()):

        if not dataset_directory.is_dir():
            continue

        cases.extend(

            _load_thermal_dataset(

                dataset_directory,

                dataset=dataset_directory.name,
            )
        )

    return cases


def _load_thermal_dataset(
    directory: Path,
    *,
    dataset: str,
) -> list[OpticalCase]:
    """
    Load all thermal cases contained within a single thermal dataset.

    Expected directory layout

    dataset/
        wavelength/
            temperature/
                field_x.xxxxxx/
                    psf.txt
                    mtf.txt
                    wavefront.txt
    """

    cases: list[OpticalCase] = []

    for wavelength_directory in sorted(directory.iterdir()):

        if not wavelength_directory.is_dir():
            continue

        wavelength = float(
            wavelength_directory.name
        )

        #
        # Input folders are named in nm.
        # Convert to µm for internal storage.
        #
        if wavelength >= 10:
            wavelength /= 1000.0

        wavelength_um = wavelength

        # ---------------------------------------------------------
        # Temperature
        # ---------------------------------------------------------

        for temperature_directory in sorted(
            wavelength_directory.iterdir()
        ):

            if not temperature_directory.is_dir():
                continue

            temperature = float(
                temperature_directory.name
            )

            # -----------------------------------------------------
            # Field
            # -----------------------------------------------------

            for field_directory in sorted(
                temperature_directory.iterdir()
            ):

                if not field_directory.is_dir():
                    continue

                field_name = field_directory.name

                if not field_name.lower().startswith("field_"):
                    continue

                #
                # Supports
                #
                # field_1
                # field_1.0
                # field_1.000000
                #
                field_index = int(
                    float(
                        field_name.removeprefix("field_")
                    )
                )

                cases.append(

                    _create_case(

                        case_id=(
                            f"{THERMAL_CASE_PREFIX}"
                            f"_{dataset.upper()}"
                            f"_W{wavelength_um * 1000:.0f}"
                            f"_F{field_index:02d}"
                            f"_T{temperature:+.0f}"
                        ),

                        name=(
                            f"{dataset.capitalize()} | "
                            f"{wavelength_um:.3f} µm | "
                            f"Field {field_index} | "
                            f"{temperature:+.0f} °C"
                        ),

                        analysis_type=AnalysisType.THERMAL,

                        case_directory=field_directory,

                        dataset=dataset,

                        wavelength_um=wavelength_um,

                        field_index=field_index,

                        temperature_c=temperature,
                    )
                )

    return cases


# ---------------------------------------------------------------------
# Monte Carlo
# ---------------------------------------------------------------------


def _load_montecarlo_cases(
    directory: Path,
) -> list[OpticalCase]:
    """
    Load Monte Carlo analysis cases.

    Current directory layout

    montecarlo/
        MC_001/
        MC_002/
        ...
    """

    cases: list[OpticalCase] = []

    for index, case_directory in enumerate(
        sorted(directory.iterdir()),
        start=1,
    ):

        if not case_directory.is_dir():
            continue

        cases.append(

            _create_case(

                case_id=(
                    f"{MONTE_CARLO_CASE_PREFIX}_"
                    f"{index:03d}"
                ),

                name=f"Monte Carlo {index}",

                analysis_type=AnalysisType.MONTE_CARLO,

                case_directory=case_directory,

                statistical_case=index,
            )
        )

    return cases