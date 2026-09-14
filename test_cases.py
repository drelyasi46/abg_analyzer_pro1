from core.abg_engine import ABGEngine

engine = ABGEngine()

cases = [

    # =====================================================
    # CASE 1
    # =====================================================

    {
        "name": "Normal ABG",

        "input": {
            "ph": 7.40,
            "pco2": 40,
            "hco3": 24,
            "na": 140,
            "k": 4,
            "cl": 104,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Normal Acid-Base Status",
            "ag": "Normal",
        }
    },

    # =====================================================
    # CASE 2
    # =====================================================

    {
        "name": "High AG Metabolic Acidosis (DKA)",

        "input": {
            "ph": 7.18,
            "pco2": 24,
            "hco3": 9,
            "na": 136,
            "k": 5.8,
            "cl": 98,
            "albumin": 4,
            "lactate": 2.2,
        },

        "expected": {
            "primary": "Metabolic Acidosis",
            "ag": "High",
        }
    },

    # =====================================================
    # CASE 3
    # =====================================================

    {
        "name": "Normal AG Metabolic Acidosis",

        "input": {
            "ph": 7.28,
            "pco2": 30,
            "hco3": 14,
            "na": 140,
            "k": 4,
            "cl": 116,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Metabolic Acidosis",
            "ag": "Normal",
        }
    },

    # =====================================================
    # CASE 4
    # =====================================================

    {
        "name": "Acute Respiratory Acidosis",

        "input": {
            "ph": 7.25,
            "pco2": 60,
            "hco3": 26,
            "na": 140,
            "k": 4,
            "cl": 102,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Respiratory Acidosis",
        }
    },

    # =====================================================
    # CASE 5
    # =====================================================

    {
        "name": "Chronic Respiratory Acidosis",

        "input": {
            "ph": 7.37,
            "pco2": 60,
            "hco3": 34,
            "na": 140,
            "k": 4,
            "cl": 98,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Respiratory Acidosis",
        }
    },

    # =====================================================
    # CASE 6
    # =====================================================

    {
        "name": "Acute Respiratory Alkalosis",

        "input": {
            "ph": 7.55,
            "pco2": 25,
            "hco3": 21,
            "na": 140,
            "k": 4,
            "cl": 104,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Respiratory Alkalosis",
        }
    },
        # =====================================================
    # CASE 7
    # =====================================================

    {
        "name": "Chronic Respiratory Alkalosis",

        "input": {
            "ph": 7.46,
            "pco2": 25,
            "hco3": 18,
            "na": 140,
            "k": 4,
            "cl": 106,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Respiratory Alkalosis",
        }
    },

    # =====================================================
    # CASE 8
    # =====================================================

    {
        "name": "Metabolic Alkalosis",

        "input": {
            "ph": 7.52,
            "pco2": 48,
            "hco3": 38,
            "na": 140,
            "k": 3,
            "cl": 92,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Metabolic Alkalosis",
        }
    },

    # =====================================================
    # CASE 9
    # =====================================================

    {
        "name": "Mixed Respiratory + Metabolic Acidosis",

        "input": {
            "ph": 7.10,
            "pco2": 60,
            "hco3": 18,
            "na": 140,
            "k": 5,
            "cl": 100,
            "albumin": 4,
            "lactate": 3,
        },

        "expected": {
            "primary": "Mixed",
        }
    },

    # =====================================================
    # CASE 10
    # =====================================================

    {
        "name": "Severe Lactic Acidosis",

        "input": {
            "ph": 7.05,
            "pco2": 20,
            "hco3": 6,
            "na": 140,
            "k": 5,
            "cl": 98,
            "albumin": 4,
            "lactate": 8,
        },

        "expected": {
            "primary": "Metabolic Acidosis",
            "ag": "High",
        }
    },

    # =====================================================
    # CASE 11
    # =====================================================

    {
        "name": "Uremic Metabolic Acidosis",

        "input": {
            "ph": 7.22,
            "pco2": 28,
            "hco3": 12,
            "na": 138,
            "k": 5.9,
            "cl": 100,
            "albumin": 4,
            "lactate": 1.8,
        },

        "expected": {
            "primary": "Metabolic Acidosis",
            "ag": "High",
        }
    },

    # =====================================================
    # CASE 12
    # =====================================================

    {
        "name": "Persistent Vomiting",

        "input": {
            "ph": 7.55,
            "pco2": 48,
            "hco3": 40,
            "na": 140,
            "k": 2.8,
            "cl": 88,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Metabolic Alkalosis",
        }
    },
        # =====================================================
    # CASE 13
    # =====================================================

    {
        "name": "Respiratory + Metabolic Acidosis",

        "input": {
            "ph": 7.08,
            "pco2": 65,
            "hco3": 18,
            "na": 140,
            "k": 5.4,
            "cl": 100,
            "albumin": 4,
            "lactate": 3,
        },

        "expected": {
            "primary": "Mixed",
        }
    },

    # =====================================================
    # CASE 14
    # =====================================================

    {
        "name": "Respiratory + Metabolic Alkalosis",

        "input": {
            "ph": 7.60,
            "pco2": 28,
            "hco3": 32,
            "na": 140,
            "k": 2.9,
            "cl": 92,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Mixed",
        }
    },

    # =====================================================
    # CASE 15
    # =====================================================

    {
        "name": "COPD with Vomiting",

        "input": {
            "ph": 7.41,
            "pco2": 65,
            "hco3": 40,
            "na": 140,
            "k": 2.8,
            "cl": 88,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Respiratory Acidosis",
        }
    },

    # =====================================================
    # CASE 16
    # =====================================================

    {
        "name": "DKA + Respiratory Failure",

        "input": {
            "ph": 7.05,
            "pco2": 45,
            "hco3": 12,
            "na": 138,
            "k": 6.2,
            "cl": 98,
            "albumin": 4,
            "lactate": 3,
        },

        "expected": {
            "primary": "Metabolic Acidosis",
            "ag": "High",
        }
    },

    # =====================================================
    # CASE 17
    # =====================================================

    {
        "name": "Salicylate Poisoning",

        "input": {
            "ph": 7.46,
            "pco2": 20,
            "hco3": 14,
            "na": 140,
            "k": 4.2,
            "cl": 100,
            "albumin": 4,
            "lactate": 2,
        },

        "expected": {
            "primary": "Mixed",
            "ag": "High",
        }
    },

    # =====================================================
    # CASE 18
    # =====================================================

    {
        "name": "Septic Shock",

        "input": {
            "ph": 7.18,
            "pco2": 24,
            "hco3": 9,
            "na": 140,
            "k": 4.5,
            "cl": 100,
            "albumin": 4,
            "lactate": 9,
        },

        "expected": {
            "primary": "Metabolic Acidosis",
            "ag": "High",
        }
    },
        # =====================================================
    # CASE 19
    # =====================================================

    {
        "name": "Triple Disorder",

        "input": {
            "ph": 7.40,
            "pco2": 60,
            "hco3": 36,
            "na": 140,
            "k": 4.2,
            "cl": 95,
            "albumin": 4,
            "lactate": 3,
        },

        "expected": {
            "primary": "Respiratory Acidosis",
        }
    },

    # =====================================================
    # CASE 20
    # =====================================================

    {
        "name": "Severe COPD",

        "input": {
            "ph": 7.36,
            "pco2": 70,
            "hco3": 38,
            "na": 140,
            "k": 4,
            "cl": 98,
            "albumin": 4,
            "lactate": 1,
        },

        "expected": {
            "primary": "Respiratory Acidosis",
        }
    },

    # =====================================================
    # CASE 21
    # =====================================================

    {
        "name": "Pulmonary Embolism",

        "input": {
            "ph": 7.52,
            "pco2": 27,
            "hco3": 21,
            "na": 140,
            "k": 4,
            "cl": 104,
            "albumin": 4,
            "lactate": 2,
        },

        "expected": {
            "primary": "Respiratory Alkalosis",
        }
    },

    # =====================================================
    # CASE 22
    # =====================================================

    {
        "name": "Cardiac Arrest",

        "input": {
            "ph": 6.95,
            "pco2": 70,
            "hco3": 14,
            "na": 142,
            "k": 6,
            "cl": 100,
            "albumin": 4,
            "lactate": 12,
        },

        "expected": {
            "primary": "Mixed",
        }
    },

]
print("\n" + "=" * 70)

passed = 0
failed = 0

for i, case in enumerate(cases, start=1):

    print("\n" + "=" * 70)
    print(f"CASE {i}: {case['name']}")
    print("=" * 70)

    report = engine.analyze(**case["input"])
    report_text = "\n".join(report)

    print(report_text)

    ok = True
    expected = case["expected"]

    if "primary" in expected:
        if expected["primary"] not in report_text:
            ok = False
            print(f"\n❌ Expected Primary: {expected['primary']}")

    if "ag" in expected:
        expected_ag = (
            "High Anion Gap"
            if expected["ag"] == "High"
            else "Normal Anion Gap"
        )

        if expected_ag not in report_text:
            ok = False
            print(f"\n❌ Expected: {expected_ag}")

    if ok:
        passed += 1
        print("\n✅ PASS")
    else:
        failed += 1
        print("\n❌ FAIL")

print("\n" + "=" * 70)
print("ABG ENGINE VALIDATION")
print("=" * 70)
print(f"Passed : {passed}")
print(f"Failed : {failed}")
print(f"Total  : {passed + failed}")