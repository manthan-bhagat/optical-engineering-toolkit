"""
analysis_type.py

Enumeration defining the supported optical analysis types.

Purpose
-------
Every OpticalCase belongs to exactly one analysis category.

Using an enumeration instead of plain strings provides

- type safety
- IDE auto-completion
- consistent naming
- easier filtering and validation

Examples
--------
>>> AnalysisType.NOMINAL
>>> AnalysisType.THERMAL
>>> AnalysisType.MONTE_CARLO

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from enum import Enum


# ---------------------------------------------------------------------
# Analysis Types
# ---------------------------------------------------------------------


class AnalysisType(str, Enum):
    """
    Supported optical analysis categories.

    These values identify the origin of an OpticalCase and determine
    how collections of cases are grouped, plotted, and exported.
    """

    NOMINAL = "nominal"
    """
    Nominal optical design.
    """

    THERMAL = "thermal"
    """
    Thermo-optical analysis performed at different temperatures.
    """

    MONTE_CARLO = "monte_carlo"
    """
    Statistical Monte Carlo tolerance analysis.
    """

    TOLERANCE = "tolerance"
    """
    Deterministic optical tolerance analysis.
    """

    STRAY_LIGHT = "stray_light"
    """
    Stray light analysis.
    """

    SCATTERING = "scattering"
    """
    Surface and bulk scattering analysis.
    """

    DISTORTION = "distortion"
    """
    Image distortion analysis.
    """

    FOCUS = "focus"
    """
    Focus sweep or refocus analysis.
    """

    WAVELENGTH = "wavelength"
    """
    Multi-wavelength optical performance analysis.
    """

    FIELD = "field"
    """
    Performance evaluated across field positions.
    """

    # -----------------------------------------------------------------
    # Metadata
    # -----------------------------------------------------------------

    @property
    def directory_name(self) -> str:
        """
        Canonical directory name used for exported results.

        Returns
        -------
        str
            Directory name under the output root.
        """

        return self.value

    @property
    def display_name(self) -> str:
        """
        Human-readable analysis name.
        """

        return {
            AnalysisType.NOMINAL: "Nominal Design",
            AnalysisType.THERMAL: "Thermal Analysis",
            AnalysisType.MONTE_CARLO: "Monte Carlo Analysis",
            AnalysisType.TOLERANCE: "Tolerance Analysis",
            AnalysisType.STRAY_LIGHT: "Stray Light Analysis",
            AnalysisType.SCATTERING: "Scattering Analysis",
            AnalysisType.DISTORTION: "Distortion Analysis",
            AnalysisType.FOCUS: "Focus Analysis",
            AnalysisType.WAVELENGTH: "Wavelength Analysis",
            AnalysisType.FIELD: "Field Analysis",
        }[self]