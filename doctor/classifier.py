def classify(message):

    # اطلاعات محیط توسعه، مشکل Build نیستند
    info_patterns = [
        ".buildozer found",
        "bin found",
        ".venv found",
        "venv found",
        "venv_buildozer found",
        "venv_win found",
        "Running on Windows"
    ]

    for pattern in info_patterns:
        if pattern in message:
            return "INFO"


    # خطاهای واقعی Build
    error_patterns = [
        "Python 3.14",
        "workflow missing",
        "buildozer.spec missing",
        "Cython config.pxi",
        "Network download failure"
    ]

    for pattern in error_patterns:
        if pattern in message:
            return "ERROR"


    # هشدارهای مهم
    warning_patterns = [
        "Buildozer not installed",
        "Python version not pinned",
        "python-for-android-master"
    ]

    for pattern in warning_patterns:
        if pattern in message:
            return "WARNING"


    return None