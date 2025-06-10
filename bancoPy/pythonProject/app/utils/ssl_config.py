"""
SSL Configuration for SINPE Banking System
"""

import ssl
import os
from pathlib import Path


class SSLConfig:
    """SSL Configuration Manager"""
    
    def __init__(self):
        self.ssl_dir = Path(__file__).parent.parent / "ssl"
        self.ssl_dir.mkdir(exist_ok=True)
        
    def create_self_signed_cert(self):
        """Create self-signed certificate for development"""
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime
            
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # Create certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "CR"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "San Jose"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "San Jose"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SINPE Banking"),
                x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.DNSName("127.0.0.1"),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Write certificate
            cert_path = self.ssl_dir / "cert.pem"
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            # Write private key
            key_path = self.ssl_dir / "key.pem"
            with open(key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            return str(cert_path), str(key_path)
            
        except ImportError:
            print("Warning: cryptography package not available. SSL disabled.")
            return None, None
        except Exception as e:
            print(f"Error creating SSL certificate: {e}")
            return None, None
    
    def get_ssl_context(self):
        """Get SSL context for Flask application"""
        cert_path = self.ssl_dir / "cert.pem"
        key_path = self.ssl_dir / "key.pem"
        
        # Create certificates if they don't exist
        if not cert_path.exists() or not key_path.exists():
            cert_file, key_file = self.create_self_signed_cert()
            if not cert_file or not key_file:
                return None
        
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(str(cert_path), str(key_path))
            return context
        except Exception as e:
            print(f"Error loading SSL context: {e}")
            return None
    
    def get_requests_ssl_config(self):
        """Get SSL configuration for requests library"""
        cert_path = self.ssl_dir / "cert.pem"
        
        if cert_path.exists():
            return str(cert_path)
        else:
            # Use system certificates
            try:
                import certifi
                return certifi.where()
            except ImportError:
                return True  # Use default SSL verification


# Global SSL configuration
ssl_config = SSLConfig()
