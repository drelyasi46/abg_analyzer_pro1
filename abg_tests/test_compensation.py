import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.compensation_engine import CompensationEngine


def test(name, primary_disorder, pco2, hco3, expected_status, chronic=False):
    result = CompensationEngine.evaluate(
        primary_disorder=primary_disorder,
        pco2=pco2,
        hco3=hco3,
        chronic=chronic
    )

    actual = result.status

    assert actual == expected_status, (
        f"{name}: expected {expected_status}, got {actual}"
    )

    print(f"PASS: {name}")


def main():

    # =========================================
    # METABOLIC ACIDOSIS
    # Winter's formula:
    # expected PCO2 = 1.5 × HCO3 + 8 ± 2
    # =========================================

    test(
        "MA - exact expected",
        "Metabolic Acidosis", 29, 14,
        "APPROPRIATE"
    )

    test(
        "MA - lower boundary",
        "Metabolic Acidosis", 27, 14,
        "APPROPRIATE"
    )

    test(
        "MA - upper boundary",
        "Metabolic Acidosis", 31, 14,
        "APPROPRIATE"
    )

    test(
        "MA - superimposed respiratory acidosis",
        "Metabolic Acidosis", 35, 14,
        "SUPERIMPOSED_RESP_ACIDOSIS"
    )

    test(
        "MA - superimposed respiratory alkalosis",
        "Metabolic Acidosis", 20, 14,
        "SUPERIMPOSED_RESP_ALKALOSIS"
    )

    # =========================================
    # METABOLIC ALKALOSIS
    # Expected PCO2 = 0.7 × (HCO3 - 24) + 40 ± 5
    # =========================================

    test(
        "MAlk - exact expected",
        "Metabolic Alkalosis", 45.6, 32,
        "APPROPRIATE"
    )

    test(
        "MAlk - lower boundary",
        "Metabolic Alkalosis", 40.6, 32,
        "APPROPRIATE"
    )

    test(
        "MAlk - upper boundary",
        "Metabolic Alkalosis", 50.6, 32,
        "APPROPRIATE"
    )

    test(
        "MAlk - superimposed respiratory acidosis",
        "Metabolic Alkalosis", 60, 32,
        "SUPERIMPOSED_RESP_ACIDOSIS"
    )

    test(
        "MAlk - superimposed respiratory alkalosis",
        "Metabolic Alkalosis", 30, 32,
        "SUPERIMPOSED_RESP_ALKALOSIS"
    )

    # =========================================
    # ACUTE RESPIRATORY ACIDOSIS
    # HCO3 expected = 24 + 0.1 × ΔPCO2 ± 2
    # =========================================

    test(
        "Acute respiratory acidosis - appropriate",
        "Respiratory Acidosis", 60, 26,
        "APPROPRIATE", chronic=False
    )

    test(
        "Acute respiratory acidosis - metabolic acidosis",
        "Respiratory Acidosis", 60, 22,
        "SUPERIMPOSED_METABOLIC_ACIDOSIS", chronic=False
    )

    test(
        "Acute respiratory acidosis - metabolic alkalosis",
        "Respiratory Acidosis", 60, 30,
        "SUPERIMPOSED_METABOLIC_ALKALOSIS", chronic=False
    )

    # =========================================
    # CHRONIC RESPIRATORY ACIDOSIS
    # HCO3 expected = 24 + 0.4 × ΔPCO2 ± 2
    # =========================================

    test(
        "Chronic respiratory acidosis - appropriate",
        "Respiratory Acidosis", 60, 32,
        "APPROPRIATE", chronic=True
    )

    test(
        "Chronic respiratory acidosis - metabolic acidosis",
        "Respiratory Acidosis", 60, 28,
        "SUPERIMPOSED_METABOLIC_ACIDOSIS", chronic=True
    )

    test(
        "Chronic respiratory acidosis - metabolic alkalosis",
        "Respiratory Acidosis", 60, 38,
        "SUPERIMPOSED_METABOLIC_ALKALOSIS", chronic=True
    )

    # =========================================
    # ACUTE RESPIRATORY ALKALOSIS
    # HCO3 expected = 24 - 0.2 × ΔPCO2 ± 2
    # =========================================

    test(
        "Acute respiratory alkalosis - appropriate",
        "Respiratory Alkalosis", 30, 22,
        "APPROPRIATE", chronic=False
    )

    test(
        "Acute respiratory alkalosis - metabolic acidosis",
        "Respiratory Alkalosis", 30, 19,
        "SUPERIMPOSED_METABOLIC_ACIDOSIS", chronic=False
    )

    test(
        "Acute respiratory alkalosis - metabolic alkalosis",
        "Respiratory Alkalosis", 30, 26,
        "SUPERIMPOSED_METABOLIC_ALKALOSIS", chronic=False
    )

    # =========================================
    # CHRONIC RESPIRATORY ALKALOSIS
    # HCO3 expected = 24 - 0.4 × ΔPCO2 ± 2
    # =========================================

    test(
        "Chronic respiratory alkalosis - appropriate",
        "Respiratory Alkalosis", 30, 20,
        "APPROPRIATE", chronic=True
    )

    test(
        "Chronic respiratory alkalosis - metabolic acidosis",
        "Respiratory Alkalosis", 30, 16,
        "SUPERIMPOSED_METABOLIC_ACIDOSIS", chronic=True
    )

    test(
        "Chronic respiratory alkalosis - metabolic alkalosis",
        "Respiratory Alkalosis", 30, 24,
        "SUPERIMPOSED_METABOLIC_ALKALOSIS", chronic=True
    )

    print("\nAll compensation tests passed.")


if __name__ == "__main__":
    main()
