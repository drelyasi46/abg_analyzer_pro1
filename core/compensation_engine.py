from dataclasses import dataclass


@dataclass
class CompensationResult:
    expected: float
    low: float
    high: float
    measured: float
    status: str
    message: str


class CompensationEngine:

    @staticmethod
    def evaluate(primary_disorder, pco2, hco3, chronic=False):

        if primary_disorder == "Metabolic Acidosis":
            return CompensationEngine._metabolic_acidosis(pco2, hco3)

        elif primary_disorder == "Metabolic Alkalosis":
            return CompensationEngine._metabolic_alkalosis(pco2, hco3)

        elif primary_disorder == "Respiratory Acidosis":
            return CompensationEngine._respiratory_acidosis(pco2, hco3, chronic)

        elif primary_disorder == "Respiratory Alkalosis":
            return CompensationEngine._respiratory_alkalosis(pco2, hco3, chronic)

        return None

    @staticmethod
    def _metabolic_acidosis(pco2, hco3):

        # Winter Formula
        expected = (1.5 * hco3) + 8

        low = expected - 2
        high = expected + 2

        if low <= pco2 <= high:
            status = "APPROPRIATE"
            message = "Appropriate respiratory compensation."

        elif pco2 > high:
            status = "SUPERIMPOSED_RESP_ACIDOSIS"
            message = "Superimposed respiratory acidosis."

        else:
            status = "SUPERIMPOSED_RESP_ALKALOSIS"
            message = "Superimposed respiratory alkalosis."

        return CompensationResult(
            expected=round(expected, 1),
            low=round(low, 1),
            high=round(high, 1),
            measured=round(pco2, 1),
            status=status,
            message=message,
        )

    
    @staticmethod
    def _metabolic_alkalosis(pco2, hco3):

        # Expected respiratory compensation
        # PCO2 = 0.7 × (HCO3 - 24) + 40 ± 5
        expected = (0.7 * (hco3 - 24)) + 40

        low = expected - 5
        high = expected + 5

        if low <= pco2 <= high:
            status = "APPROPRIATE"
            message = "Appropriate respiratory compensation."

        elif pco2 > high:
            status = "SUPERIMPOSED_RESP_ACIDOSIS"
            message = "Superimposed respiratory acidosis."

        else:
            status = "SUPERIMPOSED_RESP_ALKALOSIS"
            message = "Superimposed respiratory alkalosis."

        return CompensationResult(
            expected=round(expected, 1),
            low=round(low, 1),
            high=round(high, 1),
            measured=round(pco2, 1),
            status=status,
            message=message,
        )
    @staticmethod
    def _respiratory_alkalosis(pco2, hco3, chronic):

        # Normal values
        normal_pco2 = 40
        normal_hco3 = 24

        delta_pco2 = normal_pco2 - pco2

        if chronic:
            # Chronic respiratory alkalosis:
            # HCO3 decreases ~4 mEq/L per 10 mmHg decrease in PCO2
            expected = normal_hco3 - (0.4 * delta_pco2)

            message_type = "Chronic"

        else:
            # Acute respiratory alkalosis:
            # HCO3 decreases ~2 mEq/L per 10 mmHg decrease in PCO2
            expected = normal_hco3 - (0.2 * delta_pco2)

            message_type = "Acute"

        low = expected - 2
        high = expected + 2

        if low <= hco3 <= high:
            status = "APPROPRIATE"
            message = f"{message_type} respiratory compensation appropriate."

        elif hco3 < low:
            status = "SUPERIMPOSED_METABOLIC_ACIDOSIS"
            message = "Superimposed metabolic acidosis."

        else:
            status = "SUPERIMPOSED_METABOLIC_ALKALOSIS"
            message = "Superimposed metabolic alkalosis."

        return CompensationResult(
            expected=round(expected, 1),
            low=round(low, 1),
            high=round(high, 1),
            measured=round(hco3, 1),
            status=status,
            message=message,
        )
    @staticmethod
    def _respiratory_acidosis(pco2, hco3, chronic):

        # Normal values
        normal_pco2 = 40
        normal_hco3 = 24

        delta_pco2 = pco2 - normal_pco2

        if chronic:
            # Chronic respiratory acidosis:
            # HCO3 rises ~4 mEq/L per 10 mmHg increase in PCO2
            expected = normal_hco3 + (0.4 * delta_pco2)

            message_type = "Chronic"

        else:
            # Acute respiratory acidosis:
            # HCO3 rises ~1 mEq/L per 10 mmHg increase in PCO2
            expected = normal_hco3 + (0.1 * delta_pco2)

            message_type = "Acute"

        low = expected - 2
        high = expected + 2

        if low <= hco3 <= high:
            status = "APPROPRIATE"
            message = f"{message_type} respiratory compensation appropriate."

        elif hco3 < low:
            status = "SUPERIMPOSED_METABOLIC_ACIDOSIS"
            message = "Superimposed metabolic acidosis."

        else:
            status = "SUPERIMPOSED_METABOLIC_ALKALOSIS"
            message = "Superimposed metabolic alkalosis."

        return CompensationResult(
            expected=round(expected, 1),
            low=round(low, 1),
            high=round(high, 1),
            measured=round(hco3, 1),
            status=status,
            message=message,
        )