#!/usr/bin/env python3
"""
PTC Global Network - Simple like Bitcoin
Just start and connect to the global PTC network automatically
"""

import json
import time
import urllib.request
import urllib.error
import threading
import logging
import random

logger = logging.getLogger(__name__)

class PTCGlobalNetwork:
    """Simple global PTC network - connects automatically like Bitcoin"""
    
    def __init__(self, rpc_port: int = 19443):
        self.rpc_port = rpc_port
        self.sync_enabled = True
        
        # Global PTC seed nodes - hardcoded like Bitcoin
        self.seed_nodes = [
            "ptc-seed1.ptcnetwork.org:19443",
            "ptc-seed2.ptcnetwork.org:19443", 
            "ptc-seed3.ptcnetwork.org:19443",
            # Fallback to public servers
            "167.99.80.45:19443",  # Example public node
            "134.209.102.23:19443", # Example public node
            # Local testing
            "127.0.0.1:19443"
        ]
        
        self.active_peers = []
        
    def start(self):
        """Start connecting to global PTC network"""
        logger.info("🌐 Connecting to global PTC network...")
        
        # Find working seed nodes
        threading.Thread(target=self._connect_to_network, daemon=True).start()
        threading.Thread(target=self._sync_blockchain, daemon=True).start()
        
    def _connect_to_network(self):
        """Connect to global PTC network automatically"""
        while self.sync_enabled and len(self.active_peers) < 3:
            # Try random seed nodes
            random.shuffle(self.seed_nodes)
            
            for seed in self.seed_nodes[:5]:  # Try max 5 seeds
                try:
                    if self._test_node(seed):
                        if seed not in self.active_peers:
                            self.active_peers.append(seed)
                            logger.info(f"🤝 Connected to PTC network via {seed}")
                            
                        if len(self.active_peers) >= 3:
                            break
                            
                except Exception as e:
                    logger.debug(f"Could not connect to {seed}: {e}")
                    
            if len(self.active_peers) == 0:
                logger.warning("🔄 No PTC nodes found, retrying in 10 seconds...")
                time.sleep(10)
            else:
                break
                
        if len(self.active_peers) > 0:
            logger.info(f"✅ Connected to global PTC network ({len(self.active_peers)} peers)")
        else:
            logger.warning("⚠️  Running offline - will retry connecting")
            
    def _test_node(self, node_address: str) -> bool:
        """Test if a node is accessible"""
        try:
            result = self._peer_rpc_call(node_address, "getinfo")
            return result.get("blocks", 0) > 0
        except:
            return False
            
    def _sync_blockchain(self):
        """Sync with global PTC blockchain"""
        while self.sync_enabled:
            time.sleep(15)  # Sync every 15 seconds
            
            if not self.active_peers:
                continue
                
            try:
                local_height = self._get_local_height()
                
                # Find the best peer (highest block count)
                best_peer = None
                best_height = local_height
                
                for peer in self.active_peers:
                    try:
                        peer_height = self._get_peer_height(peer)
                        if peer_height > best_height:
                            best_height = peer_height
                            best_peer = peer
                    except:
                        continue
                        
                # Sync from best peer if needed
                if best_peer and best_height > local_height:
                    logger.info(f"📥 Syncing blockchain: {local_height} → {best_height} (from {best_peer})")
                    # In a real implementation, we would sync the missing blocks
                    
            except Exception as e:
                logger.debug(f"Sync error: {e}")
                
    def _get_local_height(self) -> int:
        """Get local blockchain height"""
        try:
            result = self._local_rpc_call("getinfo")
            return result.get("blocks", 0)
        except:
            return 0
            
    def _get_peer_height(self, peer: str) -> int:
        """Get peer blockchain height"""
        try:
            result = self._peer_rpc_call(peer, "getinfo")
            return result.get("blocks", 0)
        except:
            return 0
            
    def _local_rpc_call(self, method: str, params: list = None) -> dict:
        """Make RPC call to local daemon"""
        if params is None:
            params = []
            
        data = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
        data_encoded = json.dumps(data).encode('utf-8')
        
        request = urllib.request.Request(
            f'http://127.0.0.1:{self.rpc_port}',
            data=data_encoded,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(request, timeout=3) as response:
            result = json.loads(response.read().decode())
            return result.get("result", {})
            
    def _peer_rpc_call(self, peer: str, method: str, params: list = None) -> dict:
        """Make RPC call to peer node"""
        if params is None:
            params = []
            
        data = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
        data_encoded = json.dumps(data).encode('utf-8')
        
        request = urllib.request.Request(
            f'http://{peer}',
            data=data_encoded,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode())
            return result.get("result", {})
            
    def get_network_status(self) -> dict:
        """Get network status"""
        return {
            "connected": len(self.active_peers) > 0,
            "peers": len(self.active_peers),
            "network": "global_ptc",
            "active_peers": self.active_peers
        }
        
    def broadcast_transaction(self, tx_data: dict):
        """Broadcast transaction to network"""
        for peer in self.active_peers:
            try:
                self._peer_rpc_call(peer, "submittransaction", [tx_data])
                logger.info(f"📢 Broadcasted transaction to {peer}")
            except Exception as e:
                logger.debug(f"Failed to broadcast to {peer}: {e}")
                
    def stop(self):
        """Stop network sync"""
        self.sync_enabled = False
        logger.info("🛑 Disconnected from global PTC network")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    network = PTCGlobalNetwork()
    network.start()
    
    try:
        while True:
            time.sleep(5)
            status = network.get_network_status()
            if status["connected"]:
                logger.info(f"🌐 PTC Global Network: {status['peers']} peers connected")
            else:
                logger.info("🔄 Connecting to PTC network...")
    except KeyboardInterrupt:
        network.stop()