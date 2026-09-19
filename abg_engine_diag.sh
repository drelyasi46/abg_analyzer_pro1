#!/usr/bin/env bash

set +e

echo "=============================================="
echo "       ABG ANALYZER PRO - ENGINE DIAG"
echo "=============================================="
echo

echo "[1] SYSTEM"
echo "Ubuntu:"
lsb_release -ds 2>/dev/null
echo "Kernel:"
uname -a
echo

echo "[2] PROJECT"
echo "PWD: $(pwd)"
echo
echo "--- buildozer.spec ---"
grep -E '^(title|package.name|package.domain|requirements|android.api|android.minapi|android.ndk|android.archs|android.sdk_path|android.ndk_path|p4a.source_dir)' buildozer.spec 2>/dev/null
echo

echo "[3] PYTHON"
command -v python3
python3 --version
python3 -m pip --version
echo

echo "[4] BUILDOZER"
command -v buildozer
buildozer --version
echo

echo "[5] PYTHON-FOR-ANDROID"
P4A_DIR=".buildozer/android/platform/python-for-android"

if [ -d "$P4A_DIR" ]; then
    echo "p4a directory: FOUND"
    cd "$P4A_DIR"
    git rev-parse --is-inside-work-tree 2>/dev/null
    git rev-parse --short HEAD 2>/dev/null
    git status --short 2>/dev/null | head -20
    cd - >/dev/null
else
    echo "p4a directory: NOT FOUND"
fi
echo

echo "[6] ANDROID SDK"
SDK="/mnt/c/Users/Emd/AppData/Local/Android/Sdk"

if [ -d "$SDK" ]; then
    echo "SDK: FOUND -> $SDK"
else
    echo "SDK: NOT FOUND"
fi

echo
echo "Platforms:"
find "$SDK/platforms" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort | tail -20

echo
echo "Build-tools:"
find "$SDK/build-tools" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort | tail -20

echo
echo "NDK:"
find "$SDK/ndk" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort

echo

echo "[7] SDKMANAGER"
SDKMANAGER="$SDK/cmdline-tools/latest/bin/sdkmanager"

if [ -x "$SDKMANAGER" ]; then
    echo "sdkmanager: FOUND"
    "$SDKMANAGER" --version 2>&1 | head -20
else
    echo "sdkmanager: NOT FOUND"
fi
echo

echo "[8] ADB"
ADB="$SDK/platform-tools/adb.exe"

if [ -f "$ADB" ]; then
    echo "ADB: FOUND"
    "$ADB" version 2>&1 | head -5
    echo
    "$ADB" devices 2>&1
else
    echo "ADB: NOT FOUND"
fi
echo

echo "[9] BUILD CACHE"
echo ".buildozer size:"
du -sh .buildozer 2>/dev/null

echo
echo "Downloaded archives:"
find .buildozer -type f \( \
    -name "*.tar.gz" -o \
    -name "*.zip" -o \
    -name "*.tar.bz2" \
    \) 2>/dev/null | tail -30

echo

echo "[10] IMPORTANT RECIPE FILES"
find .buildozer/android/platform/python-for-android/pythonforandroid/recipes \
    -maxdepth 2 -type f \
    \( -name "*.py" -o -name "*.recipe" \) \
    2>/dev/null | grep -E \
    'python3|openssl|libwebp|sdl2_image|libjpeg|libpng|libffi|setuptools|cython' \
    | head -100

echo

echo "[11] DISK"
df -h "$HOME" /
echo

echo "[12] MEMORY"
free -h
echo

echo "[13] CRITICAL ERROR SCAN"
if [ -f buildozer.log ]; then
    echo "--- buildozer.log errors ---"
    grep -Ei \
    'error:|exception:|traceback|failed|timeout|403|404|ssl|ModuleNotFoundError|No such file|Android.mk|recipe' \
    buildozer.log 2>/dev/null | tail -100
else
    echo "buildozer.log not found"
fi

echo
echo "=============================================="
echo "              DIAG COMPLETE"
echo "=============================================="
