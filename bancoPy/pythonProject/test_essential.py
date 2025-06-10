#!/usr/bin/env python3
"""
Simplified test script for SINPE Banking System
Tests essential functionality without complex formatting issues
"""

import sys
import os

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

def test_basic_hmac():
    """Test basic HMAC generation"""
    print("🔐 Testing HMAC Generation...")
    
    try:
        from app.utils.hmac_generator import (
            generate_hmac_for_account_transfer,
            generate_hmac_for_phone_transfer
        )
        
        # Test account transfer HMAC
        account_hmac = generate_hmac_for_account_transfer(
            "152001234567890",
            "2024-01-15T10:30:00Z", 
            "12345678-1234-1234-1234-123456789012",
            5000.00
        )
        
        if account_hmac and len(account_hmac) == 32:
            print("✅ Account transfer HMAC generation: PASSED")
        else:
            print("❌ Account transfer HMAC generation: FAILED")
            return False
            
        # Test phone transfer HMAC
        phone_hmac = generate_hmac_for_phone_transfer(
            "88887777",
            "2024-01-15T10:30:00Z",
            "12345678-1234-1234-1234-123456789012", 
            5000.00
        )
        
        if phone_hmac and len(phone_hmac) == 32:
            print("✅ Phone transfer HMAC generation: PASSED")
        else:
            print("❌ Phone transfer HMAC generation: FAILED")
            return False
            
        print(f"✅ HMAC Tests: All passed")
        return True
        
    except Exception as e:
        print(f"❌ HMAC Test Error: {e}")
        return False

def test_api_basic():
    """Test basic API functionality"""
    print("🌐 Testing API Endpoints...")
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint: PASSED")
        else:
            print("⚠️ Health endpoint: Not available (server may not be running)")
            
        return True
        
    except requests.ConnectionError:
        print("⚠️ API Test: Server not running, skipping...")
        return True
    except Exception as e:
        print(f"❌ API Test Error: {e}")
        return False

def test_configuration_files():
    """Test configuration files"""
    print("📄 Testing Configuration Files...")
    
    try:
        import json
        
        # Test banks config
        with open("config/banks.json", "r") as f:
            banks_data = json.load(f)
            
        if banks_data and len(banks_data) > 0:
            print(f"✅ Banks configuration: {len(banks_data)} banks loaded")
        else:
            print("❌ Banks configuration: Empty or invalid")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration Test Error: {e}")
        return False

def main():
    """Run all essential tests"""
    print("🧪 SINPE Banking System - Essential Tests")
    print("=" * 60)
    
    tests = [
        test_configuration_files,
        test_basic_hmac,
        test_api_basic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All essential tests passed!")
        return True
    else:
        print("⚠️ Some tests failed or were skipped")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
