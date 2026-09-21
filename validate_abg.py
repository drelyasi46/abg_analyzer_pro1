import ast
from pathlib import Path

from core.abg_engine import ABGEngine


source = Path("test_cases.py").read_text(encoding="utf-8-sig")
tree = ast.parse(source)

cases = None

for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "cases":
                cases = ast.literal_eval(node.value)
                break

if cases is None:
    raise RuntimeError("Could not find 'cases' in test_cases.py")


passed = 0
failed = 0


for i, case in enumerate(cases, start=1):

    print()
    print("=" * 70)
    print(f"CASE {i}: {case['name']}")
    print("=" * 70)

    result = ABGEngine.analyze(**case["input"])
    expected = case["expected"]

    primary = result["primary_disorder"]
    compensation = result["compensation"]
    anion_gap = result["anion_gap"]
    delta_ratio = result["delta_ratio"]
    triple_result = result["triple_disorder"]

    compensation_status = (
        compensation.status
        if compensation is not None
        else None
    )

    ag_status = (
        anion_gap.get("status")
        if anion_gap is not None
        else None
    )

    delta_status = (
        delta_ratio.get("status")
        if delta_ratio is not None
        else None
    )

    mixed = triple_result.get("mixed_disorder", False)
    triple = triple_result.get("triple_disorder", False)
    disorders = triple_result.get("disorders", [])

    print(f"Primary       : {primary}")
    print(f"Compensation  : {compensation_status}")
    print(f"Anion Gap     : {ag_status}")
    print(f"Delta Ratio   : {delta_status}")
    print(f"Mixed         : {mixed}")
    print(f"Triple        : {triple}")
    print(f"Disorders     : {disorders}")

    ok = True
    errors = []

    # --------------------------------------------------------
    # Primary disorder
    # --------------------------------------------------------

    if "primary" in expected:

        expected_primary = expected["primary"]

        if expected_primary == "Normal Acid-Base Status":

            if primary != "Normal":
                ok = False
                errors.append(
                    f"Expected Normal, got {primary}"
                )

        elif expected_primary == "Mixed":

            if not mixed:
                ok = False
                errors.append(
                    "Expected mixed_disorder=True"
                )

        else:

            if primary != expected_primary:
                ok = False
                errors.append(
                    f"Expected {expected_primary}, got {primary}"
                )

    # --------------------------------------------------------
    # Anion gap
    # --------------------------------------------------------

    if "ag" in expected:

        expected_ag = expected["ag"]

        if expected_ag == "High":

            if ag_status != "HIGH_ANION_GAP":
                ok = False
                errors.append(
                    f"Expected HIGH_ANION_GAP, got {ag_status}"
                )

        elif expected_ag == "Normal":

            if ag_status != "NORMAL_ANION_GAP":
                ok = False
                errors.append(
                    f"Expected NORMAL_ANION_GAP, got {ag_status}"
                )

    # --------------------------------------------------------
    # Triple case
    # --------------------------------------------------------

    if case["name"] == "Triple Disorder":

        if triple:
            print("Triple validation : PASS")
        else:
            print(
                "Triple validation : NOT APPLICABLE "
                "(current input has only 2 components)"
            )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    if ok:

        passed += 1
        print()
        print("PASS")

    else:

        failed += 1
        print()
        print("FAIL")

        for error in errors:
            print(f"  - {error}")


print()
print("=" * 70)
print("ABG ENGINE VALIDATION")
print("=" * 70)
print(f"Passed : {passed}")
print(f"Failed : {failed}")
print(f"Total  : {passed + failed}")

if failed == 0:
    print()
    print("ALL VALIDATIONS PASSED")
else:
    print()
    print("VALIDATION COMPLETED WITH FAILURES")
