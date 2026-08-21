"""
psf_analysis.py

Data model representing the optical metrics derived from a Zemax
Point Spread Function (PSF).

Purpose
-------
This class stores the quantities computed from the raw PSF intensity
distribution contained in a PSFData object.

Unlike PSFData, which contains only information explicitly exported
by Zemax, this class stores derived optical performance metrics.

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
# PSF Analysis Model
# ---------------------------------------------------------------------

@dataclass(slots=True)
class PSFAnalysis:
    """
    Represents the optical performance metrics derived from a PSF.

    Notes
    -----
    This class stores only quantities computed during PSF analysis.

    The raw PSF image and metadata remain in PSFData.

    Metrics that cannot be uniquely determined (for example, the FWHM
    of a highly aberrated PSF with no unique half-maximum crossing)
    are represented by NaN rather than raising an exception.
    """

    # -------------------------------------------------------------
    # Centroid
    # -------------------------------------------------------------

    centroid_x_um: float
    """
    Intensity-weighted centroid along the X direction.

    Units
    -----
    Micrometers (µm)
    """

    centroid_y_um: float
    """
    Intensity-weighted centroid along the Y direction.

    Units
    -----
    Micrometers (µm)
    """

    # -------------------------------------------------------------
    # Slice-Based Full Width at Half Maximum
    # -------------------------------------------------------------

    fwhm_x_um: float
    """
    Full Width at Half Maximum along the X direction.

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    Computed from the horizontal intensity profile passing through the
    brightest pixel.

    For highly aberrated PSFs, a unique half-maximum crossing may not
    exist. In such cases, this value is reported as NaN.
    """

    fwhm_y_um: float
    """
    Full Width at Half Maximum along the Y direction.

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    Computed from the vertical intensity profile passing through the
    brightest pixel.

    For highly aberrated PSFs, a unique half-maximum crossing may not
    exist. In such cases, this value is reported as NaN.
    """

    equivalent_fwhm_um: float
    """
    Equivalent (circularized) slice-based Full Width at Half Maximum.

    Defined as the geometric mean of the horizontal and vertical FWHM
    values.

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    If either horizontal or vertical FWHM is undefined, this value is
    reported as NaN.
    """

    # -------------------------------------------------------------
    # Half-Maximum Region Geometry
    # -------------------------------------------------------------

    major_axis_um: float
    """
    Major-axis length of the ellipse fitted to the connected
    half-maximum region.

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    The ellipse is computed from the second spatial moments of the
    connected half-maximum region containing the global PSF maximum.

    Unlike the slice-based FWHM, this is a true two-dimensional
    geometric descriptor and is independent of image rotation.
    """

    minor_axis_um: float
    """
    Minor-axis length of the ellipse fitted to the connected
    half-maximum region.

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    This represents the orthogonal width of the fitted ellipse derived
    from the second spatial moments of the half-maximum region.
    """

    equivalent_diameter_um: float
    """
    EquivalentEquivalent circular diameter of the connected half-maximum region,
    defined as the diameter of a circle having the same area as the region.

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    This is the diameter of a circle having the same area as the
    measured connected half-maximum region.
    """

    orientation_deg: float
    """
    Orientation of the fitted ellipse major axis.

    Units
    -----
    Degrees (°)

    Notes
    -----
    The orientation is measured relative to the image coordinate system
    and describes the rotation of the ellipse fitted to the connected
    half-maximum region.
    """

    eccentricity: float
    """
    Eccentricity of the fitted ellipse.

    Dimensionless.

    Notes
    -----
    Values range from

    • 0 → circular

    to

    • approaching 1 → highly elongated.
    """

    # -------------------------------------------------------------
    # Encircled Energy
    # -------------------------------------------------------------

    ee50_radius_um: float
    """
    Radius containing 50% of the total PSF energy.

    Units
    -----
    Micrometers (µm)
    """

    ee80_radius_um: float
    """
    Radius containing 80% of the total PSF energy.

    Units
    -----
    Micrometers (µm)
    """

    ee90_radius_um: float
    """
    Radius containing 90% of the total PSF energy.

    Units
    -----
    Micrometers (µm)
    """

    ee95_radius_um: float
    """
    Radius containing 95% of the total PSF energy.

    Units
    -----
    Micrometers (µm)
    """

    # -------------------------------------------------------------
    # Peak Intensity
    # -------------------------------------------------------------

    peak_intensity: float
    """
    Maximum relative intensity within the PSF.

    Dimensionless.

    Notes
    -----
    Since Zemax exports normalized PSFs, this value is typically close
    to 1.0 but is preserved for completeness.
    """

    # -------------------------------------------------------------
    # Airy Reference and PSF Wings
    # -------------------------------------------------------------

    airy_radius_um: float
    """
    Diffraction-defined Airy reference radius.

    Defined as the radius to the first minimum of the ideal Airy
    diffraction pattern:

        r = 1.22 λ F#

    Units
    -----
    Micrometers (µm)

    Notes
    -----
    The radius is evaluated at the wavelength associated with the
    OpticalCase and provides a wavelength-scaled reference boundary
    for evaluating PSF energy concentration and redistribution into
    the PSF wings.
    """

    energy_within_airy_radius: float
    """
    Fraction of the total PSF energy enclosed within the Airy
    reference radius.

    Dimensionless.

    Notes
    -----
    The enclosed energy is computed about the intensity-weighted PSF
    centroid using the same radial convention as the encircled-energy
    calculations.

    A value of 1.0 would indicate that all sampled PSF energy lies
    within the Airy reference radius.
    """

    psf_wing_fraction: float
    """
    Fraction of the total PSF energy lying outside the Airy reference
    radius.

    Dimensionless.

    Defined as

        PSF Wing Fraction
        =
        1 - Energy Within Airy Radius

    Notes
    -----
    This metric quantifies the fraction of sampled PSF energy
    redistributed outside the diffraction-defined Airy reference
    radius.

    A larger value indicates greater energy redistribution into the
    PSF wings.
    """