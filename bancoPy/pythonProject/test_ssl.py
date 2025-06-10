#!/usr/bin/env python3
"""
Test SSL Configuration for SINPE Banking System
"""
import sys
import os

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

def test_ssl_config():
    """Test SSL configuration and certificate generation"""
    print("🔐 Testing SSL Configuration...")
    
    try:
        from app.utils.ssl_config import ssl_config
        print("✅ SSL config module imported successfully")
        
        # Test certificate creation
        cert_path, key_path = ssl_config.create_self_signed_cert()
        if cert_path and key_path:
            print(f"✅ SSL certificates created successfully:")
            print(f"   Certificate: {cert_path}")
            print(f"   Private Key: {key_path}")
        else:
            print("⚠️  SSL certificates could not be created (cryptography not available)")
        
        # Test SSL context creation
        ssl_context = ssl_config.get_ssl_context()
        if ssl_context:
            print("✅ SSL context created successfully")
        else:
            print("⚠️  SSL context could not be created")
            
        # Test requests SSL config
        requests_ssl = ssl_config.get_requests_ssl_config()
        print(f"✅ Requests SSL config: {requests_ssl}")
        
    except Exception as e:
        print(f"❌ Error testing SSL configuration: {e}")
        return False
    
    return True

def test_psutil_availability():
    """Test psutil availability with graceful degradation"""
    print("\n🔧 Testing psutil availability...")
    
    try:
        import psutil
        print("✅ psutil is available")
        print(f"   CPU count: {psutil.cpu_count()}")
        print(f"   Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
        return True
    except ImportError:
        print("⚠️  psutil is not available - system monitoring will be limited")
        return False

def test_cryptography_availability():
    """Test cryptography library availability"""
    print("\n🔐 Testing cryptography library...")
    
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes
        print("✅ cryptography library is available")
        return True
    except ImportError:
        print("⚠️  cryptography library is not available - SSL will be disabled")
        return False

def test_imports():
    """Test all critical imports"""
    print("\n📦 Testing critical imports...")
    
    critical_modules = [
        "flask",
        "sqlalchemy", 
        "requests",
        "json",
        "datetime",
        "uuid"
    ]
    
    failed_imports = []
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

if __name__ == "__main__":
    print("🧪 SINPE Banking System - SSL and Dependencies Test")
    print("=" * 60)
    
    ssl_ok = test_ssl_config()
    psutil_ok = test_psutil_availability() 
    crypto_ok = test_cryptography_availability()
    imports_ok = test_imports()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   SSL Configuration: {'✅ OK' if ssl_ok else '❌ FAILED'}")
    print(f"   psutil: {'✅ Available' if psutil_ok else '⚠️  Limited'}")
    print(f"   cryptography: {'✅ Available' if crypto_ok else '⚠️  Disabled'}")
    print(f"   Critical Imports: {'✅ OK' if imports_ok else '❌ FAILED'}")
    
    if imports_ok and ssl_ok:
        print("\n🎉 System is ready to run!")
        print("   - SSL support:", "✅ Enabled" if crypto_ok else "⚠️  Disabled")
        print("   - Monitoring:", "✅ Full" if psutil_ok else "⚠️  Limited")
    else:
        print("\n⚠️  System has issues that need to be resolved")
    
    print("\n" + "=" * 60)
