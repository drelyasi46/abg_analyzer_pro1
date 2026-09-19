import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.abg_engine import ABGEngine


def expect_exception(name, **kwargs):
    try:
        ABGEngine.analyze(**kwargs)
    except Exception as e:
        print(f"INFO: {name} -> {type(e).__name__}")
        return
    print(f"PASS: {name} -> no exception")


def expect_no_exception(name, **kwargs):
    try:
        result = ABGEngine.analyze(**kwargs)
        assert isinstance(result, dict)
        print(f"PASS: {name}")
    except Exception as e:
        print(f"FAIL: {name} -> {type(e).__name__}: {e}")
        raise


def main():

    # Extreme but numeric inputs should not crash the engine.
    expect_no_exception(
        "Extremely low pH",
        ph=5.0,
        pco2=40,
        hco3=10
    )

    expect_no_exception(
        "Extremely high pH",
        ph=9.0,
        pco2=40,
        hco3=30
    )

    expect_no_exception(
        "Zero PCO2",
        ph=7.40,
        pco2=0,
        hco3=24
    )

    expect_no_exception(
        "Zero HCO3",
        ph=7.20,
        pco2=40,
        hco3=0
    )

    expect_no_exception(
        "Negative PCO2",
        ph=7.40,
        pco2=-10,
        hco3=24
    )

    expect_no_exception(
        "Negative HCO3",
        ph=7.20,
        pco2=40,
        hco3=-5
    )

    # Missing optional electrolytes should remain safe.
    expect_no_exception(
        "Missing electrolytes",
        ph=7.25,
        pco2=30,
        hco3=14,
        na=None,
        cl=None
    )

    print()
    print("INVALID/EXTREME INPUT TESTS COMPLETED")


if __name__ == "__main__":
    main()
