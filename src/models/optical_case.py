"""
optical_case.py

Central data model representing one complete Zemax analysis case.

Purpose
-------
Every Zemax analysis operating point (nominal, thermal, Monte Carlo,
tolerance, etc.) is represented internally as a single OpticalCase
object.

An OpticalCase acts as the central container that combines

- case metadata
- parsed Zemax data
- derived optical analysis results

All downstream modules (CSV export, Excel export, plotting, reporting,
etc.) operate exclusively on OpticalCase objects.

Design Philosophy
-----------------
            Zemax Reports
                  │
            Individual Parsers
                  │
          Raw Data Models
                  │
        Individual Analysis Modules
                  │
            Analysis Models
                  │
             OpticalCase
                  │
      CSV • Excel • Plots • Reports

An OpticalCase represents one unique operating point in the analysis
parameter space.

Examples
--------
Nominal Design

Thermal
    (Wavelength, Field, Temperature)

Monte Carlo
    (Wavelength, Field, Trial)

This design keeps the parser layer independent of directory layout while
allowing higher-level modules to group results naturally.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Standard Library Imports
# ---------------------------------------------------------------------

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.analysis_type import AnalysisType
from src.models.psf_analysis import PSFAnalysis
from src.models.psf_data import PSFData

#
# Future imports
#
# from src.models.mtf_data import MTFData
# from src.models.mtf_analysis import MTFAnalysis
# from src.models.rms_spot_data import RMSSpotData
# from src.models.rms_spot_analysis import RMSSpotAnalysis
# from src.models.wavefront_data import WavefrontData
# from src.models.wavefront_analysis import WavefrontAnalysis


# ---------------------------------------------------------------------
# Optical Case
# ---------------------------------------------------------------------

@dataclass(slots=True)
class OpticalCase:
    """
    Represents one complete optical analysis operating point.

    Each OpticalCase corresponds to one Zemax solution together with
    its associated analysis metadata.

    The class stores both the raw parser outputs and the derived
    optical analysis results.
    """

    # -------------------------------------------------------------
    # Case Metadata
    # -------------------------------------------------------------

    case_id: str
    """
    Unique identifier for this optical case.

    Examples
    --------
    NOMINAL

    THERMAL_W200_F01_T+20

    MC_W200_F03_0172
    """

    analysis_type: AnalysisType
    """
    Type of optical analysis.
    """

    case_directory: Path
    """
    Directory containing all Zemax reports associated with this case.
    """

    name: Optional[str] = None
    """
    Human-readable case name.
    """

    # -------------------------------------------------------------
    # Optical Coordinates
    # -------------------------------------------------------------

    wavelength_um: Optional[float] = None
    """
    Analysis wavelength.

    Units
    -----
    Micrometers (µm)

    Examples
    --------
    0.200

    0.250

    0.500
    """

    field_index: Optional[int] = None
    """
    Zemax Field Data Editor index.

    Examples
    --------
    1

    5

    12
    """

    # -------------------------------------------------------------
    # Thermal Metadata
    # -------------------------------------------------------------

    temperature_c: Optional[float] = None
    """
    Optical system temperature.

    Units
    -----
    Degrees Celsius (°C)

    Used only for thermal analyses.
    """

    # -------------------------------------------------------------
    # Statistical Metadata
    # -------------------------------------------------------------

    statistical_case: Optional[int | str] = None
    """
    Statistical identifier.

    Used by Monte Carlo analyses.

    Examples
    --------
    15

    Median

    Worst

    Best
    """

    # -------------------------------------------------------------
    # Parsed Zemax Data
    # -------------------------------------------------------------

    psf_data: Optional[PSFData] = None
    """
    Raw Point Spread Function data parsed from Zemax.
    """

    #
    # Future additions
    #
    # mtf_data: Optional[MTFData] = None
    # rms_spot_data: Optional[RMSSpotData] = None
    # wavefront_data: Optional[WavefrontData] = None

    # -------------------------------------------------------------
    # Derived Optical Analysis
    # -------------------------------------------------------------

    psf_analysis: Optional[PSFAnalysis] = None
    """
    Derived optical metrics computed from the PSF.
    """

    #
    # Future additions
    #
    # mtf_analysis: Optional[MTFAnalysis] = None
    # rms_spot_analysis: Optional[RMSSpotAnalysis] = None
    # wavefront_analysis: Optional[WavefrontAnalysis] = None