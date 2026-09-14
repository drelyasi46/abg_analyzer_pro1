from doctor.classifier import classify


def ok(msg):
    return {
        "status": "OK",
        "message": msg
    }


def warning(msg):
    return {
        "status": "WARNING",
        "message": msg
    }


def error(msg):
    return {
        "status": "ERROR",
        "message": msg
    }


def normalize_results(results):

    normalized = []

    for item in results:

        message = item.get(
            "message",
            ""
        )

        level = classify(
            message
        )

        if level:
            item["status"] = level

        normalized.append(item)

    return normalized