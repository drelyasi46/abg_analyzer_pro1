from core.compensation_engine import CompensationEngine
from core.delta_ratio import DeltaRatioEngine
from core.triple_disorder import TripleDisorderEngine


# Sepsis + diarrhea + respiratory alkalosis pattern

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
    primary_disorder="Metabolic Acidosis",
    compensation_result=compensation,
    delta_ratio=delta
)

print(result)
