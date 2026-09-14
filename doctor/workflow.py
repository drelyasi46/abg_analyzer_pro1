import os
import re


def check_workflow():

    print("\n[GITHUB WORKFLOW ANALYSIS]")

    path = ".github/workflows/build.yml"

    if not os.path.exists(path):
        print("WARNING Workflow file not found")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    checks = [
        (
            "Python version not pinned",
            r"python-version|python3",
            "Make sure Python 3.11 is explicitly used"
        ),
        (
            "Buildozer installation found",
            r"pip install.*buildozer",
            "OK"
        ),
        (
            "Cython version not pinned",
            r"cython(?!==)",
            "Pin Cython version"
        ),
        (
            "APK artifact upload missing",
            r"path:.*bin/.*apk",
            "OK"
        ),
    ]

    for name, pattern, advice in checks:

        if re.search(pattern, content, re.IGNORECASE):
            print("CHECK:", name)
            print("Advice:", advice)

    print("Workflow analysis complete")