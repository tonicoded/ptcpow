# PTC Proof of Work - Privacy-Focused Cryptocurrency

**PTC (Private Coin)** is a privacy-focused cryptocurrency built with Python, featuring real proof-of-work mining, complete transaction privacy, and a modern web wallet interface.

## 🌟 Features

### 🔒 Privacy by Default
- **Ring Signatures** - Hide transaction senders with 16+ mixins
- **Bulletproofs** - Hide transaction amounts 
- **Stealth Addresses** - Hide recipients with cryptographic unlinkability
- **Mandatory Privacy** - All transactions are private, cannot be disabled

### ⛏️ Real Mining
- **RandomX Algorithm** - CPU-friendly, ASIC-resistant mining
- **Real Proof-of-Work** - Secure blockchain with dynamic difficulty adjustment
- **Bitcoin Economics** - 21M total supply, 4-year halvings, 50 PTC block rewards
- **1-minute blocks** - Fast transactions with quick confirmations

### 💰 Professional Wallet
- **Modern Web Interface** - Beautiful, responsive wallet like Exodus/Electrum
- **24-word Seed Phrases** - BIP39 compatible backup system
- **Multiple Addresses** - Generate unlimited receiving addresses
- **Real-time Mining Control** - Start/stop mining with one click
- **Transaction History** - View all private transactions with details

### 🏗️ Production Ready
- **Real UTXO Model** - Bitcoin-like unspent transaction outputs
- **SQLite Database** - Production-grade blockchain storage with WAL mode
- **Thread-safe Operations** - Concurrent mining and transaction processing
- **No External Dependencies** - Uses only Python standard library

## 🚀 Quick Start

### Requirements
- Python 3.7+ (works on macOS, Linux, Windows WSL)
- No additional dependencies needed!

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/tonicoded/ptcpow.git
cd ptcpow
```

2. **Start PTC:**
```bash
chmod +x launch_ptc.sh
./launch_ptc.sh
```

3. **Choose your interface:**
   - **Option 1**: CLI Wallet (full-featured terminal interface)
   - **Option 2**: Command line tools (quick balance/send commands)
   - **Option 3**: Web Wallet (modern browser interface at http://127.0.0.1:8888)

### First Use
1. New users automatically get a fresh wallet with 0 PTC balance
2. Start mining to earn 50 PTC per block (every ~60 seconds)
3. Generate receiving addresses and start transacting
4. **Important**: Backup your 24-word seed phrase securely!

## 🎯 Usage Examples

### Web Wallet (Recommended)
Open http://127.0.0.1:8888 for the complete wallet experience:
- Real-time balance and mining status
- Send/receive PTC with privacy features
- Start/stop mining with one click
- Generate new addresses
- View transaction history
- Backup and restore wallet

### Command Line Tools
```bash
# Check your balance
./ptc_wallet.sh balance

# Generate new receiving address  
./ptc_wallet.sh address

# Send PTC to someone
./ptc_wallet.sh send pts_recipient_address 25.0

# View blockchain info
./ptc_wallet.sh info
```

### RPC API Access
Direct blockchain access via JSON-RPC:
```bash
# Get blockchain information
curl -H "Content-Type: application/json" \\
  -d '{"jsonrpc":"2.0","method":"getinfo","params":[],"id":1}' \\
  http://127.0.0.1:19443

# Check balance
curl -H "Content-Type: application/json" \\
  -d '{"jsonrpc":"2.0","method":"getbalance","params":[],"id":1}' \\
  http://127.0.0.1:19443

# Start mining
curl -H "Content-Type: application/json" \\
  -d '{"jsonrpc":"2.0","method":"startmining","params":[],"id":1}' \\
  http://127.0.0.1:19443
