import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kivymd.app import MDApp
from widgets.result_card import ResultCard


class SmokeApp(MDApp):
    def build(self):
        return ResultCard()


def main():
    app = SmokeApp()

    card = app.build()

    assert card.label.text == "Enter ABG values and press ANALYZE ABG.", (
        "Initial ResultCard text is incorrect"
    )

    report = [
        "Primary metabolic acidosis.",
        "High anion gap metabolic acidosis (HAGMA).",
    ]

    card.set_report(report)

    assert "Primary metabolic acidosis." in card.label.text
    assert "High anion gap metabolic acidosis (HAGMA)." in card.label.text

    print("PASS: ResultCard initialization")
    print("PASS: ResultCard.set_report()")
    print("PASS: GUI smoke test")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
