import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import ABGApp


def main():
    app = ABGApp()

    # Build the real application UI.
    app.build()

    # Use a valid metabolic acidosis case.
    values = {
        "ph": 7.25,
        "pco2": 30.0,
        "hco3": 13.0,
        "na": 140.0,
        "k": 4.0,
        "cl": 100.0,
        "albumin": 4.0,
        "lactate": 2.0,
    }

    # Execute the same callback used by the real ANALYZE button.
    app.analyze(values)

    result_text = app.result_card.label.text

    assert result_text, "ResultCard report is empty"

    assert "metabolic acidosis" in result_text.lower(), (
        "Expected metabolic acidosis in final GUI report"
    )

    print("PASS: ABGApp.build()")
    print("PASS: ABGApp.analyze()")
    print("PASS: ABGEngine → interpretation → report")
    print("PASS: ResultCard received final report")
    print("PASS: GUI end-to-end smoke test")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
