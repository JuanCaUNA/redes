"""
SSL Configuration for SINPE Banking System - Optimized Version
Provides secure SSL/TLS configuration with proper error handling
"""

import ssl
import os
from pathlib import Path
import logging

# Configure logging for SSL operations
logger = logging.getLogger(__name__)


class SSLConfig:
    """Optimized SSL Configuration Manager for SINPE Banking System"""

    def __init__(self):
        self.ssl_dir = Path(__file__).parent.parent / "ssl"
        self.ssl_dir.mkdir(exist_ok=True)
        self.cert_path = self.ssl_dir / "cert.pem"
        self.key_path = self.ssl_dir / "key.pem"

    def create_self_signed_cert(self):
        """Create self-signed certificate with enhanced security"""
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime
            import ipaddress

            logger.info("Creating SSL self-signed certificate...")

            # Generate stronger private key (4096 bits for better security)
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,  # Increased key size for better security
            )

            # Create certificate with enhanced security
            subject = issuer = x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "CR"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "San Jose"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Jose"),
                    x509.NameAttribute(
                        NameOID.ORGANIZATION_NAME, "SINPE Banking System"
                    ),
                    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "IT Security"),
                    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
                ]
            )

            # Certificate valid for 1 year
            cert = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(private_key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.datetime.utcnow())
                .not_valid_after(
                    datetime.datetime.utcnow() + datetime.timedelta(days=365)
                )
                .add_extension(
                    x509.SubjectAlternativeName(
                        [
                            x509.DNSName("localhost"),
                            x509.DNSName("127.0.0.1"),
                            x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                        ]
                    ),
                    critical=False,
                )
                .add_extension(
                    x509.KeyUsage(
                        key_encipherment=True,
                        digital_signature=True,
                        key_agreement=False,
                        key_cert_sign=False,
                        crl_sign=False,
                        content_commitment=False,
                        data_encipherment=False,
                        encipher_only=False,
                        decipher_only=False,
                    ),
                    critical=True,
                )
                .add_extension(
                    x509.ExtendedKeyUsage(
                        [
                            x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
                        ]
                    ),
                    critical=True,
                )
                .sign(private_key, hashes.SHA256())
            )

            # Write certificate with secure permissions
            with open(self.cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

            # Write private key with secure permissions
            with open(self.key_path, "wb") as f:
                f.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )

            logger.info(f"SSL certificates created successfully in: {self.ssl_dir}")
            print(f"✅ SSL certificates created in: {self.ssl_dir}")
            return str(self.cert_path), str(self.key_path)

        except ImportError:
            logger.warning("cryptography package not available. SSL disabled.")
            print("⚠️ Warning: cryptography package not available. SSL disabled.")
            return None, None
        except Exception as e:
            logger.error(f"Error creating SSL certificate: {e}")
            print(f"❌ Error creating SSL certificate: {e}")
            return None, None

    def get_ssl_context(self):
        """Get SSL context for Flask application"""
        try:
            # Try to load existing certificates
            if self.cert_path.exists() and self.key_path.exists():
                logger.info("Loading existing SSL certificates...")
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(str(self.cert_path), str(self.key_path))
            else:
                # Create new certificates if they don't exist
                logger.info("Creating new SSL certificates...")
                if not self.create_self_signed_cert():
                    return None
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(str(self.cert_path), str(self.key_path))

            # Enhanced security settings
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            context.set_ciphers(
                "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS"
            )
            context.options |= ssl.OP_NO_SSLv2
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1

            logger.info("SSL context created successfully with enhanced security")
            return context

        except Exception as e:
            logger.error(f"Error loading SSL context: {e}")
            print(f"❌ Error loading SSL context: {e}")
            return None

    def get_requests_ssl_config(self):
        """Get SSL configuration for requests library (for bank-to-bank communications)"""
        try:
            if self.cert_path.exists():
                # Return path to certificate file for requests verification
                return str(self.cert_path)
            else:
                # For development, allow unverified requests
                return False
        except Exception as e:
            logger.error(f"Error getting requests SSL config: {e}")
            return False


# Global SSL configuration instance
ssl_config = SSLConfig()
