"""
select_representative_trials.py

Purpose
-------
Parse a Zemax Monte Carlo tolerance analysis report, identify
representative Monte Carlo trials, and generate:

    1. representative_trials.csv
    2. export_monte_carlo.zpl

The ZPL macro is generated from a template by replacing

    {{REPRESENTATIVE_TRIALS}}

with fully expanded representative trial export blocks.

Representative Cases
--------------------
The following representative Monte Carlo trials are exported:

    • Best
    • 2nd Percentile
    • 10th Percentile
    • 20th Percentile
    • Median (50th Percentile)
    • Mean
    • 80th Percentile
    • 90th Percentile
    • 98th Percentile
    • Worst

Each representative trial exports every wavelength, every field,
and every enabled optical analysis.

Generated ZPL
-------------
The generated macro is completely self-contained.

Each representative trial block:

    • Loads the Monte Carlo lens
    • Determines the dataset dimensions
    • Exports every wavelength
    • Exports the spot diagram
    • Exports every field
        • Huygens PSF
        • FFT MTF
        • Wavefront Map

No ZPL labels or GOTOs are generated. Conditional execution uses
structured IF ... ENDIF blocks.
"""

from __future__ import annotations

import csv
import re

from pathlib import Path

# ======================================================================
# Project Paths
# ======================================================================

ROOT = Path(
    r"C:\archive\manthan\projects\uv-vis-instrument"
)

OPTICS = (
    ROOT
    / "optical_designs"
    / "05-nominal-optical-design"
)

TOOLKIT = (
    ROOT
    / "development"
    / "optical-engineering-toolkit"
)

INPUT_FILE = (
    OPTICS
    / "tolerance-analysis-result.txt"
)

CSV_OUTPUT = (
    OPTICS
    / "representative_trials.csv"
)

TEMPLATE_FILE = (
    TOOLKIT
    / "templates"
    / "export_monte_carlo_template.zpl"
)

MACRO_OUTPUT = (
    Path(
        r"C:\Users\InstruZemax\Documents\ZEMAX\Macros"
    )
    / "export_monte_carlo.zpl"
)

# ======================================================================
# Report Parsing Expressions
# ======================================================================

TRIAL_PATTERN = re.compile(
    r"^\s*(\d+)\s+([0-9Ee+\-.]+)\s+([0-9Ee+\-.]+)"
)

BEST_PATTERN = re.compile(
    r"Best\s+([0-9Ee+\-.]+)\s+Trial\s+(\d+)"
)

WORST_PATTERN = re.compile(
    r"Worst\s+([0-9Ee+\-.]+)\s+Trial\s+(\d+)"
)

MEAN_PATTERN = re.compile(
    r"Mean\s+([0-9Ee+\-.]+)"
)

PERCENTILE_PATTERN = re.compile(
    r"(\d+)%\s*>\s*([0-9Ee+\-.]+)"
)

# ======================================================================
# Parse Monte Carlo Report
# ======================================================================

print("==============================================================")
print("Representative Monte Carlo Trial Selection")
print("==============================================================")
print()

print("Reading tolerance analysis report...")
print(INPUT_FILE)
print()

trials = []

best_trial = None
best_value = None

worst_trial = None
worst_value = None

mean_value = None

percentiles = {}

with INPUT_FILE.open(
    "r",
    encoding="utf-16",
    errors="ignore",
) as report:

    for line in report:

        match = TRIAL_PATTERN.search(line)

        if match:

            trial = int(
                match.group(1)
            )

            criterion = float(
                match.group(2)
            )

            trials.append(
                (
                    trial,
                    criterion,
                )
            )

            continue

        match = BEST_PATTERN.search(line)

        if match:

            best_value = float(
                match.group(1)
            )

            best_trial = int(
                match.group(2)
            )

            continue

        match = WORST_PATTERN.search(line)

        if match:

            worst_value = float(
                match.group(1)
            )

            worst_trial = int(
                match.group(2)
            )

            continue

        match = MEAN_PATTERN.search(line)

        if match:

            mean_value = float(
                match.group(1)
            )

            continue

        match = PERCENTILE_PATTERN.search(line)

        if match:

            percentiles[
                int(match.group(1))
            ] = float(
                match.group(2)
            )

# ======================================================================
# Validation
# ======================================================================

print("Report Summary")
print("------------------------------")
print(f"Trials Found      : {len(trials)}")
print(f"Best Trial        : {best_trial}")
print(f"Worst Trial       : {worst_trial}")
print(f"Mean Criterion    : {mean_value}")
print(f"Percentiles Found : {sorted(percentiles.keys())}")
print()

