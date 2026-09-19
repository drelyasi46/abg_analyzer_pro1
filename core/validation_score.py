from core.abg_engine import ABGEngine


engine = ABGEngine()


cases = [

    {
        "name": "DKA",

        "input": {
            "ph": 7.18,
            "pco2": 24,
            "hco3": 9,
            "na": 138,
            "cl": 98,
            "albumin": 4.0,
            "lactate": 2.0,
        },

        "checks": {

            "Primary Diagnosis": [
                "Metabolic Acidosis"
            ],

            "Compensation": [
                "Appropriate Respiratory Compensation"
            ],

            "Anion Gap": [
                "High Anion Gap"
            ],

            "Delta Ratio": [
                "Delta Ratio"
            ],

            "Mixed Disorder": [
                "No Mixed Disorder"
            ],

        }
    },


    {
        "name": "DKA + Vomiting",

        "input": {
            "ph": 7.32,
            "pco2": 30,
            "hco3": 15,
            "na": 140,
            "cl": 90,
            "albumin": 4.0,
            "lactate": 2.5,
        },

        "checks": {

            "Primary Diagnosis": [
                "Metabolic Acidosis"
            ],

            "Anion Gap": [
                "High Anion Gap"
            ],

            "Delta Ratio": [
                "Delta Ratio"
            ],

        }
    }

]


total_score = 0
total_possible = 0


for case in cases:

    print("=" * 70)
    print(case["name"])
    print("=" * 70)


    report = engine.analyze(
        **case["input"]
    )


    score = 0
    possible = 0


    for category, expected in case["checks"].items():

        possible += 1

        passed = False

        for item in expected:

            if item in report:
                passed = True


        if passed:
            score += 1
            print(f"{category:<25} 1/1")
        else:
            print(f"{category:<25} 0/1")


    print("-" * 70)

    print(
        f"CASE SCORE: {score}/{possible}"
    )


    total_score += score
    total_possible += possible



print("\n")
print("=" * 70)

print(
    f"TOTAL SCORE: {total_score}/{total_possible}"
)

print(
    f"Accuracy: {(total_score/total_possible)*100:.1f}%"
)

print("=" * 70)