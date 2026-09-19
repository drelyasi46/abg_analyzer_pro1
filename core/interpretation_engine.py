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

        # -----------------------------------------
        # Primary disorder
        # -----------------------------------------
        primary_messages = {
            "Metabolic Acidosis":
                "Primary metabolic acidosis.",
            "Metabolic Alkalosis":
                "Primary metabolic alkalosis.",
            "Respiratory Acidosis":
                "Primary respiratory acidosis.",
            "Respiratory Alkalosis":
                "Primary respiratory alkalosis.",
        }

        if primary_disorder in primary_messages:
            report.append(primary_messages[primary_disorder])

        # -----------------------------------------
        # Compensation / mixed respiratory component
        # -----------------------------------------
        if compensation:

            if compensation.status == "APPROPRIATE":
                report.append(compensation.message)

            elif compensation.status == "SUPERIMPOSED_RESP_ACIDOSIS":
                report.append(
                    "Concurrent respiratory acidosis detected."
                )

            elif compensation.status == "SUPERIMPOSED_RESP_ALKALOSIS":
                report.append(
                    "Concurrent respiratory alkalosis detected."
                )

            elif compensation.status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":
                report.append(
                    "Concurrent metabolic acidosis detected."
                )

            elif compensation.status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":
                report.append(
                    "Concurrent metabolic alkalosis detected."
                )

        # -----------------------------------------
        # Anion Gap
        # -----------------------------------------
        if anion_gap:

            if anion_gap["status"] == "HIGH_ANION_GAP":

                if primary_disorder == "Metabolic Acidosis":
                    report.append(
                        "High anion gap metabolic acidosis (HAGMA)."
                    )

                elif primary_disorder == "Normal":
                    report.append(
                        "Elevated anion gap without metabolic acidosis."
                    )

            elif anion_gap["status"] == "NORMAL_ANION_GAP":

                if primary_disorder == "Metabolic Acidosis":
                    report.append(
                        "Normal anion gap metabolic acidosis (NAGMA)."
                    )

        # -----------------------------------------
        # Delta Ratio
        # -----------------------------------------
        if delta_ratio:

            status = delta_ratio.get("status")

            if status == "PURE_HAGMA":
                report.append(
                    "Pure high anion gap metabolic acidosis."
                )

            elif status == "HAGMA_PLUS_METABOLIC_ALKALOSIS":
                report.append(
                    "Mixed HAGMA + metabolic alkalosis."
                )

            elif status == "HAGMA_PLUS_NAGMA":
                report.append(
                    "Mixed HAGMA + normal anion gap metabolic acidosis."
                )

        # -----------------------------------------
        # Triple disorder
        # -----------------------------------------
        if triple and triple.get("triple_disorder"):

            report.append(
                "Triple acid-base disorder detected."
            )

        return {
            "clinical_report": report
        }
