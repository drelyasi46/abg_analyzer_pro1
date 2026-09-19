#!/bin/bash
set -e

ROOT="$HOME/abg_analyzer_pro"
CACHE="$ROOT/.buildozer/android/platform/build-arm64-v8a/packages"
OPENSSL_DIR="$CACHE/openssl"
OPENSSL_FILE="$OPENSSL_DIR/openssl-1.1.1w.tar.gz"

echo "========================================"
echo " ABG Analyzer Pro - Automatic Build"
echo "========================================"

cd "$ROOT"

echo "[1/4] Checking Python-for-Android..."

P4A="$ROOT/.buildozer/android/platform/python-for-android"

if [ ! -f "$P4A/pythonforandroid/recipes/python3/__init__.py" ]; then
    echo "ERROR: python-for-android is missing."
    exit 1
fi

P4A_PY=$(grep -E "version = ['\"]" \
    "$P4A/pythonforandroid/recipes/python3/__init__.py" \
    | head -1)

echo "p4a Python recipe: $P4A_PY"

echo "[2/4] Preparing OpenSSL cache..."

mkdir -p "$OPENSSL_DIR"

if [ -f "$OPENSSL_FILE" ] && [ "$(stat -c%s "$OPENSSL_FILE")" -gt 1000000 ]; then
    echo "OpenSSL already cached:"
    ls -lh "$OPENSSL_FILE"
else
    echo "Downloading OpenSSL 1.1.1w..."

    rm -f "$OPENSSL_FILE"

    curl -fL \
        --retry 8 \
        --retry-delay 3 \
        --connect-timeout 30 \
        -A "Mozilla/5.0" \
        "https://github.com/openssl/openssl/archive/refs/tags/OpenSSL_1_1_1w.tar.gz" \
        -o "$OPENSSL_FILE"

    if [ ! -s "$OPENSSL_FILE" ]; then
        echo "ERROR: OpenSSL download failed."
        exit 1
    fi

    echo "OpenSSL downloaded:"
    ls -lh "$OPENSSL_FILE"
fi

echo "[3/4] Verifying OpenSSL archive..."

tar -tzf "$OPENSSL_FILE" >/dev/null

echo "OpenSSL archive OK."

echo "[4/4] Starting Buildozer..."

buildozer -v android debug

echo
echo "========================================"
echo " BUILD FINISHED"
echo "========================================"
