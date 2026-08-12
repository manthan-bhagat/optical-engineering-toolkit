"""
mtf_report.py

Container representing the complete contents of a Zemax FFT MTF
text report.

Purpose
-------
Unlike a Huygens PSF report, a single Zemax MTF report contains

    • one diffraction-limited reference
    • multiple optical field measurements

This class groups those parsed results into a single object that can
be passed through the remainder of the optical analysis pipeline.

Design Philosophy
-----------------
Zemax Report
      ↓
 MTFParser
      ↓
MTFParserResult
      ↓
 OpticalCase

The parser is responsible only for extracting the raw Zemax data.

No optical analysis or derived metrics are computed here.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.mtf_data import MTFData


# ---------------------------------------------------------------------
# MTF Report Model
# ---------------------------------------------------------------------

@dataclass(slots=True)
class MTFReport:
    """
    Represents the complete raw contents of a Zemax FFT MTF report.

    Notes
    -----
    A Zemax FFT MTF report contains one or more wavelength sections.

    Each wavelength section consists of

    - one diffraction-limited reference dataset
    - one optical field dataset

    The ordering of both lists is preserved exactly as reported by
    Zemax. The i-th diffraction dataset corresponds to the i-th field
    dataset and shares the same wavelength.

    All datasets are stored exactly as extracted from the Zemax export.
    No derived optical quantities are computed here.
    """

    diffraction: list[MTFData]
    """
    Diffraction-limited MTF datasets.

    One dataset is stored for each wavelength section contained in the
    Zemax report.

    The ordering matches the wavelength order reported by Zemax.
    """

    fields: list[MTFData]
    """
    Optical field MTF datasets.

    One dataset is stored for each wavelength section contained in the
    Zemax report.

    The i-th field dataset corresponds to the i-th diffraction dataset.
    """