class SeverityEngine:

    MAX_SCORE = 14

    @staticmethod
    def evaluate(
        primary_disorder=None,
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
        recommendations = []

        # ----------------------------------------------------
        # pH
        # ----------------------------------------------------
        if ph is not None:

            if ph < 7.10 or ph > 7.60:
                score += 3
                alerts.append("Life-threatening pH.")

            elif ph < 7.20 or ph > 7.55:
                score += 2
                alerts.append("Severe acid-base disturbance.")

            elif ph < 7.30 or ph > 7.50:
                score += 1

        # ----------------------------------------------------
        # HCO3
        # ----------------------------------------------------
        if hco3 is not None:

            if hco3 < 10:
                score += 2
                alerts.append("Severe metabolic acidosis.")

            elif hco3 < 15:
                score += 1

        # ----------------------------------------------------
        # PCO2
        # ----------------------------------------------------
        if pco2 is not None:

            if pco2 >= 70:
                score += 2
                alerts.append("Severe hypercapnia.")

            elif pco2 <= 20:
                score += 1
                alerts.append("Marked hypocapnia.")

        # ----------------------------------------------------
        # Compensation / Mixed disorder
        # ----------------------------------------------------
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

        # ----------------------------------------------------
        # Anion Gap
        # ----------------------------------------------------
        if anion_gap:

            if anion_gap.get("status") == "HIGH_ANION_GAP":

                if primary_disorder == "Metabolic Acidosis":
                    score += 1
                    alerts.append("High anion gap present.")

                elif delta_ratio and delta_ratio.get("status") in (
                    "HAGMA_PLUS_NAGMA",
                    "HAGMA_PLUS_METABOLIC_ALKALOSIS",
                ):
                    score += 1
                    alerts.append("High anion gap present.")

        # ----------------------------------------------------
        # Delta Ratio
        # ----------------------------------------------------
        if delta_ratio:

            if delta_ratio.get("status") in (
                "HAGMA_PLUS_NAGMA",
                "HAGMA_PLUS_METABOLIC_ALKALOSIS",
            ):
                score += 1

        # ----------------------------------------------------
        # Triple Disorder
        # ----------------------------------------------------
        if triple and triple.get("triple_disorder"):
            score += 3
            alerts.append("Triple acid-base disorder.")

        # ----------------------------------------------------
        # Severity classification
        # ----------------------------------------------------
        if score >= 8:
            severity = "CRITICAL"

        elif score >= 5:
            severity = "HIGH"

        elif score >= 2:
            severity = "MODERATE"

        else:
            severity = "LOW"

        # ----------------------------------------------------
        # Clinical recommendations
        # These are intentionally generic clinical-safety
        # recommendations, not disease-specific prescriptions.
        # ----------------------------------------------------
        if severity in ("CRITICAL", "HIGH"):

            recommendations.append(
                "Immediate clinical assessment and ABC evaluation."
            )

            recommendations.append(
                "Assess oxygenation, ventilation, circulation and mental status."
            )

            recommendations.append(
                "Confirm the gas abnormality when clinically appropriate "
                "and correlate with the patient's clinical condition."
            )

            recommendations.append(
                "Identify and treat the underlying cause of the acid-base disorder."
            )

            recommendations.append(
                "Consider urgent senior paediatric / critical-care review "
                "when severe clinical abnormalities are present."
            )

        elif severity == "MODERATE":

            recommendations.append(
                "Correlate the acid-base abnormality with the clinical condition."
            )

            recommendations.append(
                "Review possible underlying causes and contributing factors."
            )

            recommendations.append(
                "Repeat blood gas and relevant laboratory tests when clinically indicated."
            )

        else:

            recommendations.append(
                "Interpret the result in clinical context."
            )

        if "Severe hypercapnia." in alerts:
            recommendations.append(
                "Assess adequacy of ventilation and look for respiratory compromise."
            )

        if "Life-threatening pH." in alerts:
            recommendations.append(
                "Severe pH abnormality requires urgent clinical assessment and escalation."
            )

        if "Triple acid-base disorder." in alerts:
            recommendations.append(
                "Review for multiple simultaneous pathological processes and reassess the patient."
            )

        return {
            "severity": severity,
            "score": score,
            "max_score": SeverityEngine.MAX_SCORE,
            "alerts": alerts,
            "recommendations": recommendations,
        }
