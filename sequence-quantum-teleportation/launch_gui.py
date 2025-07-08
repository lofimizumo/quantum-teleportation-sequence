#!/usr/bin/env python3
"""
Launch script for Quantum Teleportation Simulator GUI
====================================================

This script provides an easy way to launch the Streamlit GUI
with proper configuration and error handling.
"""

import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'streamlit',
        'plotly',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install them using:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_simulation_files():
    """Check if simulation files are present."""
    required_files = [
        'QT_main.py',
        'QT_sender.py',
        'QT_receiver.py',
        'streamlit_app.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required simulation files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def launch_streamlit():
    """Launch the Streamlit application."""
    try:
        print("🚀 Starting Quantum Teleportation Simulator GUI...")
        print("📱 The GUI will open in your default web browser")
        print("🔗 URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.headless', 'false',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")

def main():
    """Main function."""
    print("⚛️  Quantum Teleportation Simulator - GUI Launcher")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies found")
    
    # Check simulation files
    print("🔍 Checking simulation files...")
    if not check_simulation_files():
        sys.exit(1)
    print("✅ All simulation files found")
    
    # Launch GUI
    launch_streamlit()

if __name__ == "__main__":
    main() 