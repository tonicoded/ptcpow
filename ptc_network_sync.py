#!/usr/bin/env python3
"""
PTC Network Sync - Simple HTTP-based blockchain synchronization
Allows multiple PTC nodes to share the same blockchain
"""

import json
import time
import urllib.request
import urllib.error
import threading
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class PTCNetworkSync:
    """Simple HTTP-based network synchronization for PTC blockchain"""
    
    def __init__(self, rpc_port: int = 19443):
        self.rpc_port = rpc_port
        self.peer_nodes = []
        self.sync_enabled = True
        self.last_sync_height = 0
        
        # Load peer nodes from environment or default
        import os
        if os.getenv("PTC_PEER_NODES"):
            self.peer_nodes = os.getenv("PTC_PEER_NODES").split(",")
            logger.info(f"🌐 Using peer nodes: {self.peer_nodes}")
        
    def start_sync(self):
        """Start periodic blockchain synchronization"""
        if not self.peer_nodes:
            logger.info("📡 No peer nodes configured - running in standalone mode")
            return
            
        logger.info("🔄 Starting blockchain synchronization...")
        threading.Thread(target=self._sync_loop, daemon=True).start()
        
    def _sync_loop(self):
        """Main synchronization loop"""
        while self.sync_enabled:
            try:
                self._sync_with_peers()
                time.sleep(10)  # Sync every 10 seconds
            except Exception as e:
                logger.debug(f"Sync error: {e}")
                
    def _sync_with_peers(self):
        """Synchronize blockchain with peer nodes"""
        local_height = self._get_local_height()
        
        for peer in self.peer_nodes:
            try:
                peer_height = self._get_peer_height(peer)
                if peer_height > local_height:
                    logger.info(f"📥 Syncing with {peer} (height {peer_height} vs local {local_height})")
                    self._sync_blocks_from_peer(peer, local_height, peer_height)
                    break  # Only sync from one peer at a time
                    
            except Exception as e:
                logger.debug(f"Could not sync with {peer}: {e}")
                
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
            
    def _sync_blocks_from_peer(self, peer: str, start_height: int, end_height: int):
        """Sync blocks from peer"""
        for height in range(start_height + 1, min(end_height + 1, start_height + 10)):  # Sync max 10 blocks at once
            try:
                block_data = self._peer_rpc_call(peer, "getblock", [height])
                if block_data:
                    # Submit block to local chain
                    self._submit_block_locally(block_data)
                    logger.info(f"📦 Synced block {height} from {peer}")
                    
            except Exception as e:
                logger.debug(f"Failed to sync block {height}: {e}")
                break
                
    def _submit_block_locally(self, block_data: dict):
        """Submit synced block to local blockchain"""
        # This would validate and add the block to local chain
        # For now, we'll use a simplified approach
        try:
            result = self._local_rpc_call("submitblock", [block_data])
            return result
        except Exception as e:
            logger.debug(f"Failed to submit block locally: {e}")
            
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
        
        with urllib.request.urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode())
            return result.get("result", {})
            
    def _peer_rpc_call(self, peer: str, method: str, params: list = None) -> dict:
        """Make RPC call to peer node"""
        if params is None:
            params = []
            
        # Parse peer address
        if ":" in peer:
            host, port = peer.split(":")
            rpc_port = int(port) - 1  # Assume RPC is one port lower
        else:
            host = peer
            rpc_port = 19443
            
        data = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
        data_encoded = json.dumps(data).encode('utf-8')
        
        request = urllib.request.Request(
            f'http://{host}:{rpc_port}',
            data=data_encoded,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode())
            return result.get("result", {})
            
    def broadcast_new_block(self, block_height: int):
        """Broadcast new block to peer nodes"""
        if not self.peer_nodes:
            return
            
        for peer in self.peer_nodes:
            try:
                self._notify_peer_new_block(peer, block_height)
            except Exception as e:
                logger.debug(f"Failed to notify {peer} of new block: {e}")
                
    def _notify_peer_new_block(self, peer: str, height: int):
        """Notify peer of new block"""
        try:
            # Simple notification - peer will sync on next cycle
            logger.debug(f"📢 Notified {peer} of new block {height}")
        except Exception as e:
            logger.debug(f"Notification to {peer} failed: {e}")
            
    def add_peer(self, peer_address: str):
        """Add new peer node"""
        if peer_address not in self.peer_nodes:
            self.peer_nodes.append(peer_address)
            logger.info(f"➕ Added peer: {peer_address}")
            
    def get_network_status(self) -> dict:
        """Get network synchronization status"""
        active_peers = 0
        for peer in self.peer_nodes:
            try:
                self._get_peer_height(peer)
                active_peers += 1
            except:
                pass
                
        return {
            "sync_enabled": self.sync_enabled,
            "peer_count": len(self.peer_nodes),
            "active_peers": active_peers,
            "last_sync_height": self.last_sync_height,
            "peers": self.peer_nodes
        }
        
    def stop(self):
        """Stop network synchronization"""
        self.sync_enabled = False
        logger.info("🛑 Network sync stopped")

if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    sync = PTCNetworkSync()
    sync.start_sync()
    
    try:
        while True:
            time.sleep(5)
            status = sync.get_network_status()
            logger.info(f"Network: {status['active_peers']}/{status['peer_count']} peers active")
    except KeyboardInterrupt:
        sync.stop()