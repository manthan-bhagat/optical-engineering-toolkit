"""
Parser for the tolerance Root-Sum-Square estimate section.
"""

from __future__ import annotations

from src.models.rss_estimate import RSSEstimate


class RSSParser:
    """
    Parser for the Zemax Root-Sum-Square performance estimate.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> RSSEstimate:
        """
        Parse the Root-Sum-Square performance estimate.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        RSSEstimate
            Parsed RSS performance estimate.
        """

        lines = sections["rss"]

        nominal = 0.0
        estimated_change = 0.0
        estimated_value = 0.0

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("Nominal"):

                nominal = float(
                    stripped.split(":", 1)[1].strip()
                )

            elif stripped.startswith("Estimated change"):

                estimated_change = float(
                    stripped.split(":", 1)[1].strip()
                )

            elif stripped.startswith("Estimated RMS"):

                estimated_value = float(
                    stripped.split(":", 1)[1].strip()
                )

        return RSSEstimate(
            nominal=nominal,
            estimated_change=estimated_change,
            estimated_value=estimated_value,
        )