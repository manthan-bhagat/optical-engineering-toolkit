"""
baseline.py

Baseline optical performance plotting routines.

Purpose
-------
Generates wavelength-dependent engineering plots for the baseline
optical design.

The baseline analysis may contain multiple independently evaluated
optical configurations. Each configuration is treated as a separate
reference design and receives its own complete plot suite.

For every configuration and every registered metric, both

- combined plots containing all fields
- individual plots containing one field

can be generated as a function of wavelength.

Individual plots are currently retained in the implementation but are
temporarily disabled in the configuration plot suite.

No optical metric is hardcoded in this module.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from collections import defaultdict
from typing import Iterable

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.analysis_type import AnalysisType
from src.models.optical_case import OpticalCase

from src.config import (
    BASELINE_CONFIGURATION_NAMES,
)

from src.plotting.common import (
    plot_metric,
    plot_multi_metric,
)

from src.plotting.metrics import (
    BASELINE_PLOT_METRICS,
    resolve_attribute,
)

from src.plotting.paths import (
    get_baseline_combined_plot_path,
    get_baseline_field_plot_path,
)


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _get_configuration_name(
    configuration: int,
) -> str:
    """
    Return the human-readable filter name for a configuration.

    Examples
    --------
    1 -> No Filter
    2 -> BB1
    7 -> BB6
    8 -> NB1
    10 -> NB3

    Unknown configurations fall back to their numerical identifier.
    """

    return (
        BASELINE_CONFIGURATION_NAMES.get(
            configuration,
            f"Configuration {configuration}",
        )
    )


def _group_by_configuration(
    cases: Iterable[OpticalCase],
) -> dict[
    int,
    list[OpticalCase],
]:
    """
    Group baseline cases by optical configuration.

    Cases without configuration metadata are ignored.
    """

    grouped: dict[
        int,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if (
            optical_case.analysis_type
            != AnalysisType.BASELINE
        ):
            continue

        if optical_case.configuration is None:
            continue

        grouped[
            optical_case.configuration
        ].append(
            optical_case
        )

    return grouped


def _group_by_field(
    cases: Iterable[OpticalCase],
) -> dict[
    int,
    list[OpticalCase],
]:
    """
    Group baseline cases by field.

    Cases inside each field are sorted by wavelength.
    """

    grouped: dict[
        int,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if (
            optical_case.field_index is None
            or optical_case.wavelength_um is None
        ):
            continue

        grouped[
            optical_case.field_index
        ].append(
            optical_case
        )

    for field_cases in grouped.values():

        field_cases.sort(
            key=lambda case: case.wavelength_um
        )

    return grouped


# ---------------------------------------------------------------------
# Individual Plot Generation
# ---------------------------------------------------------------------


def _generate_individual_plots(
    configuration: int,
    cases: list[OpticalCase],
) -> None:
    """
    Generate one wavelength plot per field for every registered metric.

    All plots belong to one baseline configuration.

    This functionality is currently retained but not called by the
    configuration plot suite.
    """

    configuration_name = (
        _get_configuration_name(
            configuration
        )
    )

    grouped_fields = _group_by_field(
        cases
    )

    for field_index in sorted(
        grouped_fields
    ):

        field_cases = grouped_fields[
            field_index
        ]

        for metric in BASELINE_PLOT_METRICS:

            wavelengths: list[float] = []
            values: list[float] = []

            for case in field_cases:

                try:

                    value = resolve_attribute(
                        case,
                        metric.attribute_path,
                    )

                except AttributeError:

                    continue

                if value is None:

                    continue

                wavelengths.append(
                    case.wavelength_um * 1000.0
                )

                values.append(
                    value
                )

            if not values:

                continue

            title = (
                f"{metric.title}\n"
                f"{configuration_name} | "
                f"Field {field_index}"
            )

            plot_metric(
                x=wavelengths,
                y=values,
                xlabel="Wavelength (nm)",
                ylabel=metric.ylabel,
                title=title,
                output_file=(
                    get_baseline_field_plot_path(
                        configuration,
                        field_index,
                        metric.filename,
                    )
                ),
            )


# ---------------------------------------------------------------------
# Combined Plot Generation
# ---------------------------------------------------------------------


def _generate_combined_plots(
    configuration: int,
    cases: list[OpticalCase],
) -> None:
    """
    Generate one combined wavelength plot for every registered metric.

    Each combined plot contains one curve per field.

    All curves belong to one baseline configuration.
    """

    configuration_name = (
        _get_configuration_name(
            configuration
        )
    )

    grouped_fields = _group_by_field(
        cases
    )

    for metric in BASELINE_PLOT_METRICS:

        series: list[
            dict[str, object]
        ] = []

        for field_index in sorted(
            grouped_fields
        ):

            field_cases = grouped_fields[
                field_index
            ]

            wavelengths: list[float] = []
            values: list[float] = []

            for case in field_cases:

                try:

                    value = resolve_attribute(
                        case,
                        metric.attribute_path,
                    )

                except AttributeError:

                    continue

                if value is None:

                    continue

                wavelengths.append(
                    case.wavelength_um * 1000.0
                )

                values.append(
                    value
                )

            if not values:

                continue

            series.append(
                {
                    "field":
                        field_index,

                    "label":
                        f"Field {field_index}",

                    "x":
                        wavelengths,

                    "y":
                        values,
                }
            )

        if not series:

            continue

        title = (
            f"{metric.title}\n"
            f"{configuration_name}"
        )

        plot_multi_metric(
            series=series,
            xlabel="Wavelength (nm)",
            ylabel=metric.ylabel,
            title=title,
            output_file=(
                get_baseline_combined_plot_path(
                    configuration,
                    metric.filename,
                )
            ),
            legend_title="Field",
        )


# ---------------------------------------------------------------------
# Configuration Plot Suite
# ---------------------------------------------------------------------


def _generate_configuration_plots(
    configuration: int,
    cases: list[OpticalCase],
) -> None:
    """
    Generate the complete plot suite for one baseline configuration.

    Individual field plots are currently disabled but their generation
    routine remains available for future use.
    """

    _generate_combined_plots(
        configuration,
        cases,
    )

    # -------------------------------------------------------------
    # Individual plots temporarily disabled
    # -------------------------------------------------------------

    # _generate_individual_plots(
    #     configuration,
    #     cases,
    # )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_baseline_plots(
    cases: Iterable[OpticalCase],
    configuration: int,
) -> None:
    """
    Generate the complete plot suite for one baseline configuration.

    For every registered metric, a combined plot containing every field
    is generated as a function of wavelength.

    Individual field plots are currently disabled.
    """

    baseline_cases = [

        case

        for case in cases

        if (
            case.analysis_type
            == AnalysisType.BASELINE
        )

    ]

    if not baseline_cases:

        return

    _generate_configuration_plots(
        configuration,
        baseline_cases,
    )