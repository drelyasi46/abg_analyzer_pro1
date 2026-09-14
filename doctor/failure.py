import re

from doctor.patterns import FAILURE_PATTERNS


def analyze_log(text):

    results = []

    for item in FAILURE_PATTERNS:

        if re.search(
            item["keyword"],
            text,
            re.IGNORECASE
        ):

            results.append(
                {
                    "status": "ERROR",
                    "message": item["title"],
                    "advice": item["advice"],
                    "confidence": item["confidence"]
                }
            )


    if not results:

        results.append(
            {
                "status": "OK",
                "message": "No known failure pattern detected"
            }
        )


    return results