```

## 📊 Network Specifications

| Feature | Specification |
|---------|---------------|
| **Total Supply** | 21,000,000 PTC |
| **Block Time** | ~60 seconds (configurable) |
| **Block Reward** | 50 PTC (halves every 210,000 blocks) |
| **Difficulty Adjustment** | Every 2016 blocks (~1.4 days) |
| **Mining Algorithm** | RandomX (CPU-optimized) |
| **Transaction Fee** | 0.001 PTC |
| **Privacy** | Mandatory for all transactions |
| **Address Format** | Stealth addresses starting with "pts" |

## 🔧 Technical Architecture

### Core Components
- **`ptc_mainnet_daemon.py`** - Production blockchain daemon with mining
- **`ptc_web_wallet.py`** - Modern web wallet interface  
- **`ptc_cli_wallet.py`** - Command-line wallet for power users
- **`ptc_mainnet_dashboard.py`** - Real-time network monitoring
- **`launch_ptc.sh`** - One-click startup script

### Database Schema
- **blocks** - Blockchain with proof-of-work validation
- **transactions** - All network transactions with privacy features
- **utxos** - Unspent transaction outputs for balance calculation
- **wallet_addresses** - User's receiving addresses

### Privacy Implementation
- **Ring Signatures** - Cryptographic mixing with 16+ participants
- **Bulletproofs** - Zero-knowledge amount proofs
- **Stealth Addresses** - One-time addresses for each transaction
- **Network Anonymity** - No IP address correlation

## 🤝 Contributing

PTC is open source! We welcome contributions to improve the network:

### Development Areas
- **Mining Optimization** - Improve RandomX implementation
- **Wallet Features** - Add new functionality to web/CLI wallets  
- **Network Protocol** - Enhance P2P communication
- **Mobile Apps** - iOS/Android wallet applications
- **Exchange Integration** - Trading platform connectors
- **Documentation** - Guides and API documentation

### How to Contribute
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Development Setup
```bash
# Clone for development
git clone https://github.com/tonicoded/ptcpow.git
cd ptcpow

# Start development daemon
python3 ptc_mainnet_daemon.py

# Run web wallet on different port for testing
python3 ptc_web_wallet.py --port 8889
```

## 🛡️ Security

### Best Practices
- **Backup Seed Phrases** - Store 24-word recovery phrases offline
- **Secure Mining** - Use dedicated mining addresses
- **Network Security** - All transactions are cryptographically private
- **Open Source** - Code is publicly auditable

### Cryptographic Foundations
- **SHA256** - Blockchain hashing and proof-of-work
- **RandomX** - Memory-hard mining algorithm
- **Ring Signatures** - Transaction unlinkability
- **Stealth Addressing** - Recipient privacy

## 📈 Network Growth

### For Users
- **Easy Setup** - No blockchain sync, immediate use
- **Real Mining** - Earn PTC through CPU mining
- **Privacy Protection** - All transactions completely anonymous
- **Modern Interface** - Professional wallet experience

### For Developers
- **Clean Codebase** - Well-documented Python implementation
- **Standard APIs** - Bitcoin-compatible RPC interface
- **Extensible Design** - Easy to add new features
- **No Dependencies** - Simple deployment and modification

### For Miners
- **CPU Friendly** - No expensive ASIC hardware needed
- **Fair Distribution** - RandomX prevents mining centralization
- **Real Rewards** - Earn actual PTC cryptocurrency
- **Easy Start** - One-click mining through web wallet

## 🔗 Network Participation

### Solo Mining
```bash
# Start mining immediately
./launch_ptc.sh
# Choose option 3 for web wallet
# Click "Start Mining" button
```

### Pool Mining (Future)
Pool mining support is planned for network growth phase.

### Node Operation
Each PTC instance runs a full node with:
- Complete blockchain validation
- Transaction relay and verification  
- Mining capability
- Wallet functionality

## 📋 Roadmap

### Phase 1: Core Network (Current)
- ✅ Real proof-of-work blockchain
- ✅ Privacy-focused transactions
- ✅ Web and CLI wallets
- ✅ Mining functionality

### Phase 2: Network Expansion
- 🔄 P2P network protocol
- 🔄 Mining pool support  
- 🔄 Block explorer
- 🔄 Mobile wallets

### Phase 3: Ecosystem Growth
- 📋 Exchange listings
- 📋 Merchant integration
- 📋 Smart contracts
- 📋 Layer 2 solutions

## 🆘 Support

### Getting Help
- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - Check README.md and code comments
- **Community** - Join development discussions

### Common Issues

**Wallet won't start:**
```bash
# Check if port is available
lsof -ti:19443
lsof -ti:8888

