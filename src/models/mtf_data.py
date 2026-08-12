"""
mtf_data.py

Data model representing the information extracted from a Zemax
FFT MTF text report.

Purpose
-------
This class is the structured output produced by the MTF parser.

It stores only the information that is explicitly present in the
Zemax report. No optical analysis or derived calculations are
performed here.

Design Philosophy
-----------------
Parser
    ↓
MTFData
    ↓
Metrics Module
    ↓
OpticalCase

Keeping the parsed data separate from derived metrics makes the
pipeline easier to maintain, test, and extend.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass


# ---------------------------------------------------------------------
# MTF Data Model
# ---------------------------------------------------------------------

@dataclass(slots=True)
class MTFData:
    """
    Represents the raw information extracted from a Zemax FFT MTF report.

    Notes
    -----
    This object intentionally stores only the quantities directly
    available in the Zemax export.

    The parser extracts the MTF values at the configured analysis
    spatial frequencies.

    It does NOT compute any derived quantities or statistics.

    Those are computed later by the metrics module.
    """

    # -------------------------------------------------------------
    # Optical Metadata
    # -------------------------------------------------------------

    wavelength_um: float
    """
    Wavelength used for the MTF analysis.

    Units
    -----
    Micrometers (µm)

    Example
    -------
    0.2000
    """

    field_x_deg: float
    """
    X field coordinate.

    Units
    -----
    Degrees
    """

    field_y_deg: float
    """
    Y field coordinate.

    Units
    -----
    Degrees
    """

    # -------------------------------------------------------------
    # MTF @ 17.2 lp/mm
    # -------------------------------------------------------------

    tangential_17_2: float
    """
    Tangential MTF at 17.2 lp/mm.
    """

    sagittal_17_2: float
    """
    Sagittal MTF at 17.2 lp/mm.
    """

    # -------------------------------------------------------------
    # MTF @ 41.7 lp/mm
    # -------------------------------------------------------------

    tangential_41_7: float
    """
    Tangential MTF at 41.7 lp/mm.
    """

    sagittal_41_7: float
    """
    Sagittal MTF at 41.7 lp/mm.
    """