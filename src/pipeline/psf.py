"""
psf.py

Processing pipeline for Zemax Point Spread Function (PSF) analysis.

Purpose
-------
This module executes the complete PSF workflow for a single
OpticalCase.

Pipeline
--------
PSF Report
      │
      ▼
PSF Parser
      │
      ▼
PSFData
      │
      ▼
PSF Analysis
      │
      ▼
PSFAnalysis
      │
      ▼
OpticalCase

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.analysis.psf import analyze_psf

from src.config import PSF_REPORT

from src.models.optical_case import OpticalCase

from src.parsers.psf import PSFParser

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def process_psf(
    optical_case: OpticalCase,
) -> None:
    """
    Execute the complete PSF processing pipeline for one optical case.

    Parameters
    ----------
    optical_case
        Optical case to process.

    Notes
    -----
    If the case does not contain a PSF report, this function simply
    returns without modification.
    """

    psf_file = (
        optical_case.case_directory
        / PSF_REPORT
    )

    if not psf_file.exists():
        return

    # -------------------------------------------------------------
    # Parse Zemax PSF report.
    # -------------------------------------------------------------

    psf_data = PSFParser(
        psf_file
    ).parse()

    # -------------------------------------------------------------
    # Analyze parsed PSF.
    # -------------------------------------------------------------

    psf_analysis = analyze_psf(
        psf_data
    )

    # -------------------------------------------------------------
    # Store results.
    # -------------------------------------------------------------

    optical_case.psf_data = psf_data

    optical_case.psf_analysis = psf_analysis