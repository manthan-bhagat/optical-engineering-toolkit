"""
wavefront.py

Processing pipeline for Zemax Wavefront Map analysis.

Purpose
-------
This module executes the complete Wavefront workflow for a single
OpticalCase.

Pipeline
--------
Wavefront Report
        │
        ▼
Wavefront Parser
        │
        ▼
WavefrontData
        │
        ▼
Wavefront Analysis
        │
        ▼
WavefrontAnalysis
        │
        ▼
OpticalCase

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.analysis.wavefront import analyze_wavefront

from src.config import WAVEFRONT_REPORT

from src.models.optical_case import OpticalCase

from src.parsers.wavefront import WavefrontParser

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def process_wavefront(
    optical_case: OpticalCase,
) -> None:
    """
    Execute the complete Wavefront processing pipeline for one optical
    case.

    Parameters
    ----------
    optical_case
        Optical case to process.

    Notes
    -----
    If the case does not contain a Wavefront Map report, this function
    simply returns without modification.
    """

    wavefront_file = (
        optical_case.case_directory
        / WAVEFRONT_REPORT
    )

    if not wavefront_file.exists():
        return

    # -------------------------------------------------------------
    # Parse Zemax Wavefront Map report.
    # -------------------------------------------------------------

    wavefront_data = WavefrontParser(
        wavefront_file
    ).parse()

    # -------------------------------------------------------------
    # Analyze parsed wavefront.
    # -------------------------------------------------------------

    wavefront_analysis = analyze_wavefront(
        wavefront_data
    )

    # -------------------------------------------------------------
    # Store results.
    # -------------------------------------------------------------

    optical_case.wavefront_data = wavefront_data

    optical_case.wavefront_analysis = wavefront_analysis