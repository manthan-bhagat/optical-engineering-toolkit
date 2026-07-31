"""
config.py

Central configuration for the Zemax Optical Analysis Toolkit.

Purpose
-------
This module defines the directory structure, naming conventions,
engineering constants, export settings, and plotting defaults used
throughout the toolkit.

Every module should import configuration values from this file instead
of hardcoding project-wide conventions.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Project Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(".")

INPUT_DIRECTORY = PROJECT_ROOT / "input"

OUTPUT_DIRECTORY = PROJECT_ROOT / "output"

# ---------------------------------------------------------------------
# Analysis Input Paths
# ---------------------------------------------------------------------

THERMAL_INPUT_DIRECTORY = INPUT_DIRECTORY / "thermal"

MONTE_CARLO_INPUT_DIRECTORY = INPUT_DIRECTORY / "montecarlo"

TOLERANCE_INPUT_DIRECTORY = INPUT_DIRECTORY / "tolerance"

#
# Future analyses
#
# STRAY_LIGHT_INPUT_DIRECTORY = INPUT_DIRECTORY / "straylight"
# DISTORTION_INPUT_DIRECTORY = INPUT_DIRECTORY / "distortion"
# FIELD_CURVATURE_INPUT_DIRECTORY = INPUT_DIRECTORY / "field_curvature"

# ---------------------------------------------------------------------
# Analysis Output Paths
# ---------------------------------------------------------------------

THERMAL_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "thermal"

MONTE_CARLO_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "montecarlo"

TOLERANCE_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "tolerance"

# STRAY_LIGHT_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "straylight"
# DISTORTION_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "distortion"
# FIELD_CURVATURE_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "field_curvature"

# ---------------------------------------------------------------------
# Zemax Report Filenames
# ---------------------------------------------------------------------

PSF_REPORT = "psf.txt"

MTF_REPORT = "mtf.txt"

RMS_SPOT_REPORT = "rms_spot.txt"

WAVEFRONT_REPORT = "wavefront.txt"

#
# Future reports
#
# DISTORTION_REPORT = "distortion.txt"
# FIELD_CURVATURE_REPORT = "field_curvature.txt"

# ---------------------------------------------------------------------
# Case Naming
# ---------------------------------------------------------------------

THERMAL_CASE_PREFIX = "T"

MONTE_CARLO_CASE_PREFIX = "MC"

TOLERANCE_CASE_PREFIX = "TL"

# ---------------------------------------------------------------------
# Engineering Constants
# ---------------------------------------------------------------------

MTF_EVALUATION_FREQUENCY = 42.0
"""
Spatial frequency (cycles/mm) used for MTF evaluation and reporting.
"""

EE_TARGET = 0.80
"""
Default encircled energy target (80%).
"""

# ---------------------------------------------------------------------
# Plot Settings
# ---------------------------------------------------------------------

FIGURE_SIZE = (9, 5.5)
"""
Default matplotlib figure size in inches.
"""

FIGURE_DPI = 300
"""
Output figure resolution.
"""

PLOT_LINE_WIDTH = 2.0
"""
Line width for single-series plots.
"""

MULTI_PLOT_LINE_WIDTH = 0.5
"""
Line width for multi-series plots.
"""

PLOT_MARKER = "o"
"""
Marker style for single-series plots.
"""

PLOT_MARKER_SIZE = 5
"""
Marker size for single-series plots.
"""

GRID_ALPHA = 0.5
"""
Grid transparency.
"""

GRID_LINESTYLE = ":"
"""
Grid line style.
"""

GRID_LINE_WIDTH = 0.6
"""
Grid line width.
"""

LEGEND_LOCATION = "center left"
"""
Legend anchor location.
"""

LEGEND_BBOX = (1.02, 0.5)
"""
Legend anchor position.
"""

LEGEND_FONT_SIZE = 8
"""
Legend font size.
"""

LEGEND_TITLE_FONT_SIZE = 9
"""
Legend title font size.
"""

LEGEND_FRAME = True
"""
Draw a border around the legend.
"""

FIELD_COLORS = [
    "#1f77b4",  # Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Olive
    "#17becf",  # Cyan
    "#000000",  # Black
    "#1f3a93",  # Navy
]

# ---------------------------------------------------------------------
# Export Formatting
# ---------------------------------------------------------------------

CSV_DECIMALS = 3
"""
Number of decimal places used when exporting numerical values.
"""

# ---------------------------------------------------------------------
# Export Columns
# ---------------------------------------------------------------------

RESULT_COLUMNS = (

    # -------------------------------------------------------------
    # Case Information
    # -------------------------------------------------------------

    "Case ID",
    "Analysis Type",
    "Temperature (°C)",
    "Statistical Case",

    # -------------------------------------------------------------
    # Spot Size
    # -------------------------------------------------------------

    "RMS Spot Radius (µm)",

    # -------------------------------------------------------------
    # Slice-Based PSF Metrics
    # -------------------------------------------------------------

    "PSF FWHM X (µm)",
    "PSF FWHM Y (µm)",
    "Equivalent PSF FWHM (µm)",

    # -------------------------------------------------------------
    # Half-Maximum Region Geometry
    # -------------------------------------------------------------

    "Half-Maximum Major Axis (µm)",
    "Half-Maximum Minor Axis (µm)",
    "Half-Maximum Equivalent Diameter (µm)",
    "Half-Maximum Orientation (°)",
    "Half-Maximum Eccentricity",

    # -------------------------------------------------------------
    # Encircled Energy
    # -------------------------------------------------------------

    "EE50 Radius (µm)",
    "EE80 Radius (µm)",
    "EE90 Radius (µm)",
    "EE95 Radius (µm)",

    # -------------------------------------------------------------
    # MTF
    # -------------------------------------------------------------

    f"Tangential MTF @ {MTF_EVALUATION_FREQUENCY:.0f} cycles/mm",
    f"Sagittal MTF @ {MTF_EVALUATION_FREQUENCY:.0f} cycles/mm",
    f"Mean MTF @ {MTF_EVALUATION_FREQUENCY:.0f} cycles/mm",

    # -------------------------------------------------------------
    # Wavefront
    # -------------------------------------------------------------

    "Strehl Ratio",
    "RMS WFE",
)