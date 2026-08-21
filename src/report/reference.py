"""
reference.py

Reference performance models.

Purpose
-------
Provides theoretical and engineering reference curves used by the
reporting pipeline.

These references are independent of Zemax output and are derived from
first-principles optics or system-level engineering allocations.

Responsibilities
----------------
- Diffraction-limited PSF
- Airy disk dimensions
- Diffraction EE radii
- Diffraction-limited MTF
- OTA image-quality allocation
- Ideal Strehl ratio
- Reference plot series

These functions are used only for publication-quality figures and are
not part of the optical analysis itself.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from math import pi

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import numpy as np

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    FOCAL_RATIO,
    OPTICAL_ALLOCATION_UM,
    STREHL_CRITERION,
    MTF42_CRITERION,
    ENGINEERING_WAVELENGTH_UM,
    PSF_NOMINAL_MONTE_CARLO_LIMIT_UM,
    PSF_NOMINAL_THERMAL_LIMIT_UM,
)

from src.models.analysis_type import (
    AnalysisType,
)
# ---------------------------------------------------------------------
# Airy Pattern
# ---------------------------------------------------------------------


def airy_disk_diameter(
    wavelength_um,
):
    """
    Airy disk diameter (µm).

    Diameter to the first diffraction minimum.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        2.44
        * wavelength_um
        * FOCAL_RATIO
    )


def airy_disk_radius(
    wavelength_um,
):
    """
    Airy disk radius (µm).

    Radius to the first diffraction minimum.

        r = 1.22 λ F#
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        1.22
        * wavelength_um
        * FOCAL_RATIO
    )


def diffraction_psf_fwhm(
    wavelength_um,
):
    """
    Diffraction-limited PSF FWHM (µm).

    Uses

        FWHM ≈ 1.03 λ F#

    which closely matches an Airy profile.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        1.03
        * wavelength_um
        * FOCAL_RATIO
    )


def diffraction_rms_spot(
    wavelength_um,
):
    """
    Approximate diffraction-limited RMS spot radius (µm).
    """

    return (
        diffraction_psf_fwhm(
            wavelength_um,
        )
        / 2.355
    )


# ---------------------------------------------------------------------
# Encircled Energy
# ---------------------------------------------------------------------


def diffraction_ee50(
    wavelength_um,
):
    """
    Approximate diffraction-limited EE50 radius (µm).
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        0.535
        * wavelength_um
        * FOCAL_RATIO
    )

def airy_energy_reference(
    wavelength_um,
):
    """
    Ideal diffraction-limited fraction of energy enclosed within
    the Airy disk.

    The Airy disk is defined as the region from the PSF center to
    the first diffraction minimum.

    For an unobstructed circular aperture, approximately 83.8% of
    the total energy is enclosed within this radius.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.full_like(
        wavelength_um,
        0.838,
        dtype=float,
    )

def diffraction_ee80(
    wavelength_um,
):
    """
    Approximate diffraction-limited EE80 radius (µm).
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        0.86
        * wavelength_um
        * FOCAL_RATIO
    )


def diffraction_ee90(
    wavelength_um,
):
    """
    Approximate diffraction-limited EE90 radius (µm).
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        1.15
        * wavelength_um
        * FOCAL_RATIO
    )


def diffraction_ee95(
    wavelength_um,
):
    """
    Approximate diffraction-limited EE95 radius (µm).
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return (
        1.45
        * wavelength_um
        * FOCAL_RATIO
    )


# ---------------------------------------------------------------------
# MTF
# ---------------------------------------------------------------------


def diffraction_mtf(
    wavelength_um,
    spatial_frequency,
):
    """
    Diffraction-limited incoherent MTF.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    cutoff_frequency = (
        1000.0
        / (
            wavelength_um
            * FOCAL_RATIO
        )
    )

    normalized_frequency = (
        spatial_frequency
        / cutoff_frequency
    )

    normalized_frequency = np.clip(
        normalized_frequency,
        0.0,
        1.0,
    )

    return (
        (
            2.0
            / pi
        )
        * (
            np.arccos(
                normalized_frequency
            )
            - normalized_frequency
            * np.sqrt(
                1.0
                - normalized_frequency**2
            )
        )
    )


def diffraction_mtf17(
    wavelength_um,
):
    """
    Diffraction-limited MTF at 17.2 cycles/mm.
    """

    return diffraction_mtf(
        wavelength_um,
        17.2,
    )


