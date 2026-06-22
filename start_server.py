#!/usr/bin/env python3
"""
Quantum Webscraper Startup Script
Automatically finds an available port and starts the server
"""

import os
import sys
import socket
import subprocess
import time
from pathlib import Path

def find_available_port(start_port=8081, max_attempts=100):
    """Find an available port starting from start_port"""
    # Try to use a fixed port first (8081)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', start_port))
            return start_port
    except OSError:
        pass
    
    # If fixed port is busy, find next available
    for port in range(start_port + 1, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        # Find process using the port
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pid = result.stdout.strip()
            print(f"🔄 Killing process {pid} on port {port}")
            subprocess.run(['kill', '-9', pid], check=True)
            time.sleep(1)  # Give it time to die
            return True
    except subprocess.CalledProcessError:
        pass
    return False

def main():
    print("🚀 Starting Quantum News Webscraper...")
    
    # Check if app.py exists
    if not Path('app.py').exists():
        print("❌ Error: app.py not found in current directory")
        sys.exit(1)
    
    # Try to find available port
    try:
        port = find_available_port()
        print(f"✅ Found available port: {port}")
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Set environment variable
    os.environ['PORT'] = str(port)
    
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
