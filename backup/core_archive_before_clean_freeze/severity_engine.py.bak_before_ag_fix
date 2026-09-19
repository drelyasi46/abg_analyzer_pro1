class SeverityEngine:

    @staticmethod
    def evaluate(
        compensation=None,
        anion_gap=None,
        delta_ratio=None,
        triple=None,
        hco3=None,
        pco2=None,
        ph=None
    ):

        score = 0
        alerts = []

        # pH
        if ph is not None:

            if ph < 7.10 or ph > 7.60:
                score += 3
                alerts.append("Life-threatening pH.")

            elif ph < 7.20 or ph > 7.55:
                score += 2
                alerts.append("Severe acid-base disturbance.")

            elif ph < 7.30 or ph > 7.50:
                score += 1

        # HCO3
        if hco3 is not None:

            if hco3 < 10:
                score += 2
                alerts.append("Severe metabolic acidosis.")

            elif hco3 < 15:
                score += 1

        # PCO2
        if pco2 is not None:

            if pco2 >= 70:
                score += 2
                alerts.append("Severe hypercapnia.")

            elif pco2 <= 20:
                score += 1
                alerts.append("Marked hypocapnia.")

        # Compensation
        if compensation:

            if compensation.status == "SUPERIMPOSED_RESP_ACIDOSIS":
                score += 2
                alerts.append("Concurrent respiratory acidosis.")

            elif compensation.status == "SUPERIMPOSED_RESP_ALKALOSIS":
                score += 2
                alerts.append("Concurrent respiratory alkalosis.")

            elif compensation.status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":
                score += 2
                alerts.append("Concurrent metabolic acidosis.")

            elif compensation.status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":
                score += 2
                alerts.append("Concurrent metabolic alkalosis.")

        # Anion Gap
        if anion_gap:

            if anion_gap["status"] == "HIGH_ANION_GAP":
                score += 1
                alerts.append("High anion gap present.")

        # Delta Ratio
        if delta_ratio:

            if delta_ratio["status"] != "PURE_HAGMA":
                score += 1

        # Triple Disorder
        if triple and triple.get("triple_disorder"):
            score += 3
            alerts.append("Triple acid-base disorder.")

        # Final Severity
        if score >= 8:
            severity = "CRITICAL"

        elif score >= 5:
            severity = "HIGH"

        elif score >= 2:
            severity = "MODERATE"

        else:
            severity = "LOW"

        return {
            "severity": severity,
            "score": score,
            "alerts": alerts
        }