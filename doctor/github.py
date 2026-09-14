import os

from doctor.utils import ok, warning, error


def check_github():

    results = []

    workflow = ".github/workflows/build.yml"

    if not os.path.exists(workflow):

        results.append(
            error(
                "GitHub workflow missing"
            )
        )

        return results


    results.append(
        ok(
            "workflow found"
        )
    )


    with open(
        workflow,
        "r",
        encoding="utf-8"
    ) as f:

        content = f.read()


    checks = {
        "checkout": "actions/checkout" in content,
        "upload": "actions/upload-artifact" in content,
        "buildozer": "buildozer android debug" in content,
        "python": "python" in content,
    }


    for name, exists in checks.items():

        if exists:

            results.append(
                ok(
                    f"{name} configured"
                )
            )

        else:

            results.append(
                warning(
                    f"{name} missing"
                )
            )


    # Python version pin check
    if (
        "python-version" not in content
        and "python_version" not in content
    ):

        results.append(
            warning(
                "Python version not pinned"
            )
        )


    return results