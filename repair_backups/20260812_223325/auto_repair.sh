#!/usr/bin/env bash
set -u

PROJECT="$HOME/abg_analyzer_pro"
BACKUP_ROOT="$PROJECT/repair_backups"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP="$BACKUP_ROOT/$STAMP"
LOG="$PROJECT/auto_repair_$STAMP.log"

mkdir -p "$BACKUP"

echo "============================================================"
echo " ABG Analyzer Pro - AUTO REPAIR"
echo "============================================================"
echo "Project : $PROJECT"
echo "Backup  : $BACKUP"
echo "Log     : $LOG"
echo

log() {
    echo "$*" | tee -a "$LOG"
}

backup_file() {
    local f="$1"
    if [ -f "$f" ]; then
        cp -a "$f" "$BACKUP/"
        log "BACKUP: $f"
    fi
}

test_url() {
    local name="$1"
    local url="$2"

    log ""
    log "TEST: $name"
    log "URL : $url"

    if curl -4 -I -L --connect-timeout 8 --max-time 15 \
        -sS "$url" >/dev/null 2>&1; then
        log "RESULT: PASS"
        return 0
    else
        log "RESULT: FAIL"
        return 1
    fi
}

test_git() {
    local name="$1"
    local url="$2"

    log ""
    log "TEST: $name"
    log "GIT : $url"

    if timeout 20 git ls-remote "$url" HEAD >/dev/null 2>&1; then
        log "RESULT: PASS"
        return 0
    else
        log "RESULT: FAIL"
        return 1
    fi
}

log "[1/10] Creating safe backup..."

backup_file "$PROJECT/buildozer.spec"
backup_file "$PROJECT/main.py"
backup_file "$PROJECT/auto_repair.sh"

log "Backup completed."

log ""
log "[2/10] Recording configuration..."

{
    echo
    echo "=== buildozer.spec ==="
    grep -n -E \
        "requirements|p4a.source_dir|p4a.url|p4a.branch|p4a.commit|android.api|android.minapi|android.ndk|android.ndk_path|android.archs" \
        "$PROJECT/buildozer.spec" 2>/dev/null || true

    echo
    echo "=== Python ==="
    python3 --version 2>&1 || true

    echo
    echo "=== Buildozer ==="
    buildozer --version 2>&1 || true

    echo
    echo "=== Git ==="
    git --version 2>&1 || true

    echo
    echo "=== NDK ==="
    find "$HOME/.buildozer/android/platform" \
        -maxdepth 2 -type d -name "android-ndk*" \
        2>/dev/null || true
} | tee -a "$LOG"

log ""
log "[3/10] Testing DNS..."

if getent hosts github.com >/tmp/abg_github_dns 2>/dev/null; then
    log "DNS: PASS"
    cat /tmp/abg_github_dns | tee -a "$LOG"
else
    log "DNS: FAIL"
fi

log ""
log "[4/10] Testing IPv4 connectivity..."

IPV4_OK=0

if test_url "GitHub IPv4 HTTPS" "https://github.com"; then
    IPV4_OK=1
fi

log ""
log "[5/10] Testing IPv6 connectivity..."

if curl -6 -I --connect-timeout 8 --max-time 12 \
    -sS https://github.com >/dev/null 2>&1; then
    log "IPv6: PASS"
else
    log "IPv6: FAIL (not necessarily a problem)"
fi

log ""
log "[6/10] Testing GitHub Git access..."

GIT_OK=0

if test_git "GitHub JPEG repository" \
    "https://github.com/libsdl-org/jpeg.git"; then
    GIT_OK=1
fi

log ""
log "[7/10] Testing Windows network from WSL..."

WINDOWS_IP=""

if command -v powershell.exe >/dev/null 2>&1; then

    log "PowerShell detected."

    WIN_RESULT="$(
        powershell.exe -NoProfile -Command \
        "try {
            \$r = Test-NetConnection github.com -Port 443 -WarningAction SilentlyContinue
            if (\$r.TcpTestSucceeded) { 'WINDOWS_GITHUB_443=PASS' }
            else { 'WINDOWS_GITHUB_443=FAIL' }
        } catch {
            'WINDOWS_GITHUB_443=ERROR'
        }" 2>/dev/null |
        tr -d '\r'
    )"

    log "$WIN_RESULT"

else
    log "PowerShell executable not available from WSL."
fi

log ""
log "[8/10] Inspecting existing JPEG checkout/cache..."

JPEG_DIR="$PROJECT/.buildozer/android/platform/build-arm64-v8a/build/bootstrap_builds/sdl2/jni/SDL2_image/external/jpeg"

if [ -d "$JPEG_DIR/.git" ]; then
    log "JPEG checkout already exists:"
    log "$JPEG_DIR"

    if git -C "$JPEG_DIR" rev-parse HEAD >/dev/null 2>&1; then
        log "JPEG checkout: VALID"
    else
        log "JPEG checkout: INVALID"
    fi
else
    log "JPEG checkout: NOT FOUND"
fi

log ""
log "[9/10] Inspecting p4a/NDK configuration..."

P4A_DIR="$PROJECT/.buildozer/android/platform/python-for-android"

if [ -d "$P4A_DIR" ]; then

    python3 - <<PY 2>&1 | tee -a "$LOG"
import sys

sys.path.insert(0, "$P4A_DIR")

try:
    import pythonforandroid
    from pythonforandroid import recommendations as r

    print("p4a version =", pythonforandroid.__version__)
    print("p4a path    =", pythonforandroid.__file__)
    print("recommended =", r.RECOMMENDED_NDK_VERSION)
    print("minimum    =", r.MIN_NDK_VERSION)
    print("maximum    =", r.MAX_NDK_VERSION)
    print("API        =", r.RECOMMENDED_NDK_API)

except Exception as e:
    print("p4a inspection failed:", repr(e))
PY

else
    log "p4a directory not found."
fi

log ""
log "[10/10] Automatic decision..."

echo
echo "============================================================"
echo " AUTOMATIC DIAGNOSIS"
echo "============================================================"

if [ "$GIT_OK" -eq 1 ]; then

    log "GitHub Git access is WORKING."
    log "The network is not currently blocking the JPEG checkout."
    log "No repair was necessary."

elif [ "$IPV4_OK" -eq 1 ]; then

    log "GitHub HTTPS works, but Git clone failed."
    log "Likely Git-specific configuration/problem."
    log "No destructive repair performed."

else

    log "WSL cannot establish HTTPS connection to GitHub."
    log ""
    log "PRIMARY BLOCKER:"
    log "    WSL -> github.com:443 CONNECTION FAILURE"
    log ""
    log "Affected component:"
    log "    SDL2_image -> external/jpeg"
    log ""
    log "SAFE ACTION:"
    log "    No NDK change"
    log "    No Kivy change"
    log "    No p4a change"
    log "    No cache deletion"
    log "    No .buildozer deletion"

    if command -v powershell.exe >/dev/null 2>&1; then
        log ""
        log "Windows network test was performed automatically."
        log "If Windows has GitHub access while WSL does not,"
        log "the next repair stage can use Windows as the download path."
    fi

fi

echo
echo "============================================================"
echo " SAFETY STATUS"
echo "============================================================"
echo "NO rm -rf .buildozer"
echo "NO rm -rf ~/.buildozer"
echo "NO NDK replacement"
echo "NO Kivy replacement"
echo "NO p4a replacement"
echo
echo "Backup:"
echo "$BACKUP"
echo
echo "Log:"
echo "$LOG"
echo "============================================================"

rm -f /tmp/abg_github_dns 2>/dev/null || true

