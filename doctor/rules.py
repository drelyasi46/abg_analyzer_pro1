# doctor/rules.py

RULES = {

    # Critical build problems
    "Python 3.14 detected": -30,
    "Cython config.pxi failure": -25,
    "Network download failure": -20,
    "workflow missing": -30,
    "buildozer.spec missing": -30,

    # Important warnings
    "Buildozer not installed": -5,
    "Python version not pinned": -5,
    "python-for-android-master found": -5,

    # Development artifacts
    ".buildozer found": 0,
    "bin found": 0,
    ".venv found": 0,
    "venv found": 0,
    "venv_buildozer found": 0,
    "venv_win found": 0,
}


def get_penalty(message):

    for key, value in RULES.items():

        if key in message:
            return value

    return 0