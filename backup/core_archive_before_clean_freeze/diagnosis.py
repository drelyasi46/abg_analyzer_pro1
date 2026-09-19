class DiagnosisEngine:

    @staticmethod
    def determine(ph, pco2, hco3):

        # -------------------------
        # Acid-base status
        # -------------------------
        if ph < 7.35:
            status = "Acidemia"

        elif ph > 7.45:
            status = "Alkalemia"

        else:
            status = "Near Normal pH"

        # -------------------------
        # Primary Disorder
        # -------------------------
        if ph < 7.35:

            if hco3 < 22:
                disorder = "Metabolic Acidosis"

            elif pco2 > 45:
                disorder = "Respiratory Acidosis"

            else:
                disorder = "Mixed Acidosis"

        elif ph > 7.45:

            if hco3 > 26:
                disorder = "Metabolic Alkalosis"

            elif pco2 < 35:
                disorder = "Respiratory Alkalosis"

            else:
                disorder = "Mixed Alkalosis"

        else:

            # Completely normal
            if (
                35 <= pco2 <= 45
                and 22 <= hco3 <= 26
            ):
                disorder = "Normal Acid-Base Status"

            # Compensated respiratory acidosis
            elif pco2 > 45 and hco3 > 26:
                disorder = "Respiratory Acidosis"

            # Compensated respiratory alkalosis
            elif pco2 < 35 and hco3 < 22:
                disorder = "Respiratory Alkalosis"

            else:
                disorder = "Possible Mixed Disorder"

        return status, disorder