"""
baseline.py

Baseline optical analysis pipeline.

Purpose
-------
Executes the complete baseline optical analysis workflow.

The baseline analysis reuses the nominal thermal Zemax exports at the
reference temperature and evaluates optical performance as a function of
wavelength.

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
        Baseline input directory containing the nominal thermal
        Zemax exports.
    """

    # -------------------------------------------------------------
    # Discover optical cases
    # -------------------------------------------------------------

    optical_cases = load_baseline_cases(
        Path(input_directory)
    )
    print(f"Loaded {len(optical_cases)} baseline cases")

    if not optical_cases:
        return

    # -------------------------------------------------------------
    # Process every optical case
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
    # Export
    # -------------------------------------------------------------

    export_baseline_csv(
        optical_cases,
    )

    export_baseline_excel(
        optical_cases,
    )

    # -------------------------------------------------------------
    # Plotting
    # -------------------------------------------------------------

    generate_baseline_plots(
        optical_cases,
    )