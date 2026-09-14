CLINICAL_CASES = [

    {
        "id": 1,
        "name": "DKA with appropriate compensation",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 26,
        "hco3": 12,
        "expected_status": "APPROPRIATE",
    },


    {
        "id": 2,
        "name": "DKA + respiratory failure",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 45,
        "hco3": 12,
        "expected_status": "SUPERIMPOSED_RESP_ACIDOSIS",
    },


    {
        "id": 3,
        "name": "Sepsis with lactic acidosis",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 15,
        "hco3": 12,
        "expected_status": "SUPERIMPOSED_RESP_ALKALOSIS",
    },


    {
        "id": 4,
        "name": "COPD with chronic CO2 retention",
        "primary_disorder": "Respiratory Acidosis",
        "pco2": 60,
        "hco3": 32,
        "chronic": True,
        "expected_status": "APPROPRIATE",
    },


]