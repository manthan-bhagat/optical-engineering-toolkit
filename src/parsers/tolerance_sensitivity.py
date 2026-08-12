"""
Parser for the tolerance sensitivity analysis section.
"""

from __future__ import annotations

from src.models.sensitivity_result import SensitivityResult


class SensitivityParser:
    """
    Parser for the Zemax sensitivity analysis section.
    """

    OPERANDS = {
        "TRAD",
        "TTHI",
        "TCON",
        "TSDI",
        "TSDX",
        "TSDY",
        "TSTX",
        "TSTY",
        "TIRR",
    }

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> list[SensitivityResult]:
        """
        Parse the sensitivity analysis section.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        list[SensitivityResult]
            Parsed sensitivity results.
        """

        lines = sections["sensitivity"]

        results: list[SensitivityResult] = []

        current_component = ""
        current_description = ""

        for line in lines:

            stripped = line.strip()

            #
            # Ignore blank lines.
            #
            if not stripped:
                continue

            #
            # Ignore table headers.
            #
            if stripped.startswith("|"):
                continue

            if stripped.startswith("Type"):
                continue

            #
            # Component headings.
            #
            if (
                stripped.endswith("Mirror")
                or stripped == "Detector"
            ):

                current_component = stripped
                continue

            #
            # Description lines.
            #
            tokens = stripped.split()

            if not tokens:
                continue

            if tokens[0] not in cls.OPERANDS:

                if ":" in stripped:

                    current_description = stripped

                continue

            mnemonic = tokens[0]

            #
            # Thickness tolerances contain an
            # additional compensator column.
            #
            if mnemonic == "TTHI":

                if len(tokens) < 9:
                    raise ValueError(
                        f"Malformed sensitivity row:\n{line}"
                    )

                surface = int(tokens[1])

                minimum_value = float(tokens[3])
                minimum_criterion = float(tokens[4])
                minimum_change = float(tokens[5])

                maximum_value = float(tokens[6])
                maximum_criterion = float(tokens[7])
                maximum_change = float(tokens[8])

            else:

                if len(tokens) < 8:
                    raise ValueError(
                        f"Malformed sensitivity row:\n{line}"
                    )

                surface = int(tokens[1])

                minimum_value = float(tokens[2])
                minimum_criterion = float(tokens[3])
                minimum_change = float(tokens[4])

                maximum_value = float(tokens[5])
                maximum_criterion = float(tokens[6])
                maximum_change = float(tokens[7])

            results.append(
                SensitivityResult(
                    component=current_component,
                    description=current_description,
                    mnemonic=mnemonic,
                    surface=surface,
                    minimum_value=minimum_value,
                    minimum_criterion=minimum_criterion,
                    minimum_change=minimum_change,
                    maximum_value=maximum_value,
                    maximum_criterion=maximum_criterion,
                    maximum_change=maximum_change,
                )
            )

        return results