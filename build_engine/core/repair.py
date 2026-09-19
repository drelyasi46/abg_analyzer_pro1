from build_engine.fixes.openssl import repair_openssl


class RepairManager:

    def __init__(self, engine):
        self.engine = engine

    def repair(self, failures):

        repaired = []

        if "OPENSSL_REMOTE_403" in failures:
            if repair_openssl(self.engine):
                repaired.append("OPENSSL_REMOTE_403")

        return repaired
