from core.compensation_engine import CompensationEngine
from core.anion_gap import AnionGapEngine
from core.delta_ratio import DeltaRatioEngine
from core.triple_disorder import TripleDisorderEngine
from core.interpretation_engine import InterpretationEngine


compensation = CompensationEngine.evaluate(
    primary_disorder="Metabolic Acidosis",
    pco2=15,
    hco3=10
)


ag = AnionGapEngine.calculate(
    na=140,
    cl=115,
    hco3=10
)


delta = DeltaRatioEngine.calculate(
    anion_gap=15,
    hco3=10
)


triple = TripleDisorderEngine.analyze(
    compensation,
    delta["delta_ratio"]
)


report = InterpretationEngine.generate(
    compensation,
    ag,
    delta,
    triple
)


print(report)