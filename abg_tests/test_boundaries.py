import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.abg_engine import ABGEngine


def check(name, result, expected_primary=None):
    if expected_primary is not None:
        assert result["primary_disorder"] == expected_primary, (
            f"{name}: expected {expected_primary}, "
            f"got {result['primary_disorder']}"
        )
    assert isinstance(result, dict)
    print(f"PASS: {name}")


def main():

    # -----------------------------
    # pH boundaries
    # -----------------------------
    check(
        "pH exactly 7.35",
        ABGEngine.analyze(7.35, 45, 22),
        "Normal"
    )

    check(
        "pH exactly 7.45",
        ABGEngine.analyze(7.45, 45, 26),
        "Normal"
    )

    check(
        "pH just below 7.35 with low HCO3",
        ABGEngine.analyze(7.349, 45, 21.9),
        "Metabolic Acidosis"
    )

    check(
        "pH just above 7.45 with high HCO3",
        ABGEngine.analyze(7.451, 45, 26.1),
        "Metabolic Alkalosis"
    )

    # -----------------------------
    # PCO2 boundaries
    # -----------------------------
    check(
        "PCO2 exactly 35",
        ABGEngine.analyze(7.40, 35, 24),
        "Normal"
    )

    check(
        "PCO2 exactly 45",
        ABGEngine.analyze(7.40, 45, 24),
        "Normal"
    )

    check(
        "PCO2 just below 35",
        ABGEngine.analyze(7.46, 34.9, 24),
        "Respiratory Alkalosis"
    )

    check(
        "PCO2 just above 45",
        ABGEngine.analyze(7.34, 45.1, 24),
        "Respiratory Acidosis"
    )

    # -----------------------------
    # HCO3 boundaries
    # -----------------------------
    check(
        "HCO3 exactly 22",
        ABGEngine.analyze(7.35, 45, 22),
        "Normal"
    )

    check(
        "HCO3 exactly 26",
        ABGEngine.analyze(7.45, 45, 26),
        "Normal"
    )

    check(
        "HCO3 just below 22",
        ABGEngine.analyze(7.34, 45, 21.9),
        "Metabolic Acidosis"
    )

    check(
        "HCO3 just above 26",
        ABGEngine.analyze(7.46, 45, 26.1),
        "Metabolic Alkalosis"
    )

    # -----------------------------
    # Anion gap boundary
    # -----------------------------
    r = ABGEngine.analyze(
        7.30, 30, 18,
        na=140, cl=110
    )
    assert r["anion_gap"]["anion_gap"] == 12
    assert r["anion_gap"]["status"] == "NORMAL_ANION_GAP"
    print("PASS: Anion gap exactly 12")

    r = ABGEngine.analyze(
        7.30, 30, 18,
        na=141, cl=110
    )
    assert r["anion_gap"]["anion_gap"] == 13
    assert r["anion_gap"]["status"] == "HIGH_ANION_GAP"
    print("PASS: Anion gap exactly 13")

    # -----------------------------
    # Delta ratio boundaries
    # -----------------------------

    # ratio = 0.4
    # AG = 16, HCO3 = 14
    r = ABGEngine.analyze(
        7.20, 25, 14,
        na=140, cl=110
    )
    assert r["delta_ratio"]["delta_ratio"] == 0.4
    assert r["delta_ratio"]["status"] == "HAGMA_PLUS_NAGMA"
    print("PASS: Delta ratio exactly 0.4")

    # ratio = 0.8
    # AG = 16, HCO3 = 19
    r = ABGEngine.analyze(
        7.20, 25, 19,
        na=140, cl=105
    )
    assert r["delta_ratio"]["delta_ratio"] == 0.8
    assert r["delta_ratio"]["status"] == "PURE_HAGMA"
    print("PASS: Delta ratio exactly 0.8")

    # ratio = 2.0
    # AG = 20, HCO3 = 20
    r = ABGEngine.analyze(
        7.20, 25, 20,
        na=140, cl=100
    )
    assert r["delta_ratio"]["delta_ratio"] == 2.0
    assert r["delta_ratio"]["status"] == "PURE_HAGMA"
    print("PASS: Delta ratio exactly 2.0")

    # ratio > 2
    r = ABGEngine.analyze(
        7.20, 25, 20,
        na=141, cl=100
    )
    assert r["delta_ratio"]["delta_ratio"] > 2
    assert r["delta_ratio"]["status"] == "HAGMA_PLUS_METABOLIC_ALKALOSIS"
    print("PASS: Delta ratio above 2")

    # -----------------------------
    # Missing electrolytes
    # -----------------------------
    r = ABGEngine.analyze(
        7.25, 30, 14,
        na=None, cl=None
    )
    assert r["anion_gap"] is None
    assert r["delta_ratio"] is None
    print("PASS: No electrolytes -> no AG/delta ratio")

    print()
    print("ALL BOUNDARY TESTS PASSED")


if __name__ == "__main__":
    main()
