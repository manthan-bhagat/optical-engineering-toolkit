"""
Parser for the tolerance worst offenders section.
"""

from __future__ import annotations

from src.models.worst_offender import WorstOffender


class WorstOffenderParser:
    """
    Parser for the Zemax worst offenders table.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> list[WorstOffender]:
        """
        Parse the worst offenders table.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        list[WorstOffender]
            Parsed worst offender entries.
        """

        lines = sections["worst_offenders"]

        offenders: list[WorstOffender] = []

        rank = 1

        for line in lines:

            stripped = line.strip()

            #
            # Ignore blank lines.
            #
            if not stripped:
                continue

            #
            # Ignore table header.
            #
            if stripped.startswith("Type"):
                continue

            tokens = stripped.split()

            if not tokens:
                continue

            mnemonic = tokens[0]

            #
            # Thickness tolerances include
            # an additional compensator column.
            #
            if mnemonic == "TTHI":

                if len(tokens) != 6:
                    raise ValueError(
                        f"Malformed worst offender row:\n{line}"
                    )

                surface = int(tokens[1])

                value = float(tokens[3])

                criterion = float(tokens[4])

                change = float(tokens[5])

            else:

                if len(tokens) != 5:
                    raise ValueError(
                        f"Malformed worst offender row:\n{line}"
                    )

                surface = int(tokens[1])

                value = float(tokens[2])

                criterion = float(tokens[3])

                change = float(tokens[4])

            offenders.append(
                WorstOffender(
                    rank=rank,
                    mnemonic=mnemonic,
                    surface=surface,
                    value=value,
                    criterion=criterion,
                    change=change,
                )
            )

            rank += 1

        return offenders