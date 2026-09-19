import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.anion_gap import AnionGapEngine
from core.delta_ratio import DeltaRatioEngine


def test_ag(name, na, cl, hco3, expected_ag, expected_status):
    result = AnionGapEngine.calculate(na, cl, hco3)

    assert result["anion_gap"] == expected_ag, (
        f"{name}: expected AG {expected_ag}, got {result['anion_gap']}"
    )

    assert result["status"] == expected_status, (
        f"{name}: expected {expected_status}, got {result['status']}"
    )

    print(f"PASS: {name}")


def test_delta(name, ag, hco3, expected_ratio, expected_status):
    result = DeltaRatioEngine.calculate(ag, hco3)

    assert result["delta_ratio"] == expected_ratio, (
        f"{name}: expected ratio {expected_ratio}, got {result['delta_ratio']}"
    )

    assert result["status"] == expected_status, (
        f"{name}: expected {expected_status}, got {result['status']}"
    )

    print(f"PASS: {name}")


def main():

    # =========================================
    # ANION GAP
    # =========================================

    test_ag(
        "AG below normal",
        140, 110, 18,
        12,
        "NORMAL_ANION_GAP"
    )

    test_ag(
        "AG exactly 12",
        140, 106, 22,
        12,
        "NORMAL_ANION_GAP"
    )

    test_ag(
        "AG above normal",
        140, 100, 24,
        16,
        "HIGH_ANION_GAP"
    )

    test_ag(
        "AG clearly high",
        145, 100, 20,
        25,
        "HIGH_ANION_GAP"
    )

    # =========================================
    # DELTA RATIO
    # =========================================

    test_delta(
        "Delta ratio below 0.4",
        13, 21,
        0.33,
        "HAGMA_PLUS_NAGMA"
    )

    test_delta(
        "Delta ratio exactly 0.4",
        14, 19,
        0.4,
        "HAGMA_PLUS_NAGMA"
    )

    test_delta(
        "Delta ratio between 0.4 and 0.8",
        15, 19,
        0.6,
        "HAGMA_PLUS_NAGMA"
    )

    test_delta(
        "Delta ratio exactly 0.8",
        16, 19,
        0.8,
        "PURE_HAGMA"
    )

    test_delta(
        "Delta ratio exactly 2.0",
        20, 20,
        2.0,
        "PURE_HAGMA"
    )

    test_delta(
        "Delta ratio above 2",
        22, 19,
        2.0,
        "PURE_HAGMA"
    )

    test_delta(
        "Delta ratio clearly above 2",
        25, 19,
        2.6,
        "HAGMA_PLUS_METABOLIC_ALKALOSIS"
    )

    test_delta(
        "HCO3 exactly 24",
        20, 24,
        None,
        "UNDEFINED"
    )

    test_delta(
        "HCO3 above 24",
        20, 30,
        None,
        "HAGMA_PLUS_METABOLIC_ALKALOSIS"
    )

    print("\\nAll anion gap and delta ratio tests passed.")


if __name__ == "__main__":
    main()
