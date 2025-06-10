#!/usr/bin/env python3
"""
Setup script for SINPE Banking System
Installs required dependencies and configures SSL
"""
import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using subprocess to avoid pip issues"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, check=True)
        print(f"✅ Installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False

def main():
    print("🔧 SINPE Banking System Setup")
    print("=" * 50)
    
    # Core dependencies
    core_packages = [
        "Flask==2.3.3",
        "SQLAlchemy==2.0.23", 
        "Flask-SQLAlchemy==3.1.1",
        "Flask-CORS==4.0.0",
        "requests==2.31.0",
        "cryptography==41.0.7",
        "rich==13.7.0"
    ]
    
    # Optional dependencies
    optional_packages = [
        "psutil==5.9.6",
        "PyJWT==2.8.0"
    ]
    
    print("Installing core dependencies...")
    core_success = 0
    for package in core_packages:
        if install_package(package):
            core_success += 1
    
    print(f"\nCore packages: {core_success}/{len(core_packages)} installed successfully")
    
    print("\nInstalling optional dependencies...")
    optional_success = 0
    for package in optional_packages:
        if install_package(package):
            optional_success += 1
    
    print(f"Optional packages: {optional_success}/{len(optional_packages)} installed successfully")
    
    if core_success == len(core_packages):
        print("\n🎉 Setup completed successfully!")
        print("You can now run: python main.py")
    else:
        print(f"\n⚠️  Setup incomplete. {len(core_packages) - core_success} core packages failed to install.")
        
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
