from doctor.rules import get_penalty


def calculate(results):

    score = 100

    for item in results:

        message = item.get(
            "message",
            ""
        )

        penalty = get_penalty(
            message
        )

        score += penalty


        # اگر موردی در rules نبود
        # رفتار پیش‌فرض
        if penalty == 0:

            if item.get("status") == "WARNING":
                score -= 2

            elif item.get("status") == "ERROR":
                score -= 10


    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return score