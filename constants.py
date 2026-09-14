"""
compensation.py
Standard acid-base compensation calculations
"""

class Compensation:

    @staticmethod
    def winters_formula(hco3):
        """
        Expected PaCO2 for metabolic acidosis
        Returns:
            (lower_limit, expected, upper_limit)
        """
        expected = 1.5 * hco3 + 8
        return expected - 2, expected, expected + 2

    @staticmethod
    def metabolic_alkalosis_expected_pco2(hco3):
        """
        Expected PaCO2 for metabolic alkalosis
        """
        expected = 40 + 0.7 * (hco3 - 24)
        return expected - 5, expected, expected + 5

    @staticmethod
    def acute_respiratory_acidosis_expected_hco3(pco2):
        """
        Acute respiratory acidosis:
        HCO3 rises ~1 mEq/L for every 10 mmHg rise in PaCO2 above 40
        """
        return 24 + ((pco2 - 40) / 10) * 1

    @staticmethod
    def chronic_respiratory_acidosis_expected_hco3(pco2):
        """
        Chronic respiratory acidosis:
        HCO3 rises ~3.5 mEq/L for every 10 mmHg rise in PaCO2 above 40
        """
        return 24 + ((pco2 - 40) / 10) * 3.5

    @staticmethod
    def acute_respiratory_alkalosis_expected_hco3(pco2):
        """
        Acute respiratory alkalosis:
        HCO3 falls ~2 mEq/L for every 10 mmHg fall in PaCO2 below 40
        """
        return 24 - ((40 - pco2) / 10) * 2

    @staticmethod
    def chronic_respiratory_alkalosis_expected_hco3(pco2):
        """
        Chronic respiratory alkalosis:
        HCO3 falls ~5 mEq/L for every 10 mmHg fall in PaCO2 below 40
        """
        return 24 - ((40 - pco2) / 10) * 5
    