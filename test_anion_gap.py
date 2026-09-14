from core.anion_gap import AnionGapEngine


result = AnionGapEngine.calculate(
    na=140,
    cl=104,
    hco3=12
)


print(result)