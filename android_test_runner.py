import os
import sys

from android_test_mode import run

try:
    count = run()
    print(f"ANDROID_AUTO_TEST_RESULT: PASS ({count})")
except Exception as e:
    print(f"ANDROID_AUTO_TEST_RESULT: FAIL ({type(e).__name__}: {e})")
    sys.exit(1)
