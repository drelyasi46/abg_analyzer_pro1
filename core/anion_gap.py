class AnionGapEngine:

    @staticmethod
    def calculate(na, cl, hco3):

        ag = na - (cl + hco3)

        if ag > 12:
            status = "HIGH_ANION_GAP"
            message = "Elevated anion gap."

        else:
            status = "NORMAL_ANION_GAP"
            message = "Normal anion gap."

        return {
            "anion_gap": ag,
            "status": status,
            "message": message
        }
