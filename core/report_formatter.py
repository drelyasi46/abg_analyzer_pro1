"""
Professional ABG Report Formatter
"""


class ReportFormatter:

    @staticmethod
    def format(report):

        formatted = []

        formatted.append("ABG INTERPRETATION REPORT")
        formatted.append("=" * 40)

        skip_lines = [
            "=" * 40,
            "-" * 25,
            "ABG INTERPRETATION REPORT",
        ]

        section_titles = [
            "COMPENSATION",
            "ANION GAP",
            "ANION GAP ANALYSIS",
            "DELTA RATIO",
            "CLINICAL IMPRESSION",
            "CLINICAL INTERPRETATION",
            "CLINICAL RECOMMENDATIONS",
            "RECOMMENDATIONS",
            "SEVERITY",
            "CLINICAL ALERTS",
            "LACTATE",
            "TRIPLE DISORDER",
            "TRIPLE DISORDER ANALYSIS",
        ]

        for line in report:

            if line in skip_lines:
                continue

            if line.strip() == "":
                formatted.append("")
                continue

            if line.upper() in section_titles:

                formatted.append("")
                formatted.append(line.upper())
                formatted.append("-" * 40)
                continue

            formatted.append(line)

        return "\n".join(formatted)
