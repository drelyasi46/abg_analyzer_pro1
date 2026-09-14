from core.abg_engine import ABGEngine


result = ABGEngine.analyze(
    ph=7.25,
    pco2=45,
    hco3=8,
    na=140,
    cl=100
)


print(result["report"])