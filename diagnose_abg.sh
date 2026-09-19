#!/usr/bin/env bash

set +e

echo "===== ABG ANALYZER PRO DIAGNOSTIC ====="
echo
echo "DATE:"
date
echo

echo "===== OS ====="
cat /etc/os-release | grep -E 'PRETTY_NAME|VERSION='
uname -a
echo

echo "===== PYTHON ====="
which python3
python3 --version
python3 -m pip --version
echo

echo "===== GIT ====="
which git
git --version
echo

echo "===== BUILDOZER ====="
which buildozer
buildozer --version
echo

echo "===== JAVA ====="
which java
java -version
echo

echo "===== PROJECT ====="
pwd
ls -lah
echo

echo "===== BUILDOZER SPEC ====="
grep -E '^(requirements|android\.api|android\.minapi|android\.ndk|android\.ndk_path|android\.archs|android\.enable_androidx|android\.sdk_path|p4a\.source_dir|package\.name|package\.domain)' buildozer.spec 2>/dev/null
echo

echo "===== ANDROID SDK ====="
SDK="/mnt/c/Users/Emd/AppData/Local/Android/Sdk"
if [ -d "$SDK" ]; then
    echo "SDK=$SDK"
    echo "--- platforms ---"
    find "$SDK/platforms" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort
    echo "--- build-tools ---"
    find "$SDK/build-tools" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort
    echo "--- cmdline-tools ---"
    find "$SDK/cmdline-tools" -maxdepth 2 -type f -name sdkmanager 2>/dev/null
    echo "--- ndk ---"
    find "$SDK/ndk" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort
else
    echo "SDK NOT FOUND"
fi
echo

echo "===== SDKMANAGER ====="
SDKMANAGER="$SDK/cmdline-tools/latest/bin/sdkmanager"
if [ -x "$SDKMANAGER" ]; then
    "$SDKMANAGER" --version
else
    echo "sdkmanager NOT FOUND at:"
    echo "$SDKMANAGER"
fi
echo

echo "===== BUILD DIRECTORY ====="
if [ -d .buildozer ]; then
    du -sh .buildozer
    echo "--- android platform ---"
    ls -lah .buildozer/android/platform 2>/dev/null
    echo "--- downloads ---"
    find .buildozer -type f -name '*.tar.gz' -o -name '*.zip' 2>/dev/null | tail -30
else
    echo ".buildozer does not exist"
fi
echo

echo "===== P4A ====="
P4A=".buildozer/android/platform/python-for-android"
if [ -d "$P4A" ]; then
    git -C "$P4A" rev-parse --short HEAD 2>/dev/null
    git -C "$P4A" status --short 2>/dev/null | head
    grep -R "python 3.14" -n "$P4A/pythonforandroid/recipes/python3" 2>/dev/null | head
else
    echo "P4A NOT FOUND"
fi
echo

echo "===== CRITICAL PACKAGES ====="
python3 - <<'PY'
mods = ["buildozer","Cython","setuptools","build","wheel","kivy"]
for m in mods:
    try:
        x = __import__(m)
        print(f"{m}: {getattr(x,'__version__','unknown')}")
    except Exception as e:
        print(f"{m}: NOT AVAILABLE ({e})")
PY

echo
echo "===== DISK ====="
df -h /
echo

echo "===== MEMORY ====="
free -h
echo

echo "===== END ====="
