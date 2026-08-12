"""
spot_data.py

Raw data parsed from a Zemax Spot Diagram report.

Purpose
-------
Stores the information explicitly contained within a Zemax Spot
Diagram text export.

A Spot Diagram report contains measurements for multiple field
positions. Each field is represented by a SpotField object.

No optical analysis is performed here.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.spot_field import SpotField

# ---------------------------------------------------------------------
# Spot Data
# ---------------------------------------------------------------------


@dataclass(slots=True)
class SpotData:
    """
    Raw Spot Diagram parsed from a Zemax report.

    One Spot Diagram corresponds to one operating point and contains
    measurements for every field defined in the Zemax Field Data
    Editor.
    """

    spot_fields: list[SpotField]
    """
    Spot measurements for every field contained in the report.

    The order of the list follows the order reported by Zemax.
    """