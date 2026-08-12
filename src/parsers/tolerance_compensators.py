"""
Parser for the tolerance compensator statistics section.
"""

from __future__ import annotations

from src.models.compensator_statistics import CompensatorStatistics


class CompensatorParser:
    """
    Parser for the Zemax compensator statistics section.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> list[CompensatorStatistics]:
        """
        Parse the compensator statistics.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        list[CompensatorStatistics]
            Parsed compensator statistics.
        """

        lines = sections["compensators"]

        compensators: list[CompensatorStatistics] = []

        current_name = ""

        nominal = 0.0
        minimum = 0.0
        maximum = 0.0
        mean = 0.0
        standard_deviation = 0.0

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            #
            # Ignore section heading.
            #
            if stripped == "Compensator Statistics:":
                continue

            #
            # New compensator block.
            #
            if stripped.endswith(":"):

                #
                # Save previous compensator.
                #
                if current_name:

                    compensators.append(
                        CompensatorStatistics(
                            name=current_name,
                            nominal=nominal,
                            minimum=minimum,
                            maximum=maximum,
                            mean=mean,
                            standard_deviation=standard_deviation,
                        )
                    )

                current_name = stripped[:-1]

                nominal = 0.0
                minimum = 0.0
                maximum = 0.0
                mean = 0.0
                standard_deviation = 0.0

                continue

            #
            # Statistics
            #
            key, value = stripped.split(":", 1)

            value = float(value.strip())

            key = key.strip()

            if key == "Nominal":

                nominal = value

            elif key == "Minimum":

                minimum = value

            elif key == "Maximum":

                maximum = value

            elif key == "Mean":

                mean = value

            elif key == "Standard Deviation":

                standard_deviation = value

        #
        # Store final compensator.
        #
        if current_name:

            compensators.append(
                CompensatorStatistics(
                    name=current_name,
                    nominal=nominal,
                    minimum=minimum,
                    maximum=maximum,
                    mean=mean,
                    standard_deviation=standard_deviation,
                )
            )

        return compensators