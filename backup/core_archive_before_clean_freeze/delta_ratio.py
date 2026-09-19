class DeltaRatioEngine:

    @staticmethod
    def calculate(anion_gap, hco3):

        delta_ag = anion_gap - 12
        delta_hco3 = 24 - hco3

        # --------------------------------------------------
        # HAGMA + metabolic alkalosis
        # --------------------------------------------------
        #
        # When HCO3 is > 24, the classical delta ratio
        # denominator becomes negative and is not clinically
        # useful. The appropriate interpretation is that
        # elevated HCO3 coexists with HAGMA.
        #
        if hco3 > 24:

            return {
                "delta_ratio": None,
                "delta_ag": round(delta_ag, 2),
                "delta_hco3": round(delta_hco3, 2),
                "status": "HAGMA_PLUS_METABOLIC_ALKALOSIS",
                "message": (
                    "High anion gap metabolic acidosis "
                    "with additional metabolic alkalosis."
                )
            }

        # --------------------------------------------------
        # HCO3 = 24
        # --------------------------------------------------
        #
        # At normal HCO3 there is no change in bicarbonate
        # to use as the delta-ratio denominator.
        # This does NOT establish metabolic alkalosis.
        #

        if hco3 == 24:

            return {
                "delta_ratio": None,
                "delta_ag": round(delta_ag, 2),
                "delta_hco3": 0,
                "status": "UNDEFINED",
                "message": "Delta ratio cannot be calculated."
            }

        # --------------------------------------------------
        # HCO3 < 24
        # Classical delta ratio
        # --------------------------------------------------

        if delta_hco3 <= 0:

            return {
                "delta_ratio": None,
                "delta_ag": round(delta_ag, 2),
                "delta_hco3": round(delta_hco3, 2),
                "status": "UNDEFINED",
                "message": "Delta ratio cannot be calculated."
            }

        ratio = delta_ag / delta_hco3

        # --------------------------------------------------
        # Delta ratio interpretation
        # --------------------------------------------------

        if ratio < 0.4:

            status = "HAGMA_PLUS_NAGMA"

            message = (
                "High anion gap metabolic acidosis with severe "
                "additional normal anion gap metabolic acidosis."
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
            "delta_ag": round(delta_ag, 2),
            "delta_hco3": round(delta_hco3, 2),
            "status": status,
            "message": message
        }
