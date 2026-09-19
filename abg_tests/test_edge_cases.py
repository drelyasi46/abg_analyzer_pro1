import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.abg_engine import ABGEngine


def check_no_crash(name, **kwargs):
    try:
        result = ABGEngine.analyze(**kwargs)
        assert isinstance(result, dict)
        print(f"PASS: {name}")
    except Exception as e:
        print(f"FAIL: {name} -> {type(e).__name__}: {e}")
        raise


def main():
    check_no_crash(
        "Normal borderline values",
        ph=7.35,
        pco2=45,
        hco3=22
    )

    check_no_crash(
        "Upper normal borderline values",
        ph=7.45,
        pco2=45,
        hco3=26
    )

    check_no_crash(
        "Low pH",
        ph=6.80,
        pco2=80,
        hco3=10
    )

    check_no_crash(
        "High pH",
        ph=7.80,
        pco2=20,
        hco3=40
    )

    check_no_crash(
        "Very high PCO2",
        ph=7.10,
        pco2=100,
        hco3=20
    )

    check_no_crash(
        "Very low PCO2",
        ph=7.70,
        pco2=10,
        hco3=15
    )

    check_no_crash(
        "High anion gap with HCO3 below normal",
        ph=7.20,
        pco2=25,
        hco3=12,
        na=140,
        cl=100
    )

    check_no_crash(
        "High anion gap with HCO3 above normal",
        ph=7.45,
        pco2=40,
        hco3=30,
        na=140,
        cl=90
    )

    check_no_crash(
        "Without electrolytes",
        ph=7.25,
        pco2=30,
        hco3=14
    )

    check_no_crash(
        "With potassium and albumin",
        ph=7.25,
        pco2=30,
        hco3=14,
        na=140,
        cl=100,
        k=4.0,
        albumin=4.0,
        lactate=3.0
    )

    print()
    print("ALL EDGE CASE TESTS PASSED")


if __name__ == "__main__":
    main()
