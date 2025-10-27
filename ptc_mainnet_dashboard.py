#!/usr/bin/env python3
"""
PTC Mainnet Dashboard - Clear and User-Friendly
Real-time monitoring of PTC blockchain
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
import time

class PTCMainnetDashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html>
<head>
    <title>🌐 PTC Mainnet Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
        }
        
        .header { 
            text-align: center; 
            padding: 30px 0 40px 0;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .status-banner {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .status-banner.offline {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
        }
        
        .live-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #fff;
            border-radius: 50%;
            margin-right: 10px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        
        .stat-card { 
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px; 
            border-radius: 20px; 
            text-align: center; 
            transition: transform 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-card:hover { 
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            display: block;
        }
        
        .stat-value { 
            font-size: 2.8em; 
            font-weight: bold; 
            margin-bottom: 10px;
            background: linear-gradient(45deg, #fff, #f8f9fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label { 
            font-size: 1.1em; 
            opacity: 0.9;
        }
        
        .info-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .info-section h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        .feature-item .icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        
        .commands-section {
            background: rgba(52, 73, 94, 0.8);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .command-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            margin: 10px 0;
            border-left: 4px solid #3498db;
            overflow-x: auto;
            white-space: nowrap;
        }
        
        .footer { 
            text-align: center; 
            padding: 30px 0;
            opacity: 0.8;
        }
        
        .network-health {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .health-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 25px;
            border-radius: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .loading { opacity: 0.6; }
        .error { color: #e74c3c; }
        .success { color: #27ae60; }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .stat-value { font-size: 2em; }
            body { padding: 10px; }
        }
    </style>
    <script>
        let updateInterval;
        let lastUpdateTime = 0;
        
        function formatNumber(num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            } else if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toLocaleString();
        }
        
        function updateStats() {
            const now = Date.now();
            
            // Show loading state
            document.querySelectorAll('.stat-value').forEach(el => {
                el.classList.add('loading');
            });
            
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    lastUpdateTime = now;
                    console.log('Received data:', data);
                    
                    if (data.error) {
                        console.error('API returned error:', data.error);
                        showOfflineState();
                        return;
                    }
                    
                    console.log('Data is valid, showing online state');
                    showOnlineState(data);
                    updateNetworkHealth(data);
                })
                .catch(error => {
                    console.error('Stats update failed:', error);
                    showOfflineState();
                })
                .finally(() => {
                    document.querySelectorAll('.stat-value').forEach(el => {
                        el.classList.remove('loading');
                    });
                });
        }
        
        function showOnlineState(data) {
            const statusBanner = document.getElementById('status-banner');
            statusBanner.className = 'status-banner';
            statusBanner.innerHTML = `
                <h2><span class="live-indicator"></span>🌐 PTC MAINNET LIVE</h2>
                <p>Real blockchain mining and transactions active</p>
            `;
            
            // Update stats with proper formatting
            document.getElementById('blocks').textContent = formatNumber(data.blocks || 0);
            document.getElementById('difficulty').textContent = formatNumber(data.difficulty || 0);
            document.getElementById('reward').textContent = (data.block_reward || 50).toFixed(1) + ' PTC';
            document.getElementById('version').textContent = (data.version || 0).toLocaleString();
            
            // Update additional info
            document.getElementById('network-type').textContent = data.testnet ? 'Testnet' : 'Mainnet';
            document.getElementById('mining-status').textContent = data.mining ? 'Active' : 'Inactive';
            document.getElementById('privacy-status').textContent = data.privacy_enabled ? 'Enabled' : 'Disabled';
        }
        
        function showOfflineState() {
            const statusBanner = document.getElementById('status-banner');
            statusBanner.className = 'status-banner offline';
            statusBanner.innerHTML = `
                <h2>🔴 PTC DAEMON OFFLINE</h2>
                <p>Unable to connect to PTC daemon on port 19443</p>
            `;
            
            document.getElementById('blocks').textContent = '---';
            document.getElementById('difficulty').textContent = '---';
            document.getElementById('reward').textContent = '---';
            document.getElementById('version').textContent = '---';
            
            console.log('Dashboard showing offline state');
        }
        
        function updateNetworkHealth(data) {
            const healthContainer = document.getElementById('network-health');
            healthContainer.innerHTML = `
                <div class="health-item">
                    <span>🔗</span>
                    <span>Connections: ${data.connections || 0}</span>
                </div>
                <div class="health-item">
                    <span>⛏️</span>
                    <span>Mining: ${data.mining ? 'Active' : 'Inactive'}</span>
                </div>
                <div class="health-item">
                    <span>🔒</span>
                    <span>Privacy: ${data.privacy_enabled ? 'Enabled' : 'Disabled'}</span>
                </div>
                <div class="health-item">
                    <span>🌐</span>
                    <span>Network: ${data.testnet ? 'Testnet' : 'Mainnet'}</span>
                </div>
            `;
        }
        
        function startAutoUpdate() {
            updateStats(); // Initial update
            updateInterval = setInterval(updateStats, 5000); // Update every 5 seconds
        }
        
        function stopAutoUpdate() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        }
        
        window.addEventListener('load', startAutoUpdate);
        window.addEventListener('beforeunload', stopAutoUpdate);
        
        // Update last update time display
        setInterval(() => {
            if (lastUpdateTime > 0) {
                const elapsed = Math.floor((Date.now() - lastUpdateTime) / 1000);
                document.getElementById('last-update').textContent = 
                    elapsed < 60 ? `${elapsed}s ago` : `${Math.floor(elapsed/60)}m ago`;
            }
        }, 1000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 PTC Dashboard</h1>
            <p>Privacy-Focused Cryptocurrency • Real Blockchain Monitoring</p>
        </div>
        
        <div id="status-banner" class="status-banner">
            <h2><span class="live-indicator"></span>Loading...</h2>
            <p>Connecting to PTC daemon...</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-icon">📦</span>
                <div class="stat-value" id="blocks">Loading...</div>
                <div class="stat-label">Blocks Mined</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">⚙️</span>
                <div class="stat-value" id="difficulty">Loading...</div>
                <div class="stat-label">Network Difficulty</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">💰</span>
                <div class="stat-value" id="reward">Loading...</div>
                <div class="stat-label">Block Reward</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">🏷️</span>
                <div class="stat-value" id="version">Loading...</div>
                <div class="stat-label">Core Version</div>
            </div>
        </div>
        
        <div class="info-section">
            <h2>🔒 Privacy Features</h2>
            <p style="text-align: center; margin-bottom: 20px;">All transactions are private by default</p>
            <div class="feature-grid">
                <div class="feature-item">
                    <span class="icon">🎭</span>
                    <div>
                        <strong>Ring Signatures</strong><br>
                        <small>Hide transaction sender</small>
                    </div>
                </div>
                <div class="feature-item">
                    <span class="icon">🔐</span>
                    <div>
                        <strong>Bulletproofs</strong><br>
                        <small>Hide transaction amounts</small>
                    </div>
                </div>
                <div class="feature-item">
                    <span class="icon">👻</span>
                    <div>
                        <strong>Stealth Addresses</strong><br>
                        <small>Hide recipients</small>
                    </div>
                </div>
                <div class="feature-item">
                    <span class="icon">🛡️</span>
                    <div>
                        <strong>Mandatory Privacy</strong><br>
                        <small>Cannot be disabled</small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="commands-section">
            <h2>💻 Quick Commands</h2>
            <p style="margin-bottom: 20px;">Test PTC functionality with these commands:</p>
            
            <h3>Check Wallet Balance:</h3>
            <div class="command-box">
                curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"getbalance","params":[],"id":1}' http://127.0.0.1:19443
            </div>
            
            <h3>Generate New Address:</h3>
            <div class="command-box">
                curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"getnewaddress","params":[],"id":1}' http://127.0.0.1:19443
            </div>
            
            <h3>Send PTC (25 PTC to address):</h3>
            <div class="command-box">
                curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"sendtoaddress","params":["pts_ADDRESS_HERE",25.0],"id":1}' http://127.0.0.1:19443
            </div>
            
            <h3>Easy Wallet Script:</h3>
            <div class="command-box">
                ./ptc_wallet.sh balance
            </div>
        </div>
        
        <div class="info-section">
            <h2>📊 Network Health</h2>
            <div id="network-health" class="network-health">
                Loading network status...
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🌐 PTC (Private Coin) Mainnet Dashboard</strong></p>
            <p>Last updated: <span id="last-update">Just now</span></p>
            <p style="margin-top: 10px; opacity: 0.7;">
                Privacy by Default • Bitcoin Economics • Real Blockchain Technology
            </p>
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get stats from PTC daemon
            try:
                # Create the JSON-RPC request
                data = {"jsonrpc": "2.0", "method": "getinfo", "params": [], "id": 1}
                data_encoded = json.dumps(data).encode('utf-8')
                
                request = urllib.request.Request(
                    'http://127.0.0.1:19443',
                    data=data_encoded,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(request, timeout=5) as response:
                    result = json.loads(response.read().decode())
                    if "result" in result and result["result"]:
                        stats = result["result"]
                        # Ensure we have all required fields
                        stats.setdefault("blocks", 0)
                        stats.setdefault("difficulty", 0)
                        stats.setdefault("connections", 0)
                        stats.setdefault("version", 0)
                        stats.setdefault("mining", False)
                        stats.setdefault("privacy_enabled", False)
                        stats.setdefault("testnet", False)
                        stats.setdefault("block_reward", 50.0)
                    else:
                        stats = {"error": "invalid_response"}
                        
            except urllib.error.URLError as e:
                stats = {"error": f"connection_failed: {str(e)}"}
            except urllib.error.HTTPError as e:
                stats = {"error": f"http_error: {e.code}"}
            except json.JSONDecodeError as e:
                stats = {"error": f"json_error: {str(e)}"}
            except Exception as e:
                stats = {"error": f"unknown_error: {str(e)}"}
            
            self.wfile.write(json.dumps(stats).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        return  # Suppress HTTP logs

if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 8080), PTCMainnetDashboard)
    print("🌐 PTC Mainnet Dashboard starting...")
    print("✅ Dashboard available at: http://127.0.0.1:8080")
    print("📊 Real-time blockchain monitoring active")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
        server.shutdown()