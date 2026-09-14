from doctor.patterns import PATTERNS


def analyze_log(path):

    results = []

    try:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:
            content = f.read()

    except FileNotFoundError:

        return [
            {
                "status": "ERROR",
                "message": f"Log file not found: {path}"
            }
        ]


    for pattern in PATTERNS:

        if pattern["keyword"].lower() in content.lower():

            results.append(
                {
                    "status": "ERROR",
                    "message": pattern["title"],
                    "advice": pattern["advice"],
                    "confidence": pattern["confidence"]
                }
            )


    if not results:

        results.append(
            {
                "status": "OK",
                "message": "No known build failure pattern detected"
            }
        )


    return results