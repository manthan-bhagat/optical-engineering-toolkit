"""
Parser for the tolerance Monte Carlo statistics section.
"""

from __future__ import annotations

from src.models.monte_carlo_statistics import MonteCarloStatistics


class MonteCarloParser:
    """
    Parser for the Zemax Monte Carlo summary.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> MonteCarloStatistics:
        """
        Parse the Monte Carlo statistics section.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        MonteCarloStatistics
            Parsed Monte Carlo statistics.
        """

        lines = sections["monte_carlo"]

        trials = 0
        distribution = ""

        nominal = 0.0

        best = 0.0
        best_trial = 0

        worst = 0.0
        worst_trial = 0

        mean = 0.0
        standard_deviation = 0.0

        criterion_values: list[float] = []

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            #
            # Number of trials
            #
            if stripped.startswith("Number of trials"):

                trials = int(
                    stripped.split(":", 1)[1].strip()
                )

                continue

            #
            # Distribution
            #
            if stripped.startswith("Initial Statistics"):

                distribution = (
                    stripped
                    .split(":", 1)[1]
                    .strip()
                )

                continue

            #
            # Trial table
            #
            tokens = stripped.split()

            if (
                len(tokens) >= 3
                and tokens[0].isdigit()
            ):

                criterion_values.append(
                    float(tokens[1])
                )

                continue

            #
            # Nominal
            #
            if stripped.startswith("Nominal"):

                nominal = float(
                    stripped.split()[1]
                )

                continue

            #
            # Best
            #
            if stripped.startswith("Best"):

                tokens = stripped.split()

                best = float(tokens[1])

                best_trial = int(tokens[3])

                continue

            #
            # Worst
            #
            if stripped.startswith("Worst"):

                tokens = stripped.split()

                worst = float(tokens[1])

                worst_trial = int(tokens[3])

                continue

            #
            # Mean
            #
            if stripped.startswith("Mean"):

                mean = float(
                    stripped.split()[1]
                )

                continue

            #
            # Standard deviation
            #
            if stripped.startswith("Std Dev"):

                standard_deviation = float(
                    stripped.split()[2]
                )

        return MonteCarloStatistics(
            trials=trials,
            distribution=distribution,
            nominal=nominal,
            best=best,
            best_trial=best_trial,
            worst=worst,
            worst_trial=worst_trial,
            mean=mean,
            standard_deviation=standard_deviation,
            criterion_values=criterion_values,
        )