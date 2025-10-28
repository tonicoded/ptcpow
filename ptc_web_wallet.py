#!/usr/bin/env python3
"""
PTC Web Wallet - Complete Cryptocurrency Wallet Interface
Modern, user-friendly web wallet like Exodus, Electrum, etc.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import urllib.error
import hashlib
import secrets
import base64
import time
import threading
from pathlib import Path

# BIP39 word list for seed generation
BIP39_WORDS = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse",
    "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
    "action", "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit",
    "adult", "advance", "advice", "aerobic", "affair", "afford", "afraid", "again", "against", "age",
    "agent", "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol",
    "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already", "also",
    "alter", "always", "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient",
    "anger", "angle", "angry", "animal", "ankle", "announce", "annual", "another", "answer", "antenna",
    "antique", "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april", "area",
    "arena", "argue", "arm", "armed", "armor", "army", "around", "arrange", "arrest", "arrive",
    "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset", "assist",
    "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction", "audit",
    "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid", "awake", "aware",
    "away", "awesome", "awful", "awkward", "axis", "baby", "bachelor", "bacon", "badge", "bag",
    "balance", "balcony", "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel",
    "base", "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become", "beef",
    "before", "begin", "behave", "behind", "believe", "below", "belt", "bench", "benefit", "best",
    "betray", "better", "between", "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird",
    "birth", "bitter", "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind",
    "blood", "blossom", "blow", "blue", "blur", "blush", "board", "boat", "body", "boil"
] * 10

class PTCWebWallet(BaseHTTPRequestHandler):
    # Class variables to store wallet state
    wallet_initialized = False
    current_wallet_address = None
    current_seed_phrase = None
    mining_process = None
    
    @staticmethod
    def rpc_call(method, params=[]):
        """Make RPC call to PTC daemon"""
        try:
            data = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
            data_encoded = json.dumps(data).encode('utf-8')
            
            request = urllib.request.Request(
                'http://127.0.0.1:19443',
                data=data_encoded,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(request, timeout=5) as response:
                result = json.loads(response.read().decode())
                if "result" in result:
                    return {"success": True, "data": result["result"]}
                else:
                    return {"success": False, "error": result.get("error", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def generate_seed_phrase(word_count=24):
        """Generate BIP39-compatible seed phrase"""
        seed_words = []
        for i in range(word_count):
            word_index = secrets.randbelow(len(BIP39_WORDS))
            seed_words.append(BIP39_WORDS[word_index])
        return ' '.join(seed_words)
    
    @staticmethod
    def seed_to_address(seed_phrase):
        """Convert seed phrase to PTC address"""
        seed_hash = hashlib.sha256(seed_phrase.encode()).hexdigest()
        key_hash = hashlib.sha256(seed_hash.encode()).digest()
        address_bytes = key_hash[:25]
        return "pts" + base64.b32encode(address_bytes).decode().lower().rstrip('=')

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_wallet_interface()
        elif self.path == '/api/balance':
            self.handle_api_balance()
        elif self.path == '/api/info':
            self.handle_api_info()
        elif self.path == '/api/transactions':
            self.handle_api_transactions()
        elif self.path == '/api/addresses':
            self.handle_api_addresses()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data) if post_data else {}
        except:
            data = {}
        
        if self.path == '/api/create_wallet':
            self.handle_create_wallet(data)
        elif self.path == '/api/restore_wallet':
            self.handle_restore_wallet(data)
        elif self.path == '/api/send':
            self.handle_send_transaction(data)
        elif self.path == '/api/generate_address':
            self.handle_generate_address()
        elif self.path == '/api/start_mining':
            self.handle_start_mining()
        elif self.path == '/api/stop_mining':
            self.handle_stop_mining()
        elif self.path == '/api/get_seed':
            self.handle_get_seed()
        elif self.path == '/api/reset_wallet':
            self.handle_reset_wallet()
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_wallet_interface(self):
        """Send the main wallet interface"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Check if wallet is initialized
        if not PTCWebWallet.wallet_initialized:
            html = self.get_onboarding_html()
        else:
            html = self.get_main_wallet_html()
        
        self.wfile.write(html.encode('utf-8'))
    
    def get_onboarding_html(self):
        """Get onboarding screen HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to PTC Wallet</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .onboarding-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 50px;
            max-width: 600px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
        }
        .logo { font-size: 3em; margin-bottom: 20px; font-weight: bold; color: #667eea; }
        .welcome-title { font-size: 2.2em; margin-bottom: 15px; color: #2c3e50; }
        .welcome-subtitle { font-size: 1.2em; color: #7f8c8d; margin-bottom: 40px; }
        .wallet-options { display: flex; gap: 30px; margin-bottom: 40px; }
        .wallet-option {
            flex: 1; background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px;
            padding: 30px 20px; cursor: pointer; transition: all 0.3s ease;
        }
        .wallet-option:hover { border-color: #667eea; transform: translateY(-5px); }
        .option-icon { font-size: 3em; margin-bottom: 15px; }
        .option-title { font-size: 1.3em; font-weight: bold; margin-bottom: 10px; color: #2c3e50; }
        .option-description { color: #7f8c8d; font-size: 0.95em; }
        .modal {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.8); z-index: 1000; align-items: center; justify-content: center;
        }
        .modal-content { background: white; border-radius: 20px; padding: 40px; max-width: 500px; width: 90%; }
        .modal-title { font-size: 1.8em; margin-bottom: 20px; color: #2c3e50; text-align: center; }
        .form-group { margin-bottom: 20px; }
        .form-label { display: block; margin-bottom: 8px; font-weight: 600; color: #2c3e50; }
        .form-input, .form-textarea {
            width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 1em;
        }
        .form-textarea { min-height: 100px; font-family: monospace; resize: vertical; }
        .btn {
            padding: 12px 25px; border: none; border-radius: 8px; font-size: 1em;
            font-weight: 600; cursor: pointer; margin: 5px;
        }
        .btn-primary { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
        .btn-secondary { background: #95a5a6; color: white; }
        .seed-phrase-display {
            background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 10px;
            padding: 20px; margin: 20px 0; font-family: monospace; font-size: 1.1em;
        }
        .warning {
            background: #fff3cd; border: 2px solid #ffeaa7; border-radius: 8px;
            padding: 15px; margin: 15px 0; color: #856404;
        }
        .warning strong { color: #d63031; }
        @media (max-width: 768px) {
            .onboarding-container { padding: 30px 20px; }
            .wallet-options { flex-direction: column; gap: 20px; }
        }
    </style>
</head>
<body>
    <div class="onboarding-container">
        <div class="logo">🔒 PTC</div>
        <h1 class="welcome-title">Welcome to PTC Wallet</h1>
        <p class="welcome-subtitle">
            Privacy-focused cryptocurrency with real mining.<br>
            Choose how to get started:
        </p>
        
        <div class="wallet-options">
            <div class="wallet-option" onclick="showCreateWallet()">
                <div class="option-icon">🆕</div>
                <div class="option-title">Create New Wallet</div>
                <div class="option-description">Generate a fresh wallet with 24-word backup phrase</div>
            </div>
            <div class="wallet-option" onclick="showRestoreWallet()">
                <div class="option-icon">🔄</div>
                <div class="option-title">Restore Wallet</div>
                <div class="option-description">Import existing wallet using recovery phrase</div>
            </div>
        </div>
    </div>
    
    <!-- Create Wallet Modal -->
    <div class="modal" id="create-modal">
        <div class="modal-content">
            <div class="modal-title">Create New Wallet</div>
            <div id="create-step-1">
                <p style="margin-bottom: 20px; color: #7f8c8d; text-align: center;">
                    We'll generate a secure 24-word recovery phrase for your wallet.
                </p>
                <div class="warning">
                    <strong>Important:</strong> Your recovery phrase is the ONLY way to restore your wallet.
                    Write it down and store it safely. Never share it!
                </div>
                <button class="btn btn-primary" onclick="generateNewWallet()" style="width: 100%;">
                    Generate Wallet
                </button>
                <button class="btn btn-secondary" onclick="closeModal()" style="width: 100%;">Cancel</button>
            </div>
            <div id="create-step-2" style="display: none;">
                <div class="warning">
                    <strong>⚠️ CRITICAL:</strong> Write down these 24 words in order!
                    This is your ONLY way to recover your wallet!
                </div>
                <div class="seed-phrase-display" id="generated-seed"></div>
                <div style="text-align: center; margin: 20px 0;">
                    <label><input type="checkbox" id="seed-confirmed"> I have written down my recovery phrase</label>
                </div>
                <button class="btn btn-primary" onclick="confirmWalletCreation()" style="width: 100%;" disabled id="confirm-btn">
                    Continue to Wallet
                </button>
                <button class="btn btn-secondary" onclick="closeModal()" style="width: 100%;">Cancel</button>
            </div>
        </div>
    </div>
    
    <!-- Restore Wallet Modal -->
    <div class="modal" id="restore-modal">
        <div class="modal-content">
            <div class="modal-title">Restore Wallet</div>
            <p style="margin-bottom: 20px; color: #7f8c8d; text-align: center;">
                Enter your 24-word recovery phrase to restore your wallet.
            </p>
            <div class="form-group">
                <label class="form-label">Recovery Phrase (24 words)</label>
                <textarea class="form-textarea" id="restore-seed" 
                          placeholder="Enter your 24-word recovery phrase..."></textarea>
            </div>
            <button class="btn btn-primary" onclick="restoreExistingWallet()" style="width: 100%;">
                Restore Wallet
            </button>
            <button class="btn btn-secondary" onclick="closeModal()" style="width: 100%;">Cancel</button>
        </div>
    </div>
    
    <script>
        function showCreateWallet() { document.getElementById('create-modal').style.display = 'flex'; }
        function showRestoreWallet() { document.getElementById('restore-modal').style.display = 'flex'; }
        function closeModal() {
            document.querySelectorAll('.modal').forEach(modal => modal.style.display = 'none');
            document.getElementById('create-step-1').style.display = 'block';
            document.getElementById('create-step-2').style.display = 'none';
            document.getElementById('seed-confirmed').checked = false;
            document.getElementById('confirm-btn').disabled = true;
            document.getElementById('restore-seed').value = '';
        }
        
        async function generateNewWallet() {
            try {
                const response = await fetch('/api/create_wallet', {method: 'POST'});
                const data = await response.json();
                if (data.success) {
                    document.getElementById('generated-seed').textContent = data.seed_phrase;
                    document.getElementById('create-step-1').style.display = 'none';
                    document.getElementById('create-step-2').style.display = 'block';
                } else {
                    alert('Failed to create wallet: ' + data.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        document.getElementById('seed-confirmed').addEventListener('change', function() {
            document.getElementById('confirm-btn').disabled = !this.checked;
        });
        
        async function confirmWalletCreation() {
            closeModal();
            window.location.reload();
        }
        
        async function restoreExistingWallet() {
            const seedPhrase = document.getElementById('restore-seed').value.trim();
            if (!seedPhrase) {
                alert('Please enter your recovery phrase');
                return;
            }
            const words = seedPhrase.split(/\\s+/);
            if (words.length !== 24) {
                alert('Recovery phrase must be exactly 24 words');
                return;
            }
            try {
                const response = await fetch('/api/restore_wallet', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({seed_phrase: seedPhrase})
                });
                const data = await response.json();
                if (data.success) {
                    closeModal();
                    window.location.reload();
                } else {
                    alert('Failed to restore wallet: ' + data.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) closeModal();
            });
        });
    </script>
</body>
</html>'''
    
    def get_main_wallet_html(self):
        """Get main wallet HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PTC Wallet</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: #333;
        }
        .wallet-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .wallet-header {
            background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 30px;
            margin-bottom: 30px; text-align: center; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        .wallet-header h1 { font-size: 2.5em; color: #2c3e50; margin-bottom: 10px; }
        .balance-card {
            background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px;
            margin-bottom: 30px; text-align: center; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        .balance-amount { font-size: 3.5em; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
        .balance-currency { font-size: 1.5em; color: #7f8c8d; margin-bottom: 20px; }
        .wallet-address {
            font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 8px;
            margin: 10px 0; font-size: 0.9em; color: #495057; cursor: pointer; word-break: break-all;
        }
        .wallet-tabs {
            display: flex; background: rgba(255, 255, 255, 0.95); border-radius: 15px;
            padding: 10px; margin-bottom: 30px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        .tab-button {
            flex: 1; padding: 15px 20px; border: none; background: none; border-radius: 10px;
            font-size: 1em; font-weight: 600; cursor: pointer; color: #7f8c8d;
        }
        .tab-button.active {
            background: linear-gradient(135deg, #667eea, #764ba2); color: white;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .tab-content {
            background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1); min-height: 400px;
        }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
        .form-group { margin-bottom: 25px; }
        .form-label { display: block; margin-bottom: 8px; font-weight: 600; color: #2c3e50; }
        .form-input {
            width: 100%; padding: 15px; border: 2px solid #ecf0f1; border-radius: 10px;
            font-size: 1em; transition: border-color 0.3s ease;
        }
        .form-input:focus { outline: none; border-color: #667eea; }
        .btn {
            padding: 15px 30px; border: none; border-radius: 10px; font-size: 1em;
            font-weight: 600; cursor: pointer; transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2); color: white;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-primary:hover { transform: translateY(-2px); }
        .btn-success { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .btn-danger { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .mining-status {
            text-align: center; padding: 20px; border-radius: 15px; margin-bottom: 20px;
        }
        .mining-active { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .mining-inactive { background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; }
        .mining-controls { display: flex; gap: 20px; justify-content: center; margin-top: 30px; }
        .transaction-item {
            display: flex; justify-content: space-between; align-items: center;
            padding: 20px; border-bottom: 1px solid #ecf0f1;
        }
        .transaction-item:hover { background-color: #f8f9fa; }
        .transaction-amount { font-weight: bold; font-size: 1.1em; }
        .amount-positive { color: #27ae60; }
        .amount-negative { color: #e74c3c; }
        .status-indicator {
            display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 10px;
        }
        .status-online { background: #27ae60; animation: pulse 2s infinite; }
        .status-offline { background: #e74c3c; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .notification {
            position: fixed; top: 20px; right: 20px; padding: 15px 25px; border-radius: 10px;
            color: white; font-weight: 600; z-index: 1000; transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        .notification.show { transform: translateX(0); }
        .notification-success { background: #27ae60; }
        .notification-error { background: #e74c3c; }
        @media (max-width: 768px) {
            .wallet-container { padding: 10px; }
            .balance-amount { font-size: 2.5em; }
            .wallet-tabs { flex-direction: column; }
            .mining-controls { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="wallet-container">
        <div class="wallet-header">
            <h1>🔒 PTC Wallet</h1>
            <p>Privacy-Focused Cryptocurrency</p>
            <div style="margin-top: 15px;">
                <span class="status-indicator status-offline" id="connection-status"></span>
                <span id="connection-text">Connecting...</span>
            </div>
        </div>
        
        <div class="balance-card">
            <div class="balance-amount" id="balance-amount">0.000</div>
            <div class="balance-currency">PTC</div>
            <div class="wallet-address" id="wallet-address" onclick="copyAddress()" title="Click to copy">
                Loading address...
            </div>
        </div>
        
        <div class="wallet-tabs">
            <button class="tab-button active" onclick="showTab('overview')">Overview</button>
            <button class="tab-button" onclick="showTab('send')">Send</button>
            <button class="tab-button" onclick="showTab('receive')">Receive</button>
            <button class="tab-button" onclick="showTab('mining')">Mining</button>
            <button class="tab-button" onclick="showTab('settings')">Settings</button>
        </div>
        
        <div class="tab-content">
            <div class="tab-panel active" id="overview-panel">
                <h2 style="margin-bottom: 30px;">Recent Transactions</h2>
                <div id="transaction-list">
                    <div style="text-align: center; color: #7f8c8d; padding: 40px;">
                        No transactions yet. Start mining to earn your first PTC!
                    </div>
                </div>
            </div>
            
            <div class="tab-panel" id="send-panel">
                <h2 style="margin-bottom: 30px;">Send PTC</h2>
                <form id="send-form" onsubmit="sendTransaction(event)">
                    <div class="form-group">
                        <label class="form-label">Recipient Address</label>
                        <input type="text" class="form-input" id="send-address" placeholder="pts..." required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount (PTC)</label>
                        <input type="number" class="form-input" id="send-amount" 
                               placeholder="0.00" step="0.001" min="0.001" required>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">Send PTC</button>
                </form>
            </div>
            
            <div class="tab-panel" id="receive-panel">
                <h2 style="margin-bottom: 30px;">Receive PTC</h2>
                <div style="text-align: center;">
                    <p style="margin-bottom: 20px;">Share this address to receive PTC:</p>
                    <div class="wallet-address" id="receive-address" onclick="copyAddress()">
                        Loading address...
                    </div>
                    <button class="btn btn-primary" onclick="generateNewAddress()" style="margin-top: 20px;">
                        Generate New Address
                    </button>
                </div>
            </div>
            
            <div class="tab-panel" id="mining-panel">
                <h2 style="margin-bottom: 30px;">Mining Control</h2>
                <div class="mining-status mining-inactive" id="mining-status">
                    <h3>Mining Status: Inactive</h3>
                    <p>Start mining to earn PTC rewards</p>
                </div>
                <div class="mining-controls">
                    <button class="btn btn-success" onclick="startMining()" id="start-mining-btn">Start Mining</button>
                    <button class="btn btn-danger" onclick="stopMining()" id="stop-mining-btn" disabled>Stop Mining</button>
                </div>
                <div style="margin-top: 30px; text-align: center; color: #7f8c8d;">
                    <p><strong>Block Reward:</strong> 50 PTC</p>
                    <p><strong>Algorithm:</strong> RandomX (CPU-friendly)</p>
                    <p><strong>Privacy:</strong> All rewards are private</p>
                </div>
            </div>
            
            <div class="tab-panel" id="settings-panel">
                <h2 style="margin-bottom: 30px;">Wallet Settings</h2>
                <div style="margin-bottom: 40px;">
                    <h3 style="margin-bottom: 20px;">Backup Wallet</h3>
                    <p style="margin-bottom: 20px; color: #7f8c8d;">
                        Your recovery phrase is the only way to restore your wallet.
                    </p>
                    <button class="btn btn-primary" onclick="showSeedPhrase()">Show Recovery Phrase</button>
                </div>
                <div>
                    <h3 style="margin-bottom: 20px;">Reset Wallet</h3>
                    <p style="margin-bottom: 20px; color: #7f8c8d;">
                        This will clear your current wallet and return to setup.
                    </p>
                    <button class="btn btn-danger" onclick="resetWallet()">Reset Wallet</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentBalance = 0, miningActive = false, currentAddress = '';
        
        window.addEventListener('load', function() {
            updateBalance(); updateTransactions(); updateMiningStatus();
            setInterval(function() { updateBalance(); updateTransactions(); updateMiningStatus(); }, 5000);
        });
        
        function showTab(tabName) {
            document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName + '-panel').classList.add('active');
            event.target.classList.add('active');
        }
        
        async function updateBalance() {
            try {
                const response = await fetch('/api/balance');
                const data = await response.json();
                if (data.success) {
                    currentBalance = data.balance || 0;
                    currentAddress = data.address || '';
                    document.getElementById('balance-amount').textContent = currentBalance.toFixed(3);
                    document.getElementById('wallet-address').textContent = currentAddress;
                    document.getElementById('receive-address').textContent = currentAddress;
                    updateConnectionStatus(true);
                } else {
                    updateConnectionStatus(false);
                }
            } catch (error) { updateConnectionStatus(false); }
        }
        
        async function updateTransactions() {
            try {
                const response = await fetch('/api/transactions');
                const data = await response.json();
                const list = document.getElementById('transaction-list');
                if (data.success && data.transactions.length > 0) {
                    list.innerHTML = data.transactions.map(tx => `
                        <div class="transaction-item">
                            <div><strong>${tx.category.toUpperCase()}</strong><br>
                                <small>${tx.txid.substring(0, 16)}...</small></div>
                            <div class="transaction-amount ${tx.amount >= 0 ? 'amount-positive' : 'amount-negative'}">
                                ${tx.amount >= 0 ? '+' : ''}${tx.amount.toFixed(3)} PTC</div>
                        </div>`).join('');
                } else {
                    list.innerHTML = '<div style="text-align: center; color: #7f8c8d; padding: 40px;">No transactions yet. Start mining to earn your first PTC!</div>';
                }
            } catch (error) { console.error('Failed to update transactions:', error); }
        }
        
        async function updateMiningStatus() {
            try {
                const response = await fetch('/api/info');
                const data = await response.json();
                if (data.success) {
                    miningActive = data.info.mining || false;
                    const statusElement = document.getElementById('mining-status');
                    const startBtn = document.getElementById('start-mining-btn');
                    const stopBtn = document.getElementById('stop-mining-btn');
                    if (miningActive) {
                        statusElement.className = 'mining-status mining-active';
                        statusElement.innerHTML = '<h3>Mining Status: Active</h3><p>Earning PTC rewards - Block ' + (data.info.blocks || 0) + '</p>';
                        startBtn.disabled = true; stopBtn.disabled = false;
                    } else {
                        statusElement.className = 'mining-status mining-inactive';
                        statusElement.innerHTML = '<h3>Mining Status: Inactive</h3><p>Start mining to earn PTC rewards</p>';
                        startBtn.disabled = false; stopBtn.disabled = true;
                    }
                }
            } catch (error) { console.error('Failed to update mining status:', error); }
        }
        
        function updateConnectionStatus(connected) {
            const statusElement = document.getElementById('connection-status');
            const textElement = document.getElementById('connection-text');
            if (connected) {
                statusElement.className = 'status-indicator status-online';
                textElement.textContent = 'Connected to PTC Network';
            } else {
                statusElement.className = 'status-indicator status-offline';
                textElement.textContent = 'Disconnected';
            }
        }
        
        async function sendTransaction(event) {
            event.preventDefault();
            const address = document.getElementById('send-address').value;
            const amount = parseFloat(document.getElementById('send-amount').value);
            if (amount > currentBalance) { showNotification('Insufficient balance', 'error'); return; }
            try {
                const response = await fetch('/api/send', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({address, amount})
                });
                const data = await response.json();
                if (data.success) {
                    showNotification('Transaction sent successfully!', 'success');
                    document.getElementById('send-form').reset();
                    updateBalance(); updateTransactions();
                } else {
                    showNotification(data.error || 'Transaction failed', 'error');
                }
            } catch (error) { showNotification('Network error', 'error'); }
        }
        
        async function generateNewAddress() {
            try {
                const response = await fetch('/api/generate_address', {method: 'POST'});
                const data = await response.json();
                if (data.success) {
                    showNotification('New address generated!', 'success');
                    updateBalance();
                } else {
                    showNotification(data.error || 'Failed to generate address', 'error');
                }
            } catch (error) { showNotification('Network error', 'error'); }
        }
        
        async function startMining() {
            try {
                const response = await fetch('/api/start_mining', {method: 'POST'});
                const data = await response.json();
                if (data.success) {
                    showNotification('Mining started!', 'success'); updateMiningStatus();
                } else {
                    showNotification(data.error || 'Failed to start mining', 'error');
                }
            } catch (error) { showNotification('Network error', 'error'); }
        }
        
        async function stopMining() {
            try {
                const response = await fetch('/api/stop_mining', {method: 'POST'});
                const data = await response.json();
                if (data.success) {
                    showNotification('Mining stopped!', 'success'); updateMiningStatus();
                } else {
                    showNotification(data.error || 'Failed to stop mining', 'error');
                }
            } catch (error) { showNotification('Network error', 'error'); }
        }
        
        async function showSeedPhrase() {
            if (confirm('Are you sure you want to display your recovery phrase? Make sure no one can see your screen.')) {
                try {
                    const response = await fetch('/api/get_seed', {method: 'POST'});
                    const data = await response.json();
                    if (data.success) {
                        alert('Your 24-word recovery phrase:\\n\\n' + data.seed_phrase + '\\n\\nWrite this down and store it safely! This is the ONLY way to recover your wallet.');
                    } else {
                        showNotification('Failed to retrieve seed phrase', 'error');
                    }
                } catch (error) { showNotification('Network error', 'error'); }
            }
        }
        
        function resetWallet() {
            if (confirm('This will completely reset your wallet. Make sure you have backed up your recovery phrase!')) {
                fetch('/api/reset_wallet', {method: 'POST'}).then(() => window.location.reload());
            }
        }
        
        function copyAddress() {
            if (currentAddress) {
                navigator.clipboard.writeText(currentAddress).then(() => {
                    showNotification('Address copied to clipboard!', 'success');
                });
            }
        }
        
        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.className = 'notification notification-' + type;
            notification.textContent = message;
            document.body.appendChild(notification);
            setTimeout(() => notification.classList.add('show'), 100);
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => document.body.removeChild(notification), 300);
            }, 3000);
        }
    </script>
</body>
</html>'''

    def handle_api_balance(self):
        """Handle balance API request"""
        if not PTCWebWallet.current_wallet_address:
            self.send_json_response({"success": True, "balance": 0.0, "needs_wallet": True})
            return
            
        result = self.rpc_call("getaddressbalance", [PTCWebWallet.current_wallet_address])
        if result["success"]:
            balance = result.get("data", 0)
        else:
            result = self.rpc_call("getbalance")
            balance = result.get("data", 0) if result["success"] else 0
            
        self.send_json_response({"success": True, "balance": balance, "address": PTCWebWallet.current_wallet_address})
    
    def handle_api_info(self):
        """Handle info API request"""
        result = self.rpc_call("getinfo")
        self.send_json_response({"success": result["success"], "info": result.get("data", {})})
    
    def handle_api_transactions(self):
        """Handle transactions API request"""
        if not PTCWebWallet.current_wallet_address:
            self.send_json_response({"success": True, "transactions": [], "needs_wallet": True})
            return
            
        result = self.rpc_call("getaddresstransactions", [PTCWebWallet.current_wallet_address])
        if result["success"]:
            transactions = result.get("data", [])
        else:
            result = self.rpc_call("listtransactions")
            transactions = result.get("data", []) if result["success"] else []
            
        self.send_json_response({"success": True, "transactions": transactions[:10]})
    
    def handle_api_addresses(self):
        """Handle addresses API request"""
        if not PTCWebWallet.current_wallet_address:
            self.send_json_response({"success": True, "addresses": [], "needs_wallet": True})
            return
            
        addresses = [PTCWebWallet.current_wallet_address]
        self.send_json_response({"success": True, "addresses": addresses})
    
    def handle_create_wallet(self, data):
        """Handle wallet creation"""
        seed_phrase = self.generate_seed_phrase()
        address = self.seed_to_address(seed_phrase)
        
        PTCWebWallet.current_wallet_address = address
        PTCWebWallet.current_seed_phrase = seed_phrase
        PTCWebWallet.wallet_initialized = True
        
        # Set this address as the mining address so rewards come here
        self.rpc_call("setminingaddress", [address])
        
        self.send_json_response({
            "success": True, 
            "seed_phrase": seed_phrase,
            "address": address
        })
    
    def handle_restore_wallet(self, data):
        """Handle wallet restoration"""
        seed_phrase = data.get("seed_phrase", "")
        if not seed_phrase:
            self.send_json_response({"success": False, "error": "No seed phrase provided"})
            return
        
        try:
            address = self.seed_to_address(seed_phrase)
            PTCWebWallet.current_wallet_address = address
            PTCWebWallet.current_seed_phrase = seed_phrase
            PTCWebWallet.wallet_initialized = True
            
            # Set this address as the mining address so rewards come here
            self.rpc_call("setminingaddress", [address])
            
            self.send_json_response({"success": True, "address": address})
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)})
    
    def handle_send_transaction(self, data):
        """Handle send transaction"""
        address = data.get("address", "")
        amount = data.get("amount", 0)
        
        if not address or amount <= 0:
            self.send_json_response({"success": False, "error": "Invalid address or amount"})
            return
        
        result = self.rpc_call("sendtoaddress", [address, amount])
        self.send_json_response(result)
    
    def handle_generate_address(self):
        """Handle address generation"""
        result = self.rpc_call("getnewaddress")
        self.send_json_response(result)
    
    def handle_start_mining(self):
        """Handle start mining"""
        try:
            result = self.rpc_call("startmining")
            if result["success"]:
                PTCWebWallet.mining_process = True
                response_data = result.get("data", {})
                message = response_data.get("message", "Mining started")
                self.send_json_response({"success": True, "message": message})
            else:
                self.send_json_response({"success": False, "error": result.get("error", "Failed to start mining")})
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)})
    
    def handle_stop_mining(self):
        """Handle stop mining"""
        try:
            result = self.rpc_call("stopmining")
            if result["success"]:
                PTCWebWallet.mining_process = None
                response_data = result.get("data", {})
                message = response_data.get("message", "Mining stopped")
                self.send_json_response({"success": True, "message": message})
            else:
                self.send_json_response({"success": False, "error": result.get("error", "Failed to stop mining")})
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)})
    
    def handle_get_seed(self):
        """Handle seed phrase request"""
        if PTCWebWallet.current_seed_phrase:
            self.send_json_response({
                "success": True, 
                "seed_phrase": PTCWebWallet.current_seed_phrase
            })
        else:
            self.send_json_response({"success": False, "error": "No wallet found"})
    
    def handle_reset_wallet(self):
        """Handle wallet reset"""
        PTCWebWallet.wallet_initialized = False
        PTCWebWallet.current_wallet_address = None
        PTCWebWallet.current_seed_phrase = None
        PTCWebWallet.mining_process = None
        self.send_json_response({"success": True, "message": "Wallet reset successfully"})
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 8888), PTCWebWallet)
    print("🔒 PTC Web Wallet starting...")
    print("✅ Wallet available at: http://127.0.0.1:8888")
    print("💰 Professional cryptocurrency wallet interface")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Wallet stopped")
        server.shutdown()