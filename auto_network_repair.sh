#!/usr/bin/env bash
set -u

APP="$HOME/abg_analyzer_pro"
cd "$APP"

LOG="$APP/auto_network_repair_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "============================================================"
echo " ABG ANALYZER PRO - AUTOMATIC NETWORK/BUILD REPAIR"
echo "============================================================"

echo
echo "[1] Checking network..."

if curl -I -L --connect-timeout 15 https://github.com >/dev/null 2>&1; then
    echo "GitHub: OK"
else
    echo "GitHub: FAILED"
fi

if curl -I -L --connect-timeout 15 https://pypi.org >/dev/null 2>&1; then
    echo "PyPI: OK"
else
    echo "PyPI: FAILED"
fi

echo
echo "[2] Checking Buildozer configuration..."

sed -i 's/^requirements *=.*/requirements = python3==3.11.5,kivy==2.2.1/' buildozer.spec

echo "requirements:"
grep '^requirements' buildozer.spec

echo
echo "[3] Checking p4a..."

P4A="$APP/.buildozer/android/platform/python-for-android"

if [ ! -f "$P4A/pythonforandroid/recipes/python3/__init__.py" ]; then
    echo "p4a is missing."
    exit 1
fi

PYVER=$(grep -oP "version = '\K[0-9.]+" \
    "$P4A/pythonforandroid/recipes/python3/__init__.py" | head -1)

echo "p4a Python recipe: $PYVER"

if [ "$PYVER" != "3.11.5" ]; then
    echo
    echo "ERROR: p4a/Python mismatch."
    echo "Expected: 3.11.5"
    echo "Found:    $PYVER"
    exit 1
fi

echo
echo "[4] Looking for cached downloads..."

find "$HOME/.buildozer" \
     "$APP/.buildozer" \
     -type f \
     \( -name "*.tar.gz" -o -name "*.zip" -o -name "*.tgz" \) \
     2>/dev/null | head -100

echo
echo "[5] Showing p4a download cache..."

find "$HOME/.buildozer/android/packages" \
     "$HOME/.buildozer/android/platform" \
     -type f 2>/dev/null | \
     grep -E '\.(tar\.gz|zip|tgz)$' | head -100

echo
echo "[6] Cleaning only incomplete downloads..."

find "$HOME/.buildozer/android/packages" \
     -type f \
     \( -name "*.part" -o -name "*.tmp" \) \
     -delete 2>/dev/null || true

echo
echo "[7] Starting build with extended network timeout..."

export PIP_DEFAULT_TIMEOUT=180
export PIP_RETRIES=20

buildozer -v android debug

STATUS=$?

echo
echo "============================================================"

if [ "$STATUS" -eq 0 ]; then
    echo " BUILD SUCCESSFUL"
else
    echo " BUILD FAILED"
    echo
    echo "The complete automatic repair log is:"
    echo "$LOG"
fi

echo "============================================================"

exit "$STATUS"
