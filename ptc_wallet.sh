#!/bin/bash
# PTC Wallet Commands - Easy to Use

RPC_URL="http://127.0.0.1:19443"

case "$1" in
    "balance")
        echo "💰 Checking PTC balance..."
        curl -s -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"getbalance","params":[],"id":1}' $RPC_URL | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'Balance: {data[\"result\"]} PTC')"
        ;;
    "address")
        echo "🔑 Generating new stealth address..."
        curl -s -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"getnewaddress","params":[],"id":1}' $RPC_URL | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'New address: {data[\"result\"]}')"
        ;;
    "info")
        echo "📊 PTC blockchain info..."
        curl -s -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"getinfo","params":[],"id":1}' $RPC_URL | python3 -c "import sys,json; data=json.load(sys.stdin); r=data['result']; print(f'Blocks: {r[\"blocks\"]}\\nDifficulty: {r[\"difficulty\"]}\\nMining: {r[\"mining\"]}\\nPrivacy: {r[\"privacy_enabled\"]}')"
        ;;
    "history")
        echo "📜 Recent transactions..."
        curl -s -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"listtransactions","params":[],"id":1}' $RPC_URL | python3 -c "import sys,json; data=json.load(sys.stdin); [print(f'{tx[\"txid\"][:16]}... {tx[\"amount\"]} PTC ({tx[\"category\"]})') for tx in data['result'][:5]]"
        ;;
    "send")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: ./ptc_wallet.sh send <address> <amount>"
            echo "Example: ./ptc_wallet.sh send pts123... 10.5"
            exit 1
        fi
        echo "💸 Sending $3 PTC to $2..."
        curl -s -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"method\":\"sendtoaddress\",\"params\":[\"$2\",$3],\"id\":1}" $RPC_URL | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'Transaction ID: {data[\"result\"]}' if 'result' in data else f'Error: {data[\"error\"][\"message\"]}')"
        ;;
    *)
        echo "🔒 PTC Wallet Commands:"
        echo "  ./ptc_wallet.sh balance    - Check your PTC balance"
        echo "  ./ptc_wallet.sh address    - Generate new stealth address"
        echo "  ./ptc_wallet.sh info       - Show blockchain status"
        echo "  ./ptc_wallet.sh history    - Show recent transactions"
        echo "  ./ptc_wallet.sh send <addr> <amount> - Send PTC"
        echo ""
        echo "Example: ./ptc_wallet.sh send pts123... 10.5"
        ;;
esac