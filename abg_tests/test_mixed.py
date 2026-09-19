import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.abg_engine import ABGEngine


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"PASS: {name}")


def main():

    # HAGMA + additional NAGMA
    r = ABGEngine.analyze(
        ph=7.15,
        pco2=20,
        hco3=10,
        na=140,
        cl=110
    )
    check(
        "HAGMA + NAGMA",
        r["anion_gap"]["status"] == "HIGH_ANION_GAP"
        and r["delta_ratio"]["status"] == "HAGMA_PLUS_NAGMA"
    )

    # Pure HAGMA
    r = ABGEngine.analyze(
        ph=7.20,
        pco2=25,
        hco3=16,
        na=140,
        cl=100
    )
    check(
        "Pure HAGMA",
        r["delta_ratio"]["status"] == "PURE_HAGMA"
    )

    # HAGMA + metabolic alkalosis
    r = ABGEngine.analyze(
        ph=7.45,
        pco2=40,
        hco3=30,
        na=140,
        cl=90
    )
    check(
        "HAGMA + metabolic alkalosis",
        r["anion_gap"]["status"] == "HIGH_ANION_GAP"
        and r["delta_ratio"]["status"]
        == "HAGMA_PLUS_METABOLIC_ALKALOSIS"
    )

    # Delta ratio undefined at HCO3 = 24
    r = ABGEngine.analyze(
        ph=7.40,
        pco2=40,
        hco3=24,
        na=140,
        cl=100
    )
    check(
        "Delta ratio undefined at HCO3 24",
        r["delta_ratio"] is not None
        and r["delta_ratio"]["status"] == "UNDEFINED"
    )

    # No delta ratio when anion gap is normal
    r = ABGEngine.analyze(
        ph=7.30,
        pco2=30,
        hco3=18,
        na=140,
        cl=110
    )
    check(
        "No delta ratio for normal AG",
        r["anion_gap"]["status"] == "NORMAL_ANION_GAP"
        and r["delta_ratio"] is None
    )

    print()
    print("ALL MIXED-DISORDER TESTS PASSED")


if __name__ == "__main__":
    main()
