"""
baseline.py

Baseline optical analysis pipeline.

Purpose
-------
Executes the complete baseline optical analysis workflow.

The baseline analysis evaluates optical performance as a function of
wavelength for each Zemax configuration independently.

Pipeline
--------
Baseline Collector
        ↓
Spot Diagram
        ↓
PSF
        ↓
MTF
        ↓
Wavefront
        ↓
Group by Configuration
        ↓
CSV Export
        ↓
Excel Export
        ↓
Engineering Plots

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.collectors.baseline import (
    load_baseline_cases,
)

from src.pipeline.spot import (
    process_spot,
)

from src.pipeline.psf import (
    process_psf,
)

from src.pipeline.mtf import (
    process_mtf,
)

from src.pipeline.wavefront import (
    process_wavefront,
)

from src.export.baseline_csv import (
    export_baseline_csv,
)

from src.export.baseline_excel import (
    export_baseline_excel,
)

from src.plotting.baseline import (
    generate_baseline_plots,
)

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _group_by_configuration(
    cases,
) -> dict[int, list]:
    """
    Group baseline optical cases by Zemax configuration.

    Each configuration is processed and exported independently.
    """

    grouped = defaultdict(list)

    for optical_case in cases:

        if optical_case.configuration is None:
            raise ValueError(
                f"Baseline case '{optical_case.case_id}' "
                f"does not define a configuration."
            )

        grouped[
            optical_case.configuration
        ].append(
            optical_case
        )

    return dict(
        grouped
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def run_baseline_pipeline(
    input_directory: str | Path,
) -> None:
    """
    Execute the complete baseline optical analysis pipeline.

    Parameters
    ----------
    input_directory
        Baseline input directory containing the Zemax exports for all
        baseline configurations.
    """

    # -------------------------------------------------------------
    # Discover Optical Cases
    # -------------------------------------------------------------

    optical_cases = load_baseline_cases(
        Path(input_directory)
    )

    print(
        f"Loaded {len(optical_cases)} baseline cases"
    )

    if not optical_cases:
        return

    # -------------------------------------------------------------
    # Process Every Optical Case
    # -------------------------------------------------------------

    for optical_case in optical_cases:

        process_spot(
            optical_case,
        )

        process_psf(
            optical_case,
        )

        process_mtf(
            optical_case,
        )

        process_wavefront(
            optical_case,
        )

    # -------------------------------------------------------------
    # Group by Configuration
    # -------------------------------------------------------------

    cases_by_configuration = (
        _group_by_configuration(
            optical_cases,
        )
    )

    # -------------------------------------------------------------
    # Export and Plot Each Configuration
    # -------------------------------------------------------------

    for configuration in sorted(
        cases_by_configuration
    ):

        configuration_cases = (
            cases_by_configuration[
                configuration
            ]
        )

        print(
            f"Processing baseline configuration "
            f"{configuration} "
            f"({len(configuration_cases)} cases)"
        )

        # ---------------------------------------------------------
        # Export
        # ---------------------------------------------------------

        export_baseline_csv(
            configuration_cases,
            configuration,
        )

        export_baseline_excel(
            configuration_cases,
            configuration,
        )

        # ---------------------------------------------------------
        # Plotting
        # ---------------------------------------------------------

        generate_baseline_plots(
            configuration_cases,
            configuration,
        )