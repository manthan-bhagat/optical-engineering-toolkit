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

from src.models.optical_case import OpticalCase
from src.config import MTF_ANALYSIS_FREQUENCIES


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

        "Dataset":
            optical_case.dataset,

        "Configuration":
            optical_case.configuration,

        "Wavelength (µm)":
            optical_case.wavelength_um,

        "Field":
            optical_case.field_index,

        "Temperature (°C)":
            optical_case.temperature_c,

        "Statistical Case":
            optical_case.statistical_case,
    }


# ---------------------------------------------------------------------
# Spot Diagram
# ---------------------------------------------------------------------

def _build_rms_spot(
    optical_case: OpticalCase,
) -> dict:
    """
    Build Spot Diagram columns.
    """

    spot = optical_case.spot_field

    if spot is None:

        return {

            "Spot Field X (deg)": None,
            "Spot Field Y (deg)": None,

            "Spot Image X (mm)": None,
            "Spot Image Y (mm)": None,

            "RMS Spot Radius (µm)": None,
            "RMS Spot X Size (µm)": None,
            "RMS Spot Y Size (µm)": None,

            "Maximum Spot Radius (µm)": None,
        }

    return {

        "Spot Field X (deg)":
            spot.field_x_deg,

        "Spot Field Y (deg)":
            spot.field_y_deg,

        "Spot Image X (mm)":
            spot.image_x_mm,

        "Spot Image Y (mm)":
            spot.image_y_mm,

        "RMS Spot Radius (µm)":
            spot.rms_radius_um,

        "RMS Spot X Size (µm)":
            spot.rms_x_um,

        "RMS Spot Y Size (µm)":
            spot.rms_y_um,

        "Maximum Spot Radius (µm)":
            spot.max_radius_um,
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

            "Airy Radius (µm)": None,
            "Energy Within Airy Radius": None,
            "PSF Wing Fraction": None,
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

        #
        # Airy reference and PSF wings.
        #

        "Airy Radius (µm)":
            psf.airy_radius_um,

        "Energy Within Airy Radius":
            psf.energy_within_airy_radius,

        "PSF Wing Fraction":
            psf.psf_wing_fraction,
    }


# ---------------------------------------------------------------------
# MTF
# ---------------------------------------------------------------------

def _build_mtf(
    optical_case: OpticalCase,
) -> dict:
    """
    Build MTF-related columns.
    """

    mtf = optical_case.mtf_data
    analysis = optical_case.mtf_analysis

    frequency_1, frequency_2 = (
        MTF_ANALYSIS_FREQUENCIES
    )

    if (
        mtf is None
        or analysis is None
    ):

        return {

            #
            # Spatial Frequency 1
            #

            f"Tangential MTF @ {frequency_1:.1f} cycles/mm":
                None,

            f"Sagittal MTF @ {frequency_1:.1f} cycles/mm":
                None,

            f"Mean MTF @ {frequency_1:.1f} cycles/mm":
                None,

            #
            # Spatial Frequency 2
            #

            f"Tangential MTF @ {frequency_2:.1f} cycles/mm":
                None,

            f"Sagittal MTF @ {frequency_2:.1f} cycles/mm":
                None,

            f"Mean MTF @ {frequency_2:.1f} cycles/mm":
                None,
        }

    return {

        #
        # Spatial Frequency 1
        #

        f"Tangential MTF @ {frequency_1:.1f} cycles/mm":
            mtf.tangential_17_2,

        f"Sagittal MTF @ {frequency_1:.1f} cycles/mm":
            mtf.sagittal_17_2,

        f"Mean MTF @ {frequency_1:.1f} cycles/mm":
            analysis.mean_17_2,

        #
        # Spatial Frequency 2
        #

        f"Tangential MTF @ {frequency_2:.1f} cycles/mm":
            mtf.tangential_41_7,

        f"Sagittal MTF @ {frequency_2:.1f} cycles/mm":
            mtf.sagittal_41_7,

        f"Mean MTF @ {frequency_2:.1f} cycles/mm":
            analysis.mean_41_7,
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
    Build wavefront-related columns.
    """

    wavefront = optical_case.wavefront_analysis

    if wavefront is None:

        return {

            "Wavefront PV (waves)": None,
            "Wavefront RMS (waves)": None,

            "Wavefront PV (nm)": None,
            "Wavefront RMS (nm)": None,

            "Minimum Wavefront (waves)": None,
            "Maximum Wavefront (waves)": None,
            "Mean Wavefront (waves)": None,
            "Wavefront Standard Deviation (waves)": None,
        }

    return {

        #
        # Zemax wavefront error.
        #

        "Wavefront PV (waves)":
            wavefront.peak_to_valley_waves,

        "Wavefront RMS (waves)":
            wavefront.rms_waves,

        #
        # Physical wavefront error.
        #

        "Wavefront PV (nm)":
            wavefront.peak_to_valley_nm,

        "Wavefront RMS (nm)":
            wavefront.rms_nm,

        #
        # Wavefront statistics.
        #

        "Minimum Wavefront (waves)":
            wavefront.minimum_waves,

        "Maximum Wavefront (waves)":
            wavefront.maximum_waves,

        "Mean Wavefront (waves)":
            wavefront.mean_waves,

        "Wavefront Standard Deviation (waves)":
            wavefront.standard_deviation_waves,
    }
