import requests
import time
import logging
from datetime import datetime
import hmac
import hashlib
from client.config import Config

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': Config.API_KEY,
            'Content-Type': 'application/json'
        })
        
        # Configure SSL verification
        if not Config.VERIFY_SSL:
            self.session.verify = False
        elif Config.SSL_CERT:
            self.session.verify = Config.SSL_CERT
            
        # Configure logging
        logging.basicConfig(
            filename=Config.LOG_FILE,
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('sinpe_client')

    def _generate_hmac(self, account_number, timestamp, transaction_id, amount):
        """Generate HMAC signature for a transaction."""
        amount_str = "{:.2f}".format(float(amount))
        mensaje = account_number + timestamp + transaction_id + amount_str
        return hmac.new(Config.API_KEY.encode(), mensaje.encode(), hashlib.md5).hexdigest()

    def _make_request(self, method, endpoint, data=None, retries=0):
        """Make an HTTP request with retry logic."""
        url = f"{Config.SERVER_URL}{endpoint}"
        
        try:
            response = self.session.request(
                method,
                url,
                json=data,
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if retries < Config.MAX_RETRIES:
                self.logger.warning(f"Request failed, retrying ({retries + 1}/{Config.MAX_RETRIES}): {str(e)}")
                time.sleep(Config.RETRY_DELAY)
                return self._make_request(method, endpoint, data, retries + 1)
            else:
                self.logger.error(f"Request failed after {Config.MAX_RETRIES} retries: {str(e)}")
                raise

    def make_sinpe_transfer(self, sender_account, receiver_account, amount, description):
        """Make a SINPE transfer."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        transaction_id = f"TRX{int(time.time())}"
        
        data = {
            "version": Config.API_VERSION,
            "timestamp": timestamp,
            "transaction_id": transaction_id,
            "sender": {
                "account_number": sender_account["account_number"],
                "bank_code": Config.BANK_CODE,
                "name": sender_account["name"]
            },
            "receiver": {
                "account_number": receiver_account["account_number"],
                "bank_code": receiver_account["bank_code"],
                "name": receiver_account["name"]
            },
            "amount": {
                "value": str(amount),
                "currency": Config.DEFAULT_CURRENCY
            },
            "description": description
        }
        
        # Generate HMAC
        hmac_signature = self._generate_hmac(
            sender_account["account_number"],
            timestamp,
            transaction_id,
            amount
        )
        
        # Add HMAC to headers
        self.session.headers.update({'X-HMAC': hmac_signature})
        
        try:
            response = self._make_request('POST', '/api/sinpe-transfer', data)
            self.logger.info(f"SINPE transfer successful: {response}")
            return response
        except Exception as e:
            self.logger.error(f"SINPE transfer failed: {str(e)}")
            raise

    def make_sinpe_movil_transfer(self, sender_phone, receiver_phone, amount, description):
        """Make a SINPE Móvil transfer."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        transaction_id = f"TRX{int(time.time())}"
        
        data = {
            "version": Config.API_VERSION,
            "timestamp": timestamp,
            "transaction_id": transaction_id,
            "sender": {
                "phone_number": sender_phone
            },
            "receiver": {
                "phone_number": receiver_phone
            },
            "amount": {
                "value": str(amount),
                "currency": Config.DEFAULT_CURRENCY
            },
            "description": description
        }
        
        # Generate HMAC
        hmac_signature = self._generate_hmac(
            sender_phone,
            timestamp,
            transaction_id,
            amount
        )
        
        # Add HMAC to headers
        self.session.headers.update({'X-HMAC': hmac_signature})
        
        try:
            response = self._make_request('POST', '/api/sinpe-movil-transfer', data)
            self.logger.info(f"SINPE Móvil transfer successful: {response}")
            return response
        except Exception as e:
            self.logger.error(f"SINPE Móvil transfer failed: {str(e)}")
            raise 