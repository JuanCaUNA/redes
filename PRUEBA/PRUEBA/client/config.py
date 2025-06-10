import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Server Configuration
    SERVER_URL = os.getenv('SERVER_URL', 'https://localhost:5000')
    
    # API Configuration
    API_KEY = os.getenv('API_KEY', 'secret_key_1')
    BANK_CODE = os.getenv('BANK_CODE', 'BANCO1')
    
    # Request Configuration
    TIMEOUT = int(os.getenv('TIMEOUT', '30'))  # seconds
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '1'))  # seconds
    
    # SSL Configuration
    VERIFY_SSL = os.getenv('VERIFY_SSL', 'True').lower() == 'true'
    SSL_CERT = os.getenv('SSL_CERT', None)
    
    # Logging Configuration
    LOG_FILE = os.getenv('LOG_FILE', 'sinpe_client.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Transaction Configuration
    DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY', 'CRC')
    API_VERSION = os.getenv('API_VERSION', '1.0') 