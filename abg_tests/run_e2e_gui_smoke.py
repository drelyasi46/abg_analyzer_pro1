import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import ABGApp


CASES = [
    (
        "Normal ABG",
        {
            "ph": 7.40,
            "pco2": 40.0,
            "hco3": 24.0,
            "na": 140.0,
            "k": 4.0,
            "cl": 104.0,
            "albumin": 4.0,
            "lactate": 1.0,
        },
        "No primary acid-base disorder",
    ),
    (
        "Metabolic acidosis",
        {
            "ph": 7.25,
            "pco2": 30.0,
            "hco3": 13.0,
            "na": 140.0,
            "k": 4.0,
            "cl": 100.0,
            "albumin": 4.0,
            "lactate": 2.0,
        },
        "metabolic acidosis",
    ),
    (
        "Metabolic alkalosis",
        {
            "ph": 7.50,
            "pco2": 48.0,
            "hco3": 36.0,
            "na": 140.0,
            "k": 4.0,
            "cl": 100.0,
            "albumin": 4.0,
            "lactate": 1.0,
        },
        "metabolic alkalosis",
    ),
    (
        "Respiratory acidosis",
        {
            "ph": 7.30,
            "pco2": 60.0,
            "hco3": 29.0,
            "na": 140.0,
            "k": 4.0,
            "cl": 100.0,
            "albumin": 4.0,
            "lactate": 1.0,
        },
        "respiratory acidosis",
    ),
    (
        "Respiratory alkalosis",
        {
            "ph": 7.50,
            "pco2": 25.0,
            "hco3": 19.0,
            "na": 140.0,
            "k": 4.0,
            "cl": 100.0,
            "albumin": 4.0,
            "lactate": 1.0,
        },
        "respiratory alkalosis",
    ),
    (
        "HAGMA",
        {
            "ph": 7.25,
            "pco2": 25.0,
            "hco3": 12.0,
            "na": 140.0,
            "k": 4.0,
            "cl": 90.0,
            "albumin": 4.0,
            "lactate": 5.0,
        },
        "high anion gap metabolic acidosis",
    ),
]


def main():
    app = ABGApp()
    app.build()

    passed = 0

    for name, values, expected in CASES:
        app.analyze(values)

        result_text = app.result_card.label.text

        assert result_text, f"{name}: ResultCard report is empty"
        assert expected.lower() in result_text.lower(), (
            f"{name}: expected '{expected}' in GUI report, "
            f"got: {result_text!r}"
        )

        print(f"PASS: {name}")
        passed += 1

    print(f"PASS: {passed} GUI clinical scenarios")
    print("PASS: GUI end-to-end clinical smoke test")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
