"""
validation_result.py

Structured result object for ABG analysis.
"""


class ValidationResult:

    def __init__(self):

        self.status = None

        self.primary_disorder = None

        self.compensation = None

        self.anion_gap = None
        self.anion_gap_value = None

        self.delta_ratio = None
        self.delta_analysis = None

        self.mixed_disorder = None

        self.triple_disorder = None

        self.clinical_impression = None

        self.recommendations = []

    def to_dict(self):

        return {
            "status": self.status,
            "primary_disorder": self.primary_disorder,
            "compensation": self.compensation,
            "anion_gap": self.anion_gap,
            "anion_gap_value": self.anion_gap_value,
            "delta_ratio": self.delta_ratio,
            "delta_analysis": self.delta_analysis,
            "mixed_disorder": self.mixed_disorder,
            "triple_disorder": self.triple_disorder,
            "clinical_impression": self.clinical_impression,
            "recommendations": self.recommendations,
        }