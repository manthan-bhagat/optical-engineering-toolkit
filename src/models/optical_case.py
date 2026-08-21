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
from src.models.mtf_analysis import MTFAnalysis
from src.models.mtf_data import MTFData

from src.models.spot_field import SpotField

from src.models.wavefront_data import WavefrontData
from src.models.wavefront_analysis import WavefrontAnalysis

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

    spot_file: Optional[Path] = None
    """
    Path to the Zemax Spot Diagram report.

    Unlike PSF, MTF, and Wavefront reports, a Spot Diagram is generated once
    per operating point and contains measurements for every field position.

    Thermal
    -------
    dataset/
        wavelength/
            temperature/
                spot.txt

    Monte Carlo
    -----------
    dataset/
        wavelength/
            spot.txt
    """

    name: Optional[str] = None
    """
    Human-readable case name.
    """

    # -------------------------------------------------------------
    # Dataset Metadata
    # -------------------------------------------------------------

    dataset: Optional[str] = None
    """
    Name of the dataset containing this analysis case.

    Used to distinguish different collections of the same analysis type.

    Examples
    --------
    survival

    operational

    nominal

    baseline

    redesign
    """

    # -------------------------------------------------------------
    # Configuration Metadata
    # -------------------------------------------------------------

    configuration: Optional[int] = None
    """
    Zemax multi-configuration index associated with this analysis case.

    Used when a single optical design contains multiple physical or
    optical configurations, such as filter configurations.

    Examples
    --------
    1

    6

    9
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

    mtf_data: Optional[MTFData] = None
    """
    Raw optical-field Modulation Transfer Function (MTF) data parsed
    from Zemax.
    """

    mtf_diffraction: Optional[MTFData] = None
    """
    Diffraction-limited Modulation Transfer Function (MTF) reference
    corresponding to the same wavelength as mtf_data.
    """

    # -------------------------------------------------------------
    # Spot Diagram
    # -------------------------------------------------------------

    spot_field: Optional[SpotField] = None
    """
    Spot Diagram measurements corresponding to this optical field.

    Although Zemax exports one Spot Diagram report containing every field,
    the processing pipeline assigns only the matching SpotField to each
    OpticalCase.

    This keeps the OpticalCase consistent with the PSF, MTF, and Wavefront
    models, where each object represents one field of one operating point.
    """

    wavefront_data: Optional[WavefrontData] = None
    """
    Raw Wavefront Map data parsed from Zemax.
    """

    # -------------------------------------------------------------
    # Derived Optical Analysis
    # -------------------------------------------------------------

    psf_analysis: Optional[PSFAnalysis] = None
    """
    Derived optical metrics computed from the PSF.
    """

    mtf_analysis: Optional[MTFAnalysis] = None
    """
    Derived optical metrics computed from the MTF.
    """

    wavefront_analysis: Optional[WavefrontAnalysis] = None
    """
    Derived optical metrics computed from the Wavefront Map.
    """