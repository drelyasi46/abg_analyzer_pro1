from doctor.score import calculate


def print_report(results):

    print()
    print("=" * 50)
    print("ABG Doctor Report")
    print("=" * 50)

    for item in results:
        print(f'{item["status"]:8} {item["message"]}')

    print("-" * 50)

    score = calculate(results)

    print(f"Score : {score}/100")

    if score >= 90:
        print("READY FOR BUILD")

    elif score >= 70:
        print("BUILD POSSIBLE (Warnings)")

    else:
        print("NOT READY")