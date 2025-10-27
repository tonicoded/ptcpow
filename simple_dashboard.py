#!/usr/bin/env python3
"""
Simple PTC Dashboard - Just Works
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request

class SimpleDashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Get real data directly
            try:
                data = {"jsonrpc": "2.0", "method": "getinfo", "params": [], "id": 1}
                data_encoded = json.dumps(data).encode('utf-8')
                
                request = urllib.request.Request(
                    'http://127.0.0.1:19443',
                    data=data_encoded,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(request, timeout=3) as response:
                    result = json.loads(response.read().decode())
                    if "result" in result:
                        stats = result["result"]
                        status = "ONLINE"
                        status_color = "#27ae60"
                    else:
                        stats = {}
                        status = "ERROR"
                        status_color = "#e74c3c"
            except:
                stats = {}
                status = "OFFLINE"
                status_color = "#e74c3c"
            
            blocks = stats.get("blocks", "---")
            difficulty = stats.get("difficulty", "---")
            mining = "Active" if stats.get("mining", False) else "Inactive"
            privacy = "Enabled" if stats.get("privacy_enabled", False) else "Disabled"
            network = "Mainnet" if not stats.get("testnet", True) else "Testnet"
            reward = stats.get("block_reward", "---")
            version = stats.get("version", "---")
            
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>🌐 PTC Mainnet Dashboard</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .header h1 {{ font-size: 3em; margin-bottom: 10px; }}
        .status {{ 
            background: {status_color};
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            font-size: 1.5em;
        }}
        .stats {{ 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.8;
        }}
        .info-section {{
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
        }}
        .refresh-btn {{
            background: #3498db;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 20px auto;
            display: block;
        }}
        .refresh-btn:hover {{ background: #2980b9; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>PTC Dashboard</h1>
            <p>Privacy-Focused Cryptocurrency - Mainnet Ready</p>
        </div>
        
        <div class="status">
            PTC DAEMON {status} - Network: {network}
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{blocks}</div>
                <div class="stat-label">Blocks Mined</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{difficulty:,}</div>
                <div class="stat-label">Network Difficulty</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{reward}</div>
                <div class="stat-label">Block Reward (PTC)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{version}</div>
                <div class="stat-label">Core Version</div>
            </div>
        </div>
        
        <div class="info-section">
            <h2>Network Status</h2>
            <p><strong>Mining:</strong> {mining}</p>
            <p><strong>Privacy:</strong> {privacy}</p>
            <p><strong>Network:</strong> {network}</p>
            <p><strong>RPC Server:</strong> http://127.0.0.1:19443</p>
        </div>
        
        <div class="info-section">
            <h2>Privacy Features</h2>
            <p><strong>Ring Signatures</strong> - Hide transaction sender</p>
            <p><strong>Bulletproofs</strong> - Hide transaction amounts</p>
            <p><strong>Stealth Addresses</strong> - Hide recipients</p>
            <p><strong>Mandatory Privacy</strong> - Cannot be disabled</p>
        </div>
        
        <div class="info-section">
            <h2>Quick Commands</h2>
            <p><strong>Check Balance:</strong></p>
            <code>./ptc_wallet.sh balance</code>
            
            <p><strong>Generate Address:</strong></p>
            <code>./ptc_wallet.sh address</code>
            
            <p><strong>Send PTC:</strong></p>
            <code>./ptc_wallet.sh send ADDRESS AMOUNT</code>
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">Refresh Data</button>
        
        <div style="text-align: center; margin-top: 30px; opacity: 0.7;">
            <p>PTC (Private Coin) Mainnet Dashboard</p>
            <p>Real Blockchain - Real Mining - Real Privacy</p>
        </div>
    </div>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 8080), SimpleDashboard)
    print("🌐 Simple PTC Dashboard starting on http://127.0.0.1:8080")
    print("✅ This dashboard directly connects to your PTC daemon")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
        server.shutdown()