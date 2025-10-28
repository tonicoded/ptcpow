#!/usr/bin/env python3
"""
PTC P2P Network Layer
Connects multiple PTC nodes into one unified network like Bitcoin
"""

import socket
import threading
import json
import time
import logging
from typing import List, Dict, Set
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

class PTCPeer:
    """Represents a peer in the PTC network"""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.last_seen = time.time()
        self.connected = False
        
    def __str__(self):
        return f"{self.host}:{self.port}"

class PTCNetworkNode:
    """P2P Network node for PTC blockchain synchronization"""
    
    def __init__(self, port: int = 19444, rpc_port: int = 19443):
        self.port = port
        self.rpc_port = rpc_port
        self.peers: Dict[str, PTCPeer] = {}
        self.known_nodes: Set[str] = set()
        self.running = False
        self.server_socket = None
        
        # Default seed nodes (you can add more)
        self.seed_nodes = []
        
        # Check for seed node from environment
        if os.getenv("PTC_SEED_NODE"):
            self.seed_nodes.append(os.getenv("PTC_SEED_NODE"))
            logger.info(f"🌱 Using seed node: {os.getenv('PTC_SEED_NODE')}")
        
        # Add local testing nodes
        self.seed_nodes.extend([
            "127.0.0.1:19444",  # Local for testing
            # Add more seed nodes here when deploying
        ])
        
    def start(self):
        """Start the P2P network node"""
        self.running = True
        
        # Start server to accept incoming connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(10)
        
        logger.info(f"🌐 PTC P2P node listening on port {self.port}")
        
        # Start background threads
        threading.Thread(target=self._accept_connections, daemon=True).start()
        threading.Thread(target=self._connect_to_seeds, daemon=True).start()
        threading.Thread(target=self._sync_blockchain, daemon=True).start()
        threading.Thread(target=self._broadcast_blocks, daemon=True).start()
        
    def _accept_connections(self):
        """Accept incoming peer connections"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                peer_id = f"{addr[0]}:{addr[1]}"
                logger.info(f"🤝 New peer connected: {peer_id}")
                
                # Handle peer in background
                threading.Thread(target=self._handle_peer, args=(client_socket, addr), daemon=True).start()
                
            except Exception as e:
                if self.running:
                    logger.error(f"Error accepting connection: {e}")
                    
    def _connect_to_seeds(self):
        """Connect to seed nodes"""
        for seed in self.seed_nodes:
            if seed != f"127.0.0.1:{self.port}":  # Don't connect to ourselves
                try:
                    host, port = seed.split(':')
                    self._connect_to_peer(host, int(port))
                except Exception as e:
                    logger.debug(f"Could not connect to seed {seed}: {e}")
                    
        # Try to connect to more peers periodically
        while self.running:
            time.sleep(30)
            if len(self.peers) < 3:  # Try to maintain at least 3 connections
                self._discover_peers()
                
    def _connect_to_peer(self, host: str, port: int):
        """Connect to a specific peer"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            peer_id = f"{host}:{port}"
            self.peers[peer_id] = PTCPeer(host, port)
            self.peers[peer_id].connected = True
            
            logger.info(f"🔗 Connected to peer: {peer_id}")
            
            # Send handshake
            self._send_message(sock, {
                "type": "handshake",
                "version": "1.0",
                "port": self.port
            })
            
            # Handle this peer
            threading.Thread(target=self._handle_peer, args=(sock, (host, port)), daemon=True).start()
            
        except Exception as e:
            logger.debug(f"Could not connect to {host}:{port}: {e}")
            
    def _handle_peer(self, sock: socket.socket, addr):
        """Handle communication with a peer"""
        peer_id = f"{addr[0]}:{addr[1]}"
        
        try:
            while self.running:
                # Receive message
                data = sock.recv(4096)
                if not data:
                    break
                    
                try:
                    message = json.loads(data.decode())
                    self._process_message(message, peer_id)
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            logger.debug(f"Peer {peer_id} disconnected: {e}")
        finally:
            sock.close()
            if peer_id in self.peers:
                self.peers[peer_id].connected = False
                
    def _send_message(self, sock: socket.socket, message: dict):
        """Send message to peer"""
        try:
            data = json.dumps(message).encode()
            sock.send(data)
        except Exception as e:
            logger.debug(f"Failed to send message: {e}")
            
    def _process_message(self, message: dict, peer_id: str):
        """Process incoming message from peer"""
        msg_type = message.get("type")
        
        if msg_type == "handshake":
            logger.info(f"👋 Handshake from {peer_id}")
            
        elif msg_type == "new_block":
            logger.info(f"📦 New block received from {peer_id}")
            self._sync_new_block(message.get("block"))
            
        elif msg_type == "get_blockchain":
            logger.info(f"🔄 Blockchain sync request from {peer_id}")
            self._send_blockchain(peer_id)
            
    def _sync_blockchain(self):
        """Sync blockchain with peers"""
        while self.running:
            time.sleep(10)  # Sync every 10 seconds
            
            for peer_id, peer in self.peers.items():
                if peer.connected:
                    try:
                        # Ask for latest blocks
                        self._request_blockchain_sync(peer_id)
                    except Exception as e:
                        logger.debug(f"Sync error with {peer_id}: {e}")
                        
    def _request_blockchain_sync(self, peer_id: str):
        """Request blockchain synchronization from peer"""
        # Get current height from local daemon
        try:
            local_height = self._get_local_blockchain_height()
            # Request blocks from peers (simplified for now)
            logger.debug(f"Local blockchain height: {local_height}")
        except Exception as e:
            logger.debug(f"Could not get local height: {e}")
            
    def _get_local_blockchain_height(self) -> int:
        """Get blockchain height from local RPC daemon"""
        try:
            data = {"jsonrpc": "2.0", "method": "getinfo", "params": [], "id": 1}
            data_encoded = json.dumps(data).encode('utf-8')
            
            request = urllib.request.Request(
                f'http://127.0.0.1:{self.rpc_port}',
                data=data_encoded,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(request, timeout=2) as response:
                result = json.loads(response.read().decode())
                return result["result"]["blocks"]
                
        except Exception:
            return 0
            
    def _sync_new_block(self, block_data: dict):
        """Sync new block to local blockchain"""
        # This would validate and add the block to local chain
        logger.info(f"Syncing new block: {block_data.get('hash', 'unknown')[:16]}...")
        
    def _broadcast_blocks(self):
        """Broadcast new blocks to peers"""
        last_height = 0
        
        while self.running:
            time.sleep(5)
            
            try:
                current_height = self._get_local_blockchain_height()
                if current_height > last_height:
                    logger.info(f"📢 Broadcasting new block (height {current_height})")
                    self._broadcast_to_peers({
                        "type": "new_block",
                        "height": current_height,
                        "timestamp": time.time()
                    })
                    last_height = current_height
                    
            except Exception as e:
                logger.debug(f"Broadcast error: {e}")
                
    def _broadcast_to_peers(self, message: dict):
        """Broadcast message to all connected peers"""
        for peer_id, peer in self.peers.items():
            if peer.connected:
                try:
                    # Send to peer (simplified)
                    logger.debug(f"Broadcasting to {peer_id}")
                except Exception as e:
                    logger.debug(f"Broadcast to {peer_id} failed: {e}")
                    
    def _discover_peers(self):
        """Discover new peers from existing peers"""
        # Ask connected peers for more peer addresses
        logger.debug("🔍 Discovering new peers...")
        
    def get_network_status(self) -> dict:
        """Get current network status"""
        connected_peers = [p for p in self.peers.values() if p.connected]
        
        return {
            "connected_peers": len(connected_peers),
            "total_known_peers": len(self.peers),
            "port": self.port,
            "peers": [str(p) for p in connected_peers]
        }
        
    def stop(self):
        """Stop the P2P network node"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        logger.info("🛑 P2P network node stopped")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    node = PTCNetworkNode()
    node.start()
    
    try:
        while True:
            time.sleep(1)
            status = node.get_network_status()
            if status["connected_peers"] > 0:
                logger.info(f"🌐 Network: {status['connected_peers']} peers connected")
    except KeyboardInterrupt:
        node.stop()