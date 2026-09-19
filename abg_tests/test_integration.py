import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.abg_engine import ABGEngine


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"PASS: {name}")


def main():

    # =========================================
    # 1. NORMAL ABG — COMPLETE PIPELINE
    # =========================================

    r = ABGEngine.analyze(
        ph=7.40,
        pco2=40,
        hco3=24
    )

    check(
        "Normal: primary disorder",
        r["primary_disorder"] == "Normal"
    )

    check(
        "Normal: no compensation",
        r["compensation"] is None
    )

    check(
        "Normal: no anion gap",
        r["anion_gap"] is None
    )

    check(
        "Normal: no delta ratio",
        r["delta_ratio"] is None
    )

    check(
        "Normal: no triple disorder",
        r["triple_disorder"]["triple_disorder"] is False
    )

    check(
        "Normal: interpretation exists",
        isinstance(r["interpretation"]["clinical_report"], list)
    )

    check(
        "Normal: severity exists",
        r["severity"]["severity"] == "LOW"
    )

    check(
        "Normal: report exists",
        isinstance(r["report"], str)
        and "ABG ANALYZER PRO" in r["report"]
    )

    # =========================================
    # 2. METABOLIC ACIDOSIS + APPROPRIATE
    # =========================================

    r = ABGEngine.analyze(
        ph=7.25,
        pco2=29,
        hco3=14,
        na=140,
        cl=100
    )

    check(
        "HAGMA: primary metabolic acidosis",
        r["primary_disorder"] == "Metabolic Acidosis"
    )

    check(
        "HAGMA: appropriate compensation",
        r["compensation"].status == "APPROPRIATE"
    )

    check(
        "HAGMA: high anion gap",
        r["anion_gap"]["status"] == "HIGH_ANION_GAP"
    )

    check(
        "HAGMA: delta ratio generated",
        r["delta_ratio"] is not None
    )

    check(
        "HAGMA: no triple disorder",
        r["triple_disorder"]["triple_disorder"] is False
    )

    check(
        "HAGMA: interpretation contains primary diagnosis",
        "Primary metabolic acidosis."
        in r["interpretation"]["clinical_report"]
    )

    check(
        "HAGMA: report contains AG section",
        "ANION GAP" in r["report"]
    )

    # =========================================
    # 3. METABOLIC ACIDOSIS + RESPIRATORY ACIDOSIS
    # =========================================

    r = ABGEngine.analyze(
        ph=7.20,
        pco2=45,
        hco3=16
    )

    check(
        "Mixed acidosis: primary metabolic acidosis",
        r["primary_disorder"] == "Metabolic Acidosis"
    )

    check(
        "Mixed acidosis: respiratory acidosis detected",
        r["compensation"].status == "SUPERIMPOSED_RESP_ACIDOSIS"
    )

    check(
        "Mixed acidosis: triple disorder false",
        r["triple_disorder"]["triple_disorder"] is False
    )

    check(
        "Mixed acidosis: interpretation includes respiratory acidosis",
        "Concurrent respiratory acidosis detected."
        in r["interpretation"]["clinical_report"]
    )

    # =========================================
    # 4. RESPIRATORY ACIDOSIS — CHRONIC
    # =========================================

    r = ABGEngine.analyze(
        ph=7.36,
        pco2=60,
        hco3=32
    )

    check(
        "Chronic respiratory acidosis: primary",
        r["primary_disorder"] == "Respiratory Acidosis"
    )

    check(
        "Chronic respiratory acidosis: compensation",
        r["compensation"].message.startswith("Chronic")
    )

    check(
        "Chronic respiratory acidosis: no AG",
        r["anion_gap"] is None
    )

    # =========================================
    # 5. RESPIRATORY ALKALOSIS — CHRONIC
    # =========================================

    r = ABGEngine.analyze(
        ph=7.45,
        pco2=25,
        hco3=18
    )

    check(
        "Chronic respiratory alkalosis: primary",
        r["primary_disorder"] == "Respiratory Alkalosis"
    )

    check(
        "Chronic respiratory alkalosis: compensation",
        r["compensation"].message.startswith("Chronic")
    )

    # =========================================
    # 6. HAGMA + DELTA RATIO + REPORT
    # =========================================

    r = ABGEngine.analyze(
        ph=7.20,
        pco2=25,
        hco3=16,
        na=140,
        cl=100
    )

    check(
        "Pure HAGMA: AG",
        r["anion_gap"]["anion_gap"] == 24
    )

    check(
        "Pure HAGMA: delta ratio",
        r["delta_ratio"]["status"] == "PURE_HAGMA"
    )

    check(
        "Pure HAGMA: interpretation",
        "Pure high anion gap metabolic acidosis."
        in r["interpretation"]["clinical_report"]
    )

    check(
        "Pure HAGMA: report",
        "DELTA RATIO" in r["report"]
    )

    # =========================================
    # 7. HAGMA + NAGMA
    # =========================================

    r = ABGEngine.analyze(
        ph=7.15,
        pco2=25,
        hco3=12,
        na=140,
        cl=115
    )

    check(
        "HAGMA + NAGMA: AG high",
        r["anion_gap"]["status"] == "HIGH_ANION_GAP"
    )

    check(
        "HAGMA + NAGMA: delta status",
        r["delta_ratio"]["status"] == "HAGMA_PLUS_NAGMA"
    )

    check(
        "HAGMA + NAGMA: interpretation",
        "Mixed HAGMA + normal anion gap metabolic acidosis."
        in r["interpretation"]["clinical_report"]
    )

    # =========================================
    # 8. HAGMA + METABOLIC ALKALOSIS
    # =========================================

    r = ABGEngine.analyze(
        ph=7.50,
        pco2=40,
        hco3=30,
        na=145,
        cl=100
    )

    check(
        "HAGMA + metabolic alkalosis: AG high",
        r["anion_gap"]["status"] == "HIGH_ANION_GAP"
    )

    check(
        "HAGMA + metabolic alkalosis: delta status",
        r["delta_ratio"]["status"]
        == "HAGMA_PLUS_METABOLIC_ALKALOSIS"
    )

    check(
        "HAGMA + metabolic alkalosis: interpretation",
        "Mixed HAGMA + metabolic alkalosis."
        in r["interpretation"]["clinical_report"]
    )

    # =========================================
    # 9. TRIPLE DISORDER THROUGH FULL PIPELINE
    # =========================================

    r = ABGEngine.analyze(
        ph=7.20,
        pco2=50,
        hco3=16,
        na=145,
        cl=100
    )

    check(
        "Triple candidate: primary metabolic acidosis",
        r["primary_disorder"] == "Metabolic Acidosis"
    )

    check(
        "Triple candidate: respiratory acidosis",
        r["compensation"].status
        == "SUPERIMPOSED_RESP_ACIDOSIS"
    )

    check(
        "Triple candidate: delta ratio",
        r["delta_ratio"] is not None
    )

    check(
        "Triple candidate: triple flag is boolean",
        isinstance(
            r["triple_disorder"]["triple_disorder"],
            bool
        )
    )

    check(
        "Triple candidate: report generated",
        isinstance(r["report"], str)
        and len(r["report"]) > 0
    )

    # =========================================
    # 10. OPTIONAL ELECTROLYTES DO NOT BREAK PIPELINE
    # =========================================

    r = ABGEngine.analyze(
        ph=7.30,
        pco2=30,
        hco3=18,
        na=140,
        cl=110,
        k=4.0,
        albumin=4.0,
        lactate=2.0
    )

    check(
        "Optional parameters: analysis completes",
        isinstance(r, dict)
    )

    check(
        "Optional parameters: AG remains available",
        r["anion_gap"] is not None
    )

    check(
        "Optional parameters: report generated",
        isinstance(r["report"], str)
    )

    print()
    print("ALL INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    main()
