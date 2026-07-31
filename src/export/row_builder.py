"""
row_builder.py

Builds a flat table row from an OpticalCase.

Purpose
-------
This module converts the hierarchical OpticalCase object into a flat
dictionary suitable for tabular representations such as

- CSV
- Excel
- Pandas DataFrames

The table schema is defined here so that every exporter produces
identical output.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import MTF_EVALUATION_FREQUENCY
from src.models.optical_case import OpticalCase


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def build_case_row(
    optical_case: OpticalCase,
) -> dict:
    """
    Convert an OpticalCase into a flat dictionary.

    Parameters
    ----------
    optical_case
        Optical analysis case.

    Returns
    -------
    dict
        Flat representation suitable for tabular export.
    """

    row: dict = {}

    row.update(
        _build_case_metadata(
            optical_case
        )
    )

    row.update(
        _build_rms_spot(
            optical_case
        )
    )

    row.update(
        _build_psf(
            optical_case
        )
    )

    row.update(
        _build_mtf(
            optical_case
        )
    )

    row.update(
        _build_strehl(
            optical_case
        )
    )

    row.update(
        _build_wavefront(
            optical_case
        )
    )

    return row


# ---------------------------------------------------------------------
# Case Metadata
# ---------------------------------------------------------------------

def _build_case_metadata(
    optical_case: OpticalCase,
) -> dict:
    """
    Build case metadata columns.
    """

    return {

        "Case ID":
            optical_case.case_id,

        "Analysis Type":
            optical_case.analysis_type.value,

        "Temperature (°C)":
            optical_case.temperature_c,

        "Statistical Case":
            optical_case.statistical_case,
    }


# ---------------------------------------------------------------------
# RMS Spot Radius
# ---------------------------------------------------------------------

def _build_rms_spot(
    optical_case: OpticalCase,
) -> dict:
    """
    Build RMS spot radius columns.
    """

    #
    # Future implementation.
    #

    return {

        "RMS Spot Radius (µm)": None,
    }


# ---------------------------------------------------------------------
# PSF
# ---------------------------------------------------------------------

def _build_psf(
    optical_case: OpticalCase,
) -> dict:
    """
    Build PSF-related columns.
    """

    psf = optical_case.psf_analysis

    if psf is None:

        return {

            "PSF FWHM X (µm)": None,
            "PSF FWHM Y (µm)": None,
            "Equivalent PSF FWHM (µm)": None,

            "Half-Maximum Major Axis (µm)": None,
            "Half-Maximum Minor Axis (µm)": None,
            "Half-Maximum Equivalent Diameter (µm)": None,
            "Half-Maximum Orientation (°)": None,
            "Half-Maximum Eccentricity": None,

            "EE50 Radius (µm)": None,
            "EE80 Radius (µm)": None,
            "EE90 Radius (µm)": None,
            "EE95 Radius (µm)": None,
        }

    return {

        #
        # Slice-based PSF metrics.
        #

        "PSF FWHM X (µm)":
            psf.fwhm_x_um,

        "PSF FWHM Y (µm)":
            psf.fwhm_y_um,

        "Equivalent PSF FWHM (µm)":
            psf.equivalent_fwhm_um,

        #
        # Half-maximum region geometry.
        #

        "Half-Maximum Major Axis (µm)":
            psf.major_axis_um,

        "Half-Maximum Minor Axis (µm)":
            psf.minor_axis_um,

        "Half-Maximum Equivalent Diameter (µm)":
            psf.equivalent_diameter_um,

        "Half-Maximum Orientation (°)":
            psf.orientation_deg,

        "Half-Maximum Eccentricity":
            psf.eccentricity,

        #
        # Encircled energy.
        #

        "EE50 Radius (µm)":
            psf.ee50_radius_um,

        "EE80 Radius (µm)":
            psf.ee80_radius_um,

        "EE90 Radius (µm)":
            psf.ee90_radius_um,

        "EE95 Radius (µm)":
            psf.ee95_radius_um,
    }


# ---------------------------------------------------------------------
# MTF
# ---------------------------------------------------------------------

def _build_mtf(
    optical_case: OpticalCase,
) -> dict:
    """
    Build MTF columns.
    """

    #
    # Future implementation.
    #

    return {

        f"Tangential MTF @ {MTF_EVALUATION_FREQUENCY:.0f} cycles/mm":
            None,

        f"Sagittal MTF @ {MTF_EVALUATION_FREQUENCY:.0f} cycles/mm":
            None,

        f"Mean MTF @ {MTF_EVALUATION_FREQUENCY:.0f} cycles/mm":
            None,
    }


# ---------------------------------------------------------------------
# Strehl Ratio
# ---------------------------------------------------------------------

def _build_strehl(
    optical_case: OpticalCase,
) -> dict:
    """
    Build Strehl ratio columns.
    """

    return {

        "Strehl Ratio":
            (
                None
                if optical_case.psf_data is None
                else optical_case.psf_data.strehl_ratio
            ),
    }


# ---------------------------------------------------------------------
# Wavefront Error
# ---------------------------------------------------------------------

def _build_wavefront(
    optical_case: OpticalCase,
) -> dict:
    """
    Build wavefront error columns.
    """

    #
    # Future implementation.
    #

    return {

        "RMS WFE": None,
    }
