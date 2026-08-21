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

BASELINE_INPUT_DIRECTORY = (
    INPUT_DIRECTORY
    / "baseline"
)

MONTE_CARLO_INPUT_DIRECTORY = INPUT_DIRECTORY / "monte-carlo"

TOLERANCE_INPUT_DIRECTORY = INPUT_DIRECTORY / "tolerance"

#
# Future analyses
#
# STRAY_LIGHT_INPUT_DIRECTORY = INPUT_DIRECTORY / "straylight"
# DISTORTION_INPUT_DIRECTORY = INPUT_DIRECTORY / "distortion"
# FIELD_CURVATURE_INPUT_DIRECTORY = INPUT_DIRECTORY / "field_curvature"

# ---------------------------------------------------------------------
# LaTeX Output Paths
# ---------------------------------------------------------------------

LATEX_OUTPUT_DIRECTORY = (
    OUTPUT_DIRECTORY
    / "latex"
)

THERMAL_LATEX_OUTPUT_DIRECTORY = (
    LATEX_OUTPUT_DIRECTORY
    / "thermal"
)

BASELINE_LATEX_OUTPUT_DIRECTORY = (
    LATEX_OUTPUT_DIRECTORY
    / "baseline"
)

MONTE_CARLO_LATEX_OUTPUT_DIRECTORY = (
    LATEX_OUTPUT_DIRECTORY
    / "monte_carlo"
)

LATEX_METRICS_DIRECTORY_NAME = "metrics"

LATEX_REPORT_DIRECTORY_NAME = "report"

# ---------------------------------------------------------------------
# Analysis Output Paths
# ---------------------------------------------------------------------

THERMAL_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "thermal"

BASELINE_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "baseline"

MONTE_CARLO_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "monte_carlo"

TOLERANCE_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "tolerance"

# ---------------------------------------------------------------------
# Report Output Paths
# ---------------------------------------------------------------------

THERMAL_REPORT_OUTPUT_DIRECTORY = (
    THERMAL_OUTPUT_DIRECTORY
    / "reports"
)

BASELINE_REPORT_OUTPUT_DIRECTORY = (
    BASELINE_OUTPUT_DIRECTORY
    / "reports"
)

MONTE_CARLO_REPORT_OUTPUT_DIRECTORY = (
    MONTE_CARLO_OUTPUT_DIRECTORY
    / "reports"
)

SUMMARY_DIRECTORY_NAME = "summary"

METRICS_DIRECTORY_NAME = "metrics"

REPORT_DIRECTORY_NAME = "report"

SUMMARY_CSV_FILENAME = "summary.csv"

SUMMARY_EXCEL_FILENAME = "summary.xlsx"

THERMAL_PRIMARY_DATASET = "Nominal"

MONTE_CARLO_PRIMARY_DATASET = "Worst"

# STRAY_LIGHT_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "straylight"
# DISTORTION_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "distortion"
# FIELD_CURVATURE_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY / "field_curvature"

# ---------------------------------------------------------------------
# Zemax Report Filenames
# ---------------------------------------------------------------------

PSF_REPORT = "psf.txt"

MTF_REPORT = "mtf.txt"

SPOT_REPORT = "spot.txt"

WAVEFRONT_REPORT = "wavefront.txt"

#
# Future reports
#
# DISTORTION_REPORT = "distortion.txt"
# FIELD_CURVATURE_REPORT = "field_curvature.txt"

# ---------------------------------------------------------------------
# Case Naming
# ---------------------------------------------------------------------

BASELINE_CASE_PREFIX = "BL"

THERMAL_CASE_PREFIX = "T"

MONTE_CARLO_CASE_PREFIX = "MC"

TOLERANCE_CASE_PREFIX = "TL"

# ---------------------------------------------------------------------
# Engineering Constants
# ---------------------------------------------------------------------

