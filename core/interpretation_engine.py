class InterpretationEngine:

    @staticmethod
    def generate(
        compensation=None,
        anion_gap=None,
        delta_ratio=None,
        triple=None
    ):

        report = []

        # Compensation
        if compensation:

            if compensation.status == "APPROPRIATE":
                report.append(compensation.message)

            elif compensation.status == "SUPERIMPOSED_RESP_ACIDOSIS":
                report.append("Concurrent respiratory acidosis detected.")

            elif compensation.status == "SUPERIMPOSED_RESP_ALKALOSIS":
                report.append("Concurrent respiratory alkalosis detected.")

            elif compensation.status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":
                report.append("Concurrent metabolic acidosis detected.")

            elif compensation.status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":
                report.append("Concurrent metabolic alkalosis detected.")

        # Anion Gap
        if anion_gap:

            if anion_gap["status"] == "HIGH_ANION_GAP":
                report.append("High anion gap metabolic acidosis (HAGMA).")

            elif anion_gap["status"] == "NORMAL_ANION_GAP":
                report.append("Normal anion gap metabolic acidosis (NAGMA).")

        # Delta Ratio
        if delta_ratio:

            if delta_ratio["status"] == "PURE_HAGMA":
                report.append("Pure high anion gap metabolic acidosis.")

            elif delta_ratio["status"] == "HAGMA_PLUS_METABOLIC_ALKALOSIS":
                report.append("Mixed HAGMA + metabolic alkalosis.")

            elif delta_ratio["status"] == "HAGMA_PLUS_NAGMA":
                report.append("Mixed HAGMA + normal anion gap metabolic acidosis.")

        # Triple Disorder
        if triple and triple.get("triple_disorder"):

            report.append("Triple acid-base disorder detected.")

            for disorder in triple["disorders"]:
                report.append(disorder)

        return {
            "clinical_report": report
        }