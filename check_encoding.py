from pathlib import Path

SKIP_DIRS = {
    ".venv",
    "venv",
    "venv_win",
    "venv_buildozer",
    "__pycache__",
    ".git",
    "build",
    "dist",
}

BAD_PATTERNS = ["â", "Γ", "�"]

ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "cp1252",
    "latin1",
]

print("=" * 70)
print("ENCODING DIAGNOSTIC")
print("=" * 70)

for file in Path(".").rglob("*"):

    if file.suffix not in {".py", ".kv"}:
        continue

    if any(part in SKIP_DIRS for part in file.parts):
        continue

    try:
        data = file.read_bytes()
    except Exception as e:
        print(f"\n{file}")
        print(f"  SKIPPED ({e})")
        continue

    print(f"\n{file}")

    for enc in ENCODINGS:
        try:
            text = data.decode(enc)
            bad = any(x in text for x in BAD_PATTERNS)
            print(f"  {enc:<10} OK   bad_text={bad}")
        except Exception:
            print(f"  {enc:<10} FAILED")