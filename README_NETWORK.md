# 🌐 PTC Network Setup Guide

**How to connect multiple PCs to the same PTC network**

## 🔧 Quick Setup

### Computer 1 (First Node)
```bash
git clone https://github.com/tonicoded/ptcpow.git
cd ptcpow
python3 ptc_mainnet_daemon.py &
python3 ptc_web_wallet.py &
```

### Computer 2 (Connecting Node)  
```bash
git clone https://github.com/tonicoded/ptcpow.git
cd ptcpow

# Set Computer 1's IP address
export PTC_PEER_NODES="192.168.1.100:19444"  # Replace with Computer 1's IP

python3 ptc_mainnet_daemon.py &
python3 ptc_web_wallet.py &
```

## 🌐 Automatic Network Discovery

Use the network launcher for automatic peer discovery:

```bash
./launch_ptc_network.sh
```

This script will:
- 🔍 Scan your local network for existing PTC nodes
- 🤝 Automatically connect to found nodes
- 🆕 Start a new network if none found

## 📡 Manual Network Configuration

### Option 1: Environment Variable
```bash
export PTC_PEER_NODES="192.168.1.100:19444,192.168.1.101:19444"
python3 ptc_mainnet_daemon.py
```

### Option 2: Find Network Nodes
```bash
# Scan for PTC nodes on your network
nmap -p 19443 192.168.1.0/24 | grep "open"
```

## ✅ Verify Network Connection

Check if nodes are connected:
```bash
curl -s -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"getinfo","params":[],"id":1}' http://127.0.0.1:19443
```

Look for "Network Peers" in the daemon output:
```
Network Peers: 2/3  # 2 active out of 3 known peers
```

## 🎯 Network Features

- **Automatic Sync**: Blockchains sync automatically between nodes
- **Shared Network**: All nodes share the same PTC blockchain
- **Cross-PC Transactions**: Send PTC between different computers
- **Unified Mining**: Mining rewards distributed across network

## 🚀 Testing Multi-PC Setup

1. **Start Node 1** on Computer A
2. **Start Node 2** on Computer B with Computer A's IP
3. **Create wallets** on both computers
4. **Send PTC** from Computer A to Computer B
5. **Verify** transaction appears on both nodes

Both computers will now share the same PTC blockchain! 🎉

## 🔧 Troubleshooting

- **No peers found**: Check firewall settings, ensure port 19443 is open
- **Sync issues**: Restart both nodes, check network connectivity
- **Different balances**: Wait for sync to complete (usually <30 seconds)

---

**Your PTC network is now unified across multiple computers!** 🌐