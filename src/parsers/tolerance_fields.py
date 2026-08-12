"""
Parser for the tolerance field definition table.
"""

from __future__ import annotations

from src.models.tolerance_field import ToleranceField


class FieldParser:
    """
    Parser for the tolerance field definition table.
    """

    @classmethod
    def parse(
        cls,
        sections: dict[str, list[str]],
    ) -> list[ToleranceField]:
        """
        Parse the tolerance field table.

        Parameters
        ----------
        sections
            Report sections.

        Returns
        -------
        list[ToleranceField]
            Parsed field definitions.
        """

        lines = sections["fields"]

        fields: list[ToleranceField] = []

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            tokens = stripped.split()

            #
            # Valid field rows always begin with
            # the field index.
            #
            if not tokens[0].isdigit():
                continue

            if len(tokens) < 8:
                raise ValueError(
                    f"Invalid tolerance field row:\n{line}"
                )

            fields.append(
                ToleranceField(
                    index=int(tokens[0]),
                    x_field=float(tokens[1]),
                    y_field=float(tokens[2]),
                    weight=float(tokens[3]),
                    vdx=float(tokens[4]),
                    vdy=float(tokens[5]),
                    vcx=float(tokens[6]),
                    vcy=float(tokens[7]),
                )
            )

        return fields