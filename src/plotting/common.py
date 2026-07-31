"""
common.py

Common plotting utilities for the Zemax Optical Analysis Toolkit.

Purpose
-------
This module provides reusable plotting routines shared by all analysis
types (thermal, Monte Carlo, tolerance, etc.).

The primary helpers are generic plotting functions used by higher-level
plotting modules.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path
from typing import Iterable

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
    PLOT_LINE_WIDTH,
    MULTI_PLOT_LINE_WIDTH,
    PLOT_MARKER,
    PLOT_MARKER_SIZE,
    GRID_ALPHA,
    GRID_LINESTYLE,
    GRID_LINE_WIDTH,
    LEGEND_LOCATION,
    LEGEND_BBOX,
    LEGEND_FONT_SIZE,
    LEGEND_TITLE_FONT_SIZE,
    LEGEND_FRAME,
    FIELD_COLORS,
)

# ---------------------------------------------------------------------
# Private Helpers
# ---------------------------------------------------------------------


def _create_axes():
    """
    Create a consistently styled matplotlib figure.

    Returns
    -------
    tuple
        (figure, axes)
    """

    fig, ax = plt.subplots(
        figsize=FIGURE_SIZE,
        constrained_layout=False,
    )

    return fig, ax


def _style_axes(
    ax,
    *,
    xlabel: str,
    ylabel: str,
    title: str,
) -> None:
    """
    Apply standard engineering plot styling.
    """

    ax.set_xlabel(
        xlabel,
    )

    ax.set_ylabel(
        ylabel,
    )

    ax.set_title(
        title,
        pad=12,
    )

    ax.grid(
        True,
        linestyle=GRID_LINESTYLE,
        linewidth=GRID_LINE_WIDTH,
        alpha=GRID_ALPHA,
    )

    ax.minorticks_on()

    ax.set_axisbelow(
        True,
    )

    ax.spines["top"].set_visible(
        False,
    )

    ax.spines["right"].set_visible(
        False,
    )


def _save_figure(
    fig,
    output_file: str | Path,
    *,
    reserve_legend_space: bool = False,
) -> None:
    """
    Save a figure to disk.
    """

    output_file = Path(
        output_file
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if reserve_legend_space:

        #
        # Reserve space on the right-hand side for
        # legends placed outside the plotting area.
        #
        fig.tight_layout(
            rect=(0.0, 0.0, 0.82, 1.0),
        )

    else:

        fig.tight_layout()

    fig.savefig(
        output_file,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
    )

    plt.close(
        fig,
    )

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def plot_metric(
    x: Iterable[float],
    y: Iterable[float],
    *,
    xlabel: str,
    ylabel: str,
    title: str,
    output_file: str | Path,
) -> None:
    """
    Plot a single metric.

    Parameters
    ----------
    x
        X-axis values.

    y
        Y-axis values.

    xlabel
        Horizontal axis label.

    ylabel
        Vertical axis label.

    title
        Figure title.

    output_file
        Destination image file.
    """

    x = list(x)
    y = list(y)

    if len(x) != len(y):

        raise ValueError(
            "X and Y must contain the same number of values."
        )

    if len(x) == 0:

        raise ValueError(
            "No data available for plotting."
        )

    fig, ax = _create_axes()

    ax.plot(
        x,
        y,
        marker=PLOT_MARKER,
        markersize=PLOT_MARKER_SIZE,
        linewidth=PLOT_LINE_WIDTH,
    )

    _style_axes(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    _save_figure(
        fig,
        output_file,
    )


def plot_multi_metric(
    series: Iterable[dict],
    *,
    xlabel: str,
    ylabel: str,
    title: str,
    output_file: str | Path,
    legend_title: str | None = None,
) -> None:
    """
    Plot multiple data series on the same axes.

    Parameters
    ----------
    series
        Iterable of dictionaries with keys

        - label
        - x
        - y

    xlabel
        Horizontal axis label.

    ylabel
        Vertical axis label.

    title
        Figure title.

    output_file
        Destination image file.

    legend_title
        Optional legend title.
    """

    fig, ax = _create_axes()

    plotted = False

    for curve in series:

        x = list(
            curve["x"]
        )

        y = list(
            curve["y"]
        )

        if len(x) != len(y):

            raise ValueError(
                f"Series '{curve['label']}' has mismatched X/Y lengths."
            )

        if len(x) == 0:
            continue

        #
        # Combined engineering plots intentionally
        # omit markers to reduce visual clutter.
        #
        field_index = curve.get("field")

        if field_index is None:
            color = None
        else:
            color = FIELD_COLORS[
                (field_index - 1) % len(FIELD_COLORS)
                ]

        ax.plot(
            x,
            y,
            color=color,
            linewidth=MULTI_PLOT_LINE_WIDTH,
            label=curve["label"],
        )
        plotted = True

    if not plotted:

        raise ValueError(
            "No data available for plotting."
        )

    _style_axes(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    ax.legend(
        title=legend_title,
        loc=LEGEND_LOCATION,
        bbox_to_anchor=LEGEND_BBOX,
        fontsize=LEGEND_FONT_SIZE,
        title_fontsize=LEGEND_TITLE_FONT_SIZE,
        frameon=LEGEND_FRAME,
    )

    _save_figure(
        fig,
        output_file,
        reserve_legend_space=True,
    )