from core.abg_engine import ABGEngine
import test_cases

engine = ABGEngine()


def test_all_cases():

    failed = []

    for case in test_cases.cases:

        result = engine.analyze(**case["input"])

        primary = result.get("primary_disorder", "")

        mixed = result.get("triple_disorder", {}).get(
            "mixed_disorder",
            False
        )

        ag_status = result.get("anion_gap", {}).get("status", "")

        expected_primary = case["expected"].get("primary", "")
        expected_ag = case["expected"].get("ag", "")

        if expected_primary == "Normal Acid-Base Status":
            expected_primary = "Normal"

        if expected_ag == "Normal":
            expected_ag = "NORMAL_ANION_GAP"

        if expected_ag == "High":
            expected_ag = "HIGH_ANION_GAP"

        if expected_primary == "Mixed":

            if not mixed:
                failed.append(
                    f"{case['name']}: Mixed disorder not detected"
                )

        elif expected_primary and expected_primary not in primary:
            failed.append(
                f"{case['name']} PRIMARY: {primary} != {expected_primary}"
            )

        if expected_ag and ag_status != expected_ag:
            failed.append(
                f"{case['name']} AG: {ag_status} != {expected_ag}"
            )

    assert not failed, "\n".join(failed)
