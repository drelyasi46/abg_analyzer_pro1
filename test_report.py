from core.report_composer import ReportComposer


report = ReportComposer.compose(

    interpretation={
        "clinical_report": [
            "High anion gap metabolic acidosis.",
            "Concurrent respiratory acidosis."
        ]
    },


    severity={
        "severity": "CRITICAL",
        "score": 5,
        "alerts": [
            "Possible respiratory failure."
        ]
    },


    compensation=None,


    anion_gap={
        "anion_gap": 32,
        "message":
        "High anion gap metabolic acidosis pattern."
    },


    delta_ratio={
        "delta_ratio": 1.5,
        "message":
        "Predominantly HAGMA."
    }

)


print(report)