"""
spot.py

Parser for Zemax Spot Diagram text reports.

Purpose
-------
Parses a Zemax Spot Diagram report containing spot statistics for all
fields in a single analysis.

The parser extracts only the numerical values explicitly reported by
Zemax. No optical analysis is performed.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

import re

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.spot_data import SpotData
from src.models.spot_field import SpotField

from src.parsers.base_parser import BaseParser

# ---------------------------------------------------------------------
# Spot Parser
# ---------------------------------------------------------------------


class SpotParser(BaseParser):
    """
    Parser for Zemax Spot Diagram reports.
    """

    FIELD_SPLIT_PATTERN = re.compile(
        r"Field coordinate\s*:"
    )

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------

    def parse(
        self,
    ) -> SpotData:
        """
        Parse the complete Spot Diagram report.

        Returns
        -------
        SpotData
            Parsed Spot Diagram information.
        """

        text = self.read_file()

        return SpotData(

            spot_fields=self._extract_fields(
                text
            )
        )

    # -----------------------------------------------------------------
    # Internal Helpers
    # -----------------------------------------------------------------

    def _extract_fields(
        self,
        text: str,
    ) -> list[SpotField]:
        """
        Extract every field contained in the report.

        Parameters
        ----------
        text
            Complete Zemax Spot Diagram report.

        Returns
        -------
        list[SpotField]
            Parsed field results.

        Raises
        ------
        ValueError
            If no field blocks are found.
        """

        blocks = self.FIELD_SPLIT_PATTERN.split(
            text
        )

        #
        # First block contains the report header.
        #
        blocks = blocks[1:]

        if not blocks:

            raise ValueError(
                "No Spot Diagram field data found."
            )

        spot_fields: list[SpotField] = []

        for block in blocks:

            #
            # Restore the heading removed by split() so each block is
            # parsed independently.
            #
            field_text = (
                "Field coordinate :"
                + block
            )

            spot_fields.append(

                self._parse_field(
                    field_text
                )
            )

        return spot_fields

    # -----------------------------------------------------------------

    def _parse_field(
        self,
        text: str,
    ) -> SpotField:
        """
        Parse one Spot Diagram field block.

        Parameters
        ----------
        text
            One field block.

        Returns
        -------
        SpotField
            Parsed field statistics.
        """

        field_x, field_y = self._extract_float_pair(
            text,
            "Field coordinate",
        )

        image_x, image_y = self._extract_float_pair(
            text,
            "Image coordinate",
        )

        rms_radius = self._extract_float(
            text,
            "RMS Spot Radius",
        )

        rms_x = self._extract_float(
            text,
            "RMS Spot X Size",
        )

        rms_y = self._extract_float(
            text,
            "RMS Spot Y Size",
        )

        max_radius = self._extract_float(
            text,
            "Max Spot Radius",
        )

        return SpotField(

            field_x_deg=field_x,

            field_y_deg=field_y,

            image_x_mm=image_x,

            image_y_mm=image_y,

            rms_radius_um=rms_radius,

            rms_x_um=rms_x,

            rms_y_um=rms_y,

            max_radius_um=max_radius,
        )

    # -----------------------------------------------------------------

    @staticmethod
    def _extract_float_pair(
        text: str,
        label: str,
    ) -> tuple[float, float]:
        """
        Extract a pair of floating-point values.
        """

        pattern = (
            rf"{re.escape(label)}\s*:\s*"
            r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)\s+"
            r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
        )

        match = re.search(
            pattern,
            text,
        )

        if match is None:

            raise ValueError(
                f"Unable to locate '{label}'."
            )

        return (

            float(match.group(1)),

            float(match.group(2)),
        )

    # -----------------------------------------------------------------

    @staticmethod
    def _extract_float(
        text: str,
        label: str,
    ) -> float:
        """
        Extract a single floating-point value.
        """

        pattern = (
            rf"{re.escape(label)}\s*:\s*"
            r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
        )

        match = re.search(
            pattern,
            text,
        )

        if match is None:

            raise ValueError(
                f"Unable to locate '{label}'."
            )

        return float(
            match.group(1)
        )