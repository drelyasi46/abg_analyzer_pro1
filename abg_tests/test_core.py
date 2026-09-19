import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.abg_engine import ABGEngine


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"PASS: {name}")


def main():
    # 1. Normal ABG
    r = ABGEngine.analyze(
        ph=7.40,
        pco2=40,
        hco3=24
    )
    check(
        "Normal ABG",
        r["primary_disorder"] == "Normal"
        and r["compensation"] is None
    )

    # 2. Metabolic acidosis + appropriate respiratory compensation
    r = ABGEngine.analyze(
        ph=7.25,
        pco2=29,
        hco3=14
    )
    check(
        "Metabolic acidosis",
        r["primary_disorder"] == "Metabolic Acidosis"
    )
    check(
        "Metabolic acidosis compensation",
        r["compensation"].status == "APPROPRIATE"
    )

    # 3. Metabolic acidosis + respiratory acidosis
    r = ABGEngine.analyze(
        ph=7.20,
        pco2=45,
        hco3=16
    )
    check(
        "Metabolic acidosis + respiratory acidosis",
        r["primary_disorder"] == "Metabolic Acidosis"
        and r["compensation"].status == "SUPERIMPOSED_RESP_ACIDOSIS"
    )

    # 4. Metabolic acidosis + respiratory alkalosis
    r = ABGEngine.analyze(
        ph=7.30,
        pco2=20,
        hco3=12
    )
    check(
        "Metabolic acidosis + respiratory alkalosis",
        r["primary_disorder"] == "Metabolic Acidosis"
        and r["compensation"].status == "SUPERIMPOSED_RESP_ALKALOSIS"
    )

    # 5. Metabolic alkalosis + appropriate compensation
    r = ABGEngine.analyze(
        ph=7.50,
        pco2=47,
        hco3=32
    )
    check(
        "Metabolic alkalosis",
        r["primary_disorder"] == "Metabolic Alkalosis"
    )
    check(
        "Metabolic alkalosis compensation",
        r["compensation"].status == "APPROPRIATE"
    )

    # 6. Acute respiratory acidosis
    r = ABGEngine.analyze(
        ph=7.30,
        pco2=60,
        hco3=26
    )
    check(
        "Acute respiratory acidosis",
        r["primary_disorder"] == "Respiratory Acidosis"
        and r["compensation"].message.startswith("Acute")
    )

    # 7. Chronic respiratory acidosis
    r = ABGEngine.analyze(
        ph=7.36,
        pco2=60,
        hco3=32
    )
    check(
        "Chronic respiratory acidosis",
        r["primary_disorder"] == "Respiratory Acidosis"
        and r["compensation"].message.startswith("Chronic")
    )

    # 8. Acute respiratory alkalosis
    r = ABGEngine.analyze(
        ph=7.50,
        pco2=30,
        hco3=22
    )
    check(
        "Acute respiratory alkalosis",
        r["primary_disorder"] == "Respiratory Alkalosis"
        and r["compensation"].message.startswith("Acute")
    )

    # 9. Chronic respiratory alkalosis
    r = ABGEngine.analyze(
        ph=7.45,
        pco2=25,
        hco3=18
    )
    check(
        "Chronic respiratory alkalosis",
        r["primary_disorder"] == "Respiratory Alkalosis"
        and r["compensation"].message.startswith("Chronic")
    )

    # 10. Anion gap
    r = ABGEngine.analyze(
        ph=7.25,
        pco2=29,
        hco3=14,
        na=140,
        cl=100
    )
    check(
        "High anion gap",
        r["anion_gap"]["anion_gap"] == 26
        and r["anion_gap"]["status"] == "HIGH_ANION_GAP"
    )

    # 11. Normal anion gap
    r = ABGEngine.analyze(
        ph=7.30,
        pco2=30,
        hco3=18,
        na=140,
        cl=110
    )
    check(
        "Normal anion gap",
        r["anion_gap"]["anion_gap"] == 12
        and r["anion_gap"]["status"] == "NORMAL_ANION_GAP"
    )

    # 12. Delta ratio: pure HAGMA
    r = ABGEngine.analyze(
        ph=7.20,
        pco2=25,
        hco3=16,
        na=140,
        cl=100
    )
    check(
        "Pure HAGMA delta ratio",
        r["delta_ratio"]["status"] == "PURE_HAGMA"
    )

    print()
    print("ALL CORE TESTS PASSED")


if __name__ == "__main__":
    main()
