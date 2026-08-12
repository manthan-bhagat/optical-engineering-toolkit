"""
wavefront.py

Parser for Zemax Wavefront Map text exports.

Purpose
-------
This parser reads a Zemax Wavefront Map text report and extracts the
information explicitly contained in the report.

Responsibilities
----------------
The parser extracts

- Analysis wavelength
- Field coordinates
- Peak-to-valley wavefront error
- RMS wavefront error
- Exit pupil diameter
- Wavefront grid dimensions
- Wavefront center coordinates
- Two-dimensional wavefront map

The parser DOES NOT

- compute statistics
- compute RMS in nanometers
- compute PV in nanometers
- compute wavefront histograms
- validate optical performance

Those responsibilities belong to the analysis module.

Design Philosophy
-----------------
Zemax Report
      ↓
WavefrontParser
      ↓
 WavefrontData
      ↓
Wavefront Analysis
      ↓
 OpticalCase

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

import re

# ---------------------------------------------------------------------
# Third-Party Imports
# ---------------------------------------------------------------------

import numpy as np

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.wavefront_data import WavefrontData
from src.parsers.base_parser import BaseParser

from src.utils.zemax_text import (
    find_float,
    find_section,
    find_two_ints,
)

# ---------------------------------------------------------------------
# Wavefront Parser
# ---------------------------------------------------------------------


class WavefrontParser(BaseParser):
    """
    Parser for Zemax Wavefront Map text reports.

    This parser extracts only the raw information explicitly present
    in the Zemax export.

    No optical analysis is performed here.
    """

    # -----------------------------------------------------------------
    # Regular Expression Patterns
    # -----------------------------------------------------------------

    METADATA_PATTERN = re.compile(
        r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)\s*µm\s*at\s*"
        r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)\s*,\s*"
        r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
    )

    PV_RMS_PATTERN = re.compile(
        r"Peak to valley\s*=\s*"
        r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)\s*waves,"
        r"\s*RMS\s*=\s*"
        r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
    )

    EXIT_PUPIL_PATTERN = re.compile(
        r"Exit Pupil Diameter:\s*"
        r"([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
    )

    GRID_PATTERN = re.compile(
        r"Pupil grid size:\s*(\d+)\s*by\s*(\d+)"
    )

    CENTER_PATTERN = re.compile(
        r"Center point is:\s*Col\s*(\d+)\s*,\s*Row\s*(\d+)"
    )

    # -----------------------------------------------------------------
    # Public Interface
    # -----------------------------------------------------------------

    def parse(self) -> WavefrontData:
        """
        Parse a Zemax Wavefront Map text report.

        Returns
        -------
        WavefrontData
            Structured representation of the raw wavefront information
            contained in the Zemax report.

        Raises
        ------
        ValueError
            If required metadata or the wavefront map cannot be
            extracted.
        """

        # -------------------------------------------------------------
        # Read the complete Zemax report.
        # -------------------------------------------------------------

        text = self.read_file()

        # -------------------------------------------------------------
        # Extract metadata.
        # -------------------------------------------------------------

        (
            wavelength_um,
            field_x_deg,
            field_y_deg,
        ) = self._extract_wavelength_and_field(text)

        (
            peak_to_valley,
            rms,
        ) = self._extract_wavefront_errors(text)

        exit_pupil = self._extract_exit_pupil(text)

        grid_width, grid_height = self._extract_grid_size(text)

        center_column, center_row = self._extract_center(text)

        # -------------------------------------------------------------
        # Extract wavefront matrix.
        # -------------------------------------------------------------

        wavefront_map = self._extract_wavefront_matrix(
            text=text,
            width=grid_width,
            height=grid_height,
        )

        # -------------------------------------------------------------
        # Construct parsed data model.
        # -------------------------------------------------------------

        return WavefrontData(
            wavelength_um=wavelength_um,
            field_x_deg=field_x_deg,
            field_y_deg=field_y_deg,
            peak_to_valley_waves=peak_to_valley,
            rms_waves=rms,
            exit_pupil_diameter_mm=exit_pupil,
            grid_size_x=grid_width,
            grid_size_y=grid_height,
            center_column=center_column,
            center_row=center_row,
            wavefront_map=wavefront_map,
        )

    # -----------------------------------------------------------------
    # Metadata Extraction
    # -----------------------------------------------------------------

    def _extract_wavelength_and_field(
        self,
        text: str,
    ) -> tuple[float, float, float]:
        """
        Extract wavelength and field coordinates.

        Parameters
        ----------
        text
            Complete Zemax Wavefront Map report.

        Returns
        -------
        tuple[float, float, float]
            Wavelength (µm), field X (deg), field Y (deg).
        """

        match = self.METADATA_PATTERN.search(text)

        if match is None:

            raise ValueError(
                "Unable to locate wavefront wavelength and field "
                "coordinates."
            )

        return (
            float(match.group(1)),
            float(match.group(2)),
            float(match.group(3)),
        )

    # -----------------------------------------------------------------

    def _extract_wavefront_errors(
        self,
        text: str,
    ) -> tuple[float, float]:
        """
        Extract peak-to-valley and RMS wavefront error.

        Parameters
        ----------
        text
            Complete Zemax Wavefront Map report.

        Returns
        -------
        tuple[float, float]
            Peak-to-valley error and RMS error in waves.
        """

        match = self.PV_RMS_PATTERN.search(text)

        if match is None:

            raise ValueError(
                "Unable to locate wavefront error values."
            )

        return (
            float(match.group(1)),
            float(match.group(2)),
        )

    # -----------------------------------------------------------------

    def _extract_exit_pupil(
        self,
        text: str,
    ) -> float:
        """
        Extract the exit pupil diameter.

        Parameters
        ----------
        text
            Complete Zemax Wavefront Map report.

        Returns
        -------
        float
            Exit pupil diameter in millimeters.
        """

        return find_float(
            pattern=self.EXIT_PUPIL_PATTERN,
            text=text,
            error_message=(
                "Unable to locate Exit Pupil Diameter."
            ),
        )

    # -----------------------------------------------------------------

    def _extract_grid_size(
        self,
        text: str,
    ) -> tuple[int, int]:
        """
        Extract the dimensions of the wavefront grid.

        Parameters
        ----------
        text
            Complete Zemax Wavefront Map report.

        Returns
        -------
        tuple[int, int]
            Grid width and height.
        """

        return find_two_ints(
            pattern=self.GRID_PATTERN,
            text=text,
            error_message=(
                "Unable to locate Pupil Grid Size."
            ),
        )

    # -----------------------------------------------------------------

    def _extract_center(
        self,
        text: str,
    ) -> tuple[int, int]:
        """
        Extract the Zemax-reported wavefront grid center.

        Parameters
        ----------
        text
            Complete Zemax Wavefront Map report.

        Returns
        -------
        tuple[int, int]
            Center column and row.
        """

        return find_two_ints(
            pattern=self.CENTER_PATTERN,
            text=text,
            error_message=(
                "Unable to locate Wavefront Center."
            ),
        )

    # -----------------------------------------------------------------
    # Wavefront Matrix Extraction
    # -----------------------------------------------------------------

    def _extract_wavefront_matrix(
        self,
        text: str,
        width: int,
        height: int,
    ) -> np.ndarray:
        """
        Extract the two-dimensional wavefront map.

        Parameters
        ----------
        text
            Complete Zemax Wavefront Map report.

        width
            Expected number of columns.

        height
            Expected number of rows.

        Returns
        -------
        numpy.ndarray
            Two-dimensional wavefront map.

        Raises
        ------
        ValueError
            If the wavefront map cannot be located or its dimensions do
            not match the grid size reported by Zemax.
        """

        # -------------------------------------------------------------
        # Locate the beginning of the wavefront matrix.
        # -------------------------------------------------------------

        matrix_text = find_section(
            text=text,
            start_marker="Center point is:",
        )

        # -------------------------------------------------------------
        # Remove empty lines.
        # -------------------------------------------------------------

        lines = [
            line.strip()
            for line in matrix_text.splitlines()
            if line.strip()
        ]

        # -------------------------------------------------------------
        # Skip the "Center point is:" line.
        # -------------------------------------------------------------

        lines = lines[1:]

        # -------------------------------------------------------------
        # Verify sufficient rows exist.
        # -------------------------------------------------------------

        if len(lines) < height:

            raise ValueError(
                "Wavefront map contains fewer rows than expected."
            )

        # -------------------------------------------------------------
        # Parse each matrix row.
        # -------------------------------------------------------------

        wavefront_matrix: list[list[float]] = []

        for row_index in range(height):

            values = lines[row_index].split()

            if len(values) != width:
                raise ValueError(
                    f"Expected {width} wavefront values in row "
                    f"{row_index + 1}, found {len(values)}."
                )

            try:

                wavefront_matrix.append(
                    [
                        float(value)
                        for value in values
                    ]
                )

            except ValueError as exc:

                raise ValueError(
                    f"Unable to parse wavefront value in "
                    f"row {row_index + 1}."
                ) from exc

        # -------------------------------------------------------------
        # Convert to NumPy array.
        # -------------------------------------------------------------

        return np.asarray(
            wavefront_matrix,
            dtype=np.float64,
        )