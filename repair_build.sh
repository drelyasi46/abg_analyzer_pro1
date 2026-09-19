#!/usr/bin/env bash

set -u

PROJECT="$HOME/abg_analyzer_pro"
BUILD="$PROJECT/.buildozer"
SDL="$BUILD/android/platform/build-arm64-v8a/build/bootstrap_builds/sdl2/jni/SDL2_image"

echo
echo "=============================================="
echo " ABG Analyzer Pro - Automatic Build Repair"
echo "=============================================="
echo

echo "[1/10] Checking WSL Git..."

REAL_GIT="/usr/bin/git"

if [ ! -x "$REAL_GIT" ]; then
    echo "ERROR: /usr/bin/git not found"
    exit 1
fi

echo "WSL Git:"
"$REAL_GIT" --version

export GIT="$REAL_GIT"

echo
echo "[2/10] Removing Windows Git from current build environment..."

export PATH="/home/babak/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

hash -r

echo "which git:"
which git

echo "git version:"
git --version

echo
echo "[3/10] Cleaning dangerous Git environment variables..."

unset GIT_DIR
unset GIT_WORK_TREE
unset GIT_INDEX_FILE
unset GIT_OBJECT_DIRECTORY
unset GIT_ALTERNATE_OBJECT_DIRECTORIES
unset GIT_COMMON_DIR
unset GIT_CEILING_DIRECTORIES

echo
echo "[4/10] Configuring Git for long paths and safer builds..."

git config --global core.longpaths true
git config --global fetch.writeCommitGraph false
git config --global maintenance.auto false
git config --global gc.auto 0

echo "Git configuration:"
git config --global --get core.longpaths || true
git config --global --get fetch.writeCommitGraph || true
git config --global --get maintenance.auto || true
git config --global --get gc.auto || true

echo
echo "[5/10] Checking GitHub connectivity..."

if git ls-remote https://github.com/libsdl-org/libjxl.git HEAD >/tmp/abg_git_test.txt 2>&1; then
    echo "GitHub connection: OK"
else
    echo "WARNING: GitHub connection failed"
    cat /tmp/abg_git_test.txt
fi

echo
echo "[6/10] Checking project permissions..."

sudo chown -R "$USER:$USER" "$PROJECT" 2>/dev/null || true

chmod -R u+rwX "$PROJECT" 2>/dev/null || true

echo "Project owner:"
stat -c '%U:%G %n' "$PROJECT"

echo
echo "[7/10] Removing broken SDL2_image dependency trees..."

rm -rf "$SDL/external/libjxl"
rm -rf "$SDL/external/zlib"

echo "Old libjxl/zlib trees removed."

echo
echo "[8/10] Removing temporary Git metadata..."

find "$BUILD" -type d -name ".git" -prune -exec rm -rf {} + 2>/dev/null || true

echo "Broken nested Git metadata removed."

echo
echo "[9/10] Checking for WSL path contamination..."

if env | grep -E '(^|:)\/mnt\/c\/Program Files\/Git|wsl.localhost' >/tmp/abg_path_test.txt; then
    echo "WARNING: Windows Git / WSL path contamination detected:"
    cat /tmp/abg_path_test.txt
else
    echo "Environment: clean"
fi

echo
echo "[10/10] Final environment check..."

echo "PATH:"
echo "$PATH"

echo
echo "Git:"
which git
git --version

echo
echo "ANDROIDNDK:"
echo "${ANDROIDNDK:-NOT SET}"

echo
echo "ANDROIDSDK:"
echo "${ANDROIDSDK:-NOT SET}"

echo
echo "Project:"
pwd

echo
echo "Build directory:"
echo "$BUILD"

echo
echo "=============================================="
echo " REPAIR FINISHED"
echo "=============================================="
echo
echo "If all checks above are OK, run:"
echo
echo "    buildozer -v android debug"
echo
