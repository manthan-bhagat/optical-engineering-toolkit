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
│   ├── survival/
│   │   ├── 200nm/
│   │   │   ├── results.csv
│   │   │   ├── results.xlsx
│   │   │   └── figures/
│   │   │       ├── combined/
│   │   │       └── individual/
│   │   │           ├── field_01/
│   │   │           ├── field_02/
│   │   │           └── ...
│   │   └── ...
│   │
│   ├── operational/
│   └── nominal/
│
├── montecarlo/
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
from src.models.optical_case import OpticalCase
from src.models.analysis_type import AnalysisType

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _format_wavelength(
    wavelength_um: float,
) -> str:
    """
    Format wavelength directory name.

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
    case: OpticalCase,
) -> Path:
    """
    Return the root output directory for an analysis.

    Examples
    --------
    output/thermal
    output/montecarlo
    output/tolerance
    """

    return (
        OUTPUT_DIRECTORY
        / case.analysis_type.value
    )


def get_dataset_directory(
    case: OpticalCase,
) -> Path:
    """
    Return the dataset output directory.

    Thermal
    -------
    output/
        thermal/
            survival/

    Other analyses
    --------------
    If no dataset is defined, the analysis directory is returned.
    """

    directory = get_analysis_directory(case)

    if case.analysis_type == AnalysisType.THERMAL:

        if not case.dataset:
            raise ValueError(
                "Thermal OpticalCase must define a dataset."
            )

    if case.dataset:

        directory /= case.dataset

    return directory


def get_wavelength_directory(
    case: OpticalCase,
) -> Path:
    """
    Return the wavelength output directory.

    Thermal
    -------
    output/
        thermal/
            survival/
                200nm/

    Analyses without wavelength metadata simply return the dataset
    directory.
    """

    directory = get_dataset_directory(case)

    if case.wavelength_um is None:
        return directory

    return (
        directory
        / _format_wavelength(
            case.wavelength_um
        )
    )

# ---------------------------------------------------------------------
# Export Files
# ---------------------------------------------------------------------


def get_csv_path(
    case: OpticalCase,
) -> Path:
    """
    Return the path to the CSV export.

    Examples
    --------
    output/
        thermal/
            survival/
                200nm/
                    results.csv
    """

    return (
        get_wavelength_directory(
            case
        )
        / "results.csv"
    )


def get_excel_path(
    case: OpticalCase,
) -> Path:
    """
    Return the path to the Excel export.

    Examples
    --------
    output/
        thermal/
            survival/
                200nm/
                    results.xlsx
    """

    return (
        get_wavelength_directory(
            case
        )
        / "results.xlsx"
    )

# ---------------------------------------------------------------------
# Figure Directories
# ---------------------------------------------------------------------


def get_figures_directory(
    case: OpticalCase,
) -> Path:
    """
    Return the figures directory.

    Examples
    --------
    output/
        thermal/
            survival/
                200nm/
                    figures/
    """

    return (
        get_wavelength_directory(
            case
        )
        / "figures"
    )


def get_combined_figures_directory(
    case: OpticalCase,
) -> Path:
    """
    Return the combined figures directory.
    """

    return (
        get_figures_directory(
            case
        )
        / "combined"
    )


def get_individual_figures_directory(
    case: OpticalCase,
) -> Path:
    """
    Return the individual figures directory.
    """

    return (
        get_figures_directory(
            case
        )
        / "individual"
    )


def get_field_directory(
    case: OpticalCase,
) -> Path:
    """
    Return the directory for one field.

    Examples
    --------
    output/
        thermal/
            survival/
                200nm/
                    figures/
                        individual/
                            field_01/
    """

    if case.field_index is None:
        raise ValueError(
            "OpticalCase does not define a field index."
        )

    return (
        get_individual_figures_directory(
            case
        )
        / _format_field(
            case.field_index
        )
    )

# ---------------------------------------------------------------------
# Figure Files
# ---------------------------------------------------------------------


def get_combined_plot_path(
    case: OpticalCase,
    filename: str,
) -> Path:
    """
    Return the path to one combined plot.

    Examples
    --------
    output/
        thermal/
            survival/
                200nm/
                    figures/
                        combined/
                            psf_fwhm.png
    """

    return (
        get_combined_figures_directory(
            case
        )
        / filename
    )


def get_field_plot_path(
    case: OpticalCase,
    filename: str,
) -> Path:
    """
    Return the path to one individual field plot.

    Examples
    --------
    output/
        thermal/
            survival/
                200nm/
                    figures/
                        individual/
                            field_01/
                                psf_fwhm.png
    """

    return (
        get_field_directory(
            case
        )
        / filename
    )