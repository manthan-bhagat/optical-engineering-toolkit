"""
mtf.py

Processing pipeline for Zemax Modulation Transfer Function (MTF)
analysis.

Purpose
-------
This module executes the complete MTF workflow for a single
OpticalCase.

Pipeline
--------
MTF Report
      │
      ▼
MTF Parser
      │
      ▼
MTFData
      │
      ▼
MTF Analysis
      │
      ▼
MTFAnalysis
      │
      ▼
OpticalCase

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.analysis.mtf import analyze_mtf

from src.config import MTF_REPORT

from src.models.optical_case import OpticalCase

from src.parsers.mtf import MTFParser

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def process_mtf(
    optical_case: OpticalCase,
) -> None:
    """
    Execute the complete MTF processing pipeline for one optical case.

    Parameters
    ----------
    optical_case
        Optical case to process.

    Notes
    -----
    If the case does not contain an MTF report, this function simply
    returns without modification.
    """

    mtf_file = (
        optical_case.case_directory
        / MTF_REPORT
    )

    if not mtf_file.exists():
        return

    # -------------------------------------------------------------
    # Parse Zemax MTF report.
    # -------------------------------------------------------------

    mtf_report = MTFParser(
        mtf_file
    ).parse()

    #
    # One OpticalCase corresponds to one wavelength and one field.
    #
    optical_case.mtf_diffraction = (
        mtf_report.diffraction[0]
    )

    optical_case.mtf_data = (
        mtf_report.fields[0]
    )

    # -------------------------------------------------------------
    # Analyze parsed MTF.
    # -------------------------------------------------------------

    mtf_analysis = analyze_mtf(
        optical_case.mtf_data
    )

    # -------------------------------------------------------------
    # Store results.
    # -------------------------------------------------------------

    optical_case.mtf_analysis = (
        mtf_analysis
    )