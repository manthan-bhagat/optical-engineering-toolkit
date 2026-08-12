"""
wavefront.py

Wavefront analysis routines.

Purpose
-------
Computes derived optical metrics from a parsed Zemax Wavefront Map.

Responsibilities
----------------
Computes

- Peak-to-valley wavefront error (waves, nm)
- RMS wavefront error (waves, nm)
- Minimum wavefront (waves)
- Maximum wavefront (waves)
- Mean wavefront (waves)
- Wavefront standard deviation (waves)

The analysis operates only on samples within the optical pupil.

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

from src.models.wavefront_analysis import WavefrontAnalysis
from src.models.wavefront_data import WavefrontData

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def analyze_wavefront(
    wavefront_data: WavefrontData,
) -> WavefrontAnalysis:
    """
    Analyze a parsed wavefront map.

    Parameters
    ----------
    wavefront_data
        Parsed wavefront data.

    Returns
    -------
    WavefrontAnalysis
        Derived wavefront metrics.
    """

    # -------------------------------------------------------------
    # Extract samples within the optical pupil.
    # -------------------------------------------------------------

    samples = _extract_pupil_samples(
        wavefront_data.wavefront_map
    )

    # -------------------------------------------------------------
    # Convert wavefront errors to nanometers.
    # -------------------------------------------------------------

    wavelength_nm = (
        wavefront_data.wavelength_um * 1000.0
    )

    peak_to_valley_nm = (
        wavefront_data.peak_to_valley_waves
        * wavelength_nm
    )

    rms_nm = (
        wavefront_data.rms_waves
        * wavelength_nm
    )

    # -------------------------------------------------------------
    # Construct analysis model.
    # -------------------------------------------------------------

    return WavefrontAnalysis(
        peak_to_valley_waves=(
            wavefront_data.peak_to_valley_waves
        ),
        rms_waves=(
            wavefront_data.rms_waves
        ),
        peak_to_valley_nm=peak_to_valley_nm,
        rms_nm=rms_nm,
        minimum_waves=float(
            np.min(samples)
        ),
        maximum_waves=float(
            np.max(samples)
        ),
        mean_waves=float(
            np.mean(samples)
        ),
        standard_deviation_waves=float(
            np.std(samples)
        ),
    )


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _extract_pupil_samples(
    wavefront_map: np.ndarray,
) -> np.ndarray:
    """
    Extract wavefront samples belonging to the optical pupil.

    Parameters
    ----------
    wavefront_map
        Two-dimensional Zemax wavefront map.

    Returns
    -------
    numpy.ndarray
        One-dimensional array of valid wavefront samples.

    Raises
    ------
    ValueError
        If no valid pupil samples are found.
    """

    #
    # Zemax exports zero outside the optical pupil.
    #
    samples = wavefront_map[
        wavefront_map != 0.0
    ]

    if samples.size == 0:

        raise ValueError(
            "Wavefront map contains no valid pupil samples."
        )

    return samples