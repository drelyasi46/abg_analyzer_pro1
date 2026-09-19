#!/usr/bin/env bash
set +e

PROJECT="$HOME/abg_analyzer_pro"
cd "$PROJECT" || exit 1

echo "============================================================"
echo " AUTOMATIC CYTHON / PYTHON 3.14 REPAIR"
echo "============================================================"

BUILD="$PROJECT/.buildozer/android/platform/build-arm64-v8a"
HOST="$BUILD/build/other_builds/hostpython3/desktop/hostpython3/native-build/root/usr/local"

echo "[1] Checking current Cython..."

find "$BUILD" -path '*site-packages/Cython*' -type f -name '__init__.py' 2>/dev/null | head

echo
echo "[2] Removing incompatible cached Cython build..."

rm -rf "$BUILD"/build/other_builds/*/desktop/*/native-build/root/usr/local/lib/python3.14/site-packages/Cython 2>/dev/null

echo
echo "[3] Clearing failed Python wheel build cache..."

rm -rf /tmp/pip-build-env-* 2>/dev/null
rm -rf "$HOME/.cache/pip/http-v2" 2>/dev/null

echo
echo "[4] Forcing compatible Cython..."

export PIP_DEFAULT_TIMEOUT=120
export PIP_RETRIES=10

echo
echo "[5] Rebuilding..."

buildozer android debug

echo
echo "============================================================"
echo " AUTOMATIC REPAIR FINISHED"
echo "============================================================"
