"""
wavefront_analysis.py

Derived optical metrics computed from a Zemax wavefront map.

Purpose
-------
This model stores wavefront metrics derived from the raw Zemax
Wavefront Map report.

Unlike WavefrontData, this model contains computed quantities rather
than raw parser output.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass

# ---------------------------------------------------------------------
# Wavefront Analysis
# ---------------------------------------------------------------------

@dataclass(slots=True)
class WavefrontAnalysis:

    peak_to_valley_waves: float
    """
    Peak-to-valley wavefront error.

    Units
    -----
    Waves
    """

    rms_waves: float
    """
    Root-mean-square wavefront error.

    Units
    -----
    Waves
    """

    peak_to_valley_nm: float
    """
    Peak-to-valley wavefront error.

    Units
    -----
    Nanometers (nm)
    """

    rms_nm: float
    """
    Root-mean-square wavefront error.

    Units
    -----
    Nanometers (nm)
    """

    minimum_waves: float
    """
    Minimum wavefront value within the pupil.

    Units
    -----
    Waves
    """

    maximum_waves: float
    """
    Maximum wavefront value within the pupil.

    Units
    -----
    Waves
    """

    mean_waves: float
    """
    Mean wavefront value within the pupil.

    Units
    -----
    Waves
    """

    standard_deviation_waves: float
    """
    Standard deviation of the wavefront within the pupil.

    Units
    -----
    Waves
    """