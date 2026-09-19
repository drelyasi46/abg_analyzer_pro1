import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = Path(__file__).resolve().parent

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

failed = []
total_passed = 0

print("=" * 60)
print("ABG ANALYZER PRO - FULL TEST SUITE")
print("=" * 60)

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

print("\n" + "=" * 60)

if failed:
    print("TEST SUITE: FAIL")
    print(f"Passed tests before/alongside failures: {total_passed}")
    print("Failed test files:")
    for test in failed:
        print(f"  - {test}")
else:
    print("TEST SUITE: PASS")
    print(f"Total PASS: {total_passed}")

print("=" * 60)

sys.exit(1 if failed else 0)
