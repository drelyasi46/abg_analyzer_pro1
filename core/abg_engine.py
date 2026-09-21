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
        lactate=None,
    ):

        primary_disorder = PrimaryDisorderDetector.detect(
            ph,
            pco2,
            hco3
        )

        if primary_disorder in (
            "Respiratory Acidosis",
            "Respiratory Alkalosis",
        ):
            chronic = CompensationEngine.detect_chronicity(
                primary_disorder,
                pco2,
                hco3
            )

        compensation = CompensationEngine.evaluate(
            primary_disorder=primary_disorder,
            pco2=pco2,
            hco3=hco3,
            chronic=chronic
        )

        anion_gap = None

        if na is not None and cl is not None:
            anion_gap = AnionGapEngine.calculate(na, cl, hco3, albumin)

        delta_ratio = None

        if (
            anion_gap is not None
            and anion_gap["status"] == "HIGH_ANION_GAP"
        ):
            delta_ratio = DeltaRatioEngine.calculate(
                anion_gap["anion_gap"],
                hco3
            )

        triple = TripleDisorderEngine.analyze(
            primary_disorder=primary_disorder,
            compensation_result=compensation,
            delta_ratio=delta_ratio
        )

        interpretation = InterpretationEngine.generate(
            primary_disorder=primary_disorder,
            compensation=compensation,
            anion_gap=anion_gap,
            delta_ratio=delta_ratio,
            triple=triple
        )

        severity = SeverityEngine.evaluate(
            primary_disorder=primary_disorder,
            compensation=compensation,
            anion_gap=anion_gap,
            delta_ratio=delta_ratio,
            triple=triple,
            hco3=hco3,
            pco2=pco2,
            ph=ph
        )

        report = ReportComposer.compose(
            interpretation=interpretation,
            severity=severity,
            compensation=compensation,
            anion_gap=anion_gap,
            delta_ratio=delta_ratio,
            triple=triple,
            primary_disorder=primary_disorder
        )

        return {
            "primary_disorder": primary_disorder,
            "compensation": compensation,
            "anion_gap": anion_gap,
            "delta_ratio": delta_ratio,
            "triple_disorder": triple,
            "interpretation": interpretation,
            "severity": severity,
            "report": report,
        }
