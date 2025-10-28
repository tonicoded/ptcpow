#!/usr/bin/env python3
"""
PTC Launcher - Cross-platform (Windows, Mac, Linux)
Universal launcher that works everywhere
"""

import subprocess
import time
import sys
import os
import signal
import platform

def is_windows():
    return platform.system() == "Windows"

def start_ptc():
    print("🌐 Starting PTC (Private Coin)...")
    print("🔄 Connecting to global PTC network...")
    print()
    
    processes = []
    
    try:
        # Start PTC daemon
        print("Starting PTC daemon...")
        if is_windows():
            daemon_process = subprocess.Popen([sys.executable, "ptc_mainnet_daemon.py"], 
                                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            daemon_process = subprocess.Popen([sys.executable, "ptc_mainnet_daemon.py"])
        processes.append(daemon_process)
        
        # Wait for daemon to start
        time.sleep(3)
        
        # Start web wallet
        print("Starting PTC web wallet...")
        if is_windows():
            wallet_process = subprocess.Popen([sys.executable, "ptc_web_wallet.py"],
                                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            wallet_process = subprocess.Popen([sys.executable, "ptc_web_wallet.py"])
        processes.append(wallet_process)
        
        print()
        print("✅ PTC is now running!")
        print("🌐 Wallet: http://127.0.0.1:8888")
        print("📊 Dashboard: http://127.0.0.1:8080")
        print()
        print("Press Ctrl+C to stop PTC")
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
                # Check if processes are still running
                for process in processes[:]:
                    if process.poll() is not None:
                        print(f"⚠️  Process stopped unexpectedly")
                        processes.remove(process)
                        
                if not processes:
                    print("❌ All PTC processes stopped")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping PTC...")
            
    except Exception as e:
        print(f"❌ Error starting PTC: {e}")
        
    finally:
        # Stop all processes
        for process in processes:
            try:
                if is_windows():
                    # Windows process termination
                    process.terminate()
                else:
                    # Unix process termination
                    process.terminate()
                    
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error stopping process: {e}")
                
        print("✅ PTC stopped")

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists("ptc_mainnet_daemon.py"):
        print("❌ Error: ptc_mainnet_daemon.py not found")
        print("Make sure you're in the PTC directory")
        sys.exit(1)
        
    start_ptc()