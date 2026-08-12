"""
output.py

Reporting pipeline.

Purpose
-------
Coordinates generation of every statistical reporting artifact.

Pipeline
--------

Canonical Summary
        ↓
Metric Tables
        ↓
Report Tables

This module performs no statistical calculations itself. It simply
orchestrates the reporting stages.

Author: Manthan Bhagat
Project: Master's Thesis - Zemax Optical Analysis Toolkit
"""

# ---------------------------------------------------------------------
# Local Imports
# ---------------------------------------------------------------------

from src.models.analysis_type import AnalysisType

from src.report.metric_tables import (
    export_metric_tables,
)

from src.report.report_tables import (
    export_report_tables,
)

from src.report.summary import (
    export_summary,
)

from src.report.report_figures import (
    export_report_figures,
)

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_reports(
    analysis_type: AnalysisType,
) -> None:
    """
    Generate every statistical reporting artifact for an analysis.

    Parameters
    ----------
    analysis_type
        Analysis type to report.
    """

    # -------------------------------------------------------------
    # Canonical Summary
    # -------------------------------------------------------------

    summary = export_summary(
        analysis_type,
    )

    # -------------------------------------------------------------
    # Metric Tables
    # -------------------------------------------------------------

    export_metric_tables(
        analysis_type,
        summary,
    )

    # -------------------------------------------------------------
    # Thesis Report Tables
    # -------------------------------------------------------------

    export_report_tables(
        analysis_type,
        summary,
    )

    # -------------------------------------------------------------
    # Thesis Report Figures
    # -------------------------------------------------------------

    export_report_figures(
        analysis_type,
        summary,
    )