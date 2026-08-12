"""
main.py

Entry point for the Zemax Optical Analysis Toolkit.

Usage
-----

Run everything

    python main.py

Run all thermal pipelines

    python main.py thermal

Run all Monte Carlo pipelines

    python main.py monte-carlo

Run only PSF for thermal analyses

    python main.py thermal psf

Run only MTF for every case-based analysis

    python main.py all mtf

Run standalone tolerance analysis

    python main.py tolerance

Generate thermal reports

    python main.py report thermal

Generate Monte Carlo reports

    python main.py report monte-carlo

Generate every report

    python main.py report all
"""

from __future__ import annotations

import sys

from src.collectors.case_loader import load_cases

from src.config import (
    INPUT_DIRECTORY,
    BASELINE_INPUT_DIRECTORY,
)

from src.models.analysis_type import AnalysisType

from src.pipeline.output import generate_outputs

from src.pipeline.psf import process_psf
from src.pipeline.mtf import process_mtf
from src.pipeline.spot import process_spot
from src.pipeline.wavefront import process_wavefront

from src.pipeline.baseline import (
    run_baseline_pipeline,
)

from src.pipeline.tolerance import (
    run as run_tolerance,
)

from src.report.output import (
    generate_reports,
)

# ---------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------

CASE_PIPELINES = {

    "psf": process_psf,

    "mtf": process_mtf,

    "spot": process_spot,

    "wavefront": process_wavefront,
}

STANDALONE_PIPELINES = {

    "tolerance": run_tolerance,

    "baseline": lambda: run_baseline_pipeline(
        BASELINE_INPUT_DIRECTORY,
    ),
}

REPORT_PIPELINES = {

    "baseline": AnalysisType.BASELINE,

    "thermal": AnalysisType.THERMAL,

    "monte-carlo": AnalysisType.MONTE_CARLO,
}

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _load_cases(
    analysis: str,
):
    """
    Load and filter optical cases.
    """

    cases = load_cases(
        INPUT_DIRECTORY,
    )

    if analysis == "all":

        return cases

    analysis_map = {

        "thermal": AnalysisType.THERMAL,

        "monte-carlo": AnalysisType.MONTE_CARLO,
    }

    try:

        analysis_type = analysis_map[
            analysis
        ]

    except KeyError as exc:

        valid = ", ".join(
            analysis_map.keys()
        )

        raise ValueError(
            f"Unknown analysis '{analysis}'. "
            f"Expected one of: all, {valid}."
        ) from exc

    return [

        case

        for case in cases

        if case.analysis_type == analysis_type
    ]


def _select_case_pipelines(
    pipeline: str,
):
    """
    Select OpticalCase processing pipelines.
    """

    if pipeline == "all":

        return list(
            CASE_PIPELINES.values()
        )

    try:

        return [
            CASE_PIPELINES[pipeline]
        ]

    except KeyError as exc:

        valid = ", ".join(
            CASE_PIPELINES.keys()
        )

        raise ValueError(
            f"Unknown pipeline '{pipeline}'. "
            f"Expected one of: all, {valid}."
        ) from exc


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main() -> None:
    """
    Execute the requested analysis.
    """

    analysis = (

        sys.argv[1].lower()

        if len(sys.argv) > 1

        else "all"
    )

    # -------------------------------------------------------------
    # Report generation.
    # -------------------------------------------------------------

    if analysis == "report":

        report_analysis = (

            sys.argv[2].lower()

            if len(sys.argv) > 2

            else "all"
        )

        if report_analysis == "all":

            generate_reports(
                AnalysisType.BASELINE,
            )

            generate_reports(
                AnalysisType.THERMAL,
            )

            generate_reports(
                AnalysisType.MONTE_CARLO,
            )

        else:

            try:

                generate_reports(
                    REPORT_PIPELINES[
                        report_analysis
                    ],
                )

            except KeyError as exc:

                valid = ", ".join(
                    REPORT_PIPELINES.keys()
                )

                raise ValueError(
                    f"Unknown report analysis "
                    f"'{report_analysis}'. "
                    f"Expected one of: all, {valid}."
                ) from exc

        print(
            "Report generation completed successfully.\n"
            f"Analysis: {report_analysis}"
        )

        return

    # -------------------------------------------------------------
    # Standalone pipelines.
    # -------------------------------------------------------------

    if analysis in STANDALONE_PIPELINES:

        STANDALONE_PIPELINES[
            analysis
        ]()

        print(
            f"{analysis} completed successfully."
        )

        return

    pipeline = (

        sys.argv[2].lower()

        if len(sys.argv) > 2

        else "all"
    )

    # -------------------------------------------------------------
    # Case discovery.
    # -------------------------------------------------------------

    cases = _load_cases(
        analysis,
    )

    if not cases:

        print(
            f"No '{analysis}' cases found."
        )

        return

    # -------------------------------------------------------------
    # Pipeline selection.
    # -------------------------------------------------------------

    pipelines = _select_case_pipelines(
        pipeline,
    )

    # -------------------------------------------------------------
    # Execute pipelines.
    # -------------------------------------------------------------

    for optical_case in cases:

        for process in pipelines:

            process(
                optical_case,
            )

    # -------------------------------------------------------------
    # Export outputs.
    # -------------------------------------------------------------

    generate_outputs(
        cases,
    )

    print(
        "Optical analysis completed successfully.\n"
        f"Analysis : {analysis}\n"
        f"Pipelines: {pipeline}"
    )


# ---------------------------------------------------------------------
# Script Entry Point
# ---------------------------------------------------------------------

if __name__ == "__main__":

    main()