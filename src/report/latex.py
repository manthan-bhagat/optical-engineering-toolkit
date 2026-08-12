"""
latex.py

LaTeX table generation utilities.

Purpose
-------
Provides reusable utilities for exporting pandas DataFrames as LaTeX
longtables suitable for direct inclusion in the thesis.

The generated tables use the longtable environment so they
automatically span multiple pages when required.

Column widths are automatically determined from the table contents so
that wider columns receive more space while preserving the overall page
width.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import pandas as pd

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import (
    LATEX_DECIMALS,
    LATEX_TOTAL_COLUMN_WIDTH,
)

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def save_longtable(
    dataframe: pd.DataFrame,
    output_path: Path,
    caption: str,
    label: str,
) -> None:
    """
    Export a DataFrame as a LaTeX longtable.

    Parameters
    ----------
    dataframe
        Table to export.

    output_path
        Destination .tex file.

    caption
        Longtable caption.

    label
        LaTeX label used for referencing.
    """
    dataframe = dataframe.copy()

    #
    # Present wavelength-dependent tables in ascending wavelength.
    #

    if "Wavelength (µm)" in dataframe.columns:
        dataframe = dataframe.sort_values(
            "Wavelength (µm)",
            kind="stable",
        ).reset_index(
            drop=True,
        )

    #
    # Display wavelengths in nanometres.
    #

    if "Wavelength (µm)" in dataframe.columns:
        dataframe["Wavelength (µm)"] *= 1000.0

        dataframe = dataframe.rename(
            columns={
                "Wavelength (µm)": "Wavelength (nm)",
            }
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    column_spec = (
        _build_column_specification(
            dataframe,
        )
    )

    headers = " & ".join(

        rf"\textbf{{{_escape_latex(column)}}}"

        for column in dataframe.columns

    )

    lines: list[str] = []

    lines.append(
        f"\\begin{{longtable}}{{{column_spec}}}"
    )

    lines.append(
        f"\\caption{{{_escape_latex(caption)}}}"
    )

    lines.append(
        f"\\label{{{label}}}\\\\"
    )

    lines.append("")

    lines.append("\\hline")

    lines.append(
        headers + r" \\"
    )

    lines.append("\\hline")

    lines.append(
        r"\endfirsthead"
    )

    lines.append("")

    lines.append(
        rf"\multicolumn{{{len(dataframe.columns)}}}{{c}}{{{{\bfseries Table \thetable\ Continued from previous page}}}}\\"
    )

    lines.append("\\hline")

    lines.append(
        headers + r" \\"
    )

    lines.append("\\hline")

    lines.append(
        r"\endhead"
    )

    lines.append("")

    lines.append("\\hline")

    lines.append(
        rf"\multicolumn{{{len(dataframe.columns)}}}{{r}}{{{{Continued on next page}}}}\\"
    )

    lines.append(
        r"\endfoot"
    )

    lines.append("")

    lines.append("\\hline")

    lines.append(
        r"\endlastfoot"
    )

    lines.append("")

    for _, row in dataframe.iterrows():

        values = [
            _format_cell(
                value,
            )
            for value in row
        ]

        lines.append(
            " & ".join(values)
            + r" \\"
        )

        lines.append(
            "\\hline"
        )

    lines.append("")

    lines.append(
        r"\end{longtable}"
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------


def _build_column_specification(
    dataframe: pd.DataFrame,
) -> str:
    """
    Build an adaptive LaTeX column specification.

    Column widths are proportional to the widest formatted entry within
    each column while ensuring the total width fits within the document
    text width.
    """

    minimum_width = 0.08

    lengths: list[int] = []

    for column in dataframe.columns:

        maximum_length = len(
            str(column)
        )

        for value in dataframe[column]:

            if pd.notna(value):

                maximum_length = max(
                    maximum_length,
                    len(
                        _display_string(
                            value,
                        )
                    ),
                )

        lengths.append(
            maximum_length
        )

    total_length = sum(
        lengths
    )

    widths: list[float] = []

    for length in lengths:

        width = max(
            minimum_width,
            LATEX_TOTAL_COLUMN_WIDTH
            * length
            / total_length,
        )

        widths.append(
            width
        )

    scale = (
        LATEX_TOTAL_COLUMN_WIDTH
        / sum(widths)
    )

    widths = [
        width * scale
        for width in widths
    ]

    columns: list[str] = []

    for (
        column_name,
        width,
    ) in zip(
        dataframe.columns,
        widths,
    ):

        if pd.api.types.is_numeric_dtype(
            dataframe[column_name]
        ):

            alignment = (
                ">{\\centering\\arraybackslash}"
            )

        else:

            alignment = (
                ">{\\raggedright\\arraybackslash}"
            )

        columns.append(
            f"{alignment}p{{{width:.3f}\\textwidth}}"
        )

    return (
        "|"
        + "|".join(columns)
        + "|"
    )


def _format_cell(
    value,
) -> str:
    """
    Format a DataFrame value for LaTeX.
    """

    if pd.isna(
        value,
    ):

        return ""

    return _escape_latex(
        _display_string(
            value,
        )
    )


def _display_string(
    value,
) -> str:
    """
    Convert a value to its presentation string.
    """

    if isinstance(
        value,
        float,
    ):

        return (
            f"{value:.{LATEX_DECIMALS}f}"
        )

    return str(
        value
    )


def _escape_latex(
    text: str,
) -> str:
    """
    Escape LaTeX special characters.
    """

    replacements = {

        "\\": r"\textbackslash{}",

        "&": r"\&",

        "%": r"\%",

        "$": r"\$",

        "#": r"\#",

        "_": r"\_",

        "{": r"\{",

        "}": r"\}",

        "~": r"\textasciitilde{}",

        "^": r"\textasciicircum{}",
    }

    for (
        original,
        replacement,
    ) in replacements.items():

        text = text.replace(
            original,
            replacement,
        )

    return text