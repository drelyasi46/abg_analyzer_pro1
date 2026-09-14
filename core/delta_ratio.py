class DeltaRatioEngine:

    @staticmethod
    def calculate(anion_gap, hco3):

        delta_ag = anion_gap - 12
        delta_hco3 = 24 - hco3

        if delta_hco3 <= 0:
            return {
                "delta_ratio": None,
                "status": "UNDEFINED",
                "message": "Delta ratio cannot be calculated."
            }

        ratio = delta_ag / delta_hco3

        if ratio < 0.4:
            status = "HAGMA_PLUS_NAGMA"
            message = (
                "High anion gap metabolic acidosis with severe additional "
                "normal anion gap metabolic acidosis."
            )

        elif ratio < 0.8:
            status = "HAGMA_PLUS_NAGMA"
            message = (
                "High anion gap metabolic acidosis with additional "
                "normal anion gap metabolic acidosis."
            )

        elif ratio <= 2.0:
            status = "PURE_HAGMA"
            message = (
                "Pure high anion gap metabolic acidosis."
            )

        else:
            status = "HAGMA_PLUS_METABOLIC_ALKALOSIS"
            message = (
                "High anion gap metabolic acidosis with additional "
                "metabolic alkalosis."
            )

        return {
            "delta_ratio": round(ratio, 2),
            "status": status,
            "message": message
        }