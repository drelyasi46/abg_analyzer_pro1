from core.abg_engine import ABGEngine

engine = ABGEngine()

cases = [

    {
        "name": "DKA",
        "ph": 7.18,
        "pco2": 24,
        "hco3": 9,
        "na": 138,
        "cl": 98,
        "albumin": 4.0,
        "lactate": 2.0,
        "expected": [
            "Metabolic Acidosis",
            "High Anion Gap",
        ],
    },

    {
        "name": "DKA + Vomiting",
        "ph": 7.32,
        "pco2": 30,
        "hco3": 15,
        "na": 140,
        "cl": 90,
        "albumin": 4.0,
        "lactate": 2.5,
        "expected": [
            "Metabolic Acidosis",
            "Delta Ratio",
        ],
    },

]

passed = 0

for i, case in enumerate(cases, start=1):

    print("=" * 70)
    print(f"CASE {i}: {case['name']}")
    print("=" * 70)

    report = engine.analyze(
        ph=case["ph"],
        pco2=case["pco2"],
        hco3=case["hco3"],
        na=case["na"],
        cl=case["cl"],
        albumin=case["albumin"],
        lactate=case["lactate"],
    )

    print(report)

    ok = True

    for item in case["expected"]:
        if item not in report:
            ok = False

    if ok:
        print("\nPASS")
        passed += 1
    else:
        print("\nFAIL")

print("\n")
print("=" * 70)
print(f"Passed {passed} / {len(cases)}")
print("=" * 70)