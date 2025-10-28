#!/bin/bash
# PTC - Simple Start Script (like Bitcoin)
# Just run this and you're connected to the global PTC network!

echo "🌐 Starting PTC (Private Coin)..."
echo "🔄 Connecting to global PTC network..."
echo ""

# Start PTC daemon (connects automatically to global network)
python3 ptc_mainnet_daemon.py &
DAEMON_PID=$!

# Wait for daemon to start
sleep 3

# Start web wallet
python3 ptc_web_wallet.py &
WALLET_PID=$!

echo ""
echo "✅ PTC is now running!"
echo "🌐 Wallet: http://127.0.0.1:8888"
echo "📊 Dashboard: http://127.0.0.1:8080"
echo ""
echo "Press Ctrl+C to stop PTC"

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping PTC...'; kill $DAEMON_PID $WALLET_PID 2>/dev/null; echo '✅ PTC stopped'; exit 0" INT

# Keep script running
wait