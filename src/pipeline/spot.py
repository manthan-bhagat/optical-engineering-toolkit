"""
spot.py

Processing pipeline for Zemax Spot Diagram analysis.

Purpose
-------
This module executes the Spot Diagram workflow for one OpticalCase.

Unlike PSF, MTF, and Wavefront reports, a Spot Diagram report contains
measurements for every field belonging to the same operating point.

The parsed report is therefore cached so it is read only once, after
which each OpticalCase receives only its corresponding SpotField.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.optical_case import OpticalCase
from src.models.spot_data import SpotData

from src.parsers.spot import SpotParser

# ---------------------------------------------------------------------
# Spot Cache
# ---------------------------------------------------------------------

_SPOT_CACHE: dict[
    Path,
    SpotData,
] = {}

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def process_spot(
    optical_case: OpticalCase,
) -> None:
    """
    Assign the Spot Diagram measurements corresponding to one
    OpticalCase.
    """

    spot_file = optical_case.spot_file

    if (
        spot_file is None
        or not spot_file.exists()
    ):
        return

    # -------------------------------------------------------------
    # Retrieve cached report.
    # -------------------------------------------------------------

    spot_data = _SPOT_CACHE.get(
        spot_file
    )

    if spot_data is None:

        spot_data = SpotParser(
            spot_file
        ).parse()

        _SPOT_CACHE[
            spot_file
        ] = spot_data

    # -------------------------------------------------------------
    # Locate the matching field.
    # -------------------------------------------------------------

    try:

        optical_case.spot_field = (
            spot_data.spot_fields[
                optical_case.field_index - 1
            ]
        )

    except (
        IndexError,
        TypeError,
    ):

        raise ValueError(
            f"Spot Diagram does not contain "
            f"field {optical_case.field_index}."
        )