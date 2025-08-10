#!/usr/bin/env python3
"""
Setup script for the portfolio optimization environment
"""

import subprocess
import sys

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def verify_installation():
    """Verify that key packages are installed"""
    required_packages = [
        'yfinance', 'pandas', 'numpy', 'matplotlib', 'seaborn',
        'sklearn', 'tensorflow', 'statsmodels', 'pmdarima', 'pypfopt'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package}")
    
    if missing_packages:
        print(f"\nMissing packages: {missing_packages}")
        return False
    
    print("\n✓ All packages verified successfully!")
    return True

if __name__ == "__main__":
    print("Setting up Portfolio Optimization Environment...")
    print("=" * 50)
    
    if install_requirements():
        verify_installation()
    
    print("\nEnvironment setup complete!")
    print("You can now run the portfolio_optimization_analysis.ipynb notebook")
