from core.delta_ratio import DeltaRatioEngine


result = DeltaRatioEngine.calculate(
    anion_gap=24,
    hco3=12
)


print(result)