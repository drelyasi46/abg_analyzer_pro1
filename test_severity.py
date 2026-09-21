from core.compensation_engine import CompensationEngine
from core.anion_gap import AnionGapEngine
from core.severity_engine import SeverityEngine
from core.triple_disorder import TripleDisorderEngine
from core.delta_ratio import DeltaRatioEngine


primary_disorder = "Metabolic Acidosis"

compensation = CompensationEngine.evaluate(
    primary_disorder=primary_disorder,
    pco2=45,
    hco3=8
)

ag = AnionGapEngine.calculate(
    na=140,
    cl=100,
    hco3=8
)

delta = DeltaRatioEngine.calculate(
    anion_gap=ag["anion_gap"],
    hco3=8
)

triple = TripleDisorderEngine.analyze(
    primary_disorder=primary_disorder,
    compensation_result=compensation,
    delta_ratio=delta
)

severity = SeverityEngine.evaluate(
    primary_disorder=primary_disorder,
    compensation=compensation,
    anion_gap=ag,
    delta_ratio=delta,
    triple=triple,
    hco3=8,
    pco2=45,
    ph=7.10
)

print(severity)
