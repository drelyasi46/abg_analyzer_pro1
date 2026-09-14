from core.compensation_engine import CompensationEngine
from core.mixed_disorder import MixedDisorderDetector


result = CompensationEngine.evaluate(
    primary_disorder="Metabolic Alkalosis",
    pco2=25,
    hco3=36,
)


mixed = MixedDisorderDetector.analyze(result)


print(result)
print(mixed)