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

            status = compensation_result.status

            if status == "SUPERIMPOSED_RESP_ACIDOSIS":

                if "Respiratory Acidosis" not in disorders:
                    disorders.append("Respiratory Acidosis")

            elif status == "SUPERIMPOSED_RESP_ALKALOSIS":

                if "Respiratory Alkalosis" not in disorders:
                    disorders.append("Respiratory Alkalosis")

            elif status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":

                if "Metabolic Acidosis" not in disorders:
                    disorders.append("Metabolic Acidosis")

            elif status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":

                if "Metabolic Alkalosis" not in disorders:
                    disorders.append("Metabolic Alkalosis")

        # --------------------------------------------------
        # Additional metabolic components from Delta Ratio
        # --------------------------------------------------

        if delta_ratio:

            status = delta_ratio.get("status")

            # Pure HAGMA itself represents a metabolic acidosis
            if status == "PURE_HAGMA":

                if "Metabolic Acidosis" not in disorders:
                    disorders.append("Metabolic Acidosis")

            # HAGMA + additional normal anion gap metabolic acidosis
            elif status == "HAGMA_PLUS_NAGMA":

                if "Metabolic Acidosis" not in disorders:
                    disorders.append("Metabolic Acidosis")

                if (
                    "Additional Normal Anion Gap Metabolic Acidosis"
                    not in disorders
                ):
                    disorders.append(
                        "Additional Normal Anion Gap Metabolic Acidosis"
                    )

            # HAGMA + metabolic alkalosis
            elif status == "HAGMA_PLUS_METABOLIC_ALKALOSIS":

                if "Metabolic Acidosis" not in disorders:
                    disorders.append("Metabolic Acidosis")

                if "Metabolic Alkalosis" not in disorders:
                    disorders.append("Metabolic Alkalosis")

        # --------------------------------------------------
        # Determine mixed / triple status
        # --------------------------------------------------

        # Count physiologically distinct acid-base components.
        #
        # "Additional Normal Anion Gap Metabolic Acidosis"
        # is already an additional metabolic-acidosis component
        # and therefore counts as a separate process.
        component_count = len(disorders)

        mixed_disorder = component_count >= 2
        triple_disorder = component_count >= 3

        # --------------------------------------------------
        # Messages
        # --------------------------------------------------

        if triple_disorder:
            message = "Triple acid-base disorder detected."

        elif mixed_disorder:
            message = "Mixed acid-base disorder detected."

        else:
            message = "No mixed acid-base disorder detected."

        return {
            "mixed_disorder": mixed_disorder,
            "triple_disorder": triple_disorder,
            "disorders": disorders,
            "component_count": component_count,
            "message": message,
        }