if not trials:

    raise RuntimeError(
        "No Monte Carlo trials were found."
    )

required_percentiles = [
    2,
    10,
    20,
    50,
    80,
    90,
    98,
]

for percentile in required_percentiles:

    if percentile not in percentiles:

        raise RuntimeError(
            f"Missing {percentile}% percentile."
        )

if best_trial is None:

    raise RuntimeError(
        "Unable to determine the best trial."
    )

if worst_trial is None:

    raise RuntimeError(
        "Unable to determine the worst trial."
    )

if mean_value is None:

    raise RuntimeError(
        "Unable to determine the mean criterion."
    )

# ======================================================================
# Utility Functions
# ======================================================================

def nearest_trial(
    target: float,
) -> tuple[int, float]:
    """
    Return the Monte Carlo trial whose criterion is nearest to the
    requested target value.
    """

    return min(
        trials,
        key=lambda trial:
        abs(
            trial[1] - target
        ),
    )

# ======================================================================
# Select Representative Trials
# ======================================================================

representative_trials = []

representative_trials.append(
    (
        "Best",
        best_trial,
        best_value,
    )
)

for percentile in [
    2,
    10,
    20,
    50,
]:

    trial, criterion = nearest_trial(
        percentiles[
            percentile
        ]
    )

    representative_trials.append(
        (
            f"P{percentile:02d}",
            trial,
            criterion,
        )
    )

trial, criterion = nearest_trial(
    mean_value
)

representative_trials.append(
    (
        "Mean",
        trial,
        criterion,
    )
)

for percentile in [
    80,
    90,
    98,
]:

    trial, criterion = nearest_trial(
        percentiles[
            percentile
        ]
    )

    representative_trials.append(
        (
            f"P{percentile}",
            trial,
            criterion,
        )
    )

representative_trials.append(
    (
        "Worst",
        worst_trial,
        worst_value,
    )
)

print("Representative Trials")
print("------------------------------")

for case, trial, criterion in representative_trials:

    print(
        f"{case:<6}"
        f" Trial {trial:4d}"
        f"  Criterion = {criterion:.6f}"
    )

print()

# ======================================================================
# Write Representative Trial CSV
# ======================================================================

print("Writing representative trial summary...")
print(CSV_OUTPUT)
print()

with CSV_OUTPUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as csv_file:

    writer = csv.writer(
        csv_file
    )

    writer.writerow(
        [
            "Case",
            "Trial",
            "Criterion",
        ]
    )

    writer.writerows(
        representative_trials
    )

# ======================================================================
# Generate Representative Trial Export Blocks
# ======================================================================

print("Generating representative export macro...")
print()

print("Reading ZPL template...")
print(TEMPLATE_FILE)
print()

template = TEMPLATE_FILE.read_text(
    encoding="utf-8",
)

representative_blocks = []

# ======================================================================
# Generate Representative Trial Blocks
# ======================================================================

# ======================================================================
# Generate Representative Trial Blocks
# ======================================================================

