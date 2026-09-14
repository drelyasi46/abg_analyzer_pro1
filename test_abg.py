from core.abg_engine import ABGEngine


engine = ABGEngine()


result = engine.analyze(
    ph=7.25,
    pco2=25,
    hco3=12,
    na=140,
    cl=104
)

from core.report_formatter import ReportFormatter

print(
    ReportFormatter.format(result)
)