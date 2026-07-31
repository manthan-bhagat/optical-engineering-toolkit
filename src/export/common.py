"""
common.py

Shared utilities for tabular exporters.

Purpose
-------
Provides common validation and helper routines used by all export
modules.

These helpers ensure that every exporter operates on a consistent
collection of OpticalCase objects belonging to the same analysis type,
dataset (when applicable), and wavelength.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from typing import Iterable

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.optical_case import OpticalCase

# ---------------------------------------------------------------------
# Public Helpers
# ---------------------------------------------------------------------


def validate_export_cases(
    cases: Iterable[OpticalCase],
) -> list[OpticalCase]:
    """
    Validate an export case collection.

    Every exporter expects all supplied OpticalCase objects to belong to

    - one analysis type
    - one dataset (if applicable)
    - one wavelength

    Parameters
    ----------
    cases
        Optical cases to export.

    Returns
    -------
    list[OpticalCase]
        Validated optical cases.

    Raises
    ------
    ValueError
        If the collection is empty or contains mixed analysis types,
        datasets, or wavelengths.
    """

    validated_cases = list(cases)

    if not validated_cases:
        raise ValueError(
            "No optical cases supplied for export."
        )

    first_case = validated_cases[0]

    if first_case.analysis_type is None:
        raise ValueError(
            "Optical case has no analysis type."
        )

    if first_case.wavelength_um is None:
        raise ValueError(
            "Optical case has no wavelength."
        )

    analysis_type = first_case.analysis_type
    dataset = first_case.dataset
    wavelength_um = first_case.wavelength_um

    for optical_case in validated_cases[1:]:

        if optical_case.analysis_type != analysis_type:
            raise ValueError(
                "All exported optical cases must belong "
                "to the same analysis type."
            )

        if optical_case.dataset != dataset:
            raise ValueError(
                "All exported optical cases must belong "
                "to the same dataset."
            )

        if optical_case.wavelength_um != wavelength_um:
            raise ValueError(
                "All exported optical cases must belong "
                "to the same wavelength."
            )

    return validated_cases