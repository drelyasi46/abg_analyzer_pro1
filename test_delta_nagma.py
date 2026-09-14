from core.delta_ratio import DeltaRatioEngine


result = DeltaRatioEngine.calculate(
    anion_gap=15,
    hco3=10
)


print(result)