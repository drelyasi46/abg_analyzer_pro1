import os
import platform
import subprocess

from doctor.utils import ok, warning, error


def check_android():

    results = []

    # OS check
    system = platform.system()

    if system == "Windows":
        results.append(
            warning(
                "Running on Windows - use WSL/Linux/GitHub Actions for Buildozer"
            )
        )
    else:
        results.append(
            ok(
                "Linux environment detected"
            )
        )


    # Buildozer check
    try:
        result = subprocess.run(
            ["buildozer", "--version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            results.append(
                ok(
                    "Buildozer installed: "
                    + result.stdout.strip()
                )
            )
        else:
            results.append(
                warning(
                    "Buildozer returned error"
                )
            )

    except FileNotFoundError:

        results.append(
            warning(
                "Buildozer not installed"
            )
        )


    # python-for-android
    if os.path.exists("python-for-android-master"):

        results.append(
            warning(
                "python-for-android-master found (possible conflict)"
            )
        )

    else:

        results.append(
            ok(
                "No external python-for-android found"
            )
        )


    # buildozer.spec
    if os.path.exists("buildozer.spec"):

        results.append(
            ok(
                "buildozer.spec found"
            )
        )

    else:

        results.append(
            error(
                "buildozer.spec missing"
            )
        )


    return results