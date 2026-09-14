from pathlib import Path
import shutil

ROOT = Path(".")

REPLACEMENTS = {
    "ΓÇô": "-",
    "ΓÇö": "-",
    "ΓÇ£": '"',
    "ΓÇ¥": '"',
    "ΓÇ˜": "'",
    "ΓÇ™": "'",

    "PaCO2": "PaCO2",
    "HCO3Γü╗": "HCO3",

    "Na": "Na",
    "K": "K",
    "Cl": "Cl",
}

extensions = {".py", ".kv"}

fixed = 0

for file in ROOT.rglob("*"):
    if file.suffix not in extensions:
        continue

    try:
        text = file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    original = text

    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    if text != original:
        backup = file.with_suffix(file.suffix + ".bak")
        shutil.copy2(file, backup)

        file.write_text(text, encoding="utf-8")

        print("Fixed:", file)
        fixed += 1

print()
print(f"Finished. {fixed} file(s) repaired.")