def diffraction_mtf42(
    wavelength_um,
):
    """
    Diffraction-limited MTF at 41.7 cycles/mm.
    """

    return diffraction_mtf(
        wavelength_um,
        41.7,
    )

def diffraction_wavefront_rms(
    wavelength_um,
):
    """
    Diffraction-limited wavefront RMS (waves).

    Uses the classical Maréchal criterion

        RMS = λ / 14

    expressed in waves.

    Parameters
    ----------
    wavelength_um
        Wavelength array.

    Returns
    -------
    numpy.ndarray
        Constant value of 1/14 waves.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.full_like(
        wavelength_um,
        1.0 / 14.0,
        dtype=float,
    )

# ---------------------------------------------------------------------
# Image Quality Allocation
# ---------------------------------------------------------------------


def ota_psf_limit(
    wavelength_um,
):
    """
    Maximum allowable OTA PSF (µm).
    """

    diffraction = (
        diffraction_psf_fwhm(
            wavelength_um,
        )
    )

    return np.sqrt(
        diffraction**2
        + OPTICAL_ALLOCATION_UM**2
    )

# ---------------------------------------------------------------------
# Engineering PSF Acceptance Criteria
# ---------------------------------------------------------------------


def nominal_monte_carlo_psf_limit(
    wavelength_um,
):
    """
    Nominal + Monte Carlo PSF acceptance limit (µm).

    The engineering criterion is defined at the governing wavelength
    of 200 nm and is therefore represented as a constant detector-plane
    PSF FWHM limit in the report figures.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.full_like(
        wavelength_um,
        PSF_NOMINAL_MONTE_CARLO_LIMIT_UM,
        dtype=float,
    )


def nominal_thermal_psf_limit(
    wavelength_um,
):
    """
    Nominal + thermal PSF acceptance limit (µm).

    The engineering criterion is defined at the governing wavelength
    of 200 nm and is therefore represented as a constant detector-plane
    PSF FWHM limit in the report figures.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.full_like(
        wavelength_um,
        PSF_NOMINAL_THERMAL_LIMIT_UM,
        dtype=float,
    )

# ---------------------------------------------------------------------
# Strehl
# ---------------------------------------------------------------------


def ideal_strehl(
    wavelength_um,
):
    """
    Ideal diffraction-limited Strehl ratio.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.ones_like(
        wavelength_um,
        dtype=float,
    )


def strehl_criterion(
    wavelength_um,
):
    """
    Engineering Strehl acceptance criterion.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.full_like(
        wavelength_um,
        STREHL_CRITERION,
        dtype=float,
    )


def mtf42_criterion(
    wavelength_um,
):
    """
    Engineering MTF criterion at 42 lp/mm.
    """

    wavelength_um = np.asarray(
        wavelength_um,
        dtype=float,
    )

    return np.full_like(
        wavelength_um,
        MTF42_CRITERION,
        dtype=float,
    )

# ---------------------------------------------------------------------
# Reference Plot Series
# ---------------------------------------------------------------------


def baseline_psf_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for baseline PSF FWHM figures.

    Includes the fundamental diffraction limit and the
    OTA image-quality allocation.
    """

    return [

        {
            "label": "Diffraction Limit",
            "x": wavelength_um,
            "y": diffraction_psf_fwhm(
                wavelength_um,
            ),
        },

        {
            "label": "OTA Allocation",
            "x": wavelength_um,
            "y": ota_psf_limit(
                wavelength_um,
            ),
        },

    ]


def thermal_psf_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for thermal PSF FWHM figures.

    Includes the baseline optical references and the
    nominal plus thermal acceptance limit.
    """

    return [

        *baseline_psf_reference_series(
            wavelength_um,
        ),

        {
            "label": "Thermal Limit",
            "x": wavelength_um,
            "y": nominal_thermal_psf_limit(
                wavelength_um,
            ),
        },

    ]


def monte_carlo_psf_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for Monte Carlo PSF FWHM figures.

    Includes the baseline optical references and the
    nominal plus Monte Carlo acceptance limit.
    """

    return [

        *baseline_psf_reference_series(
            wavelength_um,
        ),

        {
            "label": "Monte Carlo Limit",
            "x": wavelength_um,
            "y": nominal_monte_carlo_psf_limit(
                wavelength_um,
            ),
        },

    ]

