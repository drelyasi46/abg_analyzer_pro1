def remove_duplicates(results):

    seen = set()
    cleaned = []

    for item in results:

        key = (
            item.get("status"),
            item.get("message")
        )

        if key not in seen:
            seen.add(key)
            cleaned.append(item)

    return cleaned