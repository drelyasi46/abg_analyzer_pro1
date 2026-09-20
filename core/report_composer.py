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

        report.append("ABG ANALYZER PRO")
        report.append("")

        if interpretation:
            report.append("CLINICAL INTERPRETATION")
            report.append("")

            for item in interpretation.get("clinical_report", []):
                report.append(str(item))

            report.append("")

        if compensation:
            report.append("COMPENSATION")
            report.append("")
            report.append(f"Expected: {compensation.expected}")
            report.append(
                f"Acceptable range: {compensation.low} - {compensation.high}"
            )
            report.append(f"Measured: {compensation.measured}")
            report.append(f"Interpretation: {compensation.message}")
            report.append("")

        if anion_gap:
            report.append("ANION GAP")
            report.append("")
            report.append(
                f"Anion gap: {anion_gap['anion_gap']} mEq/L"
            )
            report.append(str(anion_gap["message"]))
            report.append("")

        if delta_ratio:
            report.append("DELTA RATIO")
            report.append("")
            report.append(
                f"Delta ratio: {delta_ratio['delta_ratio']}"
            )
            report.append(str(delta_ratio["message"]))
            report.append("")

        if triple and triple.get("triple_disorder"):
            report.append("TRIPLE DISORDER")
            report.append("")

            for item in triple["disorders"]:
                report.append(str(item))

            report.append("")

        if severity:
            report.append("SEVERITY")
            report.append("")
            report.append(f"Severity: {severity['severity']}")
            report.append(f"Score: {severity['score']}")

            if severity.get("alerts"):
                report.append("")
                report.append("CLINICAL ALERTS")
                report.append("")

                for alert in severity["alerts"]:
                    report.append(str(alert))

        return "\n".join(report).strip()
