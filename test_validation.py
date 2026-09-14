from core.compensation_engine import CompensationEngine
from core.validation_engine import ValidationEngine
from tests.clinical_cases import CLINICAL_CASES


for case in CLINICAL_CASES:

    result = CompensationEngine.evaluate(
        primary_disorder=case["primary_disorder"],
        pco2=case["pco2"],
        hco3=case["hco3"],
        chronic=case.get("chronic", False),
    )


    validation = ValidationEngine.validate(
        result,
        case["expected_status"]
    )


    print(
        case["id"],
        case["name"],
        "➡",
        validation["message"]
    )