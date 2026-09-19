"""
abg_engine.py

Professional ABG Interpretation Engine
"""

from core.diagnosis import DiagnosisEngine
from core.compensation import Compensation
from core.respiratory import RespiratoryInterpreter
from core.anion_gap import AnionGap
from core.mixed_disorders import MixedDisorders
from core.mixed_detector import MixedDisorderDetector
from core.triple_disorder import TripleDisorderDetector


class ABGEngine:

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

        report = []

        report.append("=" * 40)
        report.append("ABG INTERPRETATION REPORT")
        report.append("=" * 40)
        report.append("")

        # -------------------------------------------------
        # Diagnosis
        # -------------------------------------------------

        status, disorder = DiagnosisEngine.determine(
            ph,
            pco2,
            hco3,
        )

        report.append(status)
        report.append("")
        report.append(f"Primary Disorder: {disorder}")
        report.append("")

        mixed_result = None
        ratio = None

        # -------------------------------------------------
        # Compensation
        # -------------------------------------------------

        if disorder == "Metabolic Acidosis":

            low, expected, high = Compensation.winters_formula(
                hco3
            )

            report.append("Compensation")
            report.append("-------------------------")

            report.append(
                f"Expected PaCO₂ (Winter): {expected:.1f}"
            )

            mixed_result = (
                MixedDisorderDetector.respiratory_compensation(
                    pco2,
                    low,
                    high,
                )
            )

            report.append(mixed_result)

        elif disorder == "Metabolic Alkalosis":

            low, expected, high = (
                Compensation.metabolic_alkalosis_expected_pco2(
                    hco3
                )
            )

            report.append("Compensation")
            report.append("-------------------------")

            report.append(
                f"Expected PaCO₂ : {expected:.1f}"
            )

            mixed_result = (
                MixedDisorderDetector.respiratory_compensation(
                    pco2,
                    low,
                    high,
                )
            )

            report.append(mixed_result)

        elif disorder == "Respiratory Acidosis":

            acute = (
                Compensation.acute_respiratory_acidosis_expected_hco3(
                    pco2
                )
            )

            chronic = (
                Compensation.chronic_respiratory_acidosis_expected_hco3(
                    pco2
                )
            )

            report.append("Compensation")
            report.append("-------------------------")

            report.append(
                f"Measured HCO₃ : {hco3:.1f}"
            )

            report.append(
                f"Expected Acute : {acute:.1f}"
            )

            report.append(
                f"Expected Chronic : {chronic:.1f}"
            )

            mixed_result = (
                MixedDisorderDetector.metabolic_compensation(
                    hco3,
                    acute,
                    chronic,
                )
            )

            report.append(mixed_result)

            report.append(
                RespiratoryInterpreter.classify_respiratory_acidosis(
                    hco3,
                    acute,
                    chronic,
                )
            )

        elif disorder == "Respiratory Alkalosis":

            acute = (
                Compensation.acute_respiratory_alkalosis_expected_hco3(
                    pco2
                )
            )

            chronic = (
                Compensation.chronic_respiratory_alkalosis_expected_hco3(
                    pco2
                )
            )

            report.append("Compensation")
            report.append("-------------------------")

            report.append(
                f"Measured HCO₃ : {hco3:.1f}"
            )

            report.append(
                f"Expected Acute : {acute:.1f}"
            )

            report.append(
                f"Expected Chronic : {chronic:.1f}"
            )

            mixed_result = (
                MixedDisorderDetector.metabolic_compensation(
                    hco3,
                    acute,
                    chronic,
                )
            )

            report.append(mixed_result)

            report.append(
                RespiratoryInterpreter.classify_respiratory_alkalosis(
                    hco3,
                    acute,
                    chronic,
                )
            )

        # -------------------------------------------------
        # Part 2 starts here:
        # Anion Gap Analysis
        # -------------------------------------------------
                # -------------------------------------------------
        # Anion Gap Analysis
        # -------------------------------------------------

        ag = None

        if na is not None and cl is not None:

            report.append("")
            report.append("=" * 40)
            report.append("ANION GAP ANALYSIS")
            report.append("=" * 40)

            ag = AnionGap.calculate(
                na,
                cl,
                hco3,
            )

            report.append(
                f"Anion Gap : {ag:.1f}"
            )

            if ag > 12:
                report.append("High Anion Gap")
            else:
                report.append("Normal Anion Gap")

            # ---------------------------------------------
            # Corrected Anion Gap
            # ---------------------------------------------

            if albumin is not None:

                corrected_ag = AnionGap.corrected_anion_gap(
                    ag,
                    albumin,
                )

                report.append(
                    f"Corrected AG : {corrected_ag:.1f}"
                )

                if albumin < 4:
                    report.append(
                        "Albumin correction applied."
                    )

            # ---------------------------------------------
            # Delta Ratio
            # فقط در High AG Metabolic Acidosis
            # ---------------------------------------------

            if (
                disorder == "Metabolic Acidosis"
                and ag > 12
            ):

                ratio = AnionGap.delta_ratio(
                    ag,
                    hco3,
                )

                if ratio is not None:

                    report.append("")
                    report.append("Delta Ratio")
                    report.append("-------------------------")

                    report.append(
                        f"{ratio:.2f}"
                    )

                    report.append(
                        MixedDisorders.interpret_delta_ratio(
                            ratio
                        )
                    )
# -------------------------
# Additional Mixed Disorder Detection
# -------------------------

if (
    disorder == "Respiratory Alkalosis"
    and na is not None
    and cl is not None
    and ag > 12
):
    report.append("")
    report.append(
        "Mixed Disorder: Concurrent High Anion Gap Metabolic Acidosis"
    )

elif (
    disorder == "Respiratory Acidosis"
    and na is not None
    and cl is not None
    and ag > 12
):
    report.append("")
    report.append(
        "Mixed Disorder: Concurrent High Anion Gap Metabolic Acidosis"
    )

# -------------------------------------------------
# Triple Disorder Analysis
# -------------------------------------------------

triple_result = TripleDisorderDetector.evaluate(
    disorder,
    mixed_result,
    ratio,
)

if triple_result:

    report.append("")
    report.append("=" * 40)
    report.append("TRIPLE DISORDER ANALYSIS")
    report.append("=" * 40)

    report.append(
        triple_result
    )

# -------------------------------------------------
# Part 3 starts here:
# Lactate
# -------------------------------------------------

if lactate is not None:
    

    report.append("")
    report.append("=" * 40)
    report.append("LACTATE")
    report.append("=" * 40)

    report.append(
                f"Lactate : {lactate:.1f} mmol/L"
            )

    if lactate < 2:
                report.append("Normal")

            elif lactate < 4:
                report.append("Hyperlactatemia")

            else:
                report.append("Severe Hyperlactatemia")
                report.append(
                    "Consider tissue hypoperfusion or septic shock."
                )

        # -------------------------------------------------
        # Clinical Impression
        # -------------------------------------------------

    report.append("")
    report.append("=" * 40)
    report.append("CLINICAL IMPRESSION")
    report.append("=" * 40)

    if disorder == "Normal Acid-Base Status":

            report.append(
                "Normal acid-base status."
            )

        elif disorder == "Metabolic Acidosis":

            if ag is not None:

                if ag > 12:

                    report.append(
                        "High Anion Gap Metabolic Acidosis"
                    )

                    report.append("")
                    report.append("Possible causes:")

                    report.append("• Diabetic Ketoacidosis (DKA)")
                    report.append("• Lactic Acidosis")
                    report.append("• Renal Failure")
                    report.append("• Toxic Alcohols")
                    report.append("• Salicylate Poisoning")

                else:

                    report.append(
                        "Normal Anion Gap Metabolic Acidosis"
                    )

            else:

                report.append(
                    "Compatible with metabolic acidosis."
                )

        elif disorder == "Respiratory Acidosis":

            report.append(
                "Compatible with respiratory acidosis."
            )

        elif disorder == "Respiratory Alkalosis":

            report.append(
                "Compatible with respiratory alkalosis."
            )

        elif disorder == "Metabolic Alkalosis":

            report.append(
                "Compatible with metabolic alkalosis."
            )

        else:

            report.append(
                "Mixed acid-base disorder should be considered."
            )

        # -------------------------------------------------
        # Part 4 starts here:
        # Recommendations
        # -------------------------------------------------
        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        report.append("")
        report.append("=" * 40)
        report.append("RECOMMENDATIONS")
        report.append("=" * 40)

        if ph < 7.20:
            report.append(
                "Severe acidemia: urgent evaluation."
            )

        if ph > 7.60:
            report.append(
                "Severe alkalemia: urgent evaluation."
            )

        if lactate is not None and lactate >= 4:

            report.append(
                "Repeat lactate within 2 hours."
            )

            report.append(
                "Evaluate for septic shock."
            )

            report.append(
                "Assess tissue perfusion."
            )

        if disorder == "Metabolic Acidosis":

            report.append(
                "Check serum ketones."
            )

            report.append(
                "Review renal function."
            )

            report.append(
                "Review medication/toxin exposure."
            )

        elif disorder == "Respiratory Acidosis":

            report.append(
                "Evaluate ventilation."
            )

            report.append(
                "Assess airway and pulmonary disease."
            )

        elif disorder == "Respiratory Alkalosis":

            report.append(
                "Consider pain, anxiety, hypoxemia or sepsis."
            )

        elif disorder == "Metabolic Alkalosis":

            report.append(
                "Review volume status and chloride depletion."
            )

        report.append(
            "Correlate with clinical findings."
        )

        report.append(
            "Repeat ABG if patient's condition changes."
        )

        return report