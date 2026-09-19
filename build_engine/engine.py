#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


PROJECT_DIR = Path(__file__).resolve().parent.parent

# Make "build_engine" importable even when this file is executed directly.
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


class BuildEngine:

    def __init__(self, project_dir=None):
        self.project = Path(project_dir or PROJECT_DIR).resolve()

        self.engine = self.project / "build_engine"
        self.logs = self.engine / "logs"
        self.cache = self.engine / "cache"

        self.logs.mkdir(parents=True, exist_ok=True)
        self.cache.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs / f"build_{timestamp}.log"

        self.p4a_dir = (
            self.project
            / ".buildozer"
            / "android"
            / "platform"
            / "python-for-android"
        )

        self.local_openssl = (
            Path.home()
            / "p4a-local"
            / "openssl"
        )

        self.openssl_version = "1.1.1w"

    def log(self, message):
        line = f"[{datetime.now():%H:%M:%S}] {message}"
        print(line)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def run(self, command, env=None):
        self.log("$ " + " ".join(map(str, command)))

        proc = subprocess.Popen(
            [str(x) for x in command],
            cwd=self.project,
            env=env or os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        output = []

        for line in proc.stdout:
            print(line, end="")
            output.append(line)

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line)

        proc.wait()

        return proc.returncode, "".join(output)

    def check_environment(self):
        self.log("=== ENVIRONMENT CHECK ===")

        checks = {
            "python": shutil.which("python3"),
            "buildozer": shutil.which("buildozer"),
            "java": shutil.which("java"),
            "perl": shutil.which("perl"),
        }

        for name, path in checks.items():
            if path:
                self.log(f"{name}: {path}")
            else:
                self.log(f"{name}: MISSING")

        if self.p4a_dir.exists():
            self.log(f"P4A SOURCE: {self.p4a_dir}")
        else:
            self.log("P4A SOURCE: NOT FOUND")

        if self.local_openssl.exists():
            self.log(f"LOCAL OPENSSL: {self.local_openssl}")
        else:
            self.log("LOCAL OPENSSL: NOT FOUND")

        return True

    def configure_environment(self):
        self.log("=== CONFIGURING BUILD ENVIRONMENT ===")

        env = os.environ.copy()

        env["ANDROIDAPI"] = "34"
        env["ANDROIDMINAPI"] = "24"

        # Force the exact P4A source used by Buildozer.
        if self.p4a_dir.exists():
            env["P4A_SOURCE_DIR"] = str(self.p4a_dir)

            old_pythonpath = env.get("PYTHONPATH", "")

            paths = [str(self.p4a_dir)]

            if old_pythonpath:
                paths.append(old_pythonpath)

            env["PYTHONPATH"] = os.pathsep.join(paths)

            self.log(f"P4A_SOURCE_DIR: {self.p4a_dir}")
            self.log(f"PYTHONPATH: {env['PYTHONPATH']}")

        # Keep local OpenSSL source available to repair/build logic.
        if (self.local_openssl / "Configure").exists():
            env["P4A_openssl_DIR"] = str(self.local_openssl)
            env["P4A_OPENSSL_DIR"] = str(self.local_openssl)
            self.log(f"P4A_openssl_DIR: {self.local_openssl}")
            self.log(f"P4A_OPENSSL_DIR: {self.local_openssl}")
        else:
            self.log("P4A_OPENSSL_DIR: LOCAL SOURCE NOT FOUND")

        return env

    def detect_packages_path(self):
        """
        Detect the actual package cache used by the current Buildozer/P4A build.

        Build logs show that P4A uses:
        .buildozer/android/platform/build-arm64-v8a/packages
        """

        candidates = [
            self.project
            / ".buildozer"
            / "android"
            / "platform"
            / "build-arm64-v8a"
            / "packages",

            self.project
            / ".buildozer"
            / "android"
            / "platform"
            / "build-arm64-v8a"
            / "packages",
        ]

        for path in candidates:
            if path.exists():
                self.log(f"P4A PACKAGES PATH: {path}")
                return path

        # If the directory does not exist yet, create the expected one.
        path = candidates[0]
        path.mkdir(parents=True, exist_ok=True)

        self.log(f"P4A PACKAGES PATH CREATED: {path}")

        return path

    def seed_openssl_cache(self):
        """
        Seed the exact P4A package cache.

        This is deliberately done before P4A starts its recipe download loop.
        """

        self.log("=== OPENSSL CACHE PREPARATION ===")

        source_archive = (
            Path.home()
            / "p4a-local"
            / f"openssl-{self.openssl_version}.tar.gz"
        )

        source_dir = self.local_openssl

        if not source_archive.exists():

            if not (source_dir / "Configure").exists():
                self.log(
                    "OPENSSL CACHE PREPARATION FAILED — "
                    "local OpenSSL source not found"
                )
                return False

            self.log("CREATING LOCAL OPENSSL ARCHIVE")

            rc, _ = self.run(
                [
                    "tar",
                    "-czf",
                    str(source_archive),
                    "-C",
                    str(source_dir.parent),
                    source_dir.name,
                ]
            )

            if rc != 0 or not source_archive.exists():
                self.log(
                    "OPENSSL CACHE PREPARATION FAILED — "
                    "archive creation failed"
                )
                return False

            self.log(
                f"LOCAL OPENSSL ARCHIVE CREATED: "
                f"{source_archive}"
            )

        packages = self.detect_packages_path()
        openssl_cache = packages / "openssl"

        openssl_cache.mkdir(parents=True, exist_ok=True)

        target = (
            openssl_cache
            / f"openssl-{self.openssl_version}.tar.gz"
        )

        marker = (
            openssl_cache
            / f".mark-openssl-{self.openssl_version}.tar.gz"
        )

        # Copy only when necessary.
        if (
            not target.exists()
            or target.stat().st_size != source_archive.stat().st_size
        ):
            self.log(f"SEEDING OPENSSL CACHE: {target}")

            shutil.copy2(source_archive, target)

        marker.touch()

        self.log(f"OPENSSL ARCHIVE: {target}")
        self.log(f"OPENSSL MARKER: {marker}")

        # Verify archive exists and is non-empty.
        if not target.exists() or target.stat().st_size < 1000000:
            self.log(
                "OPENSSL CACHE PREPARATION FAILED — "
                "invalid archive"
            )
            return False

        self.log("OPENSSL CACHE: READY")

        return True

    def preflight(self, env):
        self.log("=== P4A PREFLIGHT ===")

        python = env.get(
            "PYTHON_EXECUTABLE",
            "/home/babak/ube/.venv/bin/python3",
        )

        code = r'''
import os
import sys

print("PYTHON:", sys.executable)
print("P4A_OPENSSL_DIR:", os.environ.get("P4A_OPENSSL_DIR"))
print("P4A_SOURCE_DIR:", os.environ.get("P4A_SOURCE_DIR"))

try:
    import pythonforandroid
    import pythonforandroid.recipe

    print("P4A PACKAGE:", pythonforandroid.__file__)
    print("P4A RECIPE:", pythonforandroid.recipe.__file__)

except Exception as exc:
    print("P4A IMPORT ERROR:", repr(exc))
    sys.exit(2)
'''

        rc, output = self.run(
            [python, "-c", code],
            env=env,
        )

        if rc != 0:
            self.log("P4A PREFLIGHT: FAILED")
            return False

        expected = str(
            self.p4a_dir / "pythonforandroid"
        )

        if expected not in output:
            self.log(
                "P4A PREFLIGHT: FAILED — "
                "wrong python-for-android source"
            )
            return False

        self.log("P4A PREFLIGHT: OK")

        return True

    def build_command(self):
        return [
            "buildozer",
            "-v",
            "android",
            "debug",
        ]

    def run_build(self):
        self.log("=== BUILD START ===")

        env = self.configure_environment()

        if not self.seed_openssl_cache():
            return 1, "OPENSSL CACHE PREPARATION FAILED"

        if not self.preflight(env):
            return 1, "P4A PREFLIGHT FAILED"

        return self.run(
            self.build_command(),
            env=env,
        )

    def diagnose(self, output):
        self.log("=== DIAGNOSTICS ===")

        rules = [
            (
                "HTTP Error 403",
                "OPENSSL_REMOTE_403",
                "OpenSSL remote download blocked",
            ),
            (
                "Requested API target 33 is not available",
                "ANDROID_API_MISMATCH",
                "Requested Android API is unavailable",
            ),
            (
                "ModuleNotFoundError: No module named 'appdirs'",
                "P4A_DEPENDENCY_MISSING",
                "P4A Python dependency missing",
            ),
            (
                "No module named 'cgi'",
                "PYTHON_CGI_REMOVED",
                "Python/P4A compatibility problem",
            ),
            (
                "libwebp",
                "LIBWEBP_DOWNLOAD",
                "libwebp source/download problem",
            ),
            (
                "libthorvg",
                "THORVG_DOWNLOAD",
                "thorvg source/download problem",
            ),
        ]

        found = []

        for text, code, description in rules:
            if text in output:
                self.log(
                    f"DETECTED: {code} — {description}"
                )
                found.append(code)

        if not found:
            self.log("No known failure rule detected.")

        return found

    def repair_and_retry(self, failures):
        """
        Repair only what is actually detected.

        OpenSSL repair is handled directly here because the recipe's
        download() method does not consume P4A_OPENSSL_DIR.
        """

        repaired = []

        if "OPENSSL_REMOTE_403" in failures:

            self.log("=== AUTOMATIC OPENSSL REPAIR ===")

            if self.seed_openssl_cache():
                repaired.append("OPENSSL_CACHE")
            else:
                self.log("OPENSSL AUTOMATIC REPAIR FAILED")

        return repaired

    def main(self):

        self.log("========================================")
        self.log(" ABG ANDROID BUILD ENGINE")
        self.log("========================================")

        self.check_environment()

        rc, output = self.run_build()

        if rc == 0:
            self.log("BUILD SUCCESS")
            return 0

        self.log(f"BUILD FAILED: exit code {rc}")

        failures = self.diagnose(output)

        self.log(
            "FAILURE RULES: " + ", ".join(failures)
        )

        repaired = self.repair_and_retry(failures)

        if repaired:

            self.log(
                "REPAIRED: " + ", ".join(repaired)
            )

            self.log("=== BUILD RETRY AFTER REPAIR ===")

            retry_env = self.configure_environment()

            if not self.preflight(retry_env):
                self.log("RETRY PREFLIGHT FAILED")
                return 1

            retry_rc, retry_output = self.run(
                self.build_command(),
                env=retry_env,
            )

            if retry_rc == 0:
                self.log("BUILD SUCCESS AFTER REPAIR")
                return 0

            self.log(
                f"BUILD STILL FAILED AFTER REPAIR: "
                f"exit code {retry_rc}"
            )

            retry_failures = self.diagnose(
                retry_output
            )

            self.log(
                "POST-REPAIR FAILURE RULES: "
                + ", ".join(retry_failures)
            )

            return retry_rc

        self.log("NO AUTOMATIC REPAIR AVAILABLE")

        return rc


if __name__ == "__main__":
    engine = BuildEngine(PROJECT_DIR)
    sys.exit(engine.main())