MTF_ANALYSIS_FREQUENCIES = (
    17.2,
    41.7,
)
"""
Spatial frequencies (cycles/mm) used for MTF evaluation and reporting.

The first frequency characterizes low-to-mid spatial-frequency
performance, while the second characterizes higher spatial-frequency
performance.
"""

EE_TARGET = 0.80
"""
Default encircled energy target (80%).
"""

# ---------------------------------------------------------------------
# Baseline Analysis
# ---------------------------------------------------------------------

BASELINE_TEMPERATURE_C = 20.0
"""
Reference temperature used for the baseline optical analysis.

Only thermal operating points corresponding to this temperature are
used when generating baseline wavelength-dependent results.
"""

# ---------------------------------------------------------------------
# Thermal Reporting
# ---------------------------------------------------------------------

THERMAL_REPORT_RANGE_NAMES = {

    "nominal": "Nominal",

    "operational": "Operational",

    "survival": "Extended",
}
"""
Display names used for thermal report tables.

The underlying thermal analysis continues to use the dataset name
"survival". Only report generation presents this range as
"Extended".
"""

# ---------------------------------------------------------------------
# Report Grouping
# ---------------------------------------------------------------------

THERMAL_REPORT_GROUP_COLUMN = "Dataset"

MONTE_CARLO_REPORT_GROUP_COLUMN = "Dataset"
"""
Grouping columns used by the statistical reporting pipeline.
"""

# ---------------------------------------------------------------------
# Monte Carlo Representative Trial Order
# ---------------------------------------------------------------------

MONTE_CARLO_DATASET_ORDER = (

    "Best",

    "P02",
    "P10",
    "P20",
    "P50",

    "Mean",

    "P80",
    "P90",
    "P98",

    "Worst",
)
"""
Canonical ordering of representative Monte Carlo trials.

This ordering is used for categorical plotting and reporting so that
representative trials are presented consistently across figures and
tables.

Datasets not listed here are appended after the known entries in
alphabetical order.
"""

# ---------------------------------------------------------------------
# Report Metrics
# ---------------------------------------------------------------------

REPORT_METRICS = (

    (
        "psf",
        "Equivalent PSF FWHM",
        "Equivalent PSF FWHM (µm)",
    ),

    (
        "ee80",
        "EE80 Radius",
        "EE80 Radius (µm)",
    ),

    (
        "rms_spot",
        "RMS Spot Radius",
        "RMS Spot Radius (µm)",
    ),

    (
        "mtf17",
        "Mean MTF (17.2 cycles/mm)",
        f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm",
    ),

    (
        "mtf42",
        "Mean MTF (41.7 cycles/mm)",
        f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm",
    ),

    (
        "strehl",
        "Strehl Ratio",
        "Strehl Ratio",
    ),

    (
        "wavefront_rms_waves",
        "Wavefront RMS (waves)",
        "Wavefront RMS (waves)",
    ),

    (
        "wavefront_rms_nm",
        "Wavefront RMS (nm)",
        "Wavefront RMS (nm)",
    ),
)
"""
Report metrics.

Each entry contains

    (
        output_name,
        report_title,
        results_column,
    )
"""

