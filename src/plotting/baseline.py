"""
baseline.py

Baseline optical performance plotting routines.

Purpose
-------
Generates wavelength-dependent engineering plots for the baseline
optical design.

Unlike the thermal analysis, the baseline analysis represents a single
reference operating condition. For every registered metric, both

- combined plots (all fields)
- individual plots (one field)

are generated as a function of wavelength.

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
    BASELINE_TEMPERATURE_C,
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

        if optical_case.analysis_type != AnalysisType.BASELINE:
            continue

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
    cases: list[OpticalCase],
) -> None:
    """
    Generate one wavelength plot per field for every registered metric.
    """

    grouped_fields = _group_by_field(
        cases
    )

    for field_index in sorted(grouped_fields):

        field_cases = grouped_fields[
            field_index
        ]

        representative_case = field_cases[0]

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
                f"Baseline Temperature = "
                f"{BASELINE_TEMPERATURE_C:.0f} °C\n"
                f"Field {field_index}"
            )

            plot_metric(
                x=wavelengths,
                y=values,
                xlabel="Wavelength (nm)",
                ylabel=metric.ylabel,
                title=title,
                output_file=get_baseline_field_plot_path(
                    field_index,
                    metric.filename,
                ),
            )


# ---------------------------------------------------------------------
# Combined Plot Generation
# ---------------------------------------------------------------------


def _generate_combined_plots(
    cases: list[OpticalCase],
) -> None:
    """
    Generate one combined wavelength plot for every registered metric.

    Each combined plot contains one curve per field.
    """

    grouped_fields = _group_by_field(
        cases
    )

    for metric in BASELINE_PLOT_METRICS:

        series: list[
            dict[str, object]
        ] = []

        for field_index in sorted(grouped_fields):

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
                    "field": field_index,
                    "label": (
                        f"Field {field_index}"
                    ),
                    "x": wavelengths,
                    "y": values,
                }
            )

        if not series:
            continue

        title = (
            f"{metric.title}\n"
            f"Baseline Temperature = "
            f"{BASELINE_TEMPERATURE_C:.0f} °C"
        )

        plot_multi_metric(
            series=series,
            xlabel="Wavelength (nm)",
            ylabel=metric.ylabel,
            title=title,
            output_file=get_baseline_combined_plot_path(
                metric.filename,
            ),
            legend_title="Field",
        )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_baseline_plots(
    cases: Iterable[OpticalCase],
) -> None:
    """
    Generate the complete baseline plot suite.

    For the reference baseline optical configuration, wavelength-
    dependent engineering plots are generated.

    For every registered metric, this function generates

    - one combined plot containing every field
    - one individual plot for each field

    The generated figures are written to the baseline output directory
    hierarchy managed by plotting.paths.
    """

    baseline_cases = [

        case

        for case in cases

        if case.analysis_type == AnalysisType.BASELINE

    ]

    if not baseline_cases:
        return

    _generate_combined_plots(
        baseline_cases,
    )

    _generate_individual_plots(
        baseline_cases,
    )