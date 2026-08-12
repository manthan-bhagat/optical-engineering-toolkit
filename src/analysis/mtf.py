"""
mtf.py

Analysis routines for Zemax FFT Modulation Transfer Function (MTF) data.

Purpose
-------
This module computes derived optical performance metrics from the raw
MTF values extracted from a Zemax FFT MTF report.

Unlike the parser, this module performs numerical analysis of the
parsed MTF data.

Computed Metrics
----------------
- Mean MTF @ 17.2 lp/mm
- Mean MTF @ 41.7 lp/mm

The tangential and sagittal MTF values are extracted directly from the
Zemax report by the parser.

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
# Third-Party Imports
# ---------------------------------------------------------------------

import numpy as np

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.mtf_analysis import MTFAnalysis
from src.models.mtf_data import MTFData

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def analyze_mtf(
    data: MTFData,
) -> MTFAnalysis:
    """
    Compute all derived optical metrics from parsed MTF data.

    Parameters
    ----------
    data
        Parsed MTF information.

    Returns
    -------
    MTFAnalysis
        Derived optical performance metrics.
    """

    mean_17_2 = _compute_mean_mtf(
        data.tangential_17_2,
        data.sagittal_17_2,
    )

    mean_41_7 = _compute_mean_mtf(
        data.tangential_41_7,
        data.sagittal_41_7,
    )

    return MTFAnalysis(
        mean_17_2=mean_17_2,
        mean_41_7=mean_41_7,
    )

# ---------------------------------------------------------------------
# Mean MTF
# ---------------------------------------------------------------------

def _compute_mean_mtf(
    tangential: float,
    sagittal: float,
) -> float:
    """
    Compute the mean modulation transfer function.

    Parameters
    ----------
    tangential
        Tangential MTF.

    sagittal
        Sagittal MTF.

    Returns
    -------
    float
        Mean MTF.

    Notes
    -----
    The mean MTF is defined as the arithmetic mean of the tangential
    and sagittal MTF values.

    If either value is undefined, NaN is returned.
    """

    if (
        np.isnan(tangential)
        or np.isnan(sagittal)
    ):
        return np.nan

    return float(
        (tangential + sagittal)
        / 2.0
    )