def airy_energy_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curve for energy enclosed within the Airy disk.
    """

    return [

        {
            "label": "Ideal Airy Pattern",
            "x": wavelength_um,
            "y": airy_energy_reference(
                wavelength_um,
            ),
        },

    ]

def ee80_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for EE80 figures.
    """

    return [

        {
            "label": "Diffraction Limit",
            "x": wavelength_um,
            "y": diffraction_ee80(
                wavelength_um,
            ),
        },

    ]

def ee90_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for EE90 figures.
    """

    return [

        {
            "label": "Diffraction Limit",
            "x": wavelength_um,
            "y": diffraction_ee90(
                wavelength_um,
            ),
        },

    ]

def mtf17_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for 17.2 cycles/mm MTF figures.
    """

    return [

        {
            "label": "Diffraction Limit",
            "x": wavelength_um,
            "y": diffraction_mtf17(
                wavelength_um,
            ),
        },

    ]


def mtf42_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for 41.7 cycles/mm MTF figures.
    """

    return [

        {
            "label": "Diffraction Limit",
            "x": wavelength_um,
            "y": diffraction_mtf42(
                wavelength_um,
            ),
        },

    ]


def strehl_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for Strehl ratio figures.
    """

    return [

        {
            "label": "Ideal",
            "x": wavelength_um,
            "y": ideal_strehl(
                wavelength_um,
            ),
        },

        {
            "label": "Maréchal Criterion",
            "x": wavelength_um,
            "y": strehl_criterion(
                wavelength_um,
            ),
        },

    ]


def wavefront_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for wavefront RMS figures.
    """

    return [

        {
            "label": "Maréchal Criterion",
            "x": wavelength_um,
            "y": diffraction_wavefront_rms(
                wavelength_um,
            ),
        },

    ]

def rms_spot_reference_series(
    wavelength_um,
) -> list[dict]:
    """
    Reference curves for RMS Spot Radius figures.
    """

    return [

        {
            "label": "Airy Disk Radius \n (200 nm)",
            "x": wavelength_um,
            "y": airy_disk_radius(
                wavelength_um,
            ),
        },

    ]

# ---------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------

REFERENCE_SERIES = {

    "rms_spot": rms_spot_reference_series,

    "ee80": ee80_reference_series,

    "ee90": ee90_reference_series,

    "airy_energy": airy_energy_reference_series,

    "mtf17": mtf17_reference_series,

    "mtf42": mtf42_reference_series,

    "strehl": strehl_reference_series,

    "wavefront_rms": wavefront_reference_series,

}


PSF_REFERENCE_SERIES = {

    "baseline": baseline_psf_reference_series,

    "thermal": thermal_psf_reference_series,

    "monte-carlo": monte_carlo_psf_reference_series,

}


def get_reference_series(
    analysis_type: AnalysisType,
    figure_name: str,
    wavelength_um,
) -> list[dict]:
    """
    Return reference curves for a report figure.

    Reference curves may depend on both the figure metric and
    analysis type.
    """

    if figure_name == "psf":

        if analysis_type == AnalysisType.BASELINE:

            builder = baseline_psf_reference_series

        elif analysis_type == AnalysisType.THERMAL:

            builder = thermal_psf_reference_series

        elif analysis_type == AnalysisType.MONTE_CARLO:

            builder = monte_carlo_psf_reference_series

        else:

            raise ValueError(
                f"Unsupported analysis type: {analysis_type}"
            )

        return builder(
            wavelength_um,
        )

    builder = REFERENCE_SERIES.get(
        figure_name,
    )

    if builder is None:

        return []

    return builder(
        wavelength_um,
    )

def get_engineering_reference_series(
    analysis_type: AnalysisType,
    figure_name: str,
    x_values,
) -> list[dict]:
    """
    Return engineering reference curves for validation figures.

    References are evaluated at the configured engineering wavelength
    and represented as horizontal lines across the plotted X-axis.
    """

    reference_series = get_reference_series(
        analysis_type,
        figure_name,
        np.asarray(
            [ENGINEERING_WAVELENGTH_UM],
            dtype=float,
        ),
    )

    engineering_series = []

    x_values = list(
        x_values,
    )

    for curve in reference_series:

        engineering_series.append(
            {
                "label": curve["label"],
                "x": x_values,
                "y": [
                    float(curve["y"][0])
                ] * len(x_values),
            }
        )

    return engineering_series