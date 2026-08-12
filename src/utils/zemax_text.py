"""
zemax_text.py

Reusable text parsing utilities for Zemax text exports.

Purpose
-------
Provides helper functions for extracting numerical values and text
sections from Zemax-generated reports.

These helpers remove repetitive regular-expression code from individual
parsers and provide consistent error handling throughout the project.

This module contains no optical analysis and has no knowledge of PSF,
MTF, Wavefront, or any other Zemax analysis type.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

import re


# ---------------------------------------------------------------------
# Floating-Point Number Pattern
# ---------------------------------------------------------------------

FLOAT_PATTERN = r"[+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?"


# ---------------------------------------------------------------------
# Generic Search Helpers
# ---------------------------------------------------------------------

def find_match(
    pattern: re.Pattern,
    text: str,
    error_message: str,
) -> re.Match:
    """
    Search for a regular-expression match.

    Parameters
    ----------
    pattern
        Compiled regular expression.

    text
        Text to search.

    error_message
        Exception message if the pattern is not found.

    Returns
    -------
    re.Match
        Match object.

    Raises
    ------
    ValueError
        If no match is found.
    """

    match = pattern.search(text)

    if match is None:
        raise ValueError(error_message)

    return match


# ---------------------------------------------------------------------

def find_float(
    pattern: re.Pattern,
    text: str,
    error_message: str,
) -> float:
    """
    Extract a floating-point value.

    Returns
    -------
    float
    """

    return float(
        find_match(
            pattern,
            text,
            error_message,
        ).group(1)
    )


# ---------------------------------------------------------------------

def find_int(
    pattern: re.Pattern,
    text: str,
    error_message: str,
) -> int:
    """
    Extract an integer value.

    Returns
    -------
    int
    """

    return int(
        find_match(
            pattern,
            text,
            error_message,
        ).group(1)
    )


# ---------------------------------------------------------------------

def find_two_ints(
    pattern: re.Pattern,
    text: str,
    error_message: str,
) -> tuple[int, int]:
    """
    Extract two integer values.

    Returns
    -------
    tuple[int, int]
    """

    match = find_match(
        pattern,
        text,
        error_message,
    )

    return (
        int(match.group(1)),
        int(match.group(2)),
    )


# ---------------------------------------------------------------------

def find_two_floats(
    pattern: re.Pattern,
    text: str,
    error_message: str,
) -> tuple[float, float]:
    """
    Extract two floating-point values.

    Returns
    -------
    tuple[float, float]
    """

    match = find_match(
        pattern,
        text,
        error_message,
    )

    return (
        float(match.group(1)),
        float(match.group(2)),
    )


# ---------------------------------------------------------------------
# Section Extraction
# ---------------------------------------------------------------------

def find_section(
    text: str,
    start_marker: str,
) -> str:
    """
    Return the text immediately following a marker.

    Parameters
    ----------
    text
        Complete Zemax report.

    start_marker
        Marker indicating the beginning of the desired section.

    Returns
    -------
    str
        Remaining text after the marker.

    Raises
    ------
    ValueError
        If the marker cannot be located.
    """

    index = text.find(start_marker)

    if index == -1:
        raise ValueError(
            f"Unable to locate section '{start_marker}'."
        )

    return text[index + len(start_marker):]


def find_all_matches(
    pattern: re.Pattern,
    text: str,
) -> list[re.Match]:
    """
    Return all regular-expression matches.

    Parameters
    ----------
    pattern
        Compiled regular expression.

    text
        Text to search.

    Returns
    -------
    list[re.Match]
        All matches in the order they appear.
    """

    return list(pattern.finditer(text))


def find_all_sections(
    text: str,
    start_marker: str,
) -> list[str]:
    """
    Split a Zemax report into sections beginning with a marker.

    Parameters
    ----------
    text
        Complete Zemax report.

    start_marker
        Section delimiter.

    Returns
    -------
    list[str]
        Sections beginning with the requested marker.

    Raises
    ------
    ValueError
        If no sections are found.
    """

    parts = text.split(start_marker)

    if len(parts) <= 1:
        raise ValueError(
            f"Unable to locate section '{start_marker}'."
        )

    return parts[1:]


def extract_floats(
    text: str,
) -> list[float]:
    """
    Extract every floating-point number from a string.

    Parameters
    ----------
    text
        Input text.

    Returns
    -------
    list[float]
        Floating-point values in order of appearance.
    """

    return [
        float(value)
        for value in re.findall(FLOAT_PATTERN, text)
    ]