class PrimaryDisorderDetector:

    @staticmethod
    def detect(ph, pco2, hco3):

        # -----------------------------------------
        # Normal ABG
        # -----------------------------------------
        if (
            7.35 <= ph <= 7.45
            and 35 <= pco2 <= 45
            and 22 <= hco3 <= 26
        ):
            return "Normal"

        # -----------------------------------------
        # Acidemia
        # -----------------------------------------
        if ph < 7.35:

            # Low HCO3 strongly supports primary metabolic acidosis.
            # If PCO2 is also elevated, respiratory acidosis is
            # considered superimposed rather than primary.
            if hco3 < 22:
                return "Metabolic Acidosis"

            # Normal/high HCO3 with elevated PCO2
            if pco2 > 45:
                return "Respiratory Acidosis"

            # Fallback
            if hco3 < 22:
                return "Metabolic Acidosis"

            if pco2 > 45:
                return "Respiratory Acidosis"

        # -----------------------------------------
        # Alkalemia
        # -----------------------------------------
        if ph > 7.45:

            # Elevated HCO3 strongly supports primary
            # metabolic alkalosis.
            # If PCO2 is also low, respiratory alkalosis
            # is considered superimposed.
            if hco3 > 26:
                return "Metabolic Alkalosis"

            # Normal/low HCO3 with low PCO2
            if pco2 < 35:
                return "Respiratory Alkalosis"

            # Fallback
            if hco3 > 26:
                return "Metabolic Alkalosis"

            if pco2 < 35:
                return "Respiratory Alkalosis"

        # -----------------------------------------
        # Compensated / borderline disorders
        # -----------------------------------------

        # Elevated PCO2 + elevated HCO3
        # suggests respiratory acidosis with renal compensation.
        if pco2 > 45 and hco3 > 26:
            return "Respiratory Acidosis"

        # Low PCO2 + reduced HCO3
        # suggests respiratory alkalosis with renal compensation.
        if pco2 < 35 and hco3 < 22:
            return "Respiratory Alkalosis"

        if hco3 < 22:
            return "Metabolic Acidosis"

        if hco3 > 26:
            return "Metabolic Alkalosis"

        if pco2 > 45:
            return "Respiratory Acidosis"

        if pco2 < 35:
            return "Respiratory Alkalosis"

        return "Normal"
