#!/usr/bin/env python3
"""
AI Career Guidance System - Launch Script
==========================================

This script sets up and launches the Streamlit application with proper configuration.
Perfect for IBM internship demonstration.

Usage:
    python run.py

Features:
- Automatic dependency checking
- Environment setup
- Error handling and recovery
- Performance monitoring
"""

import subprocess
import sys
import os
import importlib.util
from pathlib import Path

def check_python_version():
    """Ensure Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'matplotlib', 
        'plotly', 'sklearn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        # Handle sklearn import name difference
        import_name = 'sklearn' if package == 'sklearn' else package
        
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🔧 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                *missing_packages
            ])
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✅ All dependencies are installed")

def setup_directories():
    """Create necessary directories and files"""
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path(".streamlit")
    if not streamlit_dir.exists():
        streamlit_dir.mkdir()
        print("✅ Created .streamlit directory")
    
    # Create config.toml if it doesn't exist
    config_file = streamlit_dir / "config.toml"
    if not config_file.exists():
        config_content = """[global]
dataFrameSerialization = "legacy"

[server]
headless = true
port = 8501
enableCORS = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
        with open(config_file, 'w') as f:
            f.write(config_content)
        print("✅ Created Streamlit configuration")

def launch_application():
    """Launch the Streamlit application"""
    print("\n🚀 Starting AI Career Guidance System...")
    print("📱 The application will open in your default browser")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except FileNotFoundError:
        print("❌ Error: app.py not found in current directory")
        print("Make sure you're running this script from the project root")
        sys.exit(1)

def main():
    """Main execution function"""
    print("🎯 AI Career Guidance System - Launch Script")
    print("=" * 50)
    
    # Pre-flight checks
    check_python_version()
    check_dependencies()
    setup_directories()
    
    # Launch application
    launch_application()

if __name__ == "__main__":
    main()