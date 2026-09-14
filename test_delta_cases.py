from core.delta_ratio import DeltaRatioEngine


cases = [
    ("DKA pure HAGMA", 24, 12),
    ("DKA + vomiting", 40, 10),
    ("DKA + metabolic alkalosis", 45, 8),
]


for name, ag, hco3 in cases:

    result = DeltaRatioEngine.calculate(
        anion_gap=ag,
        hco3=hco3
    )

    print(name)
    print(result)
    print("----------------")