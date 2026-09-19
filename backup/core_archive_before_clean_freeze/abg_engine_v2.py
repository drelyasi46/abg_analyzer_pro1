"""
ABG Engine Version 2

Coordinator only
"""

from core.validation_result import ValidationResult
from core.diagnosis import DiagnosisEngine


class ABGEngine:

    def __init__(self):
        self.result = ValidationResult()

    def analyze(
        self,
        ph,
        pco2,
        hco3,
        na=None,
        k=None,
        cl=None,
        albumin=None,
        lactate=None,
    ):

        # Create a fresh result for every analysis
        self.result = ValidationResult()

        status, disorder = DiagnosisEngine.determine(
            ph,
            pco2,
            hco3,
        )

        self.result.status = status
        self.result.primary_disorder = disorder

        return self.result