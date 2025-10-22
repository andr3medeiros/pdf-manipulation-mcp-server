#!/usr/bin/env python3
"""
Script to help publish the PDF Manipulation MCP Server to PyPI.

This script automates the process of building and publishing the package.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main function to build and publish the package."""
    print("🚀 PDF Manipulation MCP Server - PyPI Publisher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if build tools are installed
    print("🔍 Checking build tools...")
    build_tools = ["build", "twine"]
    for tool in build_tools:
        result = run_command(f"pip show {tool}", f"Checking {tool}")
        if result is None:
            print(f"📦 Installing {tool}...")
            run_command(f"pip install {tool}", f"Installing {tool}")
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    run_command("rm -rf dist/ build/ *.egg-info/", "Cleaning build artifacts")
    
    # Build the package
    print("🔨 Building package...")
    result = run_command("python -m build", "Building package")
    if result is None:
        print("❌ Build failed. Please check the errors above.")
        sys.exit(1)
    
    # Check the built package
    print("🔍 Checking built package...")
    result = run_command("twine check dist/*", "Checking package")
    if result is None:
        print("❌ Package check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🎉 Package built successfully!")
    print("\nNext steps:")
    print("1. Test the package locally:")
    print("   pip install dist/*.whl")
    print("2. Upload to PyPI:")
    print("   twine upload dist/*")
    print("3. Or upload to Test PyPI first:")
    print("   twine upload --repository testpypi dist/*")
    
    print("\n📋 Package files created:")
    for file in Path("dist").glob("*"):
        print(f"   - {file}")

if __name__ == "__main__":
    main()
