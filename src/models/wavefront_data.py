"""
wavefront_data.py

Raw wavefront information extracted from a Zemax Wavefront Map report.

Purpose
-------
This model stores only the information explicitly reported by Zemax.

No optical analysis is performed here.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import numpy as np

# ---------------------------------------------------------------------
# Wavefront Data
# ---------------------------------------------------------------------

@dataclass(slots=True)
class WavefrontData:
    """
    Raw wavefront information extracted from a Zemax Wavefront Map
    report.
    """

    wavelength_um: float
    """
    Analysis wavelength.

    Units
    -----
    Micrometers (µm)
    """

    field_x_deg: float
    """
    Field X coordinate.

    Units
    -----
    Degrees
    """

    field_y_deg: float
    """
    Field Y coordinate.

    Units
    -----
    Degrees
    """

    peak_to_valley_waves: float
    """
    Peak-to-valley wavefront error.

    Units
    -----
    Waves
    """

    rms_waves: float
    """
    RMS wavefront error.

    Units
    -----
    Waves
    """

    exit_pupil_diameter_mm: float
    """
    Exit pupil diameter.

    Units
    -----
    Millimeters
    """

    grid_size_x: int
    """
    Wavefront grid width.
    """

    grid_size_y: int
    """
    Wavefront grid height.
    """

    center_column: int
    """
    Grid center column reported by Zemax.
    """

    center_row: int
    """
    Grid center row reported by Zemax.
    """

    wavefront_map: np.ndarray
    """
    Two-dimensional wavefront map.

    Units
    -----
    Waves

    Values outside the pupil are stored as NaN.
    """