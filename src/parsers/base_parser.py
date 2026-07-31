"""
base_parser.py

This module defines the abstract base class used by all Zemax text
parsers in the Optical Analysis Toolkit.

Rather than allowing every parser to implement its own file-reading
logic, this class provides common functionality such as

    • verifying that a file exists
    • automatically detecting text encoding
    • reading the file contents
    • basic error handling

Individual parsers (PSF, MTF, EE, Strehl, Wavefront, etc.) inherit from
this class and only implement the logic required to extract the optical
quantities they are responsible for.

Supported Encodings
-------------------
The parser automatically detects the most common encodings used by
Zemax text exports.

    • UTF-16 Little Endian (with BOM)
    • UTF-16 Big Endian (with BOM)
    • UTF-8 (with or without BOM)
    • Windows ANSI (CP1252)

This makes the parser robust across different Zemax versions and
different analysis exports.

Author: Manthan Bhagat
Project: Master's Thesis - Optical Analysis Toolkit
"""

# -------------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod
from pathlib import Path


# -------------------------------------------------------------------------
# Base Parser Class
# -------------------------------------------------------------------------

class BaseParser(ABC):
    """
    Abstract base class for all Zemax text parsers.

    Every parser in this project should inherit from this class.

    Responsibilities
    ----------------
    1. Verify that the requested file exists.
    2. Automatically detect the file encoding.
    3. Read the complete text file.
    4. Delegate extraction of values to the child parser.

    Child classes are required to implement the parse() method.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, file_path: Path):
        """
        Initialize the parser.

        Parameters
        ----------
        file_path : Path
            Path to the Zemax text export.
        """

        self.file_path = file_path

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _decode_bytes(data: bytes) -> str:
        """
        Decode raw file bytes using automatic encoding detection.

        Zemax text exports are unfortunately not consistent across
        analyses or software versions. Some analyses are exported as
        UTF-16, others as UTF-8, and older versions may produce ANSI
        encoded files.

        This method transparently handles all common cases.

        Parameters
        ----------
        data : bytes
            Raw file contents.

        Returns
        -------
        str
            Decoded Unicode string.

        Raises
        ------
        UnicodeDecodeError
            If the file cannot be decoded using any supported encoding.
        """

        # --------------------------------------------------------------
        # UTF-16 Little Endian BOM
        # --------------------------------------------------------------
        if data.startswith(b"\xff\xfe"):
            return data.decode("utf-16")

        # --------------------------------------------------------------
        # UTF-16 Big Endian BOM
        # --------------------------------------------------------------
        if data.startswith(b"\xfe\xff"):
            return data.decode("utf-16")

        # --------------------------------------------------------------
        # UTF-8 with BOM
        # --------------------------------------------------------------
        if data.startswith(b"\xef\xbb\xbf"):
            return data.decode("utf-8-sig")

        # --------------------------------------------------------------
        # Plain UTF-8
        # --------------------------------------------------------------
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            pass

        # --------------------------------------------------------------
        # Windows ANSI (common for older Windows applications)
        # --------------------------------------------------------------
        try:
            return data.decode("cp1252")
        except UnicodeDecodeError:
            pass

        # --------------------------------------------------------------
        # ISO Latin-1 fallback
        #
        # Latin-1 never fails and preserves all byte values, making it
        # useful as a last resort for unusual text exports.
        # --------------------------------------------------------------
        try:
            return data.decode("latin-1")
        except UnicodeDecodeError:
            pass

        # --------------------------------------------------------------
        # Nothing worked
        # --------------------------------------------------------------
        raise UnicodeDecodeError(
            "unknown",
            data,
            0,
            1,
            (
                f"Unable to determine encoding of "
                f"'{len(data)}' byte Zemax export."
            ),
        )

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def read_file(self) -> str:
        """
        Read the complete Zemax text export.

        The file encoding is detected automatically.

        Returns
        -------
        str
            Complete decoded text.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.

        UnicodeDecodeError
            If the file cannot be decoded.
        """

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        data = self.file_path.read_bytes()

        return self._decode_bytes(data)

    # ------------------------------------------------------------------
    # Abstract Interface
    # ------------------------------------------------------------------

    @abstractmethod
    def parse(self):
        """
        Extract optical quantities from the Zemax export.

        This method must be implemented by every child parser.

        Returns
        -------
        object
            Parsed result. The exact return type depends on the parser.
        """

        raise NotImplementedError