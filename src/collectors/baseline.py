"""
baseline.py

Baseline case collector.

Purpose
-------
Discovers the baseline optical analysis operating points and constructs
one OpticalCase per field.

The baseline analysis reuses the nominal thermal Zemax exports at the
reference temperature and evaluates baseline optical performance as a
function of wavelength.

Directory Layout
----------------

thermal/
    nominal/
        wavelength/
            temperature/
                spot.txt
                field_1.000000/
                    psf.txt
                    mtf.txt
                    wavefront.txt
                field_2.000000/
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
    BASELINE_TEMPERATURE_C,
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
    """

    cases: list[OpticalCase] = []

    # -------------------------------------------------------------
    # Wavelength
    # -------------------------------------------------------------

    for wavelength_directory in sorted(
        path
        for path in baseline_directory.iterdir()
        if path.is_dir()
    ):

        wavelength = float(
            wavelength_directory.name
        )

        #
        # Allow either 200 or 0.200 folder names.
        #
        if wavelength >= 10:
            wavelength /= 1000.0

        wavelength_um = wavelength

        # ---------------------------------------------------------
        # Temperature
        # ---------------------------------------------------------

        for temperature_directory in sorted(
            path
            for path in wavelength_directory.iterdir()
            if path.is_dir()
        ):

            temperature_c = float(
                temperature_directory.name
            )

            #
            # Baseline uses only the reference temperature.
            #
            if abs(
                temperature_c
                - BASELINE_TEMPERATURE_C
            ) > 1e-6:
                continue

            #
            # Shared Spot Diagram
            #
            spot_file = (
                temperature_directory
                / SPOT_REPORT
            )

            # -----------------------------------------------------
            # Fields
            # -----------------------------------------------------

            for field_directory in sorted(
                path
                for path in temperature_directory.iterdir()
                if path.is_dir()
            ):

                field_name = field_directory.name

                if not field_name.lower().startswith(
                    "field_"
                ):
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
                        field_name.removeprefix(
                            "field_"
                        )
                    )
                )

                cases.append(

                    OpticalCase(

                        case_id=(
                            f"{BASELINE_CASE_PREFIX}"
                            f"_W{wavelength_um * 1000:.0f}"
                            f"_F{field_index:02d}"
                        ),

                        name=(
                            f"Baseline | "
                            f"{wavelength_um:.3f} µm | "
                            f"Field {field_index}"
                        ),

                        analysis_type=AnalysisType.BASELINE,

                        case_directory=field_directory,

                        #
                        # Shared Spot Diagram
                        #
                        spot_file=(
                            spot_file
                            if spot_file.exists()
                            else None
                        ),

                        dataset="baseline",

                        wavelength_um=wavelength_um,

                        field_index=field_index,

                        temperature_c=temperature_c,
                    )
                )

    return cases