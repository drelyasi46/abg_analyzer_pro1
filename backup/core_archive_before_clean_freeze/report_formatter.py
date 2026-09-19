"""
report_formatter.py

Professional ABG Report Formatter
"""


class ReportFormatter:


    @staticmethod
    def format(report):

        formatted = []


        formatted.append(
            "ABG INTERPRETATION REPORT"
        )

        formatted.append(
            "────────────────────────"
        )


        skip_lines = [
            "=" * 40,
            "-" * 25,
            "ABG INTERPRETATION REPORT",
        ]


        section_titles = [
            "Compensation",
            "ANION GAP ANALYSIS",
            "Delta Ratio",
            "CLINICAL IMPRESSION",
            "RECOMMENDATIONS",
            "LACTATE",
            "TRIPLE DISORDER ANALYSIS",
        ]


        for line in report:


            if line in skip_lines:

                continue



            if line.strip() == "":

                formatted.append("")

                continue



            if line in section_titles:


                formatted.append("")

                formatted.append(
                    line.upper()
                )

                formatted.append(
                    "────────────────────────"
                )

                continue



            if line.startswith("Expected PaCO₂"):

                line = line.replace(
                    "Expected PaCO₂",
                    "Expected PaCO₂"
                )



            if line.startswith("Anion Gap :"):

                line = line.replace(
                    "Anion Gap :",
                    "Anion Gap:"
                )



            if (
                line.startswith("Check ")
                or line.startswith("Review ")
                or line.startswith("Correlate ")
                or line.startswith("Repeat ")
            ):

                line = "• " + line



            formatted.append(
                line
            )


        return "\n".join(formatted)