SUMMARY_STATISTICS = (

    "Min",

    "Max",

    "Mean",

    "Std. Dev.",
)
"""
Canonical statistical summary columns used by thermal and
Monte Carlo report tables.
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

# ---------------------------------------------------------------------
# Single-Series Plots
# ---------------------------------------------------------------------

PLOT_LINE_WIDTH = 2.0
"""
Line width for single-series plots.
"""

PLOT_MARKER = "o"
"""
Marker style for single-series plots.
"""

PLOT_MARKER_SIZE = 5
"""
Marker size for single-series plots.
"""

# ---------------------------------------------------------------------
# Multi-Series Plots
# ---------------------------------------------------------------------

MULTI_PLOT_LINE_WIDTH = 0.75
"""
Line width for multi-series plots.
"""

MULTI_PLOT_MARKER = "o"
"""
Marker style for multi-series plots.
"""

MULTI_PLOT_MARKER_SIZE = 3
"""
Marker size for multi-series plots.
"""

# ---------------------------------------------------------------------
# Axes
# ---------------------------------------------------------------------

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

# ---------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------

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

# ---------------------------------------------------------------------
# Field Colors
# ---------------------------------------------------------------------

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

LATEX_FILE_EXTENSION = ".tex"

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
    "Dataset",
    "Wavelength (µm)",
    "Field",
    "Temperature (°C)",
    "Statistical Case",

    # -------------------------------------------------------------
    # Spot Diagram
    # -------------------------------------------------------------

    "Spot Field X (deg)",
    "Spot Field Y (deg)",

    "Spot Image X (mm)",
    "Spot Image Y (mm)",

    "RMS Spot Radius (µm)",
    "RMS Spot X Size (µm)",
    "RMS Spot Y Size (µm)",

    "Maximum Spot Radius (µm)",

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
    # Airy Reference and PSF Wings
    # -------------------------------------------------------------

    "Airy Radius (µm)",
    "Energy Within Airy Radius",
    "PSF Wing Fraction",

    # -------------------------------------------------------------
    # MTF
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # MTF (17.2 lp/mm)
    # -------------------------------------------------------------

    f"Tangential MTF @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm",
    f"Sagittal MTF @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm",
    f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm",

    # -------------------------------------------------------------
    # MTF (41.7 lp/mm)
    # -------------------------------------------------------------

    f"Tangential MTF @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm",
    f"Sagittal MTF @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm",
    f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm",

    # -------------------------------------------------------------
    # Strehl Ratio
    # -------------------------------------------------------------

    "Strehl Ratio",

    # -------------------------------------------------------------
    # Wavefront Error
    # -------------------------------------------------------------

    "Wavefront PV (waves)",
    "Wavefront RMS (waves)",

    "Wavefront PV (nm)",
    "Wavefront RMS (nm)",

    # -------------------------------------------------------------
    # Wavefront Statistics
    # -------------------------------------------------------------

    "Minimum Wavefront (waves)",
    "Maximum Wavefront (waves)",
    "Mean Wavefront (waves)",
    "Wavefront Standard Deviation (waves)",
)

# ---------------------------------------------------------------------
# LaTeX Export
# ---------------------------------------------------------------------

LATEX_TOTAL_COLUMN_WIDTH = 0.845

LATEX_DECIMALS = CSV_DECIMALS

LATEX_USE_LONGTABLE = True

LATEX_CONTINUED_HEADER = (
    r"\multicolumn{{{columns}}}{{c}}"
    r"{{{\bfseries Table \thetable\ Continued from previous page}}}\\"
)

LATEX_CONTINUED_FOOTER = (
    r"\multicolumn{{{columns}}}{{r}}"
    r"{{Continued on next page}}\\"
)

LATEX_TABLE_METADATA = {

    "psf": {
        "caption": "Equivalent PSF FWHM statistics.",
        "label": "tab:psf_statistics",
    },

    "ee80": {
        "caption": "EE80 radius statistics.",
        "label": "tab:ee80_statistics",
    },

    "rms_spot": {
        "caption": "RMS spot radius statistics.",
        "label": "tab:rms_spot_statistics",
    },

    "mtf17": {
        "caption": "Mean MTF statistics at 17.2 cycles/mm.",
        "label": "tab:mtf17_statistics",
    },

    "mtf42": {
        "caption": "Mean MTF statistics at 41.7 cycles/mm.",
        "label": "tab:mtf42_statistics",
    },

    "strehl": {
        "caption": "Strehl ratio statistics.",
        "label": "tab:strehl_statistics",
    },

    "wavefront_rms_waves": {
        "caption": "Wavefront RMS statistics (waves).",
        "label": "tab:wavefront_rms_waves_statistics",
    },

    "wavefront_rms_nm": {
        "caption": "Wavefront RMS statistics (nm).",
        "label": "tab:wavefront_rms_nm_statistics",
    },
}

LATEX_COLUMN_PADDING = 0.95

LATEX_FIRST_COLUMN_WIDTH = 0.18

LATEX_NUMERIC_COLUMN_WIDTH = 0.14


# ---------------------------------------------------------------------
# Report Figure Metadata
# ---------------------------------------------------------------------

REPORT_FIGURES = {

    "rms_spot": {

        "column": "RMS Spot Radius (µm)",

        "title": "Root Mean Square (RMS) Spot Radius",

        "ylabel": "RMS Spot Radius (µm)",

        "legend": "Field",

    },

    "psf": {

        "column": "Equivalent PSF FWHM (µm)",

        "title": "Equivalent Huygens PSF FWHM",

        "ylabel": "Equivalent PSF FWHM (µm)",

        "legend": "Field",

    },

    "ee80": {

        "column": "EE80 Radius (µm)",

        "title": "80% Encircled Energy (EE80) Radius",

        "ylabel": "EE80 Radius (µm)",

        "legend": "Field",

    },

    "ee90": {

        "column": "EE90 Radius (µm)",

        "title": "90% Encircled Energy (EE90) Radius",

        "ylabel": "EE90 Radius (µm)",

        "legend": "Field",

    },

    "airy_energy": {

        "column": "Energy Within Airy Radius",

        "title": "Fraction of PSF Energy Within Airy Disk",

        "ylabel": "Encircled Energy Fraction",

        "legend": "Field",

    },

    "mtf17": {

        "column": f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm",

        "title": (
            f"Mean Modulation Transfer Function (MTF)"
            f" @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm"
        ),

        "ylabel": f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[0]:.1f} cycles/mm",

        "legend": "Field",

    },

    "mtf42": {

        "column": f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm",

        "title": (
            f"Mean Modulation Transfer Function (MTF)"
            f" @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm"
        ),

        "ylabel": f"Mean MTF @ {MTF_ANALYSIS_FREQUENCIES[1]:.1f} cycles/mm",

        "legend": "Field",

    },

    "wavefront_rms": {

        "column": "Wavefront RMS (waves)",

        "title": "Root Mean Square (RMS) Wavefront Error",

        "ylabel": "Wavefront RMS (waves)",

        "legend": "Field",

    },

    "strehl": {

        "column": "Strehl Ratio",

        "title": "Strehl Ratio",

        "ylabel": "Strehl Ratio",

        "legend": "Field",

    },

}
"""
Publication-quality report figures.

