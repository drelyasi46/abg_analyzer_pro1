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
    def detect_chronicity(primary_disorder, pco2, hco3):
        """
        Estimate acute vs chronic respiratory disorder
        from the expected renal compensation.

        This is an ABG-based heuristic and should not override
        clinical history.
        """

        normal_pco2 = 40
        normal_hco3 = 24

        if primary_disorder == "Respiratory Acidosis":

            delta = pco2 - normal_pco2

            if delta <= 0:
                return False

            acute_expected = normal_hco3 + (0.1 * delta)
            chronic_expected = normal_hco3 + (0.4 * delta)

        elif primary_disorder == "Respiratory Alkalosis":

            delta = normal_pco2 - pco2

            if delta <= 0:
                return False

            acute_expected = normal_hco3 - (0.2 * delta)
            chronic_expected = normal_hco3 - (0.4 * delta)

        else:
            return False

        acute_distance = abs(hco3 - acute_expected)
        chronic_distance = abs(hco3 - chronic_expected)

        return chronic_distance < acute_distance


    @staticmethod
    def evaluate(primary_disorder, pco2, hco3, chronic=False):

        if primary_disorder == "Metabolic Acidosis":
            return CompensationEngine._metabolic_acidosis(
                pco2,
                hco3
            )

        elif primary_disorder == "Metabolic Alkalosis":
            return CompensationEngine._metabolic_alkalosis(
                pco2,
                hco3
            )

        elif primary_disorder == "Respiratory Acidosis":
            return CompensationEngine._respiratory_acidosis(
                pco2,
                hco3,
                chronic
            )

        elif primary_disorder == "Respiratory Alkalosis":
            return CompensationEngine._respiratory_alkalosis(
                pco2,
                hco3,
                chronic
            )

        # Normal ABG has no compensation calculation.
        return None


    @staticmethod
    def _metabolic_acidosis(pco2, hco3):

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

        normal_pco2 = 40
        normal_hco3 = 24

        delta_pco2 = normal_pco2 - pco2

        if chronic:
            expected = normal_hco3 - (0.4 * delta_pco2)
            message_type = "Chronic"
        else:
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

        normal_pco2 = 40
        normal_hco3 = 24

        delta_pco2 = pco2 - normal_pco2

        if chronic:
            expected = normal_hco3 + (0.4 * delta_pco2)
            message_type = "Chronic"
        else:
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
