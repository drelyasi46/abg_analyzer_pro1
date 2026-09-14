from core.compensation_engine import CompensationEngine


result = CompensationEngine.evaluate(
    primary_disorder="Respiratory Alkalosis",
    pco2=30,
    hco3=20,
    chronic=True,
)


print(result)