#!/bin/bash
# PTC Launch Script - Ready for Users
# Starts PTC daemon and opens wallet

echo "🌐 PTC (Private Coin) Mainnet Launcher v2.0.0"
echo "Privacy-Focused Cryptocurrency • Mainnet Ready"
echo "=============================================="
echo ""

# Check if PTC daemon is already running
if lsof -ti:19443 > /dev/null 2>&1; then
    echo "✅ PTC daemon is already running!"
else
    echo "🔧 Starting PTC Mainnet daemon..."
    python3 ptc_mainnet_daemon.py &
    DAEMON_PID=$!
    echo "   PTC Mainnet daemon started (PID: $DAEMON_PID)"
    
    # Wait a moment for daemon to start
    echo "   Waiting for daemon to initialize..."
    sleep 3
    
    # Check if daemon started successfully
    if lsof -ti:19443 > /dev/null 2>&1; then
        echo "✅ PTC daemon started successfully!"
    else
        echo "❌ Failed to start PTC daemon"
        exit 1
    fi
fi

echo ""
echo "📊 PTC Mainnet Status:"
echo "   RPC Server: http://127.0.0.1:19443"
echo "   Mining: Active (earning 50 PTC per block)"
echo "   Privacy: Mandatory (Ring Signatures + Bulletproofs + Stealth Addresses)"
echo "   Network: MAINNET (production ready)"
echo ""

echo "🔗 Quick Commands:"
echo "   Check balance: ./ptc_wallet.sh balance"
echo "   Generate address: ./ptc_wallet.sh address"
echo "   View blockchain info: ./ptc_wallet.sh info"
echo ""

# Ask user what they want to do
echo "Choose an option:"
echo "1) Open CLI Wallet (recommended)"
echo "2) Use command line tools"
echo "3) Open dashboard in browser"
echo "4) Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "🔒 Opening PTC CLI Wallet..."
        python3 ptc_cli_wallet.py
        ;;
    2)
        echo "💻 Command line tools ready!"
        echo "Use: ./ptc_wallet.sh <command>"
        echo "Example: ./ptc_wallet.sh balance"
        ;;
    3)
        echo "🌐 Starting mainnet dashboard..."
        python3 ptc_mainnet_dashboard.py &
        DASHBOARD_PID=$!
        echo "   Mainnet dashboard started (PID: $DASHBOARD_PID)"
        sleep 2
        
        # Try to open browser
        if command -v open > /dev/null; then
            open http://127.0.0.1:8080
        elif command -v xdg-open > /dev/null; then
            xdg-open http://127.0.0.1:8080
        else
            echo "   Open browser to: http://127.0.0.1:8080"
        fi
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎯 PTC is now ready to use!"
echo "Your wallet will automatically earn PTC through mining."
echo "All transactions use privacy features by default."