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
├── monte-carlo/
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
    Return the directory immediately preceding the wavelength
    directory.

    Thermal
    -------
    output/
        thermal/
            survival/

    Monte Carlo
    -----------
    output/
        monte-carlo/

    Tolerance
    ---------
    Future analyses may define their own hierarchy.
    """

    directory = get_analysis_directory(
        case
    )

    # -------------------------------------------------------------
    # Thermal
    # -------------------------------------------------------------

    if case.analysis_type == AnalysisType.THERMAL:

        if not case.dataset:
            raise ValueError(
                "Thermal OpticalCase must define a dataset."
            )

        return (
            directory
            / case.dataset
        )

    # -------------------------------------------------------------
    # Monte Carlo
    # -------------------------------------------------------------

    if case.analysis_type == AnalysisType.MONTE_CARLO:

        #
        # Representative trials are the independent variable and are
        # therefore not part of the output directory hierarchy.
        #
        return directory

    # -------------------------------------------------------------
    # Default
    # -------------------------------------------------------------

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

def get_tolerance_figure_path(
    filename: str,
) -> Path:
    """
    Return the path for a tolerance analysis figure.

    Example
    -------
    output/
        tolerance/
            figures/
                histogram.png
    """

    return (
        OUTPUT_DIRECTORY
        / "tolerance"
        / "figures"
        / filename
    )

# ---------------------------------------------------------------------
# Baseline Output Directories
# ---------------------------------------------------------------------


def get_baseline_directory() -> Path:
    """
    Return the root baseline output directory.

    Example
    -------
    output/
        baseline/
    """

    return (
        OUTPUT_DIRECTORY
        / "baseline"
    )


def get_baseline_configuration_directory(
    configuration: int,
) -> Path:
    """
    Return the output directory for one baseline configuration.

    Example
    -------
    output/
        baseline/
            configuration_01/
    """

    return (
        get_baseline_directory()
        / f"configuration_{configuration:02d}"
    )


# ---------------------------------------------------------------------
# Baseline Export Files
# ---------------------------------------------------------------------


def get_baseline_csv_path(
    configuration: int,
) -> Path:
    """
    Return the CSV export path for one baseline configuration.

    Example
    -------
    output/
        baseline/
            configuration_01/
                results.csv
    """

    return (
        get_baseline_configuration_directory(
            configuration
        )
        / "results.csv"
    )


def get_baseline_excel_path(
    configuration: int,
) -> Path:
    """
    Return the Excel export path for one baseline configuration.

    Example
    -------
    output/
        baseline/
            configuration_01/
                results.xlsx
    """

    return (
        get_baseline_configuration_directory(
            configuration
        )
        / "results.xlsx"
    )


# ---------------------------------------------------------------------
# Baseline Figure Directories
# ---------------------------------------------------------------------


def get_baseline_figures_directory(
    configuration: int,
) -> Path:
    """
    Return the figures directory for one baseline configuration.

    Example
    -------
    output/
        baseline/
            configuration_01/
                figures/
    """

    return (
        get_baseline_configuration_directory(
            configuration
        )
        / "figures"
    )


def get_baseline_combined_figures_directory(
    configuration: int,
) -> Path:
    """
    Return the combined figures directory for one baseline
    configuration.
    """

    return (
        get_baseline_figures_directory(
            configuration
        )
        / "combined"
    )


def get_baseline_individual_figures_directory(
    configuration: int,
) -> Path:
    """
    Return the individual figures directory for one baseline
    configuration.
    """

    return (
        get_baseline_figures_directory(
            configuration
        )
        / "individual"
    )


def get_baseline_field_directory(
    configuration: int,
    field_index: int,
) -> Path:
    """
    Return the directory for one field within one baseline
    configuration.

    Example
    -------
    output/
        baseline/
            configuration_01/
                figures/
                    individual/
                        field_01/
    """

    return (
        get_baseline_individual_figures_directory(
            configuration
        )
        / _format_field(
            field_index
        )
    )


# ---------------------------------------------------------------------
# Baseline Figure Files
# ---------------------------------------------------------------------


def get_baseline_combined_plot_path(
    configuration: int,
    filename: str,
) -> Path:
    """
    Return the path to one combined plot for one baseline
    configuration.
    """

    return (
        get_baseline_combined_figures_directory(
            configuration
        )
        / filename
    )


def get_baseline_field_plot_path(
    configuration: int,
    field_index: int,
    filename: str,
) -> Path:
    """
    Return the path to one individual field plot for one baseline
    configuration.
    """

    return (
        get_baseline_field_directory(
            configuration,
            field_index,
        )
        / filename
    )