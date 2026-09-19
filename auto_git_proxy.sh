#!/bin/bash

set -u

WIN_GIT="/mnt/c/Program Files/Git/cmd/git.exe"

if [ ! -f "$WIN_GIT" ]; then
    echo "ERROR: Windows Git not found:"
    echo "$WIN_GIT"
    exit 1
fi

echo "=============================================="
echo " ABG Analyzer Pro - Automatic Git Dependency"
echo "=============================================="

echo
echo "[1] WSL Git:"
/usr/bin/git --version

echo
echo "[2] Windows Git:"
"$WIN_GIT" --version

echo
echo "[3] Creating automatic Git wrapper..."

mkdir -p "$HOME/bin"

cat > "$HOME/bin/git" <<'WRAPPER'
#!/bin/bash

WIN_GIT="/mnt/c/Program Files/Git/cmd/git.exe"

if [ "$1" = "clone" ]; then
    shift

    DEPTH=""
    BRANCH=""
    RECURSIVE=""
    URL=""
    DEST=""

    ARGS=()

    while [ $# -gt 0 ]; do
        case "$1" in
            --depth)
                DEPTH="$2"
                shift 2
                ;;
            -b)
                BRANCH="$2"
                shift 2
                ;;
            --recursive)
                RECURSIVE="--recursive"
                shift
                ;;
            *)
                if [[ "$1" == https://github.com/* ]]; then
                    URL="$1"
                    shift
                else
                    DEST="$1"
                    shift
                fi
                ;;
        esac
    done

    echo
    echo "=============================================="
    echo " AUTOMATIC WINDOWS-GIT CLONE"
    echo " URL:  $URL"
    echo " DEST: $DEST"
    echo "=============================================="
    echo

    if [ -z "$URL" ] || [ -z "$DEST" ]; then
        echo "ERROR: Could not parse git clone command."
        exit 1
    fi

    rm -rf "$DEST"

    mkdir -p "$(dirname "$DEST")"

    WIN_DEST=$(wslpath -w "$DEST")

    CMD=("$WIN_GIT")

    if [ -n "$DEPTH" ]; then
        CMD+=(--depth "$DEPTH")
    fi

    if [ -n "$BRANCH" ]; then
        CMD+=(-b "$BRANCH")
    fi

    if [ -n "$RECURSIVE" ]; then
        CMD+=(--recursive)
    fi

    CMD+=("$URL" "$WIN_DEST")

    echo "Running Windows Git..."
    "${CMD[@]}"

    CODE=$?

    if [ $CODE -ne 0 ]; then
        echo
        echo "Windows Git clone FAILED."
        exit $CODE
    fi

    echo
    echo "Clone completed."

    # Remove Git metadata so python-for-android does not treat
    # this as a live Git repository/submodule tree.
    if [ -d "$DEST" ]; then
        find "$DEST" -name ".git" -exec rm -rf -- {} \; 2>/dev/null || true
    fi

    echo "Git metadata cleaned."
    exit 0
fi

exec /usr/bin/git "$@"
WRAPPER

chmod +x "$HOME/bin/git"

export PATH="$HOME/bin:$PATH"
hash -r

echo
echo "[4] Active Git:"
which git
git --version

echo
echo "[5] Windows Git test:"
"$WIN_GIT" ls-remote https://github.com/libsdl-org/libjxl.git HEAD

echo
echo "=============================================="
echo " AUTOMATIC GIT HANDLER READY"
echo "=============================================="
echo
echo "Now run:"
echo
echo "buildozer -v android debug"
