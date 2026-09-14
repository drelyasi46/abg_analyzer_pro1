class ReportComposer:

    @staticmethod
    def compose(
        interpretation=None,
        severity=None,
        compensation=None,
        anion_gap=None,
        delta_ratio=None,
        triple=None
    ):

        report = []

        report.append("=" * 50)
        report.append("ABG ANALYZER PRO")
        report.append("=" * 50)

        # Clinical Interpretation
        if interpretation:

            report.append("")
            report.append("CLINICAL INTERPRETATION")
            report.append("-" * 50)

            for item in interpretation.get("clinical_report", []):
                report.append(f"• {item}")

        # Compensation
        if compensation:

            report.append("")
            report.append("COMPENSATION")
            report.append("-" * 50)

            report.append(f"Expected : {compensation.expected}")
            report.append(f"Acceptable Range : {compensation.low} - {compensation.high}")
            report.append(f"Measured : {compensation.measured}")
            report.append(f"Interpretation : {compensation.message}")

        # Anion Gap
        if anion_gap:

            report.append("")
            report.append("ANION GAP")
            report.append("-" * 50)

            report.append(f"Anion Gap : {anion_gap['anion_gap']} mEq/L")
            report.append(anion_gap["message"])

        # Delta Ratio
        if delta_ratio:

            report.append("")
            report.append("DELTA RATIO")
            report.append("-" * 50)

            report.append(f"Delta Ratio : {delta_ratio['delta_ratio']}")
            report.append(delta_ratio["message"])

        # Triple Disorder
        if triple and triple.get("triple_disorder"):

            report.append("")
            report.append("TRIPLE DISORDER")
            report.append("-" * 50)

            for item in triple["disorders"]:
                report.append(f"• {item}")

        # Severity
        if severity:

            report.append("")
            report.append("SEVERITY")
            report.append("-" * 50)

            report.append(f"Severity : {severity['severity']}")
            report.append(f"Score : {severity['score']}")

            if severity.get("alerts"):

                report.append("")
                report.append("CLINICAL ALERTS")

                for alert in severity["alerts"]:
                    report.append(f"• {alert}")

        report.append("")
        report.append("=" * 50)

        return "\n".join(report)