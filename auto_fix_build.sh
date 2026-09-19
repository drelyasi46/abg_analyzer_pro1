#!/usr/bin/env bash
set -e

APP="$HOME/abg_analyzer_pro"
cd "$APP"

echo "=========================================="
echo " ABG Analyzer Pro - AUTOMATIC REPAIR"
echo "=========================================="

echo "[1/7] Checking buildozer.spec..."

sed -i 's/^requirements *=.*/requirements = python3==3.11.5,kivy==2.2.1/' buildozer.spec
sed -i 's/^android.api *=.*/android.api = 34/' buildozer.spec
sed -i 's/^android.minapi *=.*/android.minapi = 24/' buildozer.spec
sed -i 's/^android.ndk *=.*/android.ndk = 27c/' buildozer.spec

if ! grep -q '^requirements *=.*python3==3.11.5' buildozer.spec; then
    echo "ERROR: requirements could not be fixed."
    exit 1
fi

echo "[2/7] Removing stale Buildozer Python-for-Android environment..."

rm -rf "$APP/.buildozer/android/platform/python-for-android"
rm -rf "$APP/.buildozer/android/platform/build-arm64-v8a"
rm -rf "$APP/.buildozer/android/platform/build-armeabi-v7a"

echo "[3/7] Removing stale distributions..."

rm -rf "$APP/.buildozer/android/platform/build-arm64-v8a/dists"
rm -rf "$APP/.buildozer/android/platform/build-arm64-v8a/build"

echo "[4/7] Clearing Buildozer cache for this project..."

rm -rf "$APP/.buildozer/android/platform/python-for-android"
rm -rf "$APP/.buildozer/android/platform/build-arm64-v8a"

echo "[5/7] Installing compatible python-for-android..."

P4A_DIR="/tmp/python-for-android-2024.01.21"

if [ ! -d "$P4A_DIR" ]; then
    curl -L --fail --retry 5 \
      --connect-timeout 30 \
      -o /tmp/p4a-2024.01.21.tar.gz \
      https://github.com/kivy/python-for-android/archive/refs/tags/v2024.01.21.tar.gz

    rm -rf "$P4A_DIR"
    tar -xzf /tmp/p4a-2024.01.21.tar.gz -C /tmp/
fi

mkdir -p "$APP/.buildozer/android/platform"

cp -a "$P4A_DIR" \
      "$APP/.buildozer/android/platform/python-for-android"

echo "[6/7] Verifying Python recipe..."

P4A_PY="$APP/.buildozer/android/platform/python-for-android/pythonforandroid/recipes/python3/__init__.py"

VERSION=$(grep -oP "version = '\K[0-9.]+" "$P4A_PY" | head -1)

echo "p4a Python version: $VERSION"

if [ "$VERSION" != "3.11.5" ]; then
    echo "ERROR: incompatible python-for-android detected."
    exit 1
fi

echo "Python 3.11.5 compatibility confirmed."

echo "[7/7] Starting clean Android build..."

buildozer -v android debug

echo
echo "=========================================="
echo " BUILD FINISHED"
echo "=========================================="
