"""
Zemax tolerance report parser.

This module orchestrates parsing of a Zemax tolerance analysis report.

The parser performs four tasks:

1. Read the report.
2. Split the report into logical sections.
3. Delegate each section to its dedicated parser.
4. Construct a complete ToleranceStudy object.

No engineering calculations are performed here.
"""

from __future__ import annotations

from pathlib import Path

from src.models.tolerance_study import ToleranceStudy

from src.parsers.tolerance_compensators import CompensatorParser
from src.parsers.tolerance_fields import FieldParser
from src.parsers.tolerance_monte_carlo import MonteCarloParser
from src.parsers.tolerance_percentiles import PercentileParser
from src.parsers.tolerance_rss import RSSParser
from src.parsers.tolerance_sensitivity import SensitivityParser
from src.parsers.tolerance_summary import SummaryParser
from src.parsers.tolerance_worst_offenders import WorstOffenderParser


class ToleranceParser:
    """
    Orchestrator for parsing a Zemax tolerance analysis report.
    """

    SECTION_SUMMARY = "summary"
    SECTION_MNEMONICS = "mnemonics"
    SECTION_FIELDS = "fields"
    SECTION_SENSITIVITY = "sensitivity"
    SECTION_WORST_OFFENDERS = "worst_offenders"
    SECTION_RSS = "rss"
    SECTION_MONTE_CARLO = "monte_carlo"
    SECTION_COMPENSATORS = "compensators"
    SECTION_PERCENTILES = "percentiles"

    HEADER_MAP = {
        SECTION_MNEMONICS: "Mnemonics:",
        SECTION_FIELDS: "Fields:",
        SECTION_SENSITIVITY: "Sensitivity Analysis:",
        SECTION_WORST_OFFENDERS: "Worst offenders:",
        SECTION_RSS: (
            "Estimated Performance Changes based upon "
            "Root-Sum-Square method:"
        ),
        SECTION_MONTE_CARLO: "Monte Carlo Analysis:",
        SECTION_COMPENSATORS: "Compensator Statistics:",
        SECTION_PERCENTILES: "98% >",
    }

    def parse(
        self,
        path: str | Path,
    ) -> ToleranceStudy:
        """
        Parse a Zemax tolerance analysis report.

        Parameters
        ----------
        path
            Path to the Zemax tolerance report.

        Returns
        -------
        ToleranceStudy
            Parsed tolerance study.
        """

        lines = self._read_lines(path)

        headers = self._find_headers(lines)

        sections = self._slice_sections(
            lines,
            headers,
        )

        return ToleranceStudy(
            summary=SummaryParser.parse(sections),
            fields=FieldParser.parse(sections),
            sensitivities=SensitivityParser.parse(sections),
            worst_offenders=WorstOffenderParser.parse(sections),
            rss=RSSParser.parse(sections),
            monte_carlo=MonteCarloParser.parse(sections),
            compensators=CompensatorParser.parse(sections),
            percentiles=PercentileParser.parse(sections),
        )

    @staticmethod
    def _read_lines(
        path: str | Path,
    ) -> list[str]:
        """
        Read the tolerance report into memory.

        Parameters
        ----------
        path
            Path to the report.

        Returns
        -------
        list[str]
            Report lines with trailing newlines removed.
        """

        with open(path, "r", encoding="utf-16") as file:
            return [
                line.rstrip()
                for line in file
            ]

    @classmethod
    def _find_headers(
        cls,
        lines: list[str],
    ) -> dict[str, int]:
        """
        Locate the beginning of each report section.

        Parameters
        ----------
        lines
            Report lines.

        Returns
        -------
        dict[str, int]
            Mapping between section names and starting line indices.
        """

        headers = {
            cls.SECTION_SUMMARY: 0,
        }

        for index, line in enumerate(lines):

            stripped = line.strip()

            for section, header in cls.HEADER_MAP.items():

                if stripped.startswith(header):

                    headers[section] = index
                    break

        return headers

    @classmethod
    def _slice_sections(
            cls,
            lines: list[str],
            headers: dict[str, int],
    ) -> dict[str, list[str]]:
        """
        Slice the report into logical sections.

        Parameters
        ----------
        lines
            Complete report.

        headers
            Section header locations.

        Returns
        -------
        dict[str, list[str]]
            Mapping between section name and report lines.

        Notes
        -----
        The returned sections do not include their own section header.
        Each parser therefore receives only the contents of its section.
        """

        ordered_sections = sorted(
            headers.items(),
            key=lambda item: item[1],
        )

        sections: dict[str, list[str]] = {}

        for index, (section, start) in enumerate(
                ordered_sections
        ):

            #
            # Determine where this section ends.
            #
            if index + 1 < len(ordered_sections):

                end = ordered_sections[index + 1][1]

            else:

                end = len(lines)

            #
            # Every section header is skipped except the percentile
            # section, whose first line ("98% > ...") is actual data.
            #
            if section == cls.SECTION_PERCENTILES:

                sections[section] = lines[
                    start:end
                ]

            else:

                sections[section] = lines[
                    start + 1:end
                ]

        return sections