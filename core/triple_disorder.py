class TripleDisorderEngine:

    @staticmethod
    def analyze(
        compensation_result,
        delta_ratio=None
    ):

        disorders = []


        # Respiratory component
        if compensation_result.status == "SUPERIMPOSED_RESP_ACIDOSIS":

            disorders.append(
                "Respiratory Acidosis"
            )


        elif compensation_result.status == "SUPERIMPOSED_RESP_ALKALOSIS":

            disorders.append(
                "Respiratory Alkalosis"
            )


        # Primary metabolic disorder
        if compensation_result.status.startswith("SUPERIMPOSED_RESP"):

            disorders.insert(
                0,
                "Metabolic disorder"
            )


        # Additional metabolic disorder from Delta Ratio
        if delta_ratio is not None:

            if delta_ratio >= 2:

                disorders.append(
                    "Metabolic Alkalosis"
                )


            elif delta_ratio < 0.4:

                disorders.append(
                    "Normal Anion Gap Metabolic Acidosis"
                )


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