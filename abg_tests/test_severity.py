import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.severity_engine import SeverityEngine


def comp(status):
    return SimpleNamespace(status=status)


def test(name, **kwargs):
    expected = kwargs.pop("expected")
    result = SeverityEngine.evaluate(**kwargs)

    assert result == expected, (
        f"\n{name}\n"
        f"Expected: {expected}\n"
        f"Got:      {result}"
    )

    print(f"PASS: {name}")


def main():

    # =========================================
    # BASELINE
    # =========================================

    test(
        "Normal ABG = LOW",
        ph=7.40,
        hco3=24,
        pco2=40,
        expected={
            "severity": "LOW",
            "score": 0,
            "alerts": []
        }
    )

    # =========================================
    # pH THRESHOLDS
    # =========================================

    test(
        "pH 7.30 adds 0 points at boundary",
        ph=7.30,
        expected={
            "severity": "LOW",
            "score": 0,
            "alerts": []
        }
    )

    test(
        "pH below 7.30 = 1 point",
        ph=7.29,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "pH 7.20 boundary = 1 point",
        ph=7.20,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "pH below 7.20 = severe",
        ph=7.19,
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Severe acid-base disturbance."]
        }
    )

    test(
        "pH 7.10 boundary = severe",
        ph=7.10,
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Severe acid-base disturbance."]
        }
    )

    test(
        "pH below 7.10 = critical",
        ph=7.09,
        expected={
            "severity": "MODERATE",
            "score": 3,
            "alerts": ["Life-threatening pH."]
        }
    )

    test(
        "pH above 7.50 = 1 point",
        ph=7.51,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "pH above 7.55 = severe",
        ph=7.56,
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Severe acid-base disturbance."]
        }
    )

    test(
        "pH above 7.60 = life-threatening",
        ph=7.61,
        expected={
            "severity": "MODERATE",
            "score": 3,
            "alerts": ["Life-threatening pH."]
        }
    )

    # =========================================
    # HCO3
    # =========================================

    test(
        "HCO3 15 boundary",
        hco3=15,
        expected={
            "severity": "LOW",
            "score": 0,
            "alerts": []
        }
    )

    test(
        "HCO3 below 15",
        hco3=14,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "HCO3 10 boundary",
        hco3=10,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "HCO3 below 10",
        hco3=9,
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Severe metabolic acidosis."]
        }
    )

    # =========================================
    # PCO2
    # =========================================

    test(
        "PCO2 70 boundary",
        pco2=70,
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Severe hypercapnia."]
        }
    )

    test(
        "PCO2 below 70 but above 20",
        pco2=69,
        expected={
            "severity": "LOW",
            "score": 0,
            "alerts": []
        }
    )

    test(
        "PCO2 20 boundary",
        pco2=20,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": ["Marked hypocapnia."]
        }
    )

    test(
        "PCO2 below 20",
        pco2=19,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": ["Marked hypocapnia."]
        }
    )

    # =========================================
    # COMPENSATION
    # =========================================

    test(
        "Superimposed respiratory acidosis",
        compensation=comp("SUPERIMPOSED_RESP_ACIDOSIS"),
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Concurrent respiratory acidosis."]
        }
    )

    test(
        "Superimposed respiratory alkalosis",
        compensation=comp("SUPERIMPOSED_RESP_ALKALOSIS"),
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Concurrent respiratory alkalosis."]
        }
    )

    test(
        "Superimposed metabolic acidosis",
        compensation=comp("SUPERIMPOSED_METABOLIC_ACIDOSIS"),
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Concurrent metabolic acidosis."]
        }
    )

    test(
        "Superimposed metabolic alkalosis",
        compensation=comp("SUPERIMPOSED_METABOLIC_ALKALOSIS"),
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Concurrent metabolic alkalosis."]
        }
    )

    # =========================================
    # ANION GAP
    # =========================================

    test(
        "High AG with metabolic acidosis",
        primary_disorder="Metabolic Acidosis",
        anion_gap={"status": "HIGH_ANION_GAP"},
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": ["High anion gap present."]
        }
    )

    test(
        "High AG without metabolic acidosis",
        primary_disorder="Normal",
        anion_gap={"status": "HIGH_ANION_GAP"},
        expected={
            "severity": "LOW",
            "score": 0,
            "alerts": []
        }
    )

    # =========================================
    # DELTA RATIO
    # =========================================

    test(
        "HAGMA plus NAGMA",
        delta_ratio={"status": "HAGMA_PLUS_NAGMA"},
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "HAGMA plus metabolic alkalosis",
        delta_ratio={"status": "HAGMA_PLUS_METABOLIC_ALKALOSIS"},
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    # =========================================
    # TRIPLE DISORDER
    # =========================================

    test(
        "Triple disorder",
        triple={"triple_disorder": True},
        expected={
            "severity": "MODERATE",
            "score": 3,
            "alerts": ["Triple acid-base disorder."]
        }
    )

    # =========================================
    # SEVERITY BOUNDARIES
    # =========================================

    test(
        "Score 1 = LOW",
        ph=7.29,
        expected={
            "severity": "LOW",
            "score": 1,
            "alerts": []
        }
    )

    test(
        "Score 2 = MODERATE",
        compensation=comp("SUPERIMPOSED_RESP_ACIDOSIS"),
        expected={
            "severity": "MODERATE",
            "score": 2,
            "alerts": ["Concurrent respiratory acidosis."]
        }
    )

    test(
        "Score 4 = MODERATE",
        ph=7.19,
        hco3=9,
        expected={
            "severity": "MODERATE",
            "score": 4,
            "alerts": [
                "Severe acid-base disturbance.",
                "Severe metabolic acidosis."
            ]
        }
    )

    test(
        "Score 5 exactly = HIGH",
        ph=7.19,
        hco3=9,
        pco2=70,
        expected={
            "severity": "HIGH",
            "score": 6,
            "alerts": [
                "Severe acid-base disturbance.",
                "Severe metabolic acidosis.",
                "Severe hypercapnia."
            ]
        }
    )

    test(
        "Score 8 = CRITICAL",
        ph=7.09,
        hco3=9,
        pco2=70,
        triple={"triple_disorder": True},
        expected={
            "severity": "CRITICAL",
            "score": 10,
            "alerts": [
                "Life-threatening pH.",
                "Severe metabolic acidosis.",
                "Severe hypercapnia.",
                "Triple acid-base disorder."
            ]
        }
    )

    print("\nAll severity tests passed.")


if __name__ == "__main__":
    main()
