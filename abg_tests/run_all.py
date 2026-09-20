import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = Path(__file__).resolve().parent
UI_PYTHON = ROOT / ".venv_ui" / "bin" / "python"

tests = [
    "test_core.py",
    "test_edge_cases.py",
    "test_mixed.py",
    "test_invalid_inputs.py",
    "test_boundaries.py",
    "test_compensation.py",
    "test_anion_delta.py",
    "test_triple_disorder.py",
    "test_interpretation.py",
    "test_severity.py",
    "test_report_composer.py",
    "test_integration.py",
]

gui_tests = [
    "run_gui_smoke.py",
    "run_e2e_gui_smoke.py",
]

failed = []
total_passed = 0

print("=" * 60)
print("ABG ANALYZER PRO - FULL TEST SUITE")
print("=" * 60)

# ---------------------------------------------------------
# Core / integration tests
# ---------------------------------------------------------

for test in tests:
    print(f"\n>>> Running {test}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, str(TEST_DIR / test)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="")

    passed = len(re.findall(r"^PASS:", result.stdout, re.MULTILINE))
    total_passed += passed

    if result.returncode != 0:
        failed.append(test)

    print(f"[{test}] PASS count: {passed}")


# ---------------------------------------------------------
# GUI smoke tests
# ---------------------------------------------------------

if not UI_PYTHON.exists():
    print("\n>>> GUI tests")
    print("-" * 60)
    print(f"ERROR: UI Python not found: {UI_PYTHON}")
    failed.extend(gui_tests)
else:
    for test in gui_tests:
        print(f"\n>>> Running {test}")
        print("-" * 60)

        result = subprocess.run(
            [str(UI_PYTHON), str(TEST_DIR / test)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        print(result.stdout, end="")

        if result.stderr:
            print(result.stderr, end="")

        passed = len(re.findall(r"^PASS:", result.stdout, re.MULTILINE))
        total_passed += passed

        if result.returncode != 0:
            failed.append(test)

        print(f"[{test}] PASS count: {passed}")


# ---------------------------------------------------------
# Final result
# ---------------------------------------------------------

print("\n" + "=" * 60)

if failed:
    print("TEST SUITE: FAIL")
    print(f"Total PASS: {total_passed}")
    print("Failed test files:")
    for test in failed:
        print(f"  - {test}")
else:
    print("TEST SUITE: PASS")
    print(f"Total PASS: {total_passed}")

print("=" * 60)

sys.exit(1 if failed else 0)
