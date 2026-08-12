"""
mtf.py

Parser for Zemax FFT Modulation Transfer Function (MTF) text exports.

Purpose
-------
This parser reads a Zemax FFT MTF text report and extracts the
information explicitly contained in the report.

Responsibilities
----------------
The parser extracts

- Wavelength
- Diffraction-limited MTF
- Optical field MTF

at the configured analysis spatial frequencies.

The parser DOES NOT

- compute mean MTF
- compute statistics
- compare thermal cases
- compare Monte Carlo trials
- validate optical performance

Those responsibilities belong to the analysis module.

Design Philosophy
-----------------
Zemax Report
      ↓
 MTFParser
      ↓
 MTFReport
      ↓
MTF Analysis
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

from src.config import MTF_ANALYSIS_FREQUENCIES

from src.models.mtf_data import MTFData
from src.models.mtf_report import MTFReport

from src.parsers.base_parser import BaseParser

from src.utils.zemax_text import (
    find_float,
)

# ---------------------------------------------------------------------
# MTF Parser
# ---------------------------------------------------------------------


class MTFParser(BaseParser):
    """
    Parser for Zemax FFT MTF text reports.

    This parser extracts only the raw information explicitly present
    in the Zemax export.

    No optical analysis is performed here.
    """

    # -----------------------------------------------------------------
    # Regular Expression Patterns
    # -----------------------------------------------------------------

    WAVELENGTH_PATTERN = re.compile(
        r"Data for\s*([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)\s*µm"
    )

    DIFFRACTION_PATTERN = re.compile(
        r"Field:\s*Diffraction limit"
    )

    FIELD_PATTERN = re.compile(
        r"Field:\s*([+-]?\d*\.?\d+)\s*,\s*([+-]?\d*\.?\d+)\s*\(deg\)"
    )

    TABLE_ROW_PATTERN = re.compile(
        r"""
        ^\s*
        ([+-]?\d*\.?\d+)
        \s+
        ([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)
        \s+
        ([+-]?\d*\.?\d+(?:[Ee][+-]?\d+)?)
        \s*$
        """,
        re.MULTILINE | re.VERBOSE,
    )

    # -----------------------------------------------------------------
    # Public Interface
    # -----------------------------------------------------------------

    def parse(self) -> MTFReport:
        """
        Parse a Zemax FFT MTF text report.

        Returns
        -------
        MTFReport
            Structured representation of the raw MTF report.

        Raises
        ------
        ValueError
            If any required information cannot be extracted.
        """

        # -------------------------------------------------------------
        # Read complete report.
        # -------------------------------------------------------------

        text = self.read_file()

        # -------------------------------------------------------------
        # Split report into wavelength sections.
        # -------------------------------------------------------------

        wavelength_sections = self._extract_wavelength_sections(
            text
        )

        # -------------------------------------------------------------
        # Parse each wavelength section.
        # -------------------------------------------------------------

        diffraction: list[MTFData] = []
        fields: list[MTFData] = []

        for section in wavelength_sections:

            wavelength = self._parse_wavelength(section)

            diffraction.append(
                self._parse_diffraction(
                    section=section,
                    wavelength=wavelength,
                )
            )

            fields.append(
                self._parse_field(
                    section=section,
                    wavelength=wavelength,
                )
            )

        # -------------------------------------------------------------
        # Construct parsed report.
        # -------------------------------------------------------------

        return MTFReport(
            diffraction=diffraction,
            fields=fields,
        )

    # -----------------------------------------------------------------
    # Wavelength Sections
    # -----------------------------------------------------------------

    def _extract_wavelength_sections(
            self,
            text: str,
    ) -> list[str]:
        """
        Split the Zemax FFT MTF report into wavelength sections.

        Parameters
        ----------
        text
            Complete Zemax FFT MTF report.

        Returns
        -------
        list[str]
            One report section per wavelength.

        Raises
        ------
        ValueError
            If no wavelength sections are found.
        """

        parts = text.split("Data for")

        if len(parts) <= 1:
            raise ValueError(
                "Unable to locate wavelength sections."
            )

        return [
            "Data for" + section
            for section in parts[1:]
        ]

    # -----------------------------------------------------------------

    def _parse_wavelength(
            self,
            section: str,
    ) -> float:
        """
        Extract the wavelength corresponding to a report section.

        Parameters
        ----------
        section
            Single wavelength section of the FFT MTF report.

        Returns
        -------
        float
            Wavelength in micrometers (µm).
        """

        return find_float(
            pattern=self.WAVELENGTH_PATTERN,
            text=section,
            error_message="Unable to locate wavelength.",
        )

    # -----------------------------------------------------------------
    # Table Helpers
    # -----------------------------------------------------------------

    def _parse_table(
        self,
        table: str,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Parse an MTF table.

        Parameters
        ----------
        table
            Zemax MTF table.

        Returns
        -------
        tuple[np.ndarray, np.ndarray, np.ndarray]

            Spatial frequencies

            Tangential MTF

            Sagittal MTF
        """

        frequencies = []
        tangential = []
        sagittal = []

        for match in self.TABLE_ROW_PATTERN.finditer(table):

            frequencies.append(float(match.group(1)))
            tangential.append(float(match.group(2)))
            sagittal.append(float(match.group(3)))

        if not frequencies:
            raise ValueError(
                "Unable to locate MTF table."
            )

        return (
            np.asarray(frequencies),
            np.asarray(tangential),
            np.asarray(sagittal),
        )

    # -----------------------------------------------------------------

    def _interpolate(
        self,
        frequencies: np.ndarray,
        values: np.ndarray,
        target: float,
    ) -> float:
        """
        Interpolate an MTF value at the requested spatial frequency.

        Parameters
        ----------
        frequencies
            Sampled spatial frequencies.

        values
            Corresponding MTF values.

        target
            Requested spatial frequency.

        Returns
        -------
        float
            Interpolated MTF.
        """

        return float(
            np.interp(
                target,
                frequencies,
                values,
            )
        )

    # -----------------------------------------------------------------
    # Diffraction
    # -----------------------------------------------------------------

    def _parse_diffraction(
        self,
        section: str,
        wavelength: float,
    ) -> MTFData:
        """
        Parse the diffraction-limited MTF contained within a wavelength
        section.

        Parameters
        ----------
        section
            Single wavelength section.

        wavelength
            Wavelength corresponding to the section.

        Returns
        -------
        MTFData
            Parsed diffraction-limited MTF.
        """

        match = self.DIFFRACTION_PATTERN.search(section)

        if match is None:
            raise ValueError(...)

        start = match.start()

        if start == -1:
            raise ValueError(
                "Unable to locate diffraction-limited MTF."
            )

        end = section.find("Field:", start + 1)

        if end == -1:
            raise ValueError(
                "Unable to determine end of diffraction table."
            )

        table = section[start:end]

        frequencies, tangential, sagittal = self._parse_table(
            table
        )

        return MTFData(
            wavelength_um=wavelength,
            field_x_deg=np.nan,
            field_y_deg=np.nan,
            tangential_17_2=self._interpolate(
                frequencies,
                tangential,
                MTF_ANALYSIS_FREQUENCIES[0],
            ),
            sagittal_17_2=self._interpolate(
                frequencies,
                sagittal,
                MTF_ANALYSIS_FREQUENCIES[0],
            ),
            tangential_41_7=self._interpolate(
                frequencies,
                tangential,
                MTF_ANALYSIS_FREQUENCIES[1],
            ),
            sagittal_41_7=self._interpolate(
                frequencies,
                sagittal,
                MTF_ANALYSIS_FREQUENCIES[1],
            ),
        )

    # -----------------------------------------------------------------
    # Optical Field
    # -----------------------------------------------------------------

    def _parse_field(
        self,
        section: str,
        wavelength: float,
    ) -> MTFData:
        """
        Parse the optical field MTF contained within a wavelength
        section.

        Parameters
        ----------
        section
            Single wavelength section.

        wavelength
            Wavelength corresponding to the section.

        Returns
        -------
        MTFData
            Parsed optical field MTF.
        """

        match = self.FIELD_PATTERN.search(section)

        if match is None:
            raise ValueError(
                "Unable to locate optical field."
            )

        field_x = float(match.group(1))
        field_y = float(match.group(2))

        start = match.start()

        table = section[start:]

        frequencies, tangential, sagittal = self._parse_table(
            table
        )

        return MTFData(
            wavelength_um=wavelength,
            field_x_deg=field_x,
            field_y_deg=field_y,
            tangential_17_2=self._interpolate(
                frequencies,
                tangential,
                MTF_ANALYSIS_FREQUENCIES[0],
            ),
            sagittal_17_2=self._interpolate(
                frequencies,
                sagittal,
                MTF_ANALYSIS_FREQUENCIES[0],
            ),
            tangential_41_7=self._interpolate(
                frequencies,
                tangential,
                MTF_ANALYSIS_FREQUENCIES[1],
            ),
            sagittal_41_7=self._interpolate(
                frequencies,
                sagittal,
                MTF_ANALYSIS_FREQUENCIES[1],
            ),
        )