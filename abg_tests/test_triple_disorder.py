import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.triple_disorder import TripleDisorderEngine


def compensation(status):
    return SimpleNamespace(status=status)


def test(name, primary, compensation_status=None, delta_status=None,
         expected_triple=False, expected_disorders=None):

    result = TripleDisorderEngine.analyze(
        primary_disorder=primary,
        compensation_result=(
            compensation(compensation_status)
            if compensation_status else None
        ),
        delta_ratio=(
            {"status": delta_status}
            if delta_status else None
        )
    )

    assert result["triple_disorder"] == expected_triple, (
        f"{name}: expected triple={expected_triple}, "
        f"got {result['triple_disorder']}"
    )

    if expected_disorders is not None:
        assert result["disorders"] == expected_disorders, (
            f"{name}: expected {expected_disorders}, "
            f"got {result['disorders']}"
        )

    print(f"PASS: {name}")


def main():

    # =========================================
    # SINGLE DISORDER
    # =========================================

    test(
        "Single metabolic acidosis",
        "Metabolic Acidosis",
        expected_triple=False,
        expected_disorders=["Metabolic Acidosis"]
    )

    test(
        "Single respiratory acidosis",
        "Respiratory Acidosis",
        expected_triple=False,
        expected_disorders=["Respiratory Acidosis"]
    )

    # =========================================
    # TWO DISORDERS
    # =========================================

    test(
        "Metabolic acidosis + respiratory acidosis",
        "Metabolic Acidosis",
        compensation_status="SUPERIMPOSED_RESP_ACIDOSIS",
        expected_triple=False,
        expected_disorders=[
            "Metabolic Acidosis",
            "Respiratory Acidosis"
        ]
    )

    test(
        "Metabolic alkalosis + respiratory alkalosis",
        "Metabolic Alkalosis",
        compensation_status="SUPERIMPOSED_RESP_ALKALOSIS",
        expected_triple=False,
        expected_disorders=[
            "Metabolic Alkalosis",
            "Respiratory Alkalosis"
        ]
    )

    test(
        "HAGMA + additional NAGMA",
        "Metabolic Acidosis",
        delta_status="HAGMA_PLUS_NAGMA",
        expected_triple=False,
        expected_disorders=[
            "Metabolic Acidosis",
            "Additional Normal Anion Gap Metabolic Acidosis"
        ]
    )

    # =========================================
    # TRIPLE DISORDERS
    # =========================================

    test(
        "Triple: MA + respiratory acidosis + metabolic alkalosis",
        "Metabolic Acidosis",
        compensation_status="SUPERIMPOSED_RESP_ACIDOSIS",
        delta_status="HAGMA_PLUS_METABOLIC_ALKALOSIS",
        expected_triple=True,
        expected_disorders=[
            "Metabolic Acidosis",
            "Respiratory Acidosis",
            "Metabolic Alkalosis"
        ]
    )

    test(
        "Triple: MA + respiratory alkalosis + metabolic alkalosis",
        "Metabolic Acidosis",
        compensation_status="SUPERIMPOSED_RESP_ALKALOSIS",
        delta_status="HAGMA_PLUS_METABOLIC_ALKALOSIS",
        expected_triple=True,
        expected_disorders=[
            "Metabolic Acidosis",
            "Respiratory Alkalosis",
            "Metabolic Alkalosis"
        ]
    )

    # =========================================
    # DUPLICATE PROTECTION
    # =========================================

    test(
        "No duplicate respiratory acidosis",
        "Respiratory Acidosis",
        compensation_status="SUPERIMPOSED_RESP_ACIDOSIS",
        expected_triple=False,
        expected_disorders=[
            "Respiratory Acidosis"
        ]
    )

    test(
        "No duplicate metabolic acidosis",
        "Metabolic Acidosis",
        compensation_status="SUPERIMPOSED_METABOLIC_ACIDOSIS",
        expected_triple=False,
        expected_disorders=[
            "Metabolic Acidosis"
        ]
    )

    print("\nAll triple-disorder tests passed.")


if __name__ == "__main__":
    main()
