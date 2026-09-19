#!/usr/bin/env bash

set +e

PROJECT="$HOME/abg_analyzer_pro"
cd "$PROJECT" || exit 1

LOG="auto_diagnose_v2_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee "$LOG") 2>&1

echo "============================================================"
echo "       ABG ANALYZER PRO - DIAGNOSTIC ENGINE v2"
echo "============================================================"
echo

P4A="$PROJECT/.buildozer/android/platform/python-for-android"
PY_RECIPE="$P4A/pythonforandroid/recipes/python3/__init__.py"
HOST_RECIPE="$P4A/pythonforandroid/recipes/hostpython3/__init__.py"

echo "===== ENVIRONMENT ====="
echo "System Python : $(python3 --version 2>&1)"
echo "Buildozer     : $(buildozer --version 2>&1)"
echo "Cython        : $(cython --version 2>&1)"
echo

echo "===== CONFIGURATION ====="

REQ=$(grep -E '^requirements[[:space:]]*=' buildozer.spec | head -1)
API=$(grep -E '^android.api[[:space:]]*=' buildozer.spec | head -1)
MINAPI=$(grep -E '^android.minapi[[:space:]]*=' buildozer.spec | head -1)
NDK=$(grep -E '^android.ndk[[:space:]]*=' buildozer.spec | head -1)
ARCH=$(grep -E '^android.archs[[:space:]]*=' buildozer.spec | head -1)

echo "$REQ"
echo "$API"
echo "$MINAPI"
echo "$NDK"
echo "$ARCH"
echo

REQ_PY=$(echo "$REQ" | grep -oE 'python3==[0-9]+\.[0-9]+\.[0-9]+' \
    | sed 's/python3==//')

REQ_KIVY=$(echo "$REQ" | grep -oE 'kivy==[0-9]+\.[0-9]+\.[0-9]+' \
    | sed 's/kivy==//')

PY_VER=$(grep -m1 -E '^[[:space:]]*version[[:space:]]*=' "$PY_RECIPE" \
    | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/")

HOST_VER=$(grep -m1 -E '^[[:space:]]*version[[:space:]]*=' "$HOST_RECIPE" \
    | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/")

echo "===== VERSION MATRIX ====="
echo "Requested Python : ${REQ_PY:-UNKNOWN}"
echo "P4A python3      : ${PY_VER:-UNKNOWN}"
echo "P4A hostpython3  : ${HOST_VER:-UNKNOWN}"
echo "Requested Kivy   : ${REQ_KIVY:-UNKNOWN}"
echo

echo "===== DIAGNOSIS ====="

PROBLEMS=0

if [ -n "$REQ_PY" ] && [ -n "$PY_VER" ] && [ "$REQ_PY" != "$PY_VER" ]; then
    echo "[CRITICAL] PYTHON RECIPE MISMATCH"
    echo "           buildozer.spec requests Python $REQ_PY"
    echo "           p4a recipe provides Python $PY_VER"
    PROBLEMS=$((PROBLEMS+1))
fi

if [ -n "$PY_VER" ] && [ -n "$HOST_VER" ] && [ "$PY_VER" != "$HOST_VER" ]; then
    echo "[CRITICAL] HOST PYTHON RECIPE MISMATCH"
    echo "           python3=$PY_VER"
    echo "           hostpython3=$HOST_VER"
    PROBLEMS=$((PROBLEMS+1))
fi

echo

echo "===== LAST REAL BUILD LOG ====="

LATEST=$(find "$PROJECT" -maxdepth 1 -type f \
    -name "auto_repair_*.log" \
    -printf "%T@ %p\n" 2>/dev/null \
    | sort -nr \
    | head -1 \
    | cut -d' ' -f2-)

if [ -n "$LATEST" ] && [ -f "$LATEST" ]; then

    echo "Log: $LATEST"
    echo

    echo "--- ERROR SIGNATURES ---"

    if grep -Fq "SRE module mismatch" "$LATEST"; then
        echo "[CRITICAL] SRE module mismatch"
        echo "           Classification: PYTHON_BUILD_CORRUPTION_OR_VERSION_MIX"
        PROBLEMS=$((PROBLEMS+1))
    fi

    if grep -Fq "No module named 'cgi'" "$LATEST"; then
        echo "[CRITICAL] Python cgi module missing"
        echo "           Classification: PYTHON_VERSION_COMPATIBILITY"
        PROBLEMS=$((PROBLEMS+1))
    fi

    if grep -Fq "LOAD segment not aligned" "$LATEST"; then
        echo "[CRITICAL] Native library alignment problem"
        echo "           Classification: ANDROID_PAGE_SIZE"
        PROBLEMS=$((PROBLEMS+1))
    fi

    if grep -Fq "SSL connection timeout" "$LATEST"; then
        echo "[NETWORK] Git/P4A download timeout"
        echo "          Classification: NETWORK"
        PROBLEMS=$((PROBLEMS+1))
    fi

    if grep -Fq "No space left on device" "$LATEST"; then
        echo "[SYSTEM] Disk full"
        echo "         Classification: DISK"
        PROBLEMS=$((PROBLEMS+1))
    fi

    if grep -Fq "Permission denied" "$LATEST"; then
        echo "[SYSTEM] Permission denied"
        echo "         Classification: PERMISSION"
        PROBLEMS=$((PROBLEMS+1))
    fi

    echo
    echo "--- IMPORTANT BUILD LINES ---"

    grep -E \
        "Recipe python3|Recipe hostpython3|requirements=|SRE module mismatch|cgi|Cython|Command failed|Error code" \
        "$LATEST" \
        | tail -40

else
    echo "No auto_repair build log found."
fi

echo
echo "===== BUILD STATE ====="

BUILD="$PROJECT/.buildozer/android/platform/build-arm64-v8a"

for path in \
    "$BUILD/build/other_builds/python3" \
    "$BUILD/build/other_builds/hostpython3" \
    "$BUILD/packages/python3" \
    "$BUILD/packages/hostpython3" \
    "$BUILD/dists/abganalyzer"
do
    if [ -e "$path" ]; then
        echo "PRESENT: $path"
    else
        echo "ABSENT : $path"
    fi
done

echo
echo "============================================================"

if [ "$PROBLEMS" -eq 0 ]; then
    echo "DIAGNOSIS: NO KNOWN PROBLEM DETECTED"
else
    echo "DIAGNOSIS: $PROBLEMS PROBLEM(S) DETECTED"
fi

echo
echo "IMPORTANT:"
echo "This diagnostic engine did NOT modify the project."
echo "No repair was performed."
echo
echo "Diagnostic log:"
echo "$LOG"

echo "============================================================"
