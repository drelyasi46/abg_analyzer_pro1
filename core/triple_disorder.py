class TripleDisorderEngine:

    @staticmethod
    def analyze(
        primary_disorder,
        compensation_result=None,
        delta_ratio=None
    ):

        disorders = []

        # --------------------------------------------------
        # Primary disorder
        # --------------------------------------------------

        if primary_disorder in (
            "Metabolic Acidosis",
            "Metabolic Alkalosis",
            "Respiratory Acidosis",
            "Respiratory Alkalosis",
        ):
            disorders.append(primary_disorder)

        # --------------------------------------------------
        # Additional component from compensation
        # --------------------------------------------------

        if compensation_result:

            if compensation_result.status == "SUPERIMPOSED_RESP_ACIDOSIS":

                if "Respiratory Acidosis" not in disorders:
                    disorders.append("Respiratory Acidosis")

            elif compensation_result.status == "SUPERIMPOSED_RESP_ALKALOSIS":

                if "Respiratory Alkalosis" not in disorders:
                    disorders.append("Respiratory Alkalosis")

            elif compensation_result.status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":

                if "Metabolic Acidosis" not in disorders:
                    disorders.append("Metabolic Acidosis")

            elif compensation_result.status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":

                if "Metabolic Alkalosis" not in disorders:
                    disorders.append("Metabolic Alkalosis")

        # --------------------------------------------------
        # Additional metabolic component from Delta Ratio
        # --------------------------------------------------

        if delta_ratio:

            status = delta_ratio.get("status")

            # HAGMA + NAGMA
            #
            # The primary metabolic acidosis already represents
            # the HAGMA component. Add the additional NAGMA.

            if status == "HAGMA_PLUS_NAGMA":

                if "Additional Normal Anion Gap Metabolic Acidosis" not in disorders:
                    disorders.append(
                        "Additional Normal Anion Gap Metabolic Acidosis"
                    )

            # HAGMA + metabolic alkalosis
            #
            # HAGMA represents an additional metabolic acidosis
            # when the primary disorder is not already metabolic
            # acidosis.

            elif status == "HAGMA_PLUS_METABOLIC_ALKALOSIS":

                if "Metabolic Acidosis" not in disorders:
                    disorders.append("Metabolic Acidosis")

                if "Metabolic Alkalosis" not in disorders:
                    disorders.append("Metabolic Alkalosis")

        # --------------------------------------------------
        # Triple disorder
        # --------------------------------------------------

        if len(disorders) >= 3:

            return {
                "triple_disorder": True,
                "disorders": disorders,
                "message": "Triple acid-base disorder detected."
            }

        return {
            "triple_disorder": False,
            "disorders": disorders,
            "message": "No triple disorder detected."
        }
