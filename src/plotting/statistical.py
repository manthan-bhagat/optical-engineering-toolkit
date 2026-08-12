"""
statistical.py

Generic statistical plotting utilities.

Purpose
-------
Provides reusable statistical plotting routines shared by multiple analysis
types.

Unlike common.py, which focuses on engineering line plots, this module
implements statistical visualizations such as histograms, bar charts and
cumulative distributions.

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

from src.plotting.common import (
    _create_axes,
    _style_axes,
    _save_figure,
)

# ---------------------------------------------------------------------
# Histogram
# ---------------------------------------------------------------------


def plot_histogram(
    values: Iterable[float],
    *,
    bins: int = 40,
    xlabel: str,
    ylabel: str,
    title: str,
    output_file: str | Path,
) -> None:
    """
    Plot a histogram.

    Parameters
    ----------
    values
        Data values.

    bins
        Number of histogram bins.

    xlabel
        Horizontal axis label.

    ylabel
        Vertical axis label.

    title
        Figure title.

    output_file
        Destination image file.
    """

    values = list(values)

    if not values:

        raise ValueError(
            "No data available for plotting."
        )

    fig, ax = _create_axes()

    ax.hist(
        values,
        bins=bins,
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


# ---------------------------------------------------------------------
# Vertical Bar Chart
# ---------------------------------------------------------------------


def plot_bar(
    labels: Iterable[str],
    values: Iterable[float],
    *,
    xlabel: str,
    ylabel: str,
    title: str,
    output_file: str | Path,
) -> None:
    """
    Plot a vertical bar chart.
    """

    labels = list(labels)
    values = list(values)

    if len(labels) != len(values):

        raise ValueError(
            "Labels and values must contain the same number of elements."
        )

    if not labels:

        raise ValueError(
            "No data available for plotting."
        )

    fig, ax = _create_axes()

    ax.bar(
        labels,
        values,
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


# ---------------------------------------------------------------------
# Horizontal Bar Chart
# ---------------------------------------------------------------------


def plot_horizontal_bar(
    labels: Iterable[str],
    values: Iterable[float],
    *,
    xlabel: str,
    ylabel: str,
    title: str,
    output_file: str | Path,
) -> None:
    """
    Plot a horizontal bar chart.
    """

    labels = list(labels)
    values = list(values)

    if len(labels) != len(values):

        raise ValueError(
            "Labels and values must contain the same number of elements."
        )

    if not labels:

        raise ValueError(
            "No data available for plotting."
        )

    fig, ax = _create_axes()

    ax.barh(
        labels,
        values,
    )

    ax.invert_yaxis()

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


# ---------------------------------------------------------------------
# Cumulative Distribution
# ---------------------------------------------------------------------


def plot_cdf(
    values: Iterable[float],
    *,
    xlabel: str,
    ylabel: str,
    title: str,
    output_file: str | Path,
) -> None:
    """
    Plot an empirical cumulative distribution function.
    """

    values = sorted(values)

    if not values:

        raise ValueError(
            "No data available for plotting."
        )

    n = len(values)

    cumulative = [
        (index + 1) / n
        for index in range(n)
    ]

    fig, ax = _create_axes()

    ax.plot(
        values,
        cumulative,
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