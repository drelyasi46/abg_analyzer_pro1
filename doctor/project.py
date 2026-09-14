import os

from doctor.utils import ok, warning, error


def check_project():

    results = []

    folders = [
        ".buildozer",
        "bin",
        "python-for-android-master",
        ".venv",
        "venv",
        "venv_buildozer",
        "venv_win"
    ]

    for folder in folders:

        if os.path.exists(folder):

            results.append(
                warning(
                    f"{folder} found"
                )
            )


    required = [
        "main.py",
        "main.kv",
        "buildozer.spec",
        "requirements.txt"
    ]

    for file in required:

        if os.path.exists(file):

            results.append(
                ok(
                    f"{file} found"
                )
            )

        else:

            results.append(
                error(
                    f"{file} missing"
                )
            )


    return results