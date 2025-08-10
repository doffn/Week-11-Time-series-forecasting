#!/usr/bin/env python3
"""
Test all Jupyter notebooks for execution errors
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

def test_notebook(notebook_path):
    """
    Test a single notebook by executing it
    """
    print(f"Testing {notebook_path}...")
    
    try:
        # Execute notebook
        result = subprocess.run([
            'jupyter', 'nbconvert', 
            '--to', 'notebook',
            '--execute',
            '--inplace',
            notebook_path
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print(f"✅ {notebook_path} - PASSED")
            return True
        else:
            print(f"❌ {notebook_path} - FAILED")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {notebook_path} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {notebook_path} - ERROR: {e}")
        return False

def main():
    """
    Test all notebooks in the notebooks directory
    """
    notebooks_dir = Path("notebooks")
    
    if not notebooks_dir.exists():
        print("❌ Notebooks directory not found!")
        sys.exit(1)
    
    # Find all notebook files
    notebook_files = list(notebooks_dir.glob("*.ipynb"))
    
    if not notebook_files:
        print("❌ No notebook files found!")
        sys.exit(1)
    
    print(f"Found {len(notebook_files)} notebooks to test")
    print("=" * 50)
    
    # Test each notebook
    results = []
    for notebook in notebook_files:
        success = test_notebook(str(notebook))
        results.append((notebook.name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("NOTEBOOK TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{name:<40} {status}")
    
    print(f"\nTotal: {passed}/{total} notebooks passed")
    
    if passed == total:
        print("🎉 All notebooks executed successfully!")
        sys.exit(0)
    else:
        print("💥 Some notebooks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
