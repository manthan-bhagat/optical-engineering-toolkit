"""
metrics.py

Metric registry for plotting.

Purpose
-------
Defines the optical performance metrics that can be visualized by the
plotting subsystem.

Each metric specifies

- attribute path inside an OpticalCase
- axis labels
- plot title
- output filename

Higher-level plotting modules iterate over this registry to generate
all required figures without hardcoding individual plotting calls.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PlotMetric:
    """
    Definition of one engineering plotting metric.
    """

    attribute_path: str
    """
    Dot-separated attribute path within an OpticalCase.

    Example
    -------
    psf_analysis.fwhm_x_um
    """

    ylabel: str
    """
    Y-axis label.
    """

    title: str
    """
    Figure title.
    """

    filename: str
    """
    Output image filename.
    """


# ---------------------------------------------------------------------
# Thermal Plot Registry
# ---------------------------------------------------------------------

THERMAL_PLOT_METRICS: tuple[PlotMetric, ...] = (

    # -------------------------------------------------------------
    # Slice-Based PSF
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="psf_analysis.fwhm_x_um",
        ylabel="PSF FWHM X (µm)",
        title="PSF FWHM X vs Temperature",
        filename="psf_fwhm_x_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.fwhm_y_um",
        ylabel="PSF FWHM Y (µm)",
        title="PSF FWHM Y vs Temperature",
        filename="psf_fwhm_y_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.equivalent_fwhm_um",
        ylabel="Equivalent PSF FWHM (µm)",
        title="Equivalent PSF FWHM vs Temperature",
        filename="equivalent_psf_fwhm_vs_temperature.png",
    ),

    # -------------------------------------------------------------
    # Spot Diagram
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="spot_field.rms_radius_um",
        ylabel="RMS Spot Radius (µm)",
        title="RMS Spot Radius vs Temperature",
        filename="rms_spot_radius_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="spot_field.rms_x_um",
        ylabel="RMS Spot X Size (µm)",
        title="RMS Spot X Size vs Temperature",
        filename="rms_spot_x_size_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="spot_field.rms_y_um",
        ylabel="RMS Spot Y Size (µm)",
        title="RMS Spot Y Size vs Temperature",
        filename="rms_spot_y_size_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="spot_field.max_radius_um",
        ylabel="Maximum Spot Radius (µm)",
        title="Maximum Spot Radius vs Temperature",
        filename="maximum_spot_radius_vs_temperature.png",
    ),

    # -------------------------------------------------------------
    # Half-Maximum Geometry
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="psf_analysis.major_axis_um",
        ylabel="Major Axis (µm)",
        title="Half-Maximum Major Axis vs Temperature",
        filename="major_axis_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.minor_axis_um",
        ylabel="Minor Axis (µm)",
        title="Half-Maximum Minor Axis vs Temperature",
        filename="minor_axis_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.equivalent_diameter_um",
        ylabel="Equivalent Diameter (µm)",
        title="Half-Maximum Equivalent Diameter vs Temperature",
        filename="equivalent_diameter_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.orientation_deg",
        ylabel="Orientation (°)",
        title="Half-Maximum Orientation vs Temperature",
        filename="orientation_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.eccentricity",
        ylabel="Eccentricity",
        title="Half-Maximum Eccentricity vs Temperature",
        filename="eccentricity_vs_temperature.png",
    ),

    # -------------------------------------------------------------
    # Encircled Energy
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="psf_analysis.ee50_radius_um",
        ylabel="EE50 Radius (µm)",
        title="EE50 Radius vs Temperature",
        filename="ee50_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.ee80_radius_um",
        ylabel="EE80 Radius (µm)",
        title="EE80 Radius vs Temperature",
        filename="ee80_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.ee90_radius_um",
        ylabel="EE90 Radius (µm)",
        title="EE90 Radius vs Temperature",
        filename="ee90_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="psf_analysis.ee95_radius_um",
        ylabel="EE95 Radius (µm)",
        title="EE95 Radius vs Temperature",
        filename="ee95_vs_temperature.png",
    ),

    # -------------------------------------------------------------
    # MTF (17.2 lp/mm)
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="mtf_data.tangential_17_2",
        ylabel="Tangential MTF",
        title="Tangential MTF @ 17.2 lp/mm vs Temperature",
        filename="tangential_mtf_17_2_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="mtf_data.sagittal_17_2",
        ylabel="Sagittal MTF",
        title="Sagittal MTF @ 17.2 lp/mm vs Temperature",
        filename="sagittal_mtf_17_2_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="mtf_analysis.mean_17_2",
        ylabel="Mean MTF",
        title="Mean MTF @ 17.2 lp/mm vs Temperature",
        filename="mean_mtf_17_2_vs_temperature.png",
    ),

    # -------------------------------------------------------------
    # MTF (41.7 lp/mm)
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="mtf_data.tangential_41_7",
        ylabel="Tangential MTF",
        title="Tangential MTF @ 41.7 lp/mm vs Temperature",
        filename="tangential_mtf_41_7_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="mtf_data.sagittal_41_7",
        ylabel="Sagittal MTF",
        title="Sagittal MTF @ 41.7 lp/mm vs Temperature",
        filename="sagittal_mtf_41_7_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="mtf_analysis.mean_41_7",
        ylabel="Mean MTF",
        title="Mean MTF @ 41.7 lp/mm vs Temperature",
        filename="mean_mtf_41_7_vs_temperature.png",
    ),

    # -------------------------------------------------------------
    # Wavefront
    # -------------------------------------------------------------

    PlotMetric(
        attribute_path="psf_data.strehl_ratio",
        ylabel="Strehl Ratio",
        title="Strehl Ratio vs Temperature",
        filename="strehl_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="wavefront_analysis.rms_waves",
        ylabel="RMS Wavefront Error (waves)",
        title="RMS Wavefront Error vs Temperature",
        filename="rms_wavefront_error_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="wavefront_analysis.peak_to_valley_waves",
        ylabel="Peak-to-Valley Wavefront Error (waves)",
        title="Peak-to-Valley Wavefront Error vs Temperature",
        filename="pv_wavefront_error_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="wavefront_analysis.mean_waves",
        ylabel="Mean Wavefront (waves)",
        title="Mean Wavefront vs Temperature",
        filename="mean_wavefront_vs_temperature.png",
    ),

    PlotMetric(
        attribute_path="wavefront_analysis.standard_deviation_waves",
        ylabel="Wavefront Standard Deviation (waves)",
        title="Wavefront Standard Deviation vs Temperature",
        filename="wavefront_standard_deviation_vs_temperature.png",
    ),

)

# ---------------------------------------------------------------------
# Monte Carlo Plot Registry
# ---------------------------------------------------------------------

MONTE_CARLO_PLOT_METRICS: tuple[PlotMetric, ...] = tuple(

    PlotMetric(
        attribute_path=metric.attribute_path,
        ylabel=metric.ylabel,
        title=metric.title.replace(
            "vs Temperature",
            "vs Representative Trial",
        ),
        filename=metric.filename.replace(
            "_vs_temperature",
            "_vs_representative_trial",
        ),
    )

    for metric in THERMAL_PLOT_METRICS

)

# ---------------------------------------------------------------------
# Baseline Plot Registry
# ---------------------------------------------------------------------

BASELINE_PLOT_METRICS: tuple[PlotMetric, ...] = tuple(

    PlotMetric(
        attribute_path=metric.attribute_path,
        ylabel=metric.ylabel,
        title=metric.title.replace(
            "vs Temperature",
            "vs Wavelength",
        ),
        filename=metric.filename.replace(
            "_vs_temperature",
            "_vs_wavelength",
        ),
    )

    for metric in THERMAL_PLOT_METRICS

)

# ---------------------------------------------------------------------
# Public Helpers
# ---------------------------------------------------------------------

def resolve_attribute(
    obj: Any,
    attribute_path: str,
) -> Any:
    """
    Resolve a dot-separated attribute path.

    Parameters
    ----------
    obj
        Root object.

    attribute_path
        Dot-separated attribute path.

    Returns
    -------
    Any
        Attribute value.

    Raises
    ------
    AttributeError
        If any component of the attribute path does not exist.
    """

    current = obj

    for attribute in attribute_path.split("."):

        if current is None:
            raise AttributeError(
                f"Unable to resolve attribute path "
                f"'{attribute_path}'."
            )

        try:

            current = getattr(
                current,
                attribute,
            )

        except AttributeError as exc:

            raise AttributeError(
                f"Unable to resolve attribute path "
                f"'{attribute_path}'. "
                f"Missing attribute '{attribute}'."
            ) from exc

    return current