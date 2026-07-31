"""
thermal.py

Thermal analysis plotting routines.

Purpose
-------
Generates engineering plots for thermal optical analysis.

Plots are generated automatically from the thermal plotting registry.
For every metric, both

- combined plots (all fields)
- individual plots (one field)

are produced.

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

from src.plotting.common import (
    plot_metric,
    plot_multi_metric,
)

from src.plotting.metrics import (
    THERMAL_PLOT_METRICS,
    resolve_attribute,
)

from src.plotting.paths import (
    get_combined_plot_path,
    get_field_plot_path,
)

# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _group_by_wavelength(
    cases: Iterable[OpticalCase],
) -> dict[float, list[OpticalCase]]:
    """
    Group thermal cases by wavelength.
    """

    grouped: dict[
        float,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if optical_case.analysis_type != AnalysisType.THERMAL:
            continue

        if (
            optical_case.wavelength_um is None
            or optical_case.temperature_c is None
            or optical_case.field_index is None
        ):
            continue

        grouped[
            optical_case.wavelength_um
        ].append(optical_case)

    return grouped


def _group_by_field(
    cases: Iterable[OpticalCase],
) -> dict[int, list[OpticalCase]]:
    """
    Group cases by field.

    Cases inside every field are sorted by temperature.
    """

    grouped: dict[
        int,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        grouped[
            optical_case.field_index
        ].append(optical_case)

    for field_cases in grouped.values():

        field_cases.sort(
            key=lambda case: case.temperature_c
        )

    return grouped

# ---------------------------------------------------------------------
# Individual Plot Generation
# ---------------------------------------------------------------------


def _generate_individual_plots(
    cases: list[OpticalCase],
    wavelength_um: float,
) -> None:
    """
    Generate one plot per field for every registered metric.
    """

    grouped_fields = _group_by_field(
        cases
    )

    for field_index in sorted(grouped_fields):

        field_cases = grouped_fields[
            field_index
        ]

        for metric in THERMAL_PLOT_METRICS:

            temperatures: list[float] = []
            values: list[float] = []

            for case in field_cases:

                try:
                    value = resolve_attribute(case, metric.attribute_path)

                except AttributeError as exc:

                    if "Missing attribute 'mtf_data'" in str(exc):
                        continue

                    if "Missing attribute 'wavefront_data'" in str(exc):
                        continue

                    raise
                if value is None:
                    continue

                temperatures.append(
                    case.temperature_c
                )

                values.append(
                    value
                )

            #
            # Nothing available for this metric.
            #
            if not values:
                continue

            plot_metric(
                x=temperatures,
                y=values,
                xlabel="Temperature (°C)",
                ylabel=metric.ylabel,
                title=(
                    f"{metric.title}\n"
                    f"λ = {wavelength_um:.3f} µm, "
                    f"Field {field_index}"
                ),
                output_file=get_field_plot_path(
                    AnalysisType.THERMAL,
                    wavelength_um,
                    field_index,
                    metric.filename,
                ),
            )

# ---------------------------------------------------------------------
# Combined Plot Generation
# ---------------------------------------------------------------------


def _generate_combined_plots(
    cases: list[OpticalCase],
    wavelength_um: float,
) -> None:
    """
    Generate one combined plot for every registered metric.

    Each combined plot contains one curve per field.
    """

    grouped_fields = _group_by_field(
        cases
    )

    for metric in THERMAL_PLOT_METRICS:

        series: list[
            dict[str, object]
        ] = []

        for field_index in sorted(grouped_fields):

            field_cases = grouped_fields[
                field_index
            ]

            temperatures: list[float] = []
            values: list[float] = []

            for case in field_cases:

                try:
                    value = resolve_attribute(case, metric.attribute_path)

                except AttributeError as exc:

                    if "Missing attribute 'mtf_data'" in str(exc):
                        continue

                    if "Missing attribute 'wavefront_data'" in str(exc):
                        continue

                    raise

                if value is None:
                    continue

                temperatures.append(
                    case.temperature_c
                )

                values.append(
                    value
                )

            #
            # This field has no data for this metric.
            #
            if not values:
                continue

            series.append(
                {
                    "field": field_index,
                    "label": (
                        f"Field {field_index}"
                    ),
                    "x": temperatures,
                    "y": values,
                }
            )

        #
        # No field contains this metric.
        #
        if not series:
            continue

        plot_multi_metric(
            series=series,
            xlabel="Temperature (°C)",
            ylabel=metric.ylabel,
            title=(
                f"{metric.title}\n"
                f"λ = {wavelength_um:.3f} µm"
            ),
            output_file=get_combined_plot_path(
                AnalysisType.THERMAL,
                wavelength_um,
                metric.filename,
            ),
            legend_title="Field",
        )

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_thermal_plots(
    cases: Iterable[OpticalCase],
) -> None:
    """
    Generate the complete thermal plot suite.

    For every wavelength, this function generates

    - one combined plot for every registered metric
    - one individual plot per field for every registered metric

    The generated figures are written to the standard thermal output
    directory hierarchy managed by plotting.paths.
    """

    grouped_cases = _group_by_wavelength(
        cases
    )

    if not grouped_cases:
        return

    for wavelength_um in sorted(
        grouped_cases
    ):

        wavelength_cases = grouped_cases[
            wavelength_um
        ]

        _generate_combined_plots(
            wavelength_cases,
            wavelength_um,
        )

        _generate_individual_plots(
            wavelength_cases,
            wavelength_um,
        )