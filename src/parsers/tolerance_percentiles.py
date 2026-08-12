"""
Parser for the tolerance Monte Carlo percentile section.
"""

from __future__ import annotations

from src.models.percentile import Percentile


class PercentileParser:
    """
    Parser for the Zemax Monte Carlo percentile table.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> list[Percentile]:
        """
        Parse the Monte Carlo percentile statistics.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        list[Percentile]
            Parsed percentile statistics.
        """

        lines = sections["percentiles"]

        percentiles: list[Percentile] = []

        for line in lines:

            stripped = line.strip()

            #
            # Ignore blank lines.
            #
            if not stripped:
                continue

            #
            # Percentile rows have the form
            #
            #   2%  >  0.003912
            #   10% >  0.004105
            #   50% >  0.004382
            #
            if ">" not in stripped:
                continue

            tokens = stripped.split()

            if len(tokens) != 3:
                raise ValueError(
                    f"Malformed percentile row:\n{line}"
                )

            percentage = int(
                tokens[0].rstrip("%")
            )

            criterion = float(
                tokens[2]
            )

            percentiles.append(
                Percentile(
                    percentage=percentage,
                    criterion=criterion,
                )
            )

        return percentiles