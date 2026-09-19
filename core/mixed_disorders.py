"""
mixed_disorders.py

Delta-Delta Analysis
"""


class MixedDisorders:


    @staticmethod
    def interpret_delta_ratio(ratio):

        if ratio < 0.4:

            return (
                "Delta-Delta Analysis:\n"
                "Mixed High Anion Gap Metabolic Acidosis "
                "with Normal Anion Gap Metabolic Acidosis"
            )


        elif ratio < 0.8:

            return (
                "Delta-Delta Analysis:\n"
                "Predominant High Anion Gap Metabolic Acidosis "
                "with additional Normal Anion Gap Acidosis"
            )


        elif ratio <= 2:

            return (
                "Delta-Delta Analysis:\n"
                "Compatible with pure High Anion Gap Metabolic Acidosis"
            )


        else:

            return (
                "Delta-Delta Analysis:\n"
                "High Anion Gap Metabolic Acidosis "
                "with concurrent Metabolic Alkalosis"
            )