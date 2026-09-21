from core.triple_disorder import TripleDisorderEngine


class ReportComposer:

    @staticmethod
    def compose(
        interpretation=None,
        severity=None,
        compensation=None,
        anion_gap=None,
        delta_ratio=None,
        triple=None,
        primary_disorder=None
    ):

        report = []

        report.append("ABG ANALYZER PRO")
        report.append("")

        # --------------------------------------------------
        # Clinical interpretation
        # --------------------------------------------------

        if interpretation:

            report.append("CLINICAL INTERPRETATION")
            report.append("")

            for item in interpretation.get("clinical_report", []):
                report.append(str(item))

            report.append("")

        # --------------------------------------------------
        # Mixed / Triple disorder
        # --------------------------------------------------

        if triple:

            if triple.get("triple_disorder"):

                report.append("TRIPLE DISORDER")
                report.append("")

                for item in triple.get("disorders", []):
                    report.append(str(item))

                report.append("")

            elif triple.get("mixed_disorder"):

                report.append("MIXED DISORDER")
                report.append("")

                for item in triple.get("disorders", []):
                    report.append(str(item))

                report.append("")

        # --------------------------------------------------
        # Compensation
        # --------------------------------------------------

        if compensation:

            report.append("COMPENSATION")
            report.append("")

            expected = getattr(compensation, "expected", None)
            low = getattr(compensation, "low", None)
            high = getattr(compensation, "high", None)
            measured = getattr(compensation, "measured", None)
            message = getattr(compensation, "message", None)

            disorder_text = str(primary_disorder or "").lower()

            if "metabolic" in disorder_text:
                expected_label = "Expected PaCO2"
                range_label = "Acceptable PaCO2 range"
                measured_label = "Measured PaCO2"

            elif "respiratory" in disorder_text:
                expected_label = "Expected HCO3"
                range_label = "Acceptable HCO3 range"
                measured_label = "Measured HCO3"

            else:
                expected_label = "Expected compensation"
                range_label = "Acceptable compensation range"
                measured_label = "Measured value"

            report.append(f"{expected_label}: {expected}")
            report.append(f"{range_label}: {low} - {high}")
            report.append(f"{measured_label}: {measured}")

            if message:
                report.append(f"Interpretation: {message}")

            report.append("")

        # --------------------------------------------------
        # Anion Gap
        # --------------------------------------------------

        if anion_gap:

            report.append("ANION GAP")
            report.append("")

            report.append(
                f"Anion gap: {anion_gap.get('anion_gap')} mEq/L"
            )

            if anion_gap.get("message"):
                report.append(str(anion_gap["message"]))

            report.append("")

        # --------------------------------------------------
        # Delta Ratio
        # --------------------------------------------------

        if delta_ratio:

            report.append("DELTA RATIO")
            report.append("")

            ratio = delta_ratio.get("delta_ratio")

            if ratio is None:
                report.append("Delta ratio: Not calculated")
            else:
                report.append(f"Delta ratio: {ratio}")

            if delta_ratio.get("message"):
                report.append(str(delta_ratio["message"]))

            report.append("")

        # --------------------------------------------------
        # Severity
        # --------------------------------------------------

        if severity:

            report.append("SEVERITY")
            report.append("")

            report.append(
                f"Severity level: {severity.get('severity', 'UNKNOWN')}"
            )

            score = severity.get("score", 0)
            max_score = severity.get("max_score", 14)

            report.append(
                f"App severity index: {score} / {max_score}"
            )

            if severity.get("alerts"):

                report.append("")
                report.append("CLINICAL ALERTS")
                report.append("")

                for alert in severity["alerts"]:
                    report.append(str(alert))

            if severity.get("recommendations"):

                report.append("")
                report.append("CLINICAL RECOMMENDATIONS")
                report.append("")

                for recommendation in severity["recommendations"]:
                    report.append(
                        f"- {recommendation}"
                    )

        return "\n".join(report).strip()
