from core.compensation_engine import CompensationEngine
from core.anion_gap import AnionGapEngine
from core.delta_ratio import DeltaRatioEngine
from core.triple_disorder import TripleDisorderEngine
from core.interpretation_engine import InterpretationEngine
from core.severity_engine import SeverityEngine
from core.report_composer import ReportComposer
from core.primary_detector import PrimaryDisorderDetector


class ABGEngine:

    @staticmethod
    def analyze(
        ph,
        pco2,
        hco3,
        na=None,
        cl=None,
        chronic=False,
        k=None,
        albumin=None,
        lactate=None
    ):

        # Primary disorder detection
        primary_disorder = PrimaryDisorderDetector.detect(
            ph,
            pco2,
            hco3
        )


        # Auto detect acute/chronic respiratory disorders
        if primary_disorder in (
            "Respiratory Acidosis",
            "Respiratory Alkalosis",
        ):
            chronic = CompensationEngine.detect_chronicity(
                primary_disorder,
                pco2,
                hco3
            )


        # Compensation
        compensation = CompensationEngine.evaluate(
            primary_disorder,
            pco2,
            hco3,
            chronic
        )


        # Anion Gap
        anion_gap = None

        if na is not None and cl is not None:

            anion_gap = AnionGapEngine.calculate(
                na,
                cl,
                hco3
            )


        # Delta Ratio
        delta_ratio = None

        if anion_gap:

            delta_ratio = DeltaRatioEngine.calculate(
                anion_gap["anion_gap"],
                hco3
            )


        # Triple disorder
        triple = TripleDisorderEngine.analyze(
            compensation,
            delta_ratio["delta_ratio"]
            if delta_ratio else None
        )


        # Interpretation
        interpretation = InterpretationEngine.generate(
            compensation,
            anion_gap,
            delta_ratio,
            triple
        )


        # Severity
        severity = SeverityEngine.evaluate(
            compensation,
            anion_gap,
            delta_ratio,
            triple,
            hco3,
            pco2
        )


        # Final report
        report = ReportComposer.compose(
            interpretation,
            severity,
            compensation,
            anion_gap,
            delta_ratio,
            triple
        )


        return {
            "primary_disorder": primary_disorder,
            "compensation": compensation,
            "anion_gap": anion_gap,
            "delta_ratio": delta_ratio,
            "triple_disorder": triple,
            "interpretation": interpretation,
            "severity": severity,
            "report": report
        }