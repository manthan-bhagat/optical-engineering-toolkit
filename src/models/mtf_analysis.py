"""
mtf_analysis.py

Data model representing the optical metrics derived from a Zemax
FFT Modulation Transfer Function (MTF) report.

Purpose
-------
This class stores the quantities computed from the raw MTF values
contained in an MTFData object.

Unlike MTFData, which contains only the values explicitly exported by
Zemax, this class stores derived optical performance metrics.

Design Philosophy
-----------------
Zemax Report
      ↓
 MTFParser
      ↓
  MTFData
      ↓
 MTF Analysis
      ↓
 MTFAnalysis
      ↓
 OpticalCase

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass


# ---------------------------------------------------------------------
# MTF Analysis Model
# ---------------------------------------------------------------------

@dataclass(slots=True)
class MTFAnalysis:
    """
    Represents the optical performance metrics derived from an MTF
    measurement.

    Notes
    -----
    This class stores only quantities computed during MTF analysis.

    The raw MTF values remain in MTFData.
    """

    # -------------------------------------------------------------
    # Mean MTF @ 17.2 lp/mm
    # -------------------------------------------------------------

    mean_17_2: float
    """
    Mean MTF at 17.2 lp/mm.

    Defined as the arithmetic mean of the tangential and sagittal MTF.
    """

    # -------------------------------------------------------------
    # Mean MTF @ 41.7 lp/mm
    # -------------------------------------------------------------

    mean_41_7: float
    """
    Mean MTF at 41.7 lp/mm.

    Defined as the arithmetic mean of the tangential and sagittal MTF.
    """