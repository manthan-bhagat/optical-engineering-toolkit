"""
psf_data.py

Data model representing the information extracted from a Zemax
Huygens PSF text report.

Purpose
-------
This class is the structured output produced by the PSF parser.

It stores only the information that is explicitly present in the
Zemax report. No optical analysis or derived calculations (such as
FWHM or EE80) are performed here.

Design Philosophy
-----------------
Parser
    ↓
PSFData
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
# Third-Party Imports
# ---------------------------------------------------------------------

import numpy as np


# ---------------------------------------------------------------------
# PSF Data Model
# ---------------------------------------------------------------------

@dataclass(slots=True)
class PSFData:
    """
    Represents the raw information extracted from a Zemax Huygens PSF
    report.

    Notes
    -----
    This object intentionally stores only the quantities directly
    available in the Zemax export.

    It does NOT store derived quantities such as

    - FWHM
    - Equivalent FWHM
    - EE80 Radius

    Those are computed later by the metrics module.
    """

    # -------------------------------------------------------------
    # Optical Metadata
    # -------------------------------------------------------------

    strehl_ratio: float
    """
    Strehl ratio reported by Zemax.

    Dimensionless.

    Example
    -------
    0.927
    """

    pixel_spacing_um: float
    """
    Physical spacing between adjacent PSF samples.

    Units
    -----
    Micrometers (µm)

    Example
    -------
    3.0
    """

    # -------------------------------------------------------------
    # Image Geometry
    # -------------------------------------------------------------

    image_width: int
    """
    Number of columns in the PSF image.
    """

    image_height: int
    """
    Number of rows in the PSF image.
    """

    center_x: int
    """
    Column index of the optical center reported by Zemax.

    Note
    ----
    Zemax reports pixel indices starting from 1.
    The parser should preserve these values exactly as reported.
    Any conversion to zero-based indexing should be performed by
    downstream analysis code if required.
    """

    center_y: int
    """
    Row index of the optical center reported by Zemax.

    Note
    ----
    Zemax reports pixel indices starting from 1.
    The parser should preserve these values exactly as reported.
    """
    # -------------------------------------------------------------
    # PSF Data
    # -------------------------------------------------------------

    psf: np.ndarray
    """
    Two-dimensional PSF intensity distribution.

    Shape
    -----
    (rows, columns)

    Values
    ------
    Relative intensity values exactly as exported by Zemax.

    The parser should not normalize, modify, or process these values.
    All optical calculations (FWHM, EE80, radial profiles, etc.) are
    performed later by the metrics module.

    Example
    -------
    A typical Zemax export produces a 64 × 64 floating-point array.
    """