#!/usr/bin/env bash

set +e

PROJECT="$HOME/abg_analyzer_pro"
cd "$PROJECT" || exit 1

LOG="auto_diagnose_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee "$LOG") 2>&1

echo "============================================================"
echo "        ABG ANALYZER PRO - BUILD DIAGNOSTIC ENGINE"
echo "============================================================"
echo "Time: $(date)"
echo "Project: $PROJECT"
echo

echo "===== 1. HOST PYTHON ====="
python3 --version
command -v python3
echo

echo "===== 2. BUILDOZER ====="
buildozer --version
command -v buildozer
echo

echo "===== 3. CYTHON ====="
cython --version
echo

echo "===== 4. BUILDOZER SPEC ====="
grep -nE '^(requirements|android.api|android.minapi|android.ndk|android.archs|android.enable_androidx)' \
    buildozer.spec 2>/dev/null
echo

P4A="$PROJECT/.buildozer/android/platform/python-for-android"

echo "===== 5. PYTHON-FOR-ANDROID ====="
if [ -d "$P4A" ]; then
    echo "P4A: $P4A"

    grep -n "version =" \
        "$P4A/pythonforandroid/recipes/python3/__init__.py" 2>/dev/null | head
    grep -n "version =" \
        "$P4A/pythonforandroid/recipes/hostpython3/__init__.py" 2>/dev/null | head
else
    echo "P4A NOT FOUND"
fi
echo

echo "===== 6. PYTHON RECIPE CONSISTENCY ====="

PY_RECIPE="$P4A/pythonforandroid/recipes/python3/__init__.py"
HOST_RECIPE="$P4A/pythonforandroid/recipes/hostpython3/__init__.py"

PY_VER=$(grep -m1 -E "^[[:space:]]*version[[:space:]]*=" "$PY_RECIPE" 2>/dev/null \
    | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/")

HOST_VER=$(grep -m1 -E "^[[:space:]]*version[[:space:]]*=" "$HOST_RECIPE" 2>/dev/null \
    | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/")

REQ=$(grep -E '^requirements[[:space:]]*=' buildozer.spec 2>/dev/null)

echo "python3 recipe : ${PY_VER:-UNKNOWN}"
echo "hostpython3    : ${HOST_VER:-UNKNOWN}"
echo "requirements   : ${REQ:-UNKNOWN}"
echo

echo "===== 7. STALE BUILD DIRECTORIES ====="

BUILD="$PROJECT/.buildozer/android/platform/build-arm64-v8a"

for x in \
    "$BUILD/build/other_builds/python3" \
    "$BUILD/build/other_builds/hostpython3" \
    "$BUILD/packages/python3" \
    "$BUILD/packages/hostpython3" \
    "$BUILD/dists/abganalyzer"
do
    if [ -e "$x" ]; then
        echo "STALE/PRESENT: $x"
    fi
done

echo

echo "===== 8. RECENT LOG FILES ====="

find "$PROJECT" -maxdepth 1 -type f \
    \( -name "*.log" -o -name "auto_repair_*.log" \) \
    -printf "%T@ %p\n" 2>/dev/null \
    | sort -nr \
    | head -10

echo

echo "===== 9. ERROR SIGNATURE ANALYSIS ====="

LATEST=$(find "$PROJECT" -maxdepth 1 -type f \
    \( -name "auto_repair_*.log" -o -name "*.log" \) \
    -printf "%T@ %p\n" 2>/dev/null \
    | sort -nr | head -1 | cut -d' ' -f2-)

if [ -n "$LATEST" ] && [ -f "$LATEST" ]; then

    echo "Analyzing: $LATEST"
    echo

    declare -A ERRORS

    ERRORS["SRE module mismatch"]="SRE_MISMATCH"
    ERRORS["No module named 'cgi'"]="PYTHON_CGI_REMOVED"
    ERRORS["ModuleNotFoundError"]="MISSING_MODULE"
    ERRORS["Cython.Compiler"]="CYTHON_COMPILER"
    ERRORS["LOAD segment not aligned"]="PAGE_SIZE_ALIGNMENT"
    ERRORS["SSL connection timeout"]="NETWORK_SSL"
    ERRORS["Could not resolve host"]="NETWORK_DNS"
    ERRORS["No space left on device"]="DISK_SPACE"
    ERRORS["Permission denied"]="PERMISSION"
    ERRORS["No such file or directory"]="MISSING_FILE"

    FOUND=0

    for PATTERN in "${!ERRORS[@]}"; do
        if grep -Fq "$PATTERN" "$LATEST"; then
            echo "FOUND: ${ERRORS[$PATTERN]}"
            echo "       pattern: $PATTERN"
            FOUND=1
        fi
    done

    if [ "$FOUND" -eq 0 ]; then
        echo "No known error signature detected."
    fi
else
    echo "No diagnostic log found."
fi

echo

echo "===== 10. CONSISTENCY CHECK ====="

if [ -n "$PY_VER" ] && [ -n "$HOST_VER" ]; then
    if [ "$PY_VER" = "$HOST_VER" ]; then
        echo "PASS: python3 and hostpython3 recipe versions match."
    else
        echo "FAIL: python3=$PY_VER hostpython3=$HOST_VER"
    fi
fi

echo

echo "===== DIAGNOSTIC RESULT ====="
echo "NO FILES WERE MODIFIED."
echo "Diagnostic log: $LOG"
echo "============================================================"
