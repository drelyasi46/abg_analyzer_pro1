from core.abg_engine import ABGEngine

CASES = [
    ("Normal ABG", 7.40, 40, 24, 140, 104, "No primary acid-base disorder"),
    ("Metabolic acidosis", 7.25, 30, 13, 140, 100, "metabolic acidosis"),
    ("Metabolic alkalosis", 7.50, 48, 36, 140, 100, "metabolic alkalosis"),
    ("Respiratory acidosis", 7.30, 60, 29, 140, 100, "respiratory acidosis"),
    ("Respiratory alkalosis", 7.50, 25, 19, 140, 100, "respiratory alkalosis"),
    ("HAGMA", 7.25, 25, 12, 140, 90, "high anion gap metabolic acidosis"),
]

def run():
    engine = ABGEngine()
    passed = 0

    for name, ph, pco2, hco3, na, cl, expected in CASES:
        result = engine.analyze(
            ph=ph,
            pco2=pco2,
            hco3=hco3,
            na=na,
            cl=cl,
            k=4,
            albumin=4,
            lactate=1,
        )
        report = str(result["report"])

        if expected.lower() not in report.lower():
            raise AssertionError(
                f"{name}: expected '{expected}', got {report!r}"
            )

        print(f"ANDROID_TEST_PASS: {name}")
        passed += 1

    print(f"ANDROID_TEST_PASS_COUNT: {passed}")
    return passed

if __name__ == "__main__":
    run()
