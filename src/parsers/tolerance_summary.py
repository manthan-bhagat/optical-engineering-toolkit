"""
Parser for the tolerance report summary section.
"""

from __future__ import annotations

from src.models.tolerance_summary import ToleranceSummary


class SummaryParser:
    """
    Parser for the tolerance study summary.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> ToleranceSummary:
        """
        Parse the tolerance study summary.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        ToleranceSummary
            Parsed study summary.
        """

        lines = sections["summary"]

        lens_file = ""
        title = ""
        date = ""

        units = ""

        criterion = ""
        mode = ""
        sampling = 0
        optimization_cycles = ""

        nominal_criterion = 0.0
        test_wavelength = 0.0

        compensator = ""
        compensator_min = 0.0
        compensator_max = 0.0

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("File"):

                lens_file = stripped.split(":", 1)[1].strip()

            elif stripped.startswith("Title"):

                title = stripped.split(":", 1)[1].strip()

            elif stripped.startswith("Date"):

                date = stripped.split(":", 1)[1].strip()

            elif stripped.startswith("Units are"):

                units = (
                    stripped
                    .replace("Units are", "")
                    .replace(".", "")
                    .strip()
                )

            elif stripped.startswith("Compensator:"):

                compensator = (
                    stripped
                    .split(":", 1)[1]
                    .split(",")[0]
                    .strip()
                )

                parts = stripped.split(",")

                compensator_min = float(
                    parts[1].split("=")[1]
                )

                compensator_max = float(
                    parts[2].split("=")[1]
                )

            elif stripped.startswith("Criterion"):

                criterion = stripped.split(":", 1)[1].strip()

            elif stripped.startswith("Mode"):

                mode = stripped.split(":", 1)[1].strip()

            elif stripped.startswith("Sampling"):

                sampling = int(
                    stripped.split(":", 1)[1]
                )

            elif stripped.startswith("Optimization Cycles"):

                optimization_cycles = (
                    stripped
                    .split(":", 1)[1]
                    .strip()
                )

            elif stripped.startswith("Nominal Criterion"):

                nominal_criterion = float(
                    stripped.split(":", 1)[1]
                )

            elif stripped.startswith("Test Wavelength"):

                test_wavelength = float(
                    stripped.split(":", 1)[1]
                )

        return ToleranceSummary(
            lens_file=lens_file,
            title=title,
            date=date,
            units=units,
            criterion=criterion,
            mode=mode,
            sampling=sampling,
            optimization_cycles=optimization_cycles,
            nominal_criterion=nominal_criterion,
            test_wavelength=test_wavelength,
            compensator=compensator,
            compensator_min=compensator_min,
            compensator_max=compensator_max,
        )