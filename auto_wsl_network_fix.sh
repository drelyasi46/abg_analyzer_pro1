#!/usr/bin/env bash
set +e

echo "=== AUTOMATIC WSL NETWORK REPAIR ==="

echo "[1] Restarting WSL DNS/network configuration..."

sudo resolvectl flush-caches 2>/dev/null

sudo bash -c 'cat > /etc/resolv.conf <<EOF
nameserver 1.1.1.1
nameserver 8.8.8.8
EOF'

echo "[2] Testing connectivity..."

for i in {1..5}; do
    if curl -L --connect-timeout 10 -sS https://pypi.org >/dev/null 2>&1; then
        echo "[OK] Internet is available."
        break
    fi

    echo "[WAIT] Network unavailable. Retry $i/5..."
    sleep 5
done

echo "[3] Testing Python package server..."

if curl -L --connect-timeout 15 -sS https://files.pythonhosted.org >/dev/null 2>&1; then
    echo "[OK] files.pythonhosted.org reachable."
else
    echo "[WARN] files.pythonhosted.org still unreachable."
fi

echo "[4] Configuring pip retries..."

export PIP_DEFAULT_TIMEOUT=120
export PIP_RETRIES=15

mkdir -p ~/.config/pip

cat > ~/.config/pip/pip.conf <<EOF
[global]
timeout = 120
retries = 15
EOF

echo "[5] Resuming ABG build..."

cd ~/abg_analyzer_pro

buildozer android debug

echo
echo "=== AUTOMATIC REPAIR FINISHED ==="
