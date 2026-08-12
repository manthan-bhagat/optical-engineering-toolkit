"""
figures.py

Publication-quality plotting utilities.

Purpose
-------
Provides reusable plotting routines shared by the statistical reporting
pipeline.

Unlike the engineering plotting pipeline, this module focuses solely on
producing clean publication-quality figures suitable for reports and
thesis documents.

Responsibilities
----------------
- Create consistently styled figures.
- Draw arbitrary data series.
- Draw engineering reference curves.
- Apply publication formatting.
- Export figures.

This module intentionally contains no knowledge of thermal analyses,
Monte Carlo analyses, baseline analyses, or optical engineering. It
simply renders the series supplied by higher-level reporting modules.

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
    REPORT_FIGURE_SIZE,
    REPORT_FIGURE_DPI,
    REPORT_LINE_WIDTH,
    REPORT_REFERENCE_LINE_WIDTH,
    REPORT_MARKER,
    REPORT_MARKER_SIZE,
    REPORT_GRID_ALPHA,
    REPORT_GRID_LINESTYLE,
    REPORT_GRID_LINE_WIDTH,
    REPORT_LEGEND_LOCATION,
    REPORT_LEGEND_BBOX,
    REPORT_LEGEND_FONT_SIZE,
    REPORT_LEGEND_TITLE_FONT_SIZE,
    REPORT_LEGEND_FRAME,
    REPORT_TITLE_PADDING,
)

# ---------------------------------------------------------------------
# Private Helpers
# ---------------------------------------------------------------------


def _create_axes():
    """
    Create a publication-quality matplotlib figure.

    Returns
    -------
    tuple
        (figure, axes)
    """

    fig, ax = plt.subplots(
        figsize=REPORT_FIGURE_SIZE,
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
    Apply consistent report styling.
    """

    ax.set_xlabel(
        xlabel,
    )

    ax.set_ylabel(
        ylabel,
    )

    ax.set_title(
        title,
        pad=REPORT_TITLE_PADDING,
    )

    ax.grid(
        True,
        linestyle=REPORT_GRID_LINESTYLE,
        linewidth=REPORT_GRID_LINE_WIDTH,
        alpha=REPORT_GRID_ALPHA,
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
    Save a publication-quality figure.
    """

    output_file = Path(
        output_file
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if reserve_legend_space:

        fig.tight_layout(
            rect=(0.0, 0.0, 0.82, 1.0),
        )

    else:

        fig.tight_layout()

    fig.savefig(
        output_file,
        dpi=REPORT_FIGURE_DPI,
        bbox_inches="tight",
    )

    plt.close(
        fig,
    )

# ---------------------------------------------------------------------
# Drawing Helpers
# ---------------------------------------------------------------------


def _plot_series(
    ax,
    series: Iterable[dict],
) -> bool:
    """
    Plot one or more data series.

    Parameters
    ----------
    ax
        Target matplotlib axes.

    series
        Iterable of plotting dictionaries.

    Returns
    -------
    bool
        True if at least one series was plotted.
    """

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
                f"Series '{curve.get('label')}' "
                "contains mismatched X/Y data."
            )

        if not x:
            continue

        ax.plot(
            x,
            y,
            label=curve.get(
                "label",
            ),
            color=curve.get(
                "color",
            ),
            linewidth=curve.get(
                "linewidth",
                REPORT_LINE_WIDTH,
            ),
            linestyle=curve.get(
                "linestyle",
                "-",
            ),
            marker=curve.get(
                "marker",
                REPORT_MARKER,
            ),
            markersize=curve.get(
                "markersize",
                REPORT_MARKER_SIZE,
            ),
            alpha=curve.get(
                "alpha",
                1.0,
            ),
            zorder=curve.get(
                "zorder",
                2,
            ),
        )

        std = curve.get("std")

        if std is not None:
            lower = [
                y - s
                for y, s in zip(y, std)
            ]

            upper = [
                y + s
                for y, s in zip(y, std)
            ]

            ax.fill_between(
                x,
                lower,
                upper,
                color=curve.get("color"),
                alpha=0.20,
                linewidth=0,
                zorder=curve.get(
                    "zorder",
                    2,
                ) - 0.1,
            )

        plotted = True

    return plotted



def _plot_reference_series(
    ax,
    series: Iterable[dict] | None,
) -> None:
    """
    Plot engineering reference curves.

    Parameters
    ----------
    ax
        Target matplotlib axes.

    series
        Iterable of reference curve dictionaries.

    Notes
    -----
    Reference curves are optional.

    Typical examples include

    - Diffraction limit
    - Optical allocation
    - Requirement curve
    """

    if not series:
        return

    for curve in series:

        x = list(
            curve["x"]
        )

        y = list(
            curve["y"]
        )

        if len(x) != len(y):

            raise ValueError(
                f"Reference series "
                f"'{curve.get('label')}' "
                "contains mismatched X/Y data."
            )

        if not x:
            continue

        ax.plot(
            x,
            y,
            label=curve.get(
                "label",
            ),
            color=curve.get(
                "color",
            ),
            linewidth=curve.get(
                "linewidth",
                REPORT_REFERENCE_LINE_WIDTH,
            ),
            linestyle=curve.get(
                "linestyle",
                "--",
            ),
            marker="",
            alpha=curve.get(
                "alpha",
                1.0,
            ),
            zorder=curve.get(
                "zorder",
                1,
            ),
        )

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def save_figure(
    *,
    series: Iterable[dict],
    output_file: str | Path,
    xlabel: str,
    ylabel: str,
    title: str,
    reference_series: Iterable[dict] | None = None,
    legend_title: str | None = None,
    x_limits: tuple[float, float] | None = None,
    y_limits: tuple[float, float] | None = None,
) -> None:
    """
    Generate and save a publication-quality figure.

    Parameters
    ----------
    series
        Primary data series.

    output_file
        Destination figure.

    xlabel
        X-axis label.

    ylabel
        Y-axis label.

    title
        Figure title.

    reference_series
        Optional engineering reference curves.

    legend_title
        Optional legend title.

    x_limits
        Optional X-axis limits.

    y_limits
        Optional Y-axis limits.
    """

    fig, ax = _create_axes()

    plotted = _plot_series(
        ax,
        series,
    )

    if not plotted:

        raise ValueError(
            "No data available for plotting."
        )

    _plot_reference_series(
        ax,
        reference_series,
    )

    _style_axes(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    if x_limits is not None:

        ax.set_xlim(
            *x_limits,
        )

    if y_limits is not None:

        ax.set_ylim(
            *y_limits,
        )

    handles, labels = ax.get_legend_handles_labels()

    if handles:

        ax.legend(
            title=legend_title,
            loc=REPORT_LEGEND_LOCATION,
            bbox_to_anchor=REPORT_LEGEND_BBOX,
            fontsize=REPORT_LEGEND_FONT_SIZE,
            title_fontsize=REPORT_LEGEND_TITLE_FONT_SIZE,
            frameon=REPORT_LEGEND_FRAME,
        )

        reserve_space = True

    else:

        reserve_space = False

    _save_figure(
        fig,
        output_file,
        reserve_legend_space=reserve_space,
    )