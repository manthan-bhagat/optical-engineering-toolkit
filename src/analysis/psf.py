"""
psf.py

Analysis routines for Zemax Point Spread Function (PSF) data.

Purpose
-------
This module computes optical image quality metrics from the raw PSF
intensity matrix extracted from a Zemax Huygens PSF report.

Unlike the parser, this module performs numerical analysis of the PSF.

Computed Metrics
----------------
Traditional Metrics
    - Intensity-weighted centroid
    - Slice-based PSF FWHM (X)
    - Slice-based PSF FWHM (Y)
    - Equivalent slice-based PSF FWHM
    - Encircled Energy (EE50/EE80/EE90/EE95)

Two-Dimensional Metrics
    - Half-maximum major axis
    - Half-maximum minor axis
    - Equivalent diameter
    - Orientation
    - Eccentricity

The Strehl ratio is not computed here because it is already reported
directly by Zemax.

Design Philosophy
-----------------

Zemax Report
      ↓
 PSFParser
      ↓
  PSFData
      ↓
 PSF Analysis
      ↓
 PSFAnalysis
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
# Third-Party Imports
# ---------------------------------------------------------------------

import numpy as np
from skimage.measure import (
    label,
    regionprops,
)

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import EE_TARGET
from src.models.psf_analysis import PSFAnalysis
from src.models.psf_data import PSFData

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def analyze_psf(
    data: PSFData,
) -> PSFAnalysis:
    """
    Compute all derived optical metrics from a parsed Zemax PSF.

    Parameters
    ----------
    data
        Parsed PSF information.

    Returns
    -------
    PSFAnalysis
        Derived optical performance metrics.
    """

    # -------------------------------------------------------------
    # Intensity-weighted centroid.
    #
    # Used only for encircled-energy calculations.
    # -------------------------------------------------------------

    centroid_x, centroid_y = _compute_centroid(
        data,
    )

    # -------------------------------------------------------------
    # Locate the brightest pixel.
    #
    # Slice-based FWHM measurements should always pass through the
    # global maximum rather than the centroid.
    # -------------------------------------------------------------

    peak_y, peak_x = np.unravel_index(
        np.argmax(data.psf),
        data.psf.shape,
    )

    peak_y = int(peak_y)
    peak_x = int(peak_x)

    # -------------------------------------------------------------
    # Traditional slice-based FWHM.
    # -------------------------------------------------------------

    fwhm_x = _compute_fwhm_x(
        data,
        peak_y,
    )

    fwhm_y = _compute_fwhm_y(
        data,
        peak_x,
    )

    equivalent_fwhm = _compute_equivalent_fwhm(
        fwhm_x,
        fwhm_y,
    )

    # -------------------------------------------------------------
    # Two-dimensional half-maximum region geometry.
    # -------------------------------------------------------------

    contour = _compute_half_maximum_contour(
        data,
        peak_x,
        peak_y,
    )

    # -------------------------------------------------------------
    # Encircled-energy radii.
    # -------------------------------------------------------------

    ee50_radius = _compute_encircled_energy_radius(
        data,
        centroid_x,
        centroid_y,
        fraction=0.50,
    )

    ee80_radius = _compute_encircled_energy_radius(
        data,
        centroid_x,
        centroid_y,
        fraction=EE_TARGET,
    )

    ee90_radius = _compute_encircled_energy_radius(
        data,
        centroid_x,
        centroid_y,
        fraction=0.90,
    )

    ee95_radius = _compute_encircled_energy_radius(
        data,
        centroid_x,
        centroid_y,
        fraction=0.95,
    )

    # -------------------------------------------------------------
    # Miscellaneous metrics.
    # -------------------------------------------------------------

    peak_intensity = float(
        np.max(data.psf)
    )

    centroid_x_um = (
        centroid_x
        * data.pixel_spacing_um
    )

    centroid_y_um = (
        centroid_y
        * data.pixel_spacing_um
    )

    # -------------------------------------------------------------
    # Assemble results.
    # -------------------------------------------------------------

    return PSFAnalysis(

        # ---------------------------------------------------------
        # Centroid
        # ---------------------------------------------------------

        centroid_x_um=centroid_x_um,
        centroid_y_um=centroid_y_um,

        # ---------------------------------------------------------
        # Slice-based FWHM
        # ---------------------------------------------------------

        fwhm_x_um=fwhm_x,
        fwhm_y_um=fwhm_y,
        equivalent_fwhm_um=equivalent_fwhm,

        # ---------------------------------------------------------
        # Half-maximum region geometry
        # ---------------------------------------------------------

        major_axis_um=contour.major_axis_um,
        minor_axis_um=contour.minor_axis_um,
        equivalent_diameter_um=contour.equivalent_diameter_um,
        orientation_deg=contour.orientation_deg,
        eccentricity=contour.eccentricity,

        # ---------------------------------------------------------
        # Encircled energy
        # ---------------------------------------------------------

        ee50_radius_um=ee50_radius,
        ee80_radius_um=ee80_radius,
        ee90_radius_um=ee90_radius,
        ee95_radius_um=ee95_radius,

        # ---------------------------------------------------------
        # Peak intensity
        # ---------------------------------------------------------

        peak_intensity=peak_intensity,
    )


# ---------------------------------------------------------------------
# Internal Data Structures
# ---------------------------------------------------------------------

@dataclass(slots=True)
class _ContourAnalysis:
    """
    Results of the two-dimensional half-maximum region analysis.

    All geometric quantities are computed from the connected component
    containing the global PSF maximum after thresholding the image at
    half the peak intensity.
    """

    major_axis_um: float
    minor_axis_um: float
    equivalent_diameter_um: float
    orientation_deg: float
    eccentricity: float

# ---------------------------------------------------------------------
# Half-Maximum Region Analysis
# ---------------------------------------------------------------------

def _empty_contour_analysis() -> _ContourAnalysis:
    """
    Construct an empty contour-analysis result.

    Returns
    -------
    _ContourAnalysis
        A result whose geometric quantities are all undefined (NaN).
    """

    return _ContourAnalysis(
        major_axis_um=np.nan,
        minor_axis_um=np.nan,
        equivalent_diameter_um=np.nan,
        orientation_deg=np.nan,
        eccentricity=np.nan,
    )


def _compute_half_maximum_contour(
    data: PSFData,
    peak_x: int,
    peak_y: int,
) -> _ContourAnalysis:
    """
    Measure the geometry of the connected half-maximum region
    surrounding the global PSF maximum.

    The PSF is thresholded at half of its peak intensity. Connected
    regions are identified and only the region containing the global
    maximum is measured.

    Parameters
    ----------
    data
        Parsed PSF.

    peak_x
        X coordinate of the global maximum.

    peak_y
        Y coordinate of the global maximum.

    Returns
    -------
    _ContourAnalysis
        Geometric descriptors of the fitted ellipse representing the
        connected half-maximum region.
    """

    image = np.asarray(
        data.psf,
        dtype=np.float64,
    )

    peak = float(
        image[
            peak_y,
            peak_x,
        ]
    )

    #
    # Degenerate image.
    #
    if peak <= 0.0:
        return _empty_contour_analysis()

    # -------------------------------------------------------------
    # Threshold at half maximum.
    # -------------------------------------------------------------

    half_maximum = (
        peak / 2.0
    )

    mask = (
        image >= half_maximum
    )

    # -------------------------------------------------------------
    # Label connected regions.
    #
    # Eight-connectivity is used so diagonally touching pixels belong
    # to the same optical feature.
    # -------------------------------------------------------------

    labels = label(
        mask,
        connectivity=2,
    )

    component_label = int(
        labels[
            peak_y,
            peak_x,
        ]
    )

    if component_label == 0:
        return _empty_contour_analysis()

    # -------------------------------------------------------------
    # Measure only the component containing the PSF peak.
    # -------------------------------------------------------------

    spacing = data.pixel_spacing_um

    for region in regionprops(labels):

        if region.label != component_label:
            continue

        return _ContourAnalysis(

            major_axis_um=float(
                region.axis_major_length
                * spacing
            ),

            minor_axis_um=float(
                region.axis_minor_length
                * spacing
            ),

            equivalent_diameter_um=float(
                region.equivalent_diameter_area
                * spacing
            ),

            orientation_deg=float(
                np.degrees(
                    region.orientation
                )
            ),

            eccentricity=float(
                region.eccentricity
            ),
        )

    #
    # Should never occur, but protects against unexpected behaviour.
    #
    return _empty_contour_analysis()

# ---------------------------------------------------------------------
# Centroid
# ---------------------------------------------------------------------

def _compute_centroid(
    data: PSFData,
) -> tuple[float, float]:
    """
    Compute the intensity-weighted centroid of the PSF.

    Notes
    -----
    The centroid is computed from the first spatial moments of the
    intensity distribution.

    Unlike the slice-based FWHM measurements, the centroid is used only
    for encircled-energy calculations.

    Returns
    -------
    tuple[float, float]
        Centroid coordinates in pixel units.
    """

    image = np.asarray(
        data.psf,
        dtype=np.float64,
    )

    total_intensity = float(
        image.sum()
    )

    if total_intensity <= 0.0:
        raise ValueError(
            "PSF contains zero total intensity."
        )

    y_indices, x_indices = np.indices(
        image.shape
    )

    centroid_x = float(
        (x_indices * image).sum()
        / total_intensity
    )

    centroid_y = float(
        (y_indices * image).sum()
        / total_intensity
    )

    return (
        centroid_x,
        centroid_y,
    )


# ---------------------------------------------------------------------
# Slice-Based FWHM Computation
# ---------------------------------------------------------------------

def _compute_fwhm(
    profile: np.ndarray,
    spacing_um: float,
) -> float:
    """
    Compute the Full Width at Half Maximum (FWHM) of a one-dimensional
    intensity profile.

    Parameters
    ----------
    profile
        One-dimensional intensity profile.

    spacing_um
        Physical sample spacing in micrometers.

    Returns
    -------
    float
        FWHM in micrometers.

    Notes
    -----
    The FWHM is obtained by locating the half-maximum crossings on
    either side of the profile peak and linearly interpolating between
    neighboring samples.

    If a unique pair of half-maximum crossings cannot be determined,
    NaN is returned instead of raising an exception.
    """

    profile = np.asarray(
        profile,
        dtype=np.float64,
    )

    peak_index = int(
        np.argmax(profile)
    )

    peak_value = float(
        profile[peak_index]
    )

    if peak_value <= 0.0:
        return np.nan

    half_maximum = (
        peak_value / 2.0
    )

    # -------------------------------------------------------------
    # Left crossing
    # -------------------------------------------------------------

    left_candidates = np.where(
        profile[:peak_index] < half_maximum
    )[0]

    if left_candidates.size == 0:
        return np.nan

    left = int(
        left_candidates[-1]
    )

    # -------------------------------------------------------------
    # Right crossing
    # -------------------------------------------------------------

    right_candidates = np.where(
        profile[peak_index + 1:] < half_maximum
    )[0]

    if right_candidates.size == 0:
        return np.nan

    right = (
        peak_index
        + 1
        + int(right_candidates[0])
    )

    # -------------------------------------------------------------
    # Linear interpolation (left)
    # -------------------------------------------------------------

    denominator = (
        profile[left + 1]
        - profile[left]
    )

    if abs(denominator) < 1e-12:

        left_position = float(left)

    else:

        left_position = (
            left
            + (
                (half_maximum - profile[left])
                / denominator
            )
        )

    # -------------------------------------------------------------
    # Linear interpolation (right)
    # -------------------------------------------------------------

    denominator = (
        profile[right - 1]
        - profile[right]
    )

    if abs(denominator) < 1e-12:

        right_position = float(right)

    else:

        right_position = (
            right
            - (
                (half_maximum - profile[right])
                / denominator
            )
        )

    width_pixels = (
        right_position
        - left_position
    )

    return float(
        width_pixels
        * spacing_um
    )

# ---------------------------------------------------------------------
# Slice-Based FWHM Along X
# ---------------------------------------------------------------------

def _compute_fwhm_x(
    data: PSFData,
    row: int,
) -> float:
    """
    Compute the slice-based PSF Full Width at Half Maximum (FWHM)
    along the X direction.

    Parameters
    ----------
    data
        Parsed PSF.

    row
        Image row containing the global PSF maximum.

    Returns
    -------
    float
        Horizontal FWHM in micrometers.
    """

    row = int(
        np.clip(
            row,
            0,
            data.psf.shape[0] - 1,
        )
    )

    profile = data.psf[
        row,
        :,
    ]

    return _compute_fwhm(
        profile=profile,
        spacing_um=data.pixel_spacing_um,
    )


# ---------------------------------------------------------------------
# Slice-Based FWHM Along Y
# ---------------------------------------------------------------------

def _compute_fwhm_y(
    data: PSFData,
    column: int,
) -> float:
    """
    Compute the slice-based PSF Full Width at Half Maximum (FWHM)
    along the Y direction.

    Parameters
    ----------
    data
        Parsed PSF.

    column
        Image column containing the global PSF maximum.

    Returns
    -------
    float
        Vertical FWHM in micrometers.
    """

    column = int(
        np.clip(
            column,
            0,
            data.psf.shape[1] - 1,
        )
    )

    profile = data.psf[
        :,
        column,
    ]

    return _compute_fwhm(
        profile=profile,
        spacing_um=data.pixel_spacing_um,
    )


# ---------------------------------------------------------------------
# Equivalent Slice-Based FWHM
# ---------------------------------------------------------------------

def _compute_equivalent_fwhm(
    fwhm_x: float,
    fwhm_y: float,
) -> float:
    """
    Compute the equivalent slice-based PSF FWHM.

    The equivalent FWHM is defined as the geometric mean of the
    horizontal and vertical slice-based FWHM values.

    Parameters
    ----------
    fwhm_x
        Horizontal FWHM.

    fwhm_y
        Vertical FWHM.

    Returns
    -------
    float
        Equivalent slice-based FWHM in micrometers.

    Notes
    -----
    If either slice-based FWHM is undefined or non-positive,
    the equivalent FWHM is also undefined and NaN is returned.
    """

    if (
        np.isnan(fwhm_x)
        or np.isnan(fwhm_y)
    ):
        return np.nan

    if (
        fwhm_x <= 0.0
        or fwhm_y <= 0.0
    ):
        return np.nan

    return float(
        np.sqrt(
            fwhm_x
            * fwhm_y
        )
    )

# ---------------------------------------------------------------------
# Encircled Energy
# ---------------------------------------------------------------------

def _compute_encircled_energy_radius(
    data: PSFData,
    centroid_x: float,
    centroid_y: float,
    fraction: float,
) -> float:
    """
    Compute the radius enclosing a specified fraction of the total PSF
    energy.

    Parameters
    ----------
    data
        Parsed PSF data.

    centroid_x
        Intensity-weighted centroid X coordinate in pixel units.

    centroid_y
        Intensity-weighted centroid Y coordinate in pixel units.

    fraction
        Desired enclosed-energy fraction. Typical values are
        0.50, 0.80, 0.90 and 0.95.

    Returns
    -------
    float
        Encircled-energy radius in micrometers.

    Notes
    -----
    Pixels are sorted by increasing radial distance from the
    intensity-weighted centroid. The requested enclosed-energy radius
    is obtained by linear interpolation of the cumulative energy curve.
    """

    image = np.asarray(
        data.psf,
        dtype=np.float64,
    )

    # -------------------------------------------------------------
    # Pixel coordinate grids.
    # -------------------------------------------------------------

    y_indices, x_indices = np.indices(
        image.shape
    )

    # -------------------------------------------------------------
    # Radial distance of every pixel from the centroid.
    # -------------------------------------------------------------

    radius = np.sqrt(
        (x_indices - centroid_x) ** 2
        + (y_indices - centroid_y) ** 2
    )

    # -------------------------------------------------------------
    # Flatten arrays.
    # -------------------------------------------------------------

    radius = radius.ravel()
    intensity = image.ravel()

    # -------------------------------------------------------------
    # Sort by increasing radius.
    # -------------------------------------------------------------

    order = np.argsort(radius)

    radius = radius[order]
    intensity = intensity[order]

    # -------------------------------------------------------------
    # Cumulative enclosed energy.
    # -------------------------------------------------------------

    cumulative_energy = np.cumsum(
        intensity
    )

    total_energy = float(
        cumulative_energy[-1]
    )

    if total_energy <= 0.0:
        raise ValueError(
            "PSF contains zero total intensity."
        )

    enclosed_energy = (
        cumulative_energy
        / total_energy
    )

    # -------------------------------------------------------------
    # Locate requested enclosed-energy fraction.
    # -------------------------------------------------------------

    index = int(
        np.searchsorted(
            enclosed_energy,
            fraction,
        )
    )

    if index >= len(enclosed_energy):
        raise ValueError(
            "Unable to determine encircled-energy radius."
        )

    # -------------------------------------------------------------
    # Linear interpolation.
    # -------------------------------------------------------------

    if index == 0:

        radius_pixels = float(
            radius[0]
        )

    else:

        r1 = radius[index - 1]
        r2 = radius[index]

        e1 = enclosed_energy[index - 1]
        e2 = enclosed_energy[index]

        if abs(e2 - e1) < 1e-12:

            radius_pixels = float(
                r2
            )

        else:

            interpolation_fraction = (
                (fraction - e1)
                / (e2 - e1)
            )

            radius_pixels = (
                r1
                + interpolation_fraction
                * (r2 - r1)
            )

    # -------------------------------------------------------------
    # Convert pixels → micrometers.
    # -------------------------------------------------------------

    return float(
        radius_pixels
        * data.pixel_spacing_um
    )