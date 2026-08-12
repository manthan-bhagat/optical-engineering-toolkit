"""
monte_carlo.py

Monte Carlo representative trial plotting routines.

Purpose
-------
Generates engineering plots for representative Monte Carlo optical
analysis cases.

Plots are generated automatically from the Monte Carlo plotting
registry. For every metric, both

- combined plots (all fields)
- individual plots (one field)

are produced.

Representative trials (Best, Mean, Worst, P02, P98, etc.) are treated
as categorical operating points along the horizontal axis.

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

from src.config import (
    MONTE_CARLO_DATASET_ORDER,
)

from src.models.analysis_type import AnalysisType
from src.models.optical_case import OpticalCase

from src.plotting.common import (
    plot_metric,
    plot_multi_metric,
)

from src.plotting.metrics import (
    MONTE_CARLO_PLOT_METRICS,
    resolve_attribute,
)

from src.plotting.paths import (
    get_combined_plot_path,
    get_field_plot_path,
)


# ---------------------------------------------------------------------
# Dataset Ordering
# ---------------------------------------------------------------------

_DATASET_ORDER = {
    dataset: index
    for index, dataset in enumerate(
        MONTE_CARLO_DATASET_ORDER
    )
}


def _dataset_sort_key(
    optical_case: OpticalCase,
) -> tuple[int, str]:
    """
    Return the canonical ordering key for representative trials.

    Representative trials are displayed according to the configured
    engineering ordering. Unknown datasets are appended afterwards in
    alphabetical order.
    """

    dataset = optical_case.dataset or ""

    return (
        _DATASET_ORDER.get(
            dataset,
            len(_DATASET_ORDER),
        ),
        dataset,
    )


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _group_by_wavelength(
    cases: Iterable[OpticalCase],
) -> dict[
    float,
    list[OpticalCase],
]:
    """
    Group Monte Carlo cases by wavelength.
    """

    grouped: dict[
        float,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if optical_case.analysis_type != AnalysisType.MONTE_CARLO:
            continue

        if (
            optical_case.dataset is None
            or optical_case.wavelength_um is None
            or optical_case.field_index is None
        ):
            continue

        grouped[
            optical_case.wavelength_um
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
    Group cases by field.

    Cases inside every field are sorted according to the configured
    representative trial ordering.
    """

    grouped: dict[
        int,
        list[OpticalCase],
    ] = defaultdict(list)

    for optical_case in cases:

        if optical_case.field_index is None:
            continue

        grouped[
            optical_case.field_index
        ].append(
            optical_case
        )

    for field_cases in grouped.values():

        field_cases.sort(
            key=_dataset_sort_key,
        )

    return grouped

# ---------------------------------------------------------------------
# Individual Plot Generation
# ---------------------------------------------------------------------

def _generate_individual_plots(
    cases: list[OpticalCase],
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

        representative_case = field_cases[0]

        for metric in MONTE_CARLO_PLOT_METRICS:

            representative_trials: list[str] = []
            values: list[float] = []

            for case in field_cases:

                try:
                    value = resolve_attribute(
                        case,
                        metric.attribute_path,
                    )

                except AttributeError:
                    #
                    # The analysis required for this metric has not been
                    # computed for this OpticalCase.
                    #
                    continue

                assert case.dataset is not None

                representative_trials.append(
                    case.dataset
                )

                values.append(
                    value
                )

            #
            # Nothing available for this metric.
            #
            if not values:
                continue

            assert representative_case.wavelength_um is not None

            title = (
                f"{metric.title}\n"
                f"λ = {representative_case.wavelength_um:.3f} µm, "
                f"Field {field_index}"
            )

            plot_metric(
                x=representative_trials,
                y=values,
                xlabel="Representative Trial",
                ylabel=metric.ylabel,
                title=title,
                output_file=get_field_plot_path(
                    representative_case,
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
    Generate one combined plot for every registered metric.

    Each combined plot contains one curve per field.
    """

    grouped_fields = _group_by_field(
        cases
    )

    representative_case = cases[0]

    for metric in MONTE_CARLO_PLOT_METRICS:

        series: list[
            dict[str, object]
        ] = []

        for field_index in sorted(grouped_fields):

            field_cases = grouped_fields[
                field_index
            ]

            representative_trials: list[str] = []
            values: list[float] = []

            for case in field_cases:

                try:
                    value = resolve_attribute(
                        case,
                        metric.attribute_path,
                    )

                except AttributeError:
                    #
                    # The analysis required for this metric has not been
                    # computed for this OpticalCase.
                    #
                    continue

                assert case.dataset is not None

                representative_trials.append(
                    case.dataset
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
                    "x": representative_trials,
                    "y": values,
                }
            )

        #
        # No field contains this metric.
        #
        if not series:
            continue

        assert representative_case.wavelength_um is not None

        title = (
            f"{metric.title}\n"
            f"λ = {representative_case.wavelength_um:.3f} µm"
        )

        plot_multi_metric(
            series=series,
            xlabel="Representative Trial",
            ylabel=metric.ylabel,
            title=title,
            output_file=get_combined_plot_path(
                representative_case,
                metric.filename,
            ),
            legend_title="Field",
        )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def generate_montecarlo_plots(
    cases: Iterable[OpticalCase],
) -> None:
    """
    Generate the complete Monte Carlo representative trial plot suite.

    For every wavelength, this function generates

    - one combined plot for every registered metric
    - one individual plot per field for every registered metric

    Representative trials (Best, Mean, Worst, P02, P98, etc.) are
    plotted along the horizontal axis.

    The generated figures are written to the standard Monte Carlo
    output directory hierarchy managed by plotting.paths.
    """

    grouped_cases = _group_by_wavelength(
        cases
    )

    if not grouped_cases:
        return

    for wavelength_um in sorted(grouped_cases):

        wavelength_cases = grouped_cases[
            wavelength_um
        ]

        _generate_combined_plots(
            wavelength_cases,
        )

        _generate_individual_plots(
            wavelength_cases,
        )