Each entry contains

(
    output_name,
    results_column,
    y_axis_label,
)

The reporting pipeline automatically generates

    • all-field figure
    • summary figure

for every metric.

Summary figures additionally include

    • Best
    • Mean
    • Worst

together with any physical reference curve applicable to that metric
(e.g. diffraction limit, OTA allocation, Strehl = 1).

Thermal and Monte Carlo analyses reuse the same figure definitions while
changing the grouping dimension (temperature or representative trial).
"""


APERTURE_MM = 500.0

FOCAL_RATIO = 24.0

FOCAL_LENGTH_MM = (
    APERTURE_MM
    * FOCAL_RATIO
)

CENTRAL_OBSCURATION = 0.14

PIXEL_SIZE_UM = 12.0

SYSTEM_PSF_REQUIREMENT_UM = 58.178

OPTICAL_ALLOCATION_UM = 5.8178

# ---------------------------------------------------------------------
# Report Figure Styling
# ---------------------------------------------------------------------

REPORT_FIGURE_SIZE = (9.0, 5.5)
"""
Default figure size for publication-quality report figures.
"""

REPORT_FIGURE_DPI = 300
"""
Resolution of exported report figures.
"""

REPORT_LINE_WIDTH = 1.5
"""
Default line width for ordinary data series.
"""

REPORT_REFERENCE_LINE_WIDTH = 1.75
"""
Line width used for engineering reference curves.
"""

REPORT_MEAN_LINE_WIDTH = 2.5
"""
Line width used to emphasize mean or representative curves.
"""

REPORT_MARKER = ""
"""
Default marker style for report figures.
"""

REPORT_MARKER_SIZE = 4
"""
Default marker size for report figures.
"""

REPORT_REFERENCE_LINE_STYLE = "--"
"""
Line style used for engineering reference curves.
"""

REPORT_REQUIREMENT_LINE_STYLE = ":"
"""
Line style used for requirement or specification limits.
"""

REPORT_GRID_ALPHA = 0.4
"""
Grid transparency for report figures.
"""

REPORT_GRID_LINESTYLE = ":"
"""
Grid line style for report figures.
"""

REPORT_GRID_LINE_WIDTH = 0.6
"""
Grid line width for report figures.
"""

REPORT_LEGEND_LOCATION = "center left"
"""
Legend location.
"""

REPORT_LEGEND_BBOX = (1.02, 0.5)
"""
Legend anchor position.
"""

REPORT_LEGEND_FONT_SIZE = 8
"""
Legend font size.
"""

REPORT_LEGEND_TITLE_FONT_SIZE = 9
"""
Legend title font size.
"""

REPORT_LEGEND_FRAME = True
"""
Whether the legend frame is shown.
"""

REPORT_TITLE_PADDING = 12
"""
Padding between the axes and title.
"""

REPORT_COLORS = {
    "data": "#1f77b4",
    "mean": "#000000",
    "best": "#2ca02c",
    "worst": "#d62728",
    "reference": "#7f7f7f",
    "requirement": "#9467bd",
}
"""
Canonical colors used by publication-quality report figures.

These colors are intentionally independent of the engineering plotting
pipeline.
"""

# ---------------------------------------------------------------------
# Report Wavelength Colors
# ---------------------------------------------------------------------

REPORT_WAVELENGTH_COLORS = [

    "#081D58",  # 200.0 nm - Very Dark Blue
    "#253494",  # 238.1 nm - Dark Blue
    "#225EA8",  # 243.1 nm - Medium Blue
    "#1D91C0",  # 248.1 nm - Cyan Blue
    "#7FCDBB",  # 260.0 nm - Pale Blue-Cyan

    "#00ACC1",  # 298.9 nm  - Cyan
    "#00897B",  # 303.9 nm  - Teal
    "#43A047",  # 308.9 nm  - Green
    "#7CB342",  # 310.0 nm  - Yellow-Green

    "#C0CA33",  # 350.0 nm  - Lime
    "#FDD835",  # 383.9 nm  - Yellow
    "#FFB300",  # 388.9 nm  - Amber
    "#FB8C00",  # 393.9 nm  - Orange
    "#F4511E",  # 400.0 nm  - Orange-Red

    "#E53935",  # 450.0 nm  - Red
    "#8E2424",  # 500.0 nm  - Dark Red
]

ENGINEERING_WAVELENGTH_UM = 0.200
STREHL_CRITERION = 0.80
MTF42_CRITERION = 0.50
# ---------------------------------------------------------------------
# PSF Engineering Acceptance Criteria
# ---------------------------------------------------------------------

PSF_NOMINAL_MONTE_CARLO_LIMIT_UM = 6.300
"""
Maximum allowable PSF FWHM for the nominal + Monte Carlo case
at the governing engineering wavelength of 200 nm.
"""

PSF_NOMINAL_THERMAL_LIMIT_UM = 6.953
"""
Maximum allowable PSF FWHM for the nominal + thermal case
at the governing engineering wavelength of 200 nm.
"""

THERMAL_ACTIVE_DATASET = None
"""
Dataset to process.

None        -> Process all thermal datasets.
"nominal"   -> Process only nominal.
"operational" -> Process only operational.
"survival"  -> Process only survival.
"""

BASELINE_CONFIGURATION_NAMES: dict[int, str] = {

    1: "No Filter",

    2: "BB1",
    3: "BB2",
    4: "BB3",
    5: "BB4",
    6: "BB5",
    7: "BB6",

    8: "NB1",
    9: "NB2",
    10: "NB3",
}
