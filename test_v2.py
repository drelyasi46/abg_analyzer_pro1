from core.abg_engine_v2 import ABGEngine

engine = ABGEngine()

result = engine.analyze(
    ph=7.18,
    pco2=24,
    hco3=9,
)

print("Status:", result.status)
print("Primary Disorder:", result.primary_disorder)