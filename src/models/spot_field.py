"""
spot_field.py

Data model representing one field contained within a Zemax Spot
Diagram report.

Purpose
-------
A single Zemax Spot Diagram report contains spot statistics for
multiple field positions.

Each SpotField stores the measurements corresponding to one field.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass

# ---------------------------------------------------------------------
# Spot Field
# ---------------------------------------------------------------------


@dataclass(slots=True)
class SpotField:
    """
    Spot statistics for one field position.
    """

    # -------------------------------------------------------------
    # Field Coordinates
    # -------------------------------------------------------------

    field_x_deg: float
    """
    Field X coordinate.

    Units
    -----
    Degrees.
    """

    field_y_deg: float
    """
    Field Y coordinate.

    Units
    -----
    Degrees.
    """

    # -------------------------------------------------------------
    # Image Coordinates
    # -------------------------------------------------------------

    image_x_mm: float
    """
    Image X coordinate.

    Units
    -----
    Millimeters.
    """

    image_y_mm: float
    """
    Image Y coordinate.

    Units
    -----
    Millimeters.
    """

    # -------------------------------------------------------------
    # Spot Metrics
    # -------------------------------------------------------------

    rms_radius_um: float
    """
    RMS spot radius.

    Units
    -----
    Micrometers (µm).
    """

    rms_x_um: float
    """
    RMS spot size along X.

    Units
    -----
    Micrometers (µm).
    """

    rms_y_um: float
    """
    RMS spot size along Y.

    Units
    -----
    Micrometers (µm).
    """

    max_radius_um: float
    """
    Maximum spot radius.

    Units
    -----
    Micrometers (µm).
    """