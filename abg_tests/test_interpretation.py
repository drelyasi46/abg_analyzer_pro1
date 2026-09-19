import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.interpretation_engine import InterpretationEngine


def compensation(status, message="Test compensation message."):
    return SimpleNamespace(
        status=status,
        message=message
    )


def test(name, primary=None, comp=None, ag=None, delta=None,
         triple=None, expected=None):

    result = InterpretationEngine.generate(
        primary_disorder=primary,
        compensation=comp,
        anion_gap=ag,
        delta_ratio=delta,
        triple=triple
    )

    actual = result["clinical_report"]

    assert actual == expected, (
        f"{name}:\n"
        f"Expected: {expected}\n"
        f"Got:      {actual}"
    )

    print(f"PASS: {name}")


def main():

    # =========================================
    # PRIMARY DISORDERS
    # =========================================

    test(
        "Primary metabolic acidosis",
        primary="Metabolic Acidosis",
        expected=["Primary metabolic acidosis."]
    )

    test(
        "Primary metabolic alkalosis",
        primary="Metabolic Alkalosis",
        expected=["Primary metabolic alkalosis."]
    )

    test(
        "Primary respiratory acidosis",
        primary="Respiratory Acidosis",
        expected=["Primary respiratory acidosis."]
    )

    test(
        "Primary respiratory alkalosis",
        primary="Respiratory Alkalosis",
        expected=["Primary respiratory alkalosis."]
    )

    # =========================================
    # COMPENSATION
    # =========================================

    test(
        "Appropriate compensation",
        primary="Metabolic Acidosis",
        comp=compensation(
            "APPROPRIATE",
            "Compensation appropriate."
        ),
        expected=[
            "Primary metabolic acidosis.",
            "Compensation appropriate."
        ]
    )

    test(
        "Superimposed respiratory acidosis",
        primary="Metabolic Acidosis",
        comp=compensation("SUPERIMPOSED_RESP_ACIDOSIS"),
        expected=[
            "Primary metabolic acidosis.",
            "Concurrent respiratory acidosis detected."
        ]
    )

    test(
        "Superimposed respiratory alkalosis",
        primary="Metabolic Acidosis",
        comp=compensation("SUPERIMPOSED_RESP_ALKALOSIS"),
        expected=[
            "Primary metabolic acidosis.",
            "Concurrent respiratory alkalosis detected."
        ]
    )

    test(
        "Superimposed metabolic acidosis",
        primary="Respiratory Acidosis",
        comp=compensation("SUPERIMPOSED_METABOLIC_ACIDOSIS"),
        expected=[
            "Primary respiratory acidosis.",
            "Concurrent metabolic acidosis detected."
        ]
    )

    test(
        "Superimposed metabolic alkalosis",
        primary="Respiratory Acidosis",
        comp=compensation("SUPERIMPOSED_METABOLIC_ALKALOSIS"),
        expected=[
            "Primary respiratory acidosis.",
            "Concurrent metabolic alkalosis detected."
        ]
    )

    # =========================================
    # ANION GAP
    # =========================================

    test(
        "High AG with metabolic acidosis",
        primary="Metabolic Acidosis",
        ag={
            "status": "HIGH_ANION_GAP"
        },
        expected=[
            "Primary metabolic acidosis.",
            "High anion gap metabolic acidosis (HAGMA)."
        ]
    )

    test(
        "Normal AG with metabolic acidosis",
        primary="Metabolic Acidosis",
        ag={
            "status": "NORMAL_ANION_GAP"
        },
        expected=[
            "Primary metabolic acidosis.",
            "Normal anion gap metabolic acidosis (NAGMA)."
        ]
    )

    test(
        "Elevated AG without metabolic acidosis",
        primary="Normal",
        ag={
            "status": "HIGH_ANION_GAP"
        },
        expected=[
            "Elevated anion gap without metabolic acidosis."
        ]
    )

    # =========================================
    # DELTA RATIO
    # =========================================

    test(
        "Pure HAGMA",
        primary="Metabolic Acidosis",
        delta={
            "status": "PURE_HAGMA"
        },
        expected=[
            "Primary metabolic acidosis.",
            "Pure high anion gap metabolic acidosis."
        ]
    )

    test(
        "HAGMA plus metabolic alkalosis",
        primary="Metabolic Acidosis",
        delta={
            "status": "HAGMA_PLUS_METABOLIC_ALKALOSIS"
        },
        expected=[
            "Primary metabolic acidosis.",
            "Mixed HAGMA + metabolic alkalosis."
        ]
    )

    test(
        "HAGMA plus NAGMA",
        primary="Metabolic Acidosis",
        delta={
            "status": "HAGMA_PLUS_NAGMA"
        },
        expected=[
            "Primary metabolic acidosis.",
            "Mixed HAGMA + normal anion gap metabolic acidosis."
        ]
    )

    # =========================================
    # TRIPLE DISORDER
    # =========================================

    test(
        "Triple disorder",
        primary="Metabolic Acidosis",
        comp=compensation("SUPERIMPOSED_RESP_ACIDOSIS"),
        delta={
            "status": "HAGMA_PLUS_METABOLIC_ALKALOSIS"
        },
        triple={
            "triple_disorder": True
        },
        expected=[
            "Primary metabolic acidosis.",
            "Concurrent respiratory acidosis detected.",
            "Mixed HAGMA + metabolic alkalosis.",
            "Triple acid-base disorder detected."
        ]
    )

    print("\nAll interpretation tests passed.")


if __name__ == "__main__":
    main()
