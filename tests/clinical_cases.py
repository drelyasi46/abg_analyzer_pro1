CLINICAL_CASES = [

    {
        "id": 1,
        "name": "DKA with appropriate respiratory compensation",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 26,
        "hco3": 12,
        "expected_status": "APPROPRIATE",
    },


    {
        "id": 2,
        "name": "DKA with respiratory failure",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 45,
        "hco3": 12,
        "expected_status": "SUPERIMPOSED_RESP_ACIDOSIS",
    },


    {
        "id": 3,
        "name": "Septic shock with lactic acidosis and hyperventilation",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 15,
        "hco3": 10,
        "expected_status": "SUPERIMPOSED_RESP_ALKALOSIS",
    },


    {
        "id": 4,
        "name": "COPD exacerbation with chronic CO2 retention",
        "primary_disorder": "Respiratory Acidosis",
        "pco2": 60,
        "hco3": 32,
        "chronic": True,
        "expected_status": "APPROPRIATE",
    },


    {
        "id": 5,
        "name": "COPD + vomiting induced metabolic alkalosis",
        "primary_disorder": "Metabolic Alkalosis",
        "pco2": 60,
        "hco3": 36,
        "expected_status": "SUPERIMPOSED_RESP_ACIDOSIS",
    },


    {
        "id": 6,
        "name": "Salicylate toxicity mixed disorder",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 18,
        "hco3": 12,
        "expected_status": "SUPERIMPOSED_RESP_ALKALOSIS",
    },


    {
        "id": 7,
        "name": "Cardiogenic shock with lactic acidosis and fatigue",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 50,
        "hco3": 8,
        "expected_status": "SUPERIMPOSED_RESP_ACIDOSIS",
    },


    {
        "id": 8,
        "name": "Severe pneumonia with respiratory alkalosis",
        "primary_disorder": "Respiratory Alkalosis",
        "pco2": 30,
        "hco3": 20,
        "chronic": True,
        "expected_status": "APPROPRIATE",
    },


    {
        "id": 9,
        "name": "Renal failure metabolic acidosis with COPD",
        "primary_disorder": "Metabolic Acidosis",
        "pco2": 50,
        "hco3": 10,
        "expected_status": "SUPERIMPOSED_RESP_ACIDOSIS",
    },


    {
        "id": 10,
        "name": "ICU patient with triple disorder pattern",
        "primary_disorder": "Metabolic Alkalosis",
        "pco2": 25,
        "hco3": 36,
        "expected_status": "SUPERIMPOSED_RESP_ALKALOSIS",
    },

]