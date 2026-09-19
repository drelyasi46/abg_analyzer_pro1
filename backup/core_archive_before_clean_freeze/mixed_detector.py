"""
mixed_detector.py

Professional Mixed Disorder Detection
"""


class MixedDisorderDetector:

    @staticmethod
    def respiratory_compensation(
        measured_pco2,
        expected_low,
        expected_high,
        tolerance=1.0,
    ):
        """
        Used in metabolic disorders.
        Compare measured PaCO2 with expected compensation.
        """

        if (
            expected_low - tolerance
            <= measured_pco2
            <= expected_high + tolerance
        ):
            return "Appropriate Respiratory Compensation"

        elif measured_pco2 > expected_high + tolerance:
            return (
                "Mixed Disorder: "
                "Concurrent Respiratory Acidosis"
            )

        else:
            return (
                "Mixed Disorder: "
                "Concurrent Respiratory Alkalosis"
            )

    @staticmethod
    def metabolic_compensation(
        measured_hco3,
        expected_acute,
        expected_chronic,
        tolerance=2.0,
    ):
        """
        Used in respiratory disorders.
        Compare measured HCO3 with expected renal compensation.
        """

        acute_ok = (
            abs(measured_hco3 - expected_acute)
            <= tolerance
        )

        chronic_ok = (
            abs(measured_hco3 - expected_chronic)
            <= tolerance
        )

        if acute_ok:
            return "Acute Respiratory Disorder"

        if chronic_ok:
            return "Chronic Respiratory Disorder"

        if measured_hco3 > expected_chronic:
            return (
                "Mixed Disorder: "
                "Concurrent Metabolic Alkalosis"
            )

        return (
            "Mixed Disorder: "
            "Concurrent Metabolic Acidosis"
        )