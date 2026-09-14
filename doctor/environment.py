import sys
import shutil

from doctor.utils import ok, warning


def check_environment():

    results = []

    version = sys.version_info

    results.append(
        ok(
            f"Python {version.major}.{version.minor}"
        )
    )

    if shutil.which("git"):
        results.append(
            ok("Git installed")
        )
    else:
        results.append(
            warning("Git missing")
        )

    if shutil.which("buildozer"):
        results.append(
            ok("Buildozer installed")
        )
    else:
        results.append(
            warning("Buildozer not installed")
        )

    return results