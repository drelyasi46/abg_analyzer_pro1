FAILURE_PATTERNS = [

    {
        "title": "Python 3.14 detected",
        "keyword": "Python 3.14",
        "advice": "Use Python 3.11 in GitHub Actions",
        "confidence": 95
    },

    {
        "title": "Cython config.pxi problem",
        "keyword": "config.pxi",
        "advice": "Check Kivy/Cython compatibility",
        "confidence": 90
    },

    {
        "title": "Buildozer root execution",
        "keyword": "BUILDOZER_WARN_ON_ROOT",
        "advice": "Run Buildozer with normal user",
        "confidence": 85
    },

    {
        "title": "Android NDK/SDK problem",
        "keyword": "NDK",
        "advice": "Check Android SDK and NDK setup",
        "confidence": 85
    },

    {
        "title": "Network download failure",
        "keyword": "TLS handshake",
        "advice": "Check network or download source",
        "confidence": 90
    },

    {
        "title": "APK not generated",
        "keyword": "apk",
        "advice": "Build failed before APK generation",
        "confidence": 75
    },

]