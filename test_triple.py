from core.compensation_engine import CompensationEngine
from core.delta_ratio import DeltaRatioEngine
from core.triple_disorder import TripleDisorderEngine


# Sepsis + Diarrhea + Respiratory Alkalosis

compensation = CompensationEngine.evaluate(
    primary_disorder="Metabolic Acidosis",
    pco2=15,
    hco3=10
)


delta = DeltaRatioEngine.calculate(
    anion_gap=15,
    hco3=10
)


result = TripleDisorderEngine.analyze(
    compensation,
    delta["delta_ratio"]
)


print(result)