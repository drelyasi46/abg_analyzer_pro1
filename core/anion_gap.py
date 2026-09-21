class AnionGapEngine:
    @staticmethod
    def calculate(na, cl, hco3, albumin=None):
        ag = na - (cl + hco3)

        if albumin is not None:
            corrected_ag = ag + (2.5 * (4.0 - albumin))
        else:
            corrected_ag = ag

        if corrected_ag >= 18:
            status = "HIGH_ANION_GAP"
            message = "High anion gap; high-anion-gap metabolic acidosis should be considered."
        elif corrected_ag > 12:
            status = "ELEVATED_ANION_GAP"
            message = "Mildly elevated anion gap; interpret with acid-base context."
        else:
            status = "NORMAL_ANION_GAP"
            message = "Normal anion gap."

        return {
            "anion_gap": round(ag, 2),
            "corrected_anion_gap": round(corrected_ag, 2),
            "status": status,
            "message": message,
        }
