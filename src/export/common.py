"""
common.py

Shared utilities for tabular exporters.

Purpose
-------
Provides common validation and helper routines used by all export
modules.

These helpers ensure that every exporter operates on a consistent
collection of OpticalCase objects appropriate for the corresponding
analysis type.

This module also provides shared table-merging utilities so repeated
pipeline executions update existing export files instead of replacing
previous results.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from typing import Iterable

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import pandas as pd

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.config import RESULT_COLUMNS

from src.models.analysis_type import AnalysisType
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
    - one wavelength

    Additional constraints depend on the analysis type.

    Thermal
    -------
    All cases must belong to the same dataset.

    Monte Carlo
    -----------
    Representative trials are intentionally exported together, so
    multiple datasets are permitted.

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
        If the collection is empty or contains inconsistent metadata.
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

        # ---------------------------------------------------------
        # Analysis Type
        # ---------------------------------------------------------

        if optical_case.analysis_type != analysis_type:
            raise ValueError(
                "All exported optical cases must belong "
                "to the same analysis type."
            )

        # ---------------------------------------------------------
        # Thermal Dataset
        # ---------------------------------------------------------

        if analysis_type == AnalysisType.THERMAL:

            if optical_case.dataset != dataset:
                raise ValueError(
                    "All exported thermal cases must belong "
                    "to the same dataset."
                )

        # ---------------------------------------------------------
        # Wavelength
        #
        # Thermal and Monte Carlo exports are generated one
        # wavelength at a time. Baseline exports intentionally
        # contain multiple wavelengths.
        # ---------------------------------------------------------

        if analysis_type in (
                AnalysisType.THERMAL,
                AnalysisType.MONTE_CARLO,
        ):

            if optical_case.wavelength_um != wavelength_um:
                raise ValueError(
                    "All exported optical cases must belong "
                    "to the same wavelength."
                )

    return validated_cases


# ---------------------------------------------------------------------
# Table Merge
# ---------------------------------------------------------------------


def merge_export_table(
    existing: pd.DataFrame | None,
    new: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge newly generated results into an existing export table.

    Rows are matched using the unique Case ID. Existing values are
    preserved unless a new non-null value is supplied.

    Parameters
    ----------
    existing
        Previously exported table. May be None.

    new
        Newly generated export table.

    Returns
    -------
    pandas.DataFrame
        Merged export table.
    """

    # -------------------------------------------------------------
    # First export.
    # -------------------------------------------------------------

    if existing is None or existing.empty:

        return (
            new
            .reindex(columns=RESULT_COLUMNS)
            .copy()
        )

    # -------------------------------------------------------------
    # Ensure both tables use the same schema.
    # -------------------------------------------------------------

    existing = existing.reindex(
        columns=RESULT_COLUMNS
    )

    new = new.reindex(
        columns=RESULT_COLUMNS
    )

    # -------------------------------------------------------------
    # Use Case ID as the merge key.
    # -------------------------------------------------------------

    existing = existing.set_index(
        "Case ID",
        drop=False,
    )

    new = new.set_index(
        "Case ID",
        drop=False,
    )

    # -------------------------------------------------------------
    # Update existing rows.
    # -------------------------------------------------------------

    for case_id in new.index:

        if case_id not in existing.index:

            #
            # Brand-new optical case.
            #
            existing.loc[case_id] = new.loc[
                case_id
            ]

            continue

        #
        # Only overwrite columns with newly available values.
        #
        for column in RESULT_COLUMNS:

            value = new.at[
                case_id,
                column,
            ]

            if pd.notna(value):

                existing.at[
                    case_id,
                    column,
                ] = value

    # -------------------------------------------------------------
    # Restore normal indexing.
    # -------------------------------------------------------------

    merged = (
        existing
        .reset_index(drop=True)
        .reindex(columns=RESULT_COLUMNS)
    )

    return merged