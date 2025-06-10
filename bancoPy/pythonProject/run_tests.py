#!/usr/bin/env python3
"""
Test Runner Script for SINPE Banking System
Executes all validated tests in the correct order
"""

import subprocess
import sys
import os
from datetime import datetime


def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔍 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=False,
            text=True
        )
        print(f"✅ {description}: PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: FAILED (exit code {e.returncode})")
        return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {e}")
        return False


def main():
    """Run all tests in order of priority"""
    print("🧪 SINPE Banking System - Complete Test Suite")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(r"c:\Users\juanc\Documents\GitHub\redes\bancoPy\pythonProject")
    
    # Activate virtual environment and run tests
    venv_python = r".\.venv\Scripts\python.exe"
    
    tests = [
        {
            "command": f"{venv_python} test_basic_optimized.py",
            "description": "Basic System Tests (PRIORITY 1)",
            "critical": True
        },
        {
            "command": f"{venv_python} test_essential.py",
            "description": "Essential Functionality Tests (PRIORITY 2)",
            "critical": False
        },
        {
            "command": f"{venv_python} test_api.py",
            "description": "API Endpoint Tests (PRIORITY 3)",
            "critical": False
        }
    ]
    
    passed = 0
    total = len(tests)
    critical_failed = False
    
    for test in tests:
        success = run_command(test["command"], test["description"])
        if success:
            passed += 1
        elif test["critical"]:
            critical_failed = True
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if critical_failed:
        print("❌ CRITICAL TESTS FAILED - System may not be functional")
        return False
    elif passed == total:
        print("🎉 ALL TESTS PASSED - System fully validated!")
        return True
    else:
        print("⚠️ Some non-critical tests failed - System is functional")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
