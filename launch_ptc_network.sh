#!/bin/bash
# PTC Network Launcher - Connects to unified PTC network

echo "🌐 Launching PTC Network Node..."
echo "🔍 Scanning for existing PTC nodes on network..."

PEER_NODES=""

# Check common local network ranges
echo "Scanning 192.168.1.x range..."
for ip in $(seq 1 254); do
    target="192.168.1.$ip"
    timeout 0.1 bash -c "</dev/tcp/$target/19443" 2>/dev/null && {
        echo "✅ Found PTC node at $target:19443"
        if [ -z "$PEER_NODES" ]; then
            PEER_NODES="$target:19444"
        else
            PEER_NODES="$PEER_NODES,$target:19444"
        fi
    }
done

# Check 192.168.0.x range
echo "Scanning 192.168.0.x range..."
for ip in $(seq 1 254); do
    target="192.168.0.$ip"
    timeout 0.1 bash -c "</dev/tcp/$target/19443" 2>/dev/null && {
        echo "✅ Found PTC node at $target:19443"
        if [ -z "$PEER_NODES" ]; then
            PEER_NODES="$target:19444"
        else
            PEER_NODES="$PEER_NODES,$target:19444"
        fi
    }
done

if [ -z "$PEER_NODES" ]; then
    echo "🆕 No existing nodes found - starting new network"
else
    echo "🤝 Found PTC network peers: $PEER_NODES"
    export PTC_PEER_NODES="$PEER_NODES"
fi

echo ""
echo "🚀 Starting PTC daemon with network connectivity..."
python3 ptc_mainnet_daemon.py