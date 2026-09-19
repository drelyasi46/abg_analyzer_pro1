class MixedDisorderDetector:

    @staticmethod
    def analyze(compensation_result):

        status = compensation_result.status

        if status == "APPROPRIATE":
            return {
                "mixed": False,
                "type": None,
                "message": "No mixed disorder detected."
            }

        elif status == "SUPERIMPOSED_RESP_ACIDOSIS":
            return {
                "mixed": True,
                "type": "Respiratory Acidosis",
                "message": "Mixed disorder: primary disorder with superimposed respiratory acidosis."
            }

        elif status == "SUPERIMPOSED_RESP_ALKALOSIS":
            return {
                "mixed": True,
                "type": "Respiratory Alkalosis",
                "message": "Mixed disorder: primary disorder with superimposed respiratory alkalosis."
            }

        elif status == "SUPERIMPOSED_METABOLIC_ACIDOSIS":
            return {
                "mixed": True,
                "type": "Metabolic Acidosis",
                "message": "Mixed disorder: primary respiratory disorder with superimposed metabolic acidosis."
            }

        elif status == "SUPERIMPOSED_METABOLIC_ALKALOSIS":
            return {
                "mixed": True,
                "type": "Metabolic Alkalosis",
                "message": "Mixed disorder: primary respiratory disorder with superimposed metabolic alkalosis."
            }

        return {
            "mixed": False,
            "type": None,
            "message": "Unknown pattern."
        }