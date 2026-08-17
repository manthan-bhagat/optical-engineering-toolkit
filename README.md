# Optical Engineering Toolkit

Python toolkit for turning **Zemax text exports into reproducible optical-engineering analyses, figures, tables, and reports**.

## Pipeline

```text
Zemax exports → Parsers → Models → Analysis → Collectors/Pipelines → Plotting / Export / Report
```

* **Parsers** — extract raw Zemax results; no derived analysis.
* **Models** — typed representations of optical/tolerance data.
* **Analysis** — derive PSF, MTF, wavefront, and engineering metrics.
* **Collectors/Pipelines** — assemble cases and orchestrate end-to-end processing.
* **Plotting** — engineering and report figures.
* **Export** — CSV and Excel datasets.
* **Report** — statistics, tables, figures, and LaTeX output.
* **Config** — central project/reporting definitions.

## Analysis Coverage

**Optical:** Spot, PSF, MTF, Wavefront
**Tolerance:** Sensitivity, RSS, Monte Carlo, Percentiles, Compensators, Worst Offenders
**Environment:** Thermal
**Outputs:** CSV, Excel, Figures, LaTeX reports

## Repository

```text
analysis/      Derived optical analysis
collectors/    Case/data collection
export/        CSV/Excel generation
models/        Engineering data models
parsers/       Zemax text parsers
pipeline/      End-to-end orchestration
plotting/      Figure generation
report/        Tables, statistics, figures, LaTeX
utils/         Shared Zemax/text utilities
config.py      Central configuration
project_files.txt  Project file inventory
```

## Design Rules

1. **Zemax is the source of optical results.**
2. **Parsers extract; analysis calculates.**
3. **Models carry structured engineering data.**
4. **Pipelines orchestrate; they do not duplicate analysis.**
5. **Plots/reports consume analysis results; they do not independently recalculate them.**
6. **Fix the pipeline, then regenerate outputs—never manually repair generated figures.**

The goal is a **traceable, reproducible chain from Zemax export to engineering result and final report**.
