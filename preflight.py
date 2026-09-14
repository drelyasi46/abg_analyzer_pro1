import sys

from doctor.core import run_all
from doctor.failure import analyze_log


def main():

    if len(sys.argv) >= 3 and sys.argv[1] == "--analyze":

        log_file = sys.argv[2]

        try:

            with open(
                log_file,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                content = f.read()


            print("\n[BUILD FAILURE ANALYSIS]")
            print("=" * 50)


            results = analyze_log(
                content
            )


            for item in results:

                print(
                    item["status"],
                    item["message"]
                )

                if "advice" in item:
                    print(
                        "Advice:",
                        item["advice"]
                    )

                if "confidence" in item:
                    print(
                        "Confidence:",
                        str(item["confidence"]) + "%"
                    )

                print()


        except FileNotFoundError:

            print(
                "ERROR: Log file not found:",
                log_file
            )

        return


    run_all()


if __name__ == "__main__":
    main()