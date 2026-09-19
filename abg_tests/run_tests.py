import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = Path(__file__).resolve().parent / "test_core.py"

result = subprocess.run(
    [sys.executable, str(TEST_FILE)],
    cwd=ROOT,
    text=True
)

if result.returncode == 0:
    print("\n================================")
    print("ABG ANALYZER TEST SUITE: PASS")
    print("================================")
else:
    print("\n================================")
    print("ABG ANALYZER TEST SUITE: FAIL")
    print("================================")

sys.exit(result.returncode)
