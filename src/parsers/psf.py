"""
psf.py

Parser for Zemax Huygens Point Spread Function (PSF) text exports.

Purpose
-------
This parser reads a Zemax Huygens PSF text report and extracts the
information explicitly contained in the report.

Responsibilities
----------------
The parser extracts

- Strehl Ratio
- Pixel Spacing
- Image Dimensions
- PSF Center Coordinates
- Two-dimensional PSF Intensity Matrix

The parser DOES NOT

- compute FWHM
- compute EE80
- compute radial profiles
- compute equivalent PSF
- validate optical performance

Those responsibilities belong to the analysis module.

Design Philosophy
-----------------
Zemax Report
      ↓
 PSFParser
      ↓
  PSFData
      ↓
PSF Analysis
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

from src.models.psf_data import PSFData
from src.parsers.base_parser import BaseParser

from src.utils.zemax_text import (
    find_float,
    find_section,
    find_two_ints,
)

# ---------------------------------------------------------------------
# PSF Parser
# ---------------------------------------------------------------------


class PSFParser(BaseParser):
    """
    Parser for Zemax Huygens PSF text reports.

    This parser extracts only the raw information explicitly present
    in the Zemax export.

    No optical analysis is performed here.
    """

    # -----------------------------------------------------------------
    # Regular Expression Patterns
    # -----------------------------------------------------------------

    STREHL_PATTERN = re.compile(
        r"Strehl ratio:\s*([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
    )

    PIXEL_SPACING_PATTERN = re.compile(
        r"Data spacing is\s*([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
    )

    IMAGE_GRID_PATTERN = re.compile(
        r"Image grid size:\s*(\d+)\s*by\s*(\d+)"
    )

    CENTER_PATTERN = re.compile(
        r"Center point is:\s*(\d+)\s*,\s*(\d+)"
    )

    # -----------------------------------------------------------------
    # Public Interface
    # -----------------------------------------------------------------

    def parse(self) -> PSFData:
        """
        Parse a Zemax Huygens PSF text report.

        Returns
        -------
        PSFData
            Structured representation of the raw PSF data contained in
            the Zemax report.

        Raises
        ------
        ValueError
            If any required metadata or PSF data cannot be extracted.
        """

        # -------------------------------------------------------------
        # Read the complete Zemax report.
        # -------------------------------------------------------------

        text = self.read_file()

        # -------------------------------------------------------------
        # Extract metadata.
        # -------------------------------------------------------------

        strehl_ratio = self._extract_strehl_ratio(text)

        pixel_spacing = self._extract_pixel_spacing(text)

        image_width, image_height = self._extract_image_size(text)

        center_x, center_y = self._extract_center(text)

        # -------------------------------------------------------------
        # Extract the two-dimensional PSF intensity matrix.
        # -------------------------------------------------------------

        psf = self._extract_psf_matrix(
            text=text,
            width=image_width,
            height=image_height,
        )

        # -------------------------------------------------------------
        # Construct the parsed data model.
        # -------------------------------------------------------------

        return PSFData(
            strehl_ratio=strehl_ratio,
            pixel_spacing_um=pixel_spacing,
            image_width=image_width,
            image_height=image_height,
            center_x=center_x,
            center_y=center_y,
            psf=psf,
        )

    # -----------------------------------------------------------------
    # Metadata Extraction
    # -----------------------------------------------------------------

    def _extract_strehl_ratio(self, text: str) -> float:
        """
        Extract the Strehl ratio reported by Zemax.

        Parameters
        ----------
        text
            Complete Zemax PSF report.

        Returns
        -------
        float
            Strehl ratio.
        """

        return find_float(
            pattern=self.STREHL_PATTERN,
            text=text,
            error_message="Unable to locate Strehl Ratio.",
        )

    # -----------------------------------------------------------------

    def _extract_pixel_spacing(self, text: str) -> float:
        """
        Extract the physical spacing between adjacent PSF samples.

        Parameters
        ----------
        text
            Complete Zemax PSF report.

        Returns
        -------
        float
            Pixel spacing in micrometers.
        """

        return find_float(
            pattern=self.PIXEL_SPACING_PATTERN,
            text=text,
            error_message="Unable to locate Data Spacing.",
        )

    # -----------------------------------------------------------------

    def _extract_image_size(self, text: str) -> tuple[int, int]:
        """
        Extract the dimensions of the PSF image.

        Parameters
        ----------
        text
            Complete Zemax PSF report.

        Returns
        -------
        tuple[int, int]
            Image width and height.
        """

        return find_two_ints(
            pattern=self.IMAGE_GRID_PATTERN,
            text=text,
            error_message="Unable to locate Image Grid Size.",
        )

    # -----------------------------------------------------------------

    def _extract_center(self, text: str) -> tuple[int, int]:
        """
        Extract the Zemax-reported PSF center.

        Parameters
        ----------
        text
            Complete Zemax PSF report.

        Returns
        -------
        tuple[int, int]
            Center pixel coordinates.
        """

        return find_two_ints(
            pattern=self.CENTER_PATTERN,
            text=text,
            error_message="Unable to locate PSF Center.",
        )

    # -----------------------------------------------------------------
    # PSF Matrix Extraction
    # -----------------------------------------------------------------

    def _extract_psf_matrix(
        self,
        text: str,
        width: int,
        height: int,
    ) -> np.ndarray:
        """
        Extract the two-dimensional PSF intensity matrix.

        Parameters
        ----------
        text
            Complete Zemax PSF report.

        width
            Expected number of columns in the PSF image.

        height
            Expected number of rows in the PSF image.

        Returns
        -------
        numpy.ndarray
            Two-dimensional array containing the relative PSF intensity.

        Raises
        ------
        ValueError
            If the PSF matrix cannot be located or its dimensions do not
            match the image size reported by Zemax.
        """

        # -------------------------------------------------------------
        # Locate the start of the PSF intensity data.
        # -------------------------------------------------------------

        matrix_text = find_section(
            text=text,
            start_marker="Values are relative intensity.",
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
        # Verify that enough rows exist.
        # -------------------------------------------------------------

        if len(lines) < height:
            raise ValueError(
                "PSF matrix contains fewer rows than expected."
            )

        # -------------------------------------------------------------
        # Parse each matrix row.
        # -------------------------------------------------------------

        psf_matrix: list[list[float]] = []

        for row_index in range(height):

            values = lines[row_index].split()

            if len(values) != width:
                raise ValueError(
                    f"Expected {width} values in PSF row "
                    f"{row_index + 1}, found {len(values)}."
                )

            try:

                psf_matrix.append(
                    [float(value) for value in values]
                )

            except ValueError as exc:

                raise ValueError(
                    f"Unable to parse PSF value in row "
                    f"{row_index + 1}."
                ) from exc

        # -------------------------------------------------------------
        # Convert to a NumPy array.
        # -------------------------------------------------------------

        psf = np.asarray(
            psf_matrix,
            dtype=np.float64,
        )

        if psf.shape != (height, width):
            raise ValueError(
                f"Expected PSF matrix shape ({height}, {width}), "
                f"found {psf.shape}."
            )

        return psf