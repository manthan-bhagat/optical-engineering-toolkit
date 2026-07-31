"""
main.py

Entry point for the Zemax Optical Analysis Toolkit.

Pipeline
--------
Input Directory
        │
        ▼
Case Loader
        │
        ▼
Processing Pipelines
        │
        ├── PSF
        ├── MTF (future)
        ├── RMS Spot (future)
        └── Wavefront (future)
        │
        ▼
Completed Optical Cases
        │
        ▼
Output Generation
        │
        ├── CSV
        ├── Excel
        └── Engineering Plots

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.collectors.case_loader import load_cases

from src.config import INPUT_DIRECTORY

from src.pipeline.output import generate_outputs

from src.pipeline.psf import process_psf

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main() -> None:
    """
    Execute the complete optical analysis pipeline.
    """

    # -------------------------------------------------------------
    # Discover all optical analysis cases.
    # -------------------------------------------------------------

    cases = load_cases(
        INPUT_DIRECTORY
    )

    # -------------------------------------------------------------
    # Execute processing pipelines.
    # -------------------------------------------------------------

    for optical_case in cases:

        #
        # Point Spread Function
        #
        process_psf(
            optical_case
        )

        #
        # Future pipelines
        #
        # process_mtf(optical_case)
        # process_rms_spot(optical_case)
        # process_wavefront(optical_case)

    # -------------------------------------------------------------
    # Generate all outputs.
    # -------------------------------------------------------------

    generate_outputs(
        cases
    )

    print(
        "Analysis completed successfully."
    )


# ---------------------------------------------------------------------
# Script Entry Point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()