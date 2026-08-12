"""
thermal.py

Thermal case collector.

Purpose
-------
Discovers all thermal operating points contained within the input
directory and constructs one OpticalCase per field.

Unlike PSF, MTF, and Wavefront reports, the Spot Diagram is generated
once per temperature and therefore shared by every OpticalCase at that
operating point.

Directory Layout
----------------

thermal/
    dataset/
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
    SPOT_REPORT,
    THERMAL_CASE_PREFIX,
)

from src.models.analysis_type import AnalysisType
from src.models.optical_case import OpticalCase

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def load_thermal_cases(
    thermal_directory: Path,
) -> list[OpticalCase]:
    """
    Load every thermal OpticalCase.
    """

    cases: list[OpticalCase] = []

    # -------------------------------------------------------------
    # Dataset
    # -------------------------------------------------------------

    for dataset_directory in sorted(
        path
        for path in thermal_directory.iterdir()
        if path.is_dir()
    ):

        dataset = dataset_directory.name

        # ---------------------------------------------------------
        # Wavelength
        # ---------------------------------------------------------

        for wavelength_directory in sorted(
            path
            for path in dataset_directory.iterdir()
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

            # -----------------------------------------------------
            # Temperature
            # -----------------------------------------------------

            for temperature_directory in sorted(
                path
                for path in wavelength_directory.iterdir()
                if path.is_dir()
            ):

                temperature_c = float(
                    temperature_directory.name
                )

                #
                # Shared Spot Diagram
                #
                spot_file = (
                    temperature_directory
                    / SPOT_REPORT
                )

                # -------------------------------------------------
                # Fields
                # -------------------------------------------------

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
                                f"{THERMAL_CASE_PREFIX}"
                                f"_{dataset.upper()}"
                                f"_W{wavelength_um * 1000:.0f}"
                                f"_F{field_index:02d}"
                                f"_T{temperature_c:+.0f}"
                            ),

                            name=(
                                f"{dataset.capitalize()} | "
                                f"{wavelength_um:.3f} µm | "
                                f"Field {field_index} | "
                                f"{temperature_c:+.0f} °C"
                            ),

                            analysis_type=AnalysisType.THERMAL,

                            case_directory=field_directory,

                            #
                            # Shared Spot Diagram
                            #
                            spot_file=(
                                spot_file
                                if spot_file.exists()
                                else None
                            ),

                            dataset=dataset,

                            wavelength_um=wavelength_um,

                            field_index=field_index,

                            temperature_c=temperature_c,
                        )
                    )

    return cases