for case, trial, criterion in representative_trials:

    print(
        f"Generating {case} "
        f"(Trial {trial})"
    )

    lens = f"MC_T{trial:04d}.ZMX"

    block = []

    # --------------------------------------------------------------
    # Representative Trial
    # --------------------------------------------------------------

    block.append(
        "!=============================================================="
    )

    block.append(
        f"! Representative Trial : {case}"
    )

    block.append(
        "!=============================================================="
    )

    block.append("")

    block.append(
        f'CASE$ = "{case}"'
    )

    block.append(
        f'LENSFILE$ = MCROOT$ + "{lens}"'
    )

    block.append("")

    block.append('PRINT ""')

    block.append(
        'PRINT "=============================================================="'
    )

    block.append(
        "PRINT CASE$"
    )

    block.append(
        "PRINT LENSFILE$"
    )

    block.append(
        'PRINT "=============================================================="'
    )

    block.append("")

    # --------------------------------------------------------------
    # Load Representative Lens
    # --------------------------------------------------------------

    block.append(
        "LOADLENS LENSFILE$,0,0"
    )

    block.append(
        "UPDATE"
    )

    block.append("")

    # --------------------------------------------------------------
    # Dataset Dimensions
    # --------------------------------------------------------------

    block.append(
        "NWAVES = NWAV()"
    )

    block.append(
        "NFIELDS = NFLD()"
    )

    block.append("")

    block.append(
        'PRINT "Dataset Summary"'
    )

    block.append(
        'PRINT "------------------------------"'
    )

    block.append(
        'PRINT "Wavelengths : ", NWAVES'
    )

    block.append(
        'PRINT "Fields      : ", NFIELDS'
    )

    block.append("")

    block.append(
        'PRINT ""'
    )

    block.append(
        'PRINT "Beginning export..."'
    )

    block.append(
        'PRINT "=============================================================="'
    )

    block.append("")

    # --------------------------------------------------------------
    # Representative Output Directory
    # --------------------------------------------------------------

    block.append(
        "TRIALROOT$ = OUTPUT$ + CASE$"
    )

    block.append(
        "MAKEFOLDER TRIALROOT$"
    )

    block.append("")

    # --------------------------------------------------------------
    # Loop over every wavelength
    # --------------------------------------------------------------

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append(
        "! Loop over every wavelength"
    )

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append("")

    block.append(
        "FOR WAVE,1,NWAVES,1"
    )

    block.append("")

    block.append(
        "    MODIFYSETTINGS PSFCFG$, HPS_WAVE, WAVE"
    )

    block.append(
        "    MODIFYSETTINGS MTFCFG$, MTF_WAVE, WAVE"
    )

    block.append(
        "    MODIFYSETTINGS WFMCFG$, WFM_WAVE, WAVE"
    )

    block.append("")

    block.append(
        "    WAVELENGTH = WAVL(WAVE)"
    )

    block.append(
        "    WAVELENGTHNM = WAVELENGTH * 1000"
    )

    block.append(
        "    WAVEFOLDER$ = $STR(WAVELENGTHNM)"
    )

    block.append(
        '    WAVEROOT$ = TRIALROOT$ + "\\" + WAVEFOLDER$'
    )

    block.append(
        "    MAKEFOLDER WAVEROOT$"
    )

    block.append("")

    block.append(
        '    PRINT ""'
    )

    block.append(
        '    PRINT "=============================================================="'
    )

    block.append(
        '    PRINT "Wavelength ", WAVE, " of ", NWAVES'
    )

    block.append(
        '    PRINT WAVELENGTHNM, " nm"'
    )

    block.append(
        '    PRINT "=============================================================="'
    )

    block.append("")

    # --------------------------------------------------------------
    # Spot Diagram
    #
    # One report contains all fields for the current wavelength.
    # --------------------------------------------------------------

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append(
        "! Spot Diagram"
    )

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append("")

    block.append(
        "    IF (EXPORT_MODE == 3)"
    )

    block.append(
        '        FILE$ = WAVEROOT$ + "\\spot.txt"'
    )

    block.append("")

    block.append(
        '        PRINT "Exporting Spot Diagram..."'
    )

    block.append("")

    block.append(
        "        GETTEXTFILE FILE$, Spt, SPTCFG$, 1"
    )

    block.append(
        "    ENDIF"
    )

    block.append("")

    block.append(
        "    IF (EXPORT_MODE == 5)"
    )

    block.append(
        '        FILE$ = WAVEROOT$ + "\\spot.txt"'
    )

    block.append("")

    block.append(
        '        PRINT "Exporting Spot Diagram..."'
    )

    block.append("")

    block.append(
        "        GETTEXTFILE FILE$, Spt, SPTCFG$, 1"
    )

    block.append(
        "    ENDIF"
    )

    block.append("")

    # --------------------------------------------------------------
    # Loop over every field
    # --------------------------------------------------------------

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append(
        "! Loop over every field"
    )

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append("")

    block.append(
        "    FOR FIELD,1,NFIELDS,1"
    )

    block.append("")

    block.append(
        '        FIELD$ = "field_" + $STR(FIELD)'
    )

    block.append(
        '        FIELDFOLDER$ = WAVEROOT$ + "\\" + FIELD$'
    )

    block.append(
        "        MAKEFOLDER FIELDFOLDER$"
    )

    block.append("")

    block.append(
        '        PRINT ""'
    )

    block.append(
        '        PRINT "Field ", FIELD, " / ", NFIELDS'
    )

    block.append("")

    # --------------------------------------------------------------
    # Huygens PSF
    # --------------------------------------------------------------

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append(
        "! Huygens PSF"
    )

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append("")

    block.append(
        "        IF (EXPORT_MODE == 1)"
    )

    block.append(
        "            MODIFYSETTINGS PSFCFG$, HPS_FIELD, FIELD"
    )

    block.append("")

    block.append(
        '            FILE$ = FIELDFOLDER$ + "\\psf.txt"'
    )

    block.append("")

    block.append(
        '            PRINT "Exporting Huygens PSF..."'
    )

    block.append("")

    block.append(
        "            GETTEXTFILE FILE$, Hps, PSFCFG$, 1"
    )

    block.append(
        "        ENDIF"
    )

    block.append("")

    block.append(
        "        IF (EXPORT_MODE == 5)"
    )

    block.append(
        "            MODIFYSETTINGS PSFCFG$, HPS_FIELD, FIELD"
    )

    block.append("")

    block.append(
        '            FILE$ = FIELDFOLDER$ + "\\psf.txt"'
    )

    block.append("")

    block.append(
        '            PRINT "Exporting Huygens PSF..."'
    )

    block.append("")

    block.append(
        "            GETTEXTFILE FILE$, Hps, PSFCFG$, 1"
    )

    block.append(
        "        ENDIF"
    )

    block.append("")

    # --------------------------------------------------------------
    # FFT MTF
    # --------------------------------------------------------------

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append(
        "! FFT MTF"
    )

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append("")

    block.append(
        "        IF (EXPORT_MODE == 2)"
    )

    block.append(
        "            MODIFYSETTINGS MTFCFG$, MTF_FIELD, FIELD"
    )

    block.append("")

    block.append(
        '            FILE$ = FIELDFOLDER$ + "\\mtf.txt"'
    )

    block.append("")

    block.append(
        '            PRINT "Exporting FFT MTF..."'
    )

    block.append("")

    block.append(
        "            GETTEXTFILE FILE$, Mtf, MTFCFG$, 1"
    )

    block.append(
        "        ENDIF"
    )

    block.append("")

    block.append(
        "        IF (EXPORT_MODE == 5)"
    )

    block.append(
        "            MODIFYSETTINGS MTFCFG$, MTF_FIELD, FIELD"
    )

    block.append("")

    block.append(
        '            FILE$ = FIELDFOLDER$ + "\\mtf.txt"'
    )

    block.append("")

    block.append(
        '            PRINT "Exporting FFT MTF..."'
    )

    block.append("")

    block.append(
        "            GETTEXTFILE FILE$, Mtf, MTFCFG$, 1"
    )

    block.append(
        "        ENDIF"
    )

    block.append("")

    # --------------------------------------------------------------
    # Wavefront Map
    # --------------------------------------------------------------

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append(
        "! Wavefront Map"
    )

    block.append(
        "!--------------------------------------------------------------"
    )

    block.append("")

    block.append(
        "        IF (EXPORT_MODE == 4)"
    )

    block.append(
        "            MODIFYSETTINGS WFMCFG$, WFM_FIELD, FIELD"
    )

    block.append("")

    block.append(
        '            FILE$ = FIELDFOLDER$ + "\\wavefront.txt"'
    )

    block.append("")

    block.append(
        '            PRINT "Exporting Wavefront Map..."'
    )

    block.append("")

    block.append(
        "            GETTEXTFILE FILE$, Wfm, WFMCFG$, 1"
    )

    block.append(
        "        ENDIF"
    )

    block.append("")

    block.append(
        "        IF (EXPORT_MODE == 5)"
    )

    block.append(
        "            MODIFYSETTINGS WFMCFG$, WFM_FIELD, FIELD"
    )

    block.append("")

    block.append(
        '            FILE$ = FIELDFOLDER$ + "\\wavefront.txt"'
    )

    block.append("")

    block.append(
        '            PRINT "Exporting Wavefront Map..."'
    )

    block.append("")

    block.append(
        "            GETTEXTFILE FILE$, Wfm, WFMCFG$, 1"
    )

    block.append(
        "        ENDIF"
    )

    block.append("")

    # --------------------------------------------------------------
    # End Loops
    # --------------------------------------------------------------

    block.append(
        "    NEXT"
    )

    block.append("")

    block.append(
        "NEXT"
    )

    block.append("")

    # --------------------------------------------------------------
    # Store Representative Trial Block
    # --------------------------------------------------------------

    representative_blocks.append(
        "\n".join(block)
    )


# ======================================================================
# Assemble Final Macro
# ======================================================================

print("Assembling representative export macro...")
print()

generated_blocks = "\n\n".join(
    representative_blocks
)

macro = template.replace(
    "{{REPRESENTATIVE_TRIALS}}",
    generated_blocks,
)

# ======================================================================
# Write ZPL Macro
# ======================================================================

print("Writing representative export macro...")
print(MACRO_OUTPUT)
print()

MACRO_OUTPUT.write_text(
    macro,
    encoding="utf-8",
)

print("Representative Monte Carlo export macro generated successfully.")
print()

print("Generated Files")
print("------------------------------")
print(f"Representative Trials : {CSV_OUTPUT}")
print(f"ZPL Macro             : {MACRO_OUTPUT}")
print()

print("Done.")