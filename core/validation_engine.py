class ValidationEngine:

    @staticmethod
    def validate(result, expected_status):

        if result.status == expected_status:

            return {
                "pass": True,
                "message": "PASS"
            }

        else:

            return {
                "pass": False,
                "message": 
                f"FAIL: expected {expected_status}, got {result.status}"
            }