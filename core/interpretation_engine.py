class InterpretationEngine:

    @staticmethod
    def generate(
        primary_disorder=None,
        compensation=None,
        anion_gap=None,
        delta_ratio=None,
        triple=None
    ):

        report = []

        primary_messages = {
            "Normal":
                "No primary acid-base disorder detected.",
            "Metabolic Acidosis":
                "Primary metabolic acidosis.",
            "Metabolic Alkalosis":
                "Primary metabolic alkalosis.",
            "Respiratory Acidosis":
                "Primary respiratory acidosis.",
            "Respiratory Alkalosis":
                "Primary respiratory alkalosis.",
        }

        primary_message = primary_messages.get(primary_disorder)

        if primary_message:
            report.append(primary_message)

        # --------------------------------------------------
        # Mixed / Triple disorder
        # --------------------------------------------------

        if triple:

            if triple.get("triple_disorder"):
                report.append(
                    "A triple acid-base disorder is detected."
                )

            elif triple.get("mixed_disorder"):
                report.append(
                    "A mixed acid-base disorder is detected."
                )

        # --------------------------------------------------
        # Compensation
        # --------------------------------------------------

        if compensation:

            status = compensation.status

            if status == "APPROPRIATE":
                report.append(
                    "Compensation is appropriate for the primary disorder."
                )

            elif status == "SUPERIMPOSED_RESP_ACIDOSIS":
                report.append(
                    "Additional respiratory acidosis is present."
                )

            elif status == "SUPERIMPOSED_RESP_ALKALOSIS":
                report.append(
                    "Additional respiratory alkalosis is present."
                )

            elif status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":
                report.append(
                    "Additional metabolic acidosis is present."
                )

            elif status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":
                report.append(
                    "Additional metabolic alkalosis is present."
                )

        # --------------------------------------------------
        # Anion Gap
        # --------------------------------------------------

        if anion_gap:

            status = anion_gap.get("status")

            if (
                status == "HIGH_ANION_GAP"
                and primary_disorder == "Metabolic Acidosis"
            ):
                report.append(
                    "High anion gap metabolic acidosis (HAGMA)."
                )

            elif (
                status == "NORMAL_ANION_GAP"
                and primary_disorder == "Metabolic Acidosis"
            ):
                report.append(
                    "Normal anion gap metabolic acidosis (NAGMA)."
                )

            elif (
                status == "HIGH_ANION_GAP"
                and primary_disorder == "Normal"
            ):
                report.append(
                    "Elevated anion gap without a primary metabolic acidosis."
                )

        # --------------------------------------------------
        # Delta Ratio
        # --------------------------------------------------

        if delta_ratio:

            status = delta_ratio.get("status")

            if status == "PURE_HAGMA":
                report.append(
                    "Delta ratio is consistent with predominantly HAGMA."
                )

            elif status == "HAGMA_PLUS_METABOLIC_ALKALOSIS":
                report.append(
                    "Additional metabolic alkalosis is suggested."
                )

            elif status == "HAGMA_PLUS_NAGMA":
                report.append(
                    "Additional normal anion gap metabolic acidosis is suggested."
                )

        return {
            "clinical_report": report
        }
