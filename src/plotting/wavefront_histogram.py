"""
wavefront_histogram.py

Histogram of RMS wavefront error.

Purpose
-------
Visualizes the distribution of RMS wavefront error for a collection of
optical analysis cases.

Typical Uses
------------
- Thermal analysis
- Monte Carlo representative trials
- Monte Carlo full populations

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    FIGURE_SIZE,
    FIGURE_DPI,
    GRID_ALPHA,
    GRID_LINESTYLE,
    GRID_LINE_WIDTH,
)

from src.models.optical_case import OpticalCase

from src.plotting.paths import (
    get_combined_plot_path,
)

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def plot_wavefront_histogram(
    cases: list[OpticalCase],
) -> None:
    """
    Plot the distribution of RMS wavefront error.

    Parameters
    ----------
    cases
        Optical cases to visualize.
    """

    values = [
        case.wavefront_analysis.rms_waves
        for case in cases
        if case.wavefront_analysis is not None
    ]

    if not values:
        return

    # -------------------------------------------------------------
    # Figure
    # -------------------------------------------------------------

    figure, axis = plt.subplots(
        figsize=FIGURE_SIZE,
        dpi=FIGURE_DPI,
    )

    axis.hist(
        values,
        bins="auto",
    )

    axis.set_title(
        "Wavefront RMS Error Distribution"
    )

    axis.set_xlabel(
        "RMS Wavefront Error (waves)"
    )

    axis.set_ylabel(
        "Count"
    )

    axis.grid(
        alpha=GRID_ALPHA,
        linestyle=GRID_LINESTYLE,
        linewidth=GRID_LINE_WIDTH,
    )

    # -------------------------------------------------------------
    # Save
    # -------------------------------------------------------------

    output_file = get_combined_plot_path(
        cases[0],
        "wavefront_histogram.png",
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.savefig(
        output_file,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )