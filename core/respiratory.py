class RespiratoryInterpreter:

    @staticmethod
    def classify_respiratory_acidosis(measured_hco3,
                                      acute_expected,
                                      chronic_expected):

        acute_diff = abs(measured_hco3 - acute_expected)
        chronic_diff = abs(measured_hco3 - chronic_expected)

        if acute_diff <= 2 and acute_diff < chronic_diff:
            return "Acute Respiratory Acidosis"

        elif chronic_diff <= 2 and chronic_diff < acute_diff:
            return "Chronic Respiratory Acidosis"

        elif measured_hco3 > chronic_expected + 2:
            return "Respiratory Acidosis + Metabolic Alkalosis"

        elif measured_hco3 < acute_expected - 2:
            return "Respiratory Acidosis + Metabolic Acidosis"

        return "Indeterminate Respiratory Acidosis"

    @staticmethod
    def classify_respiratory_alkalosis(measured_hco3,
                                       acute_expected,
                                       chronic_expected):

        acute_diff = abs(measured_hco3 - acute_expected)
        chronic_diff = abs(measured_hco3 - chronic_expected)

        if acute_diff <= 2 and acute_diff < chronic_diff:
            return "Acute Respiratory Alkalosis"

        elif chronic_diff <= 2 and chronic_diff < acute_diff:
            return "Chronic Respiratory Alkalosis"

        elif measured_hco3 > acute_expected + 2:
            return "Respiratory Alkalosis + Metabolic Alkalosis"

        elif measured_hco3 < chronic_expected - 2:
            return "Respiratory Alkalosis + Metabolic Acidosis"

        return "Indeterminate Respiratory Alkalosis"