class AnionGapEngine:

    @staticmethod
    def calculate(na, cl, hco3):

        ag = na - (cl + hco3)

        if ag > 12:
            status = "HIGH_ANION_GAP"

            message = (
                "High anion gap metabolic acidosis pattern."
            )

        else:
            status = "NORMAL_ANION_GAP"

            message = (
                "Normal anion gap metabolic acidosis pattern."
            )

        return {
            "anion_gap": ag,
            "status": status,
            "message": message
        }