"""
baseline.py

Baseline case collector.

Purpose
-------
Discovers baseline optical analysis operating points and constructs
one OpticalCase per configuration, wavelength, and field.

Directory Layout
----------------

baseline/
    configuration_1.000000/
        0.400000/
            spot.txt
            field_1.000000/
                psf.txt
                mtf.txt
                wavefront.txt
            field_2.000000/
            ...

    configuration_2.000000/
        ...
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    BASELINE_CASE_PREFIX,
    SPOT_REPORT,
)

from src.models.analysis_type import AnalysisType
from src.models.optical_case import OpticalCase


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def load_baseline_cases(
    baseline_directory: Path,
) -> list[OpticalCase]:
    """
    Load every baseline OpticalCase.

    One OpticalCase is created for every unique combination of

        Configuration
        Wavelength
        Field
    """

    cases: list[OpticalCase] = []

    # -------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------

    configuration_directories = sorted(
        (
            path
            for path in baseline_directory.iterdir()
            if path.is_dir()
            and path.name.lower().startswith(
                "configuration_"
            )
        ),
        key=lambda path: int(
            float(
                path.name
                .lower()
                .removeprefix(
                    "configuration_"
                )
            )
        ),
    )

    for configuration_directory in (
        configuration_directories
    ):

        configuration = int(
            float(
                configuration_directory.name
                .lower()
                .removeprefix(
                    "configuration_"
                )
            )
        )

        # ---------------------------------------------------------
        # Wavelength
        # ---------------------------------------------------------

        wavelength_directories = sorted(
            (
                path
                for path in configuration_directory.iterdir()
                if path.is_dir()
            ),
            key=lambda path: float(
                path.name
            ),
        )

        for wavelength_directory in (
            wavelength_directories
        ):

            wavelength = float(
                wavelength_directory.name
            )

            #
            # Support either nanometre or micrometre
            # directory names.
            #
            # Examples:
            #
            # 200
            # 400
            #
            # or
            #
            # 0.200000
            # 0.400000
            #
            if wavelength >= 10:
                wavelength /= 1000.0

            wavelength_um = wavelength

            # -----------------------------------------------------
            # Shared Spot Diagram
            # -----------------------------------------------------

            spot_file = (
                wavelength_directory
                / SPOT_REPORT
            )

            # -----------------------------------------------------
            # Fields
            # -----------------------------------------------------

            field_directories = sorted(
                (
                    path
                    for path in wavelength_directory.iterdir()
                    if path.is_dir()
                    and path.name
                    .lower()
                    .startswith(
                        "field_"
                    )
                ),
                key=lambda path: int(
                    float(
                        path.name
                        .lower()
                        .removeprefix(
                            "field_"
                        )
                    )
                ),
            )

            for field_directory in (
                field_directories
            ):

                field_index = int(
                    float(
                        field_directory.name
                        .lower()
                        .removeprefix(
                            "field_"
                        )
                    )
                )

                # -------------------------------------------------
                # Construct Optical Case
                # -------------------------------------------------

                cases.append(

                    OpticalCase(

                        # -----------------------------------------
                        # Identity
                        # -----------------------------------------

                        case_id=(
                            f"{BASELINE_CASE_PREFIX}"
                            f"_C{configuration:02d}"
                            f"_W{wavelength_um * 1000:.0f}"
                            f"_F{field_index:02d}"
                        ),

                        name=(
                            f"Baseline | "
                            f"Configuration {configuration} | "
                            f"{wavelength_um:.6f} µm | "
                            f"Field {field_index}"
                        ),

                        analysis_type=(
                            AnalysisType.BASELINE
                        ),

                        # -----------------------------------------
                        # File Locations
                        # -----------------------------------------

                        case_directory=(
                            field_directory
                        ),

                        spot_file=(
                            spot_file
                            if spot_file.exists()
                            else None
                        ),

                        # -----------------------------------------
                        # Dataset Metadata
                        # -----------------------------------------

                        dataset="baseline",

                        configuration=configuration,

                        wavelength_um=wavelength_um,

                        field_index=field_index,
                    )
                )

    return cases