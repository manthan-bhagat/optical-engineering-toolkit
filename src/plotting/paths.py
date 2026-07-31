"""
paths.py

Output path utilities for the Zemax Optical Analysis Toolkit.

Purpose
-------
Provides a centralized interface for constructing output directories
and filenames.

All modules should obtain output paths through this module instead of
building directory structures manually.

Output hierarchy
----------------

output/
│
├── thermal/
│   ├── 200nm/
│   │   ├── results.csv
│   │   ├── results.xlsx
│   │   └── figures/
│   │       ├── combined/
│   │       └── individual/
│   │           ├── field_01/
│   │           ├── field_02/
│   │           └── ...
│   │
│   ├── 250nm/
│   └── ...
│
├── monte_carlo/
└── tolerance/

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import OUTPUT_DIRECTORY
from src.models.analysis_type import AnalysisType

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _format_wavelength(
    wavelength_um: float,
) -> str:
    """
    Format wavelength directory name.

    Parameters
    ----------
    wavelength_um
        Wavelength in micrometres.

    Returns
    -------
    str
        Directory name.

    Examples
    --------
    0.200 -> "200nm"
    0.250 -> "250nm"
    0.486 -> "486nm"
    """

    wavelength_nm = round(
        wavelength_um * 1000
    )

    return f"{wavelength_nm}nm"


def _format_field(
    field_index: int,
) -> str:
    """
    Format field directory.

    Example
    -------
    field_01
    """

    return f"field_{field_index:02d}"


# ---------------------------------------------------------------------
# Analysis Directories
# ---------------------------------------------------------------------


def get_analysis_directory(
    analysis_type: AnalysisType,
) -> Path:
    """
    Return the root directory for an analysis.

    Examples
    --------
    output/thermal
    output/monte_carlo
    output/tolerance
    """

    return (
        OUTPUT_DIRECTORY
        / analysis_type.value
    )


def get_wavelength_directory(
    analysis_type: AnalysisType,
    wavelength_um: float,
) -> Path:
    """
    Return the wavelength output directory.
    """

    return (
        get_analysis_directory(
            analysis_type
        )
        / _format_wavelength(
            wavelength_um
        )
    )


# ---------------------------------------------------------------------
# Export Files
# ---------------------------------------------------------------------


def get_csv_path(
    analysis_type: AnalysisType,
    wavelength_um: float,
) -> Path:
    """
    Path to results.csv.
    """

    return (
        get_wavelength_directory(
            analysis_type,
            wavelength_um,
        )
        / "results.csv"
    )


def get_excel_path(
    analysis_type: AnalysisType,
    wavelength_um: float,
) -> Path:
    """
    Path to results.xlsx.
    """

    return (
        get_wavelength_directory(
            analysis_type,
            wavelength_um,
        )
        / "results.xlsx"
    )


# ---------------------------------------------------------------------
# Figure Directories
# ---------------------------------------------------------------------


def get_figures_directory(
    analysis_type: AnalysisType,
    wavelength_um: float,
) -> Path:
    """
    Return figures directory.
    """

    return (
        get_wavelength_directory(
            analysis_type,
            wavelength_um,
        )
        / "figures"
    )


def get_combined_figures_directory(
    analysis_type: AnalysisType,
    wavelength_um: float,
) -> Path:
    """
    Return combined figures directory.
    """

    return (
        get_figures_directory(
            analysis_type,
            wavelength_um,
        )
        / "combined"
    )


def get_individual_figures_directory(
    analysis_type: AnalysisType,
    wavelength_um: float,
) -> Path:
    """
    Return individual figures directory.
    """

    return (
        get_figures_directory(
            analysis_type,
            wavelength_um,
        )
        / "individual"
    )


def get_field_directory(
    analysis_type: AnalysisType,
    wavelength_um: float,
    field_index: int,
) -> Path:
    """
    Return directory for one field.

    Example
    -------
    output/
        thermal/
            200nm/
                figures/
                    individual/
                        field_01/
    """

    return (
        get_individual_figures_directory(
            analysis_type,
            wavelength_um,
        )
        / _format_field(
            field_index
        )
    )


# ---------------------------------------------------------------------
# Figure Files
# ---------------------------------------------------------------------


def get_combined_plot_path(
    analysis_type: AnalysisType,
    wavelength_um: float,
    filename: str,
) -> Path:
    """
    Path to one combined plot.
    """

    return (
        get_combined_figures_directory(
            analysis_type,
            wavelength_um,
        )
        / filename
    )


def get_field_plot_path(
    analysis_type: AnalysisType,
    wavelength_um: float,
    field_index: int,
    filename: str,
) -> Path:
    """
    Path to one individual field plot.
    """

    return (
        get_field_directory(
            analysis_type,
            wavelength_um,
            field_index,
        )
        / filename
    )