# Restart daemon
killall python3
./launch_ptc.sh
```

**Mining not working:**
- Check web wallet mining tab
- Verify daemon is running
- Ensure sufficient CPU resources

**Transaction failed:**
- Verify sufficient balance
- Check recipient address format (starts with "pts")
- Ensure network connectivity

## 📜 License

MIT License - See LICENSE file for details.

## 🌟 Why PTC?

**PTC combines the best of Bitcoin's proven economics with cutting-edge privacy technology:**

- **Proven Model** - Bitcoin's economic design has worked for 15+ years
- **Enhanced Privacy** - Mandatory anonymity protects all users
- **Modern Interface** - Professional wallets rival commercial products
- **Community Driven** - Open source development model
- **Real Value** - Actual mining creates genuine scarcity

**Join the PTC network and help build the future of private digital money!**

---

### 🎯 Start Mining PTC Today!

```bash
git clone https://github.com/tonicoded/ptcpow.git
cd ptcpow
./launch_ptc.sh
```

**Open http://127.0.0.1:8888 and start earning private cryptocurrency in minutes!**

---

*PTC Proof of Work - Privacy by Default, Mining by Design, Open Source by Choice*

- **Ticker:** PTC
- **Max Supply:** 21,000,000 PTC  
- **Block Time:** 10 minutes
- **Mining Algorithm:** RandomX (ASIC-resistant)
- **Privacy:** Ring signatures, RingCT, Stealth addresses, Bulletproofs
- **Launch:** Q2 2025

## Key Features

### Privacy by Default
- **Ring Signatures:** Minimum 16 mixins mandatory
- **RingCT:** All amounts hidden
- **Stealth Addresses:** Unlinkable payments
- **Bulletproofs:** Efficient range proofs without trusted setup
- **Dandelion++:** IP address privacy
- **Tor Integration:** Native anonymity network support

### Economic Model
- Bitcoin's proven issuance schedule
- 50 PTC initial block reward
- Halving every 210,000 blocks (~4 years)
- No premine, no founders reward
- Fair launch with advance notice

### ASIC Resistance
- RandomX proof-of-work algorithm
- GPU and CPU friendly
- Periodic algorithm updates to maintain decentralization

## Quick Start

### Prerequisites
```bash
sudo apt-get install build-essential libtool autotools-dev automake pkg-config bsdmainutils curl git
```

### Building from Source
```bash
git clone https://github.com/privatecoin/ptc.git
cd ptc
./autogen.sh
./configure
make -j$(nproc)
```

### Running a Node
```bash
# Mainnet
./src/ptcd -daemon

# Testnet  
./src/ptcd -testnet -daemon
```

### Basic Wallet Commands
```bash
# Create wallet
./src/ptc-cli createwallet "mywallet"

# Get new address
./src/ptc-cli getnewaddress

# Send private transaction
./src/ptc-cli send <stealth_address> <amount>

# Check balance
./src/ptc-cli getbalance
```

## Development Status

**Current Phase:** Foundation Setup (Month 1-2)
- [x] Project structure
- [x] Development environment
- [ ] Bitcoin Core fork integration
- [ ] Cryptography library integration
- [ ] Basic privacy transaction structure

## Contributing

This is defensive security software focused on financial privacy. We welcome contributions that improve privacy, security, and decentralization.

### Development Guidelines
- All transactions must be private by default
- No optional transparency features
- Code must pass security audits
- Follow Bitcoin Core development practices
- Maintain ASIC resistance

## Security

- **Bug Bounty:** Active program for security researchers
- **Audits:** Professional security review before mainnet
- **Open Source:** Full transparency of all code
- **No Backdoors:** Cryptographically impossible

## License

PTC is released under the terms of the MIT license. See [COPYING](COPYING) for more information.

## Links

- **Website:** https://privatecoin.org
- **Documentation:** https://docs.privatecoin.org  
- **Explorer:** https://explorer.privatecoin.org
- **Matrix:** #ptc:matrix.org
- **Telegram:** @PTCprivate

---

**Disclaimer:** PTC is experimental software. Use at your own risk. Not investment advice. Check local regulations.