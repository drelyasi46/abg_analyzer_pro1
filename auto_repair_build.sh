#!/usr/bin/env bash

set -u

PROJECT="$HOME/abg_analyzer_pro"
P4A="$PROJECT/.buildozer/android/platform/python-for-android"
PLATFORM="$PROJECT/.buildozer/android/platform"
BUILD="$PLATFORM/build-arm64-v8a"
SPEC="$PROJECT/buildozer.spec"

LOG="$PROJECT/auto_repair_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG") 2>&1

echo
echo "============================================================"
echo "       ABG ANALYZER PRO - AUTO REPAIR SYSTEM"
echo "============================================================"
echo "Time: $(date)"
echo "Project: $PROJECT"
echo

cd "$PROJECT" || exit 1

echo "===== 1. SYSTEM ====="
echo "Python:"
python3 --version || true

echo "Buildozer:"
buildozer --version || true

echo "Cython:"
cython --version || true

echo
echo "===== 2. BUILD CONFIG ====="
grep -nE '^(requirements|android\.api|android\.minapi|android\.ndk|android\.archs|android\.enable_androidx)' "$SPEC" || true

echo
echo "===== 3. P4A ====="

if [ -d "$P4A" ]; then
    echo "P4A found: $P4A"

    if [ -f "$P4A/pythonforandroid/recipes/python3/__init__.py" ]; then
        echo "python3 recipe:"
        grep -n "version =" \
            "$P4A/pythonforandroid/recipes/python3/__init__.py" | head -5
    fi

    if [ -f "$P4A/pythonforandroid/recipes/hostpython3/__init__.py" ]; then
        echo "hostpython3 recipe:"
        grep -n "version =" \
            "$P4A/pythonforandroid/recipes/hostpython3/__init__.py" | head -5
    fi
else
    echo "ERROR: P4A directory not found"
    exit 1
fi

echo
echo "===== 4. FORCE PYTHON 3.12.10 CONSISTENCY ====="

python3 - <<'PY'
from pathlib import Path

root = Path.home() / "abg_analyzer_pro"
p4a = root / ".buildozer/android/platform/python-for-android"

files = [
    p4a / "pythonforandroid/recipes/python3/__init__.py",
    p4a / "pythonforandroid/recipes/hostpython3/__init__.py",
]

for p in files:
    if not p.exists():
        print("MISSING:", p)
        continue

    s = p.read_text()

    # Replace only the exact currently problematic recipe version.
    s2 = s.replace("3.14.2", "3.12.10")

    if s2 != s:
        backup = p.with_suffix(p.suffix + ".auto_backup")
        backup.write_text(s)
        p.write_text(s2)
        print("PATCHED:", p)
    else:
        print("OK:", p)
PY

echo
echo "===== 5. VERIFY RECIPE VERSIONS ====="

PYV1=$(grep -oE "version = ['\"]3\.[0-9]+\.[0-9]+['\"]" \
    "$P4A/pythonforandroid/recipes/python3/__init__.py" | head -1 || true)

PYV2=$(grep -oE "version = ['\"]3\.[0-9]+\.[0-9]+['\"]" \
    "$P4A/pythonforandroid/recipes/hostpython3/__init__.py" | head -1 || true)

echo "python3:      $PYV1"
echo "hostpython3:  $PYV2"

if ! grep -q "3.12.10" "$P4A/pythonforandroid/recipes/python3/__init__.py"; then
    echo "ERROR: python3 recipe is not 3.12.10"
    exit 1
fi

if ! grep -q "3.12.10" "$P4A/pythonforandroid/recipes/hostpython3/__init__.py"; then
    echo "ERROR: hostpython3 recipe is not 3.12.10"
    exit 1
fi

echo
echo "===== 6. BUILD SPEC ====="

python3 - <<'PY'
from pathlib import Path

p = Path.home() / "abg_analyzer_pro/buildozer.spec"
s = p.read_text()

old = None

for line in s.splitlines():
    if line.startswith("requirements"):
        old = line
        break

if old is None:
    raise SystemExit("ERROR: requirements line not found")

new = "requirements = python3==3.12.10,kivy==2.2.1"

if old != new:
    s = s.replace(old, new)
    p.write_text(s)
    print("PATCHED:", new)
else:
    print("OK:", new)
PY

grep -n "^requirements" "$SPEC"

echo
echo "===== 7. REMOVE STALE DIST ====="

if [ -d "$BUILD/dists/abganalyzer" ]; then
    rm -rf "$BUILD/dists/abganalyzer"
    echo "Removed old abganalyzer dist"
fi

echo
echo "===== 8. REMOVE STALE HOSTPYTHON BUILD ====="

find "$BUILD" -maxdepth 5 \
    \( -iname "*hostpython3*" -o -iname "*hostpython*" \) \
    -print 2>/dev/null | head -50

echo
echo "Removing stale hostpython build/cache directories..."

find "$BUILD" -maxdepth 6 -type d \
    \( -iname "hostpython3" -o -iname "hostpython3*" \) \
    -print -exec rm -rf {} + 2>/dev/null || true

echo
echo "===== 9. REMOVE TEMP PIP BUILD ENVIRONMENTS ====="

find /tmp -maxdepth 1 -type d \
    -name "build-env-*" \
    -print \
    -exec rm -rf {} + 2>/dev/null || true

echo
echo "===== 10. CLEAR PIP BUILD CACHE ====="

python3 -m pip cache purge || true

echo
echo "===== 11. FINAL ENVIRONMENT ====="

echo "System Python:"
python3 --version

echo
echo "Buildozer:"
buildozer --version

echo
echo "Cython:"
cython --version

echo
echo "ANDROIDAPI=${ANDROIDAPI:-<not-exported>}"
echo "ANDROIDMINAPI=${ANDROIDMINAPI:-<not-exported>}"
echo "ANDROIDNDK=${ANDROIDNDK:-<not-exported>}"

echo
echo "===== 12. START CLEAN BUILD ====="

echo "Starting Buildozer..."
echo

buildozer -v android debug

STATUS=$?

echo
echo "============================================================"
echo "                 BUILD RESULT"
echo "============================================================"

if [ "$STATUS" -eq 0 ]; then
    echo "SUCCESS: ABG Analyzer APK built successfully."

    echo
    echo "APK FILES:"
    find "$PROJECT/bin" -type f \
        \( -name "*.apk" -o -name "*.aab" \) \
        -printf "%p\n" 2>/dev/null || true

else
    echo "BUILD FAILED."

    echo
    echo "===== AUTOMATIC ERROR EXTRACTION ====="

    echo "--- Python version mismatch ---"
    grep -E \
        "should have same version|version .* requested|python3.*!=" \
        "$LOG" | tail -20 || true

    echo
    echo "--- Missing Python modules ---"
    grep -E \
        "ModuleNotFoundError|ImportError" \
        "$LOG" | tail -30 || true

    echo
    echo "--- Cython errors ---"
    grep -E \
        "Cython|cython" \
        "$LOG" | tail -30 || true

    echo
    echo "--- Last errors ---"
    grep -E \
        "ERROR|error:|Error:|failed|Failed|FAILED" \
        "$LOG" | tail -50 || true

    echo
    echo "Full diagnostic log:"
    echo "$LOG"
fi

exit "$STATUS"
