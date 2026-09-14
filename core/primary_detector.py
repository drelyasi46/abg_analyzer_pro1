class PrimaryDisorderDetector:

    @staticmethod
    def detect(ph, pco2, hco3):

        # Normal
        if 7.35 <= ph <= 7.45 and 35 <= pco2 <= 45 and 22 <= hco3 <= 26:
            return "Normal"

        # Acidemia
        if ph < 7.35:

            # Metabolic Acidosis
            if hco3 < 22:
                return "Metabolic Acidosis"

            # Respiratory Acidosis
            if pco2 > 45:
                return "Respiratory Acidosis"

        # Alkalemia
        elif ph > 7.45:

            # Metabolic Alkalosis
            if hco3 > 26:
                return "Metabolic Alkalosis"

            # Respiratory Alkalosis
            if pco2 < 35:
                return "Respiratory Alkalosis"

        # Fully compensated disorders

        if hco3 < 22:
            return "Metabolic Acidosis"

        if hco3 > 26:
            return "Metabolic Alkalosis"

        if pco2 > 45:
            return "Respiratory Acidosis"

        if pco2 < 35:
            return "Respiratory Alkalosis"

        return "Normal"