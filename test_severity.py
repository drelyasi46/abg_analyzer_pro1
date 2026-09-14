from core.compensation_engine import CompensationEngine
from core.anion_gap import AnionGapEngine
from core.severity_engine import SeverityEngine
from core.triple_disorder import TripleDisorderEngine
from core.delta_ratio import DeltaRatioEngine


compensation = CompensationEngine.evaluate(
    primary_disorder="Metabolic Acidosis",
    pco2=45,
    hco3=8
)


ag = AnionGapEngine.calculate(
    na=140,
    cl=100,
    hco3=8
)


delta = DeltaRatioEngine.calculate(
    anion_gap=32,
    hco3=8
)


triple = TripleDisorderEngine.analyze(
    compensation,
    delta["delta_ratio"]
)


severity = SeverityEngine.evaluate(
    compensation,
    ag,
    delta,
    triple,
    hco3=8,
    pco2=45
)


print(severity)