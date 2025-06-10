import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # SSL Configuration
    SSL_CERT = os.getenv('SSL_CERT', 'cert.pem')
    SSL_KEY = os.getenv('SSL_KEY', 'key.pem')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sinpe.db')
    
    # Security Configuration
    API_KEYS = {
        "BANCO1": os.getenv('BANCO1_API_KEY', 'secret_key_1'),
        "BANCO2": os.getenv('BANCO2_API_KEY', 'secret_key_2'),
    }
    
    # Logging Configuration
    LOG_FILE = os.getenv('LOG_FILE', 'sinpe_transactions.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Rate Limiting
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', '100'))  # requests per minute
    
    # Transaction Limits
    MAX_TRANSACTION_AMOUNT = float(os.getenv('MAX_TRANSACTION_AMOUNT', '1000000.00'))
    MIN_TRANSACTION_AMOUNT = float(os.getenv('MIN_TRANSACTION_AMOUNT', '1.00'))
    
    # Timeout Configuration
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))  # seconds
    
    # Retry Configuration
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '1'))  # seconds 