from doctor.json_report import save_json_report
from doctor.score import calculate
from doctor.dedupe import remove_duplicates
from doctor.utils import normalize_results
from doctor.project import check_project
from doctor.android import check_android
from doctor.github import check_github
from doctor.environment import check_environment
from doctor.report import print_report


def safe_run(results, name, func):

    print(f"\n[{name}]")

    try:
        output = func()

        if output is None:
            print(f"ERROR: {name} returned None")
            return

        results.extend(output)

    except Exception as e:
        print(f"ERROR in {name}: {e}")


def run_all():

    results = []

    print("=" * 50)
    print("ABG Analyzer Pro Preflight")
    print("=" * 50)

    safe_run(results, "ENVIRONMENT", check_environment)

    safe_run(results, "PROJECT", check_project)

    safe_run(results, "ANDROID", check_android)

    safe_run(results, "GITHUB", check_github)

    results = normalize_results(results)
    results = remove_duplicates(results)

    results = normalize_results(results)
    score = calculate(results)

    save_json_report(
    results,
    score
    )
    print_report(results)