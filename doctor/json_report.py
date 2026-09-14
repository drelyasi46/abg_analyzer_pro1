import json
from datetime import datetime


def save_json_report(
    results,
    score,
    filename="doctor_report.json"
):

    report = {

        "project": "ABG Analyzer Pro",

        "generated_at": datetime.now().isoformat(),

        "score": score,

        "status":
            "BUILD POSSIBLE"
            if score >= 70
            else "NOT READY",

        "summary": {

            "total_checks": len(results),

            "ok": len(
                [
                    r for r in results
                    if r.get("status") == "OK"
                ]
            ),

            "warnings": len(
                [
                    r for r in results
                    if r.get("status") == "WARNING"
                ]
            ),

            "errors": len(
                [
                    r for r in results
                    if r.get("status") == "ERROR"
                ]
            )
        },


        "results": results
    }


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )


    print(
        "\nJSON report saved:",
        filename
    )