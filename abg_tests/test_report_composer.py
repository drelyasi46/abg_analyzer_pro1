import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.report_composer import ReportComposer


def comp():
    return SimpleNamespace(
        expected=24.0,
        low=22.0,
        high=26.0,
        measured=24.0,
        message="Compensation appropriate."
    )


def test(name, expected, **kwargs):
    result = ReportComposer.compose(**kwargs)

    assert result == expected, (
        f"\n{name}\n"
        f"Expected:\n{expected!r}\n"
        f"Got:\n{result!r}"
    )

    print(f"PASS: {name}")


def main():

    # =========================================
    # EMPTY REPORT
    # =========================================

    test(
        "Empty report",
        "ABG ANALYZER PRO"
    )

    # =========================================
    # INTERPRETATION
    # =========================================

    test(
        "Interpretation only",
        """ABG ANALYZER PRO

CLINICAL INTERPRETATION

Primary metabolic acidosis.""",
        interpretation={
            "clinical_report": [
                "Primary metabolic acidosis."
            ]
        }
    )

    # =========================================
    # COMPENSATION
    # =========================================

    test(
        "Compensation section",
        """ABG ANALYZER PRO

COMPENSATION

Expected: 24.0
Acceptable range: 22.0 - 26.0
Measured: 24.0
Interpretation: Compensation appropriate.""",
        compensation=comp()
    )

    # =========================================
    # ANION GAP
    # =========================================

    test(
        "Anion gap section",
        """ABG ANALYZER PRO

ANION GAP

Anion gap: 18 mEq/L
Elevated anion gap.""",
        anion_gap={
            "anion_gap": 18,
            "message": "Elevated anion gap."
        }
    )

    # =========================================
    # DELTA RATIO
    # =========================================

    test(
        "Delta ratio section",
        """ABG ANALYZER PRO

DELTA RATIO

Delta ratio: 1.2
Pure high anion gap metabolic acidosis.""",
        delta_ratio={
            "delta_ratio": 1.2,
            "message": "Pure high anion gap metabolic acidosis."
        }
    )

    # =========================================
    # TRIPLE DISORDER
    # =========================================

    test(
        "Triple disorder section",
        """ABG ANALYZER PRO

TRIPLE DISORDER

Metabolic Acidosis
Respiratory Acidosis
Metabolic Alkalosis""",
        triple={
            "triple_disorder": True,
            "disorders": [
                "Metabolic Acidosis",
                "Respiratory Acidosis",
                "Metabolic Alkalosis"
            ]
        }
    )

    # =========================================
    # SEVERITY WITHOUT ALERTS
    # =========================================

    test(
        "Severity without alerts",
        """ABG ANALYZER PRO

SEVERITY

Severity: LOW
Score: 0""",
        severity={
            "severity": "LOW",
            "score": 0,
            "alerts": []
        }
    )

    # =========================================
    # SEVERITY WITH ALERTS
    # =========================================

    test(
        "Severity with alerts",
        """ABG ANALYZER PRO

SEVERITY

Severity: HIGH
Score: 6

CLINICAL ALERTS

Severe acid-base disturbance.
Severe metabolic acidosis.
Severe hypercapnia.""",
        severity={
            "severity": "HIGH",
            "score": 6,
            "alerts": [
                "Severe acid-base disturbance.",
                "Severe metabolic acidosis.",
                "Severe hypercapnia."
            ]
        }
    )

    # =========================================
    # COMPLETE REPORT
    # =========================================

    test(
        "Complete report",
        """ABG ANALYZER PRO

CLINICAL INTERPRETATION

Primary metabolic acidosis.
Concurrent respiratory acidosis.
High anion gap metabolic acidosis (HAGMA).
Pure high anion gap metabolic acidosis.
Triple acid-base disorder detected.

COMPENSATION

Expected: 12.0
Acceptable range: 10.0 - 14.0
Measured: 18.0
Interpretation: Superimposed respiratory acidosis.

ANION GAP

Anion gap: 24 mEq/L
Elevated anion gap.

DELTA RATIO

Delta ratio: 1.5
Pure high anion gap metabolic acidosis.

TRIPLE DISORDER

Metabolic Acidosis
Respiratory Acidosis
Metabolic Alkalosis

SEVERITY

Severity: CRITICAL
Score: 10

CLINICAL ALERTS

Severe acid-base disturbance.
Severe metabolic acidosis.
Severe hypercapnia.
Triple acid-base disorder.""",
        interpretation={
            "clinical_report": [
                "Primary metabolic acidosis.",
                "Concurrent respiratory acidosis.",
                "High anion gap metabolic acidosis (HAGMA).",
                "Pure high anion gap metabolic acidosis.",
                "Triple acid-base disorder detected."
            ]
        },
        compensation=SimpleNamespace(
            expected=12.0,
            low=10.0,
            high=14.0,
            measured=18.0,
            message="Superimposed respiratory acidosis."
        ),
        anion_gap={
            "anion_gap": 24,
            "message": "Elevated anion gap."
        },
        delta_ratio={
            "delta_ratio": 1.5,
            "message": "Pure high anion gap metabolic acidosis."
        },
        triple={
            "triple_disorder": True,
            "disorders": [
                "Metabolic Acidosis",
                "Respiratory Acidosis",
                "Metabolic Alkalosis"
            ]
        },
        severity={
            "severity": "CRITICAL",
            "score": 10,
            "alerts": [
                "Severe acid-base disturbance.",
                "Severe metabolic acidosis.",
                "Severe hypercapnia.",
                "Triple acid-base disorder."
            ]
        }
    )

    print("\nAll report composer tests passed.")


if __name__ == "__main__":
    main()
