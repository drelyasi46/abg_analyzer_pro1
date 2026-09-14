from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

EXCLUDE_DIRS = {
    ".venv",
    "venv",
    "venv_win",
    "venv_buildozer",
    ".git",
    "__pycache__",
    "build",
    "dist",
    "bin",
    ".buildozer",
    ".gradle",
}

INCLUDE_EXTENSIONS = {
    ".py",
    ".kv",
    ".spec",
    ".json",
    ".txt",
    ".md",
}

zip_name = "abg_clean.zip"

with ZipFile(zip_name, "w", ZIP_DEFLATED) as z:

    for file in Path(".").glob("**/*"):

        try:

            if any(part in EXCLUDE_DIRS for part in file.parts):
                continue

            if not file.is_file():
                continue

            if (
                file.suffix in INCLUDE_EXTENSIONS
                or file.name == "buildozer.spec"
            ):
                z.write(file)

        except Exception:
            continue

print(f"Created: {zip_name}")