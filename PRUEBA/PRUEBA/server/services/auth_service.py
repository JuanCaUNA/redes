import hmac
import hashlib
import time
from functools import wraps
from flask import request, jsonify
from server.config import Config
from server.utils.logger import logger, log_security_event

class AuthService:
    @staticmethod
    def generate_hmac(account_number, timestamp, transaction_id, amount, clave):
        """Generate HMAC signature for a transaction."""
        amount_str = "{:.2f}".format(float(amount))
        mensaje = account_number + timestamp + transaction_id + amount_str
        return hmac.new(clave.encode(), mensaje.encode(), hashlib.md5).hexdigest()

    @staticmethod
    def validate_api_key(api_key):
        """Validate the API key."""
        return api_key in Config.API_KEYS.values()

    @staticmethod
    def validate_timestamp(timestamp):
        """Validate that the timestamp is within acceptable range."""
        try:
            request_time = time.mktime(time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ"))
            current_time = time.time()
            # Allow 5 minutes of time difference
            return abs(current_time - request_time) <= 300
        except:
            return False

    @staticmethod
    def validate_request(data):
        """Validate the request data."""
        required_fields = [
            "version", "timestamp", "transaction_id", 
            "sender", "receiver", "amount", "description"
        ]
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate timestamp
        if not AuthService.validate_timestamp(data["timestamp"]):
            return False, "Invalid timestamp"
        
        # Validate amount
        try:
            amount = float(data["amount"]["value"])
            if amount < Config.MIN_TRANSACTION_AMOUNT:
                return False, f"Amount below minimum: {Config.MIN_TRANSACTION_AMOUNT}"
            if amount > Config.MAX_TRANSACTION_AMOUNT:
                return False, f"Amount above maximum: {Config.MAX_TRANSACTION_AMOUNT}"
        except:
            return False, "Invalid amount format"
        
        return True, None

def require_auth(f):
    """Decorator for requiring authentication on endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            log_security_event('missing_api_key', {'ip': request.remote_addr})
            return jsonify({"error": "API key missing"}), 401
        
        if not AuthService.validate_api_key(api_key):
            log_security_event('invalid_api_key', {
                'ip': request.remote_addr,
                'api_key': api_key[:8] + '...'  # Log only first 8 chars
            })
            return jsonify({"error": "Invalid API key"}), 401
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate request data
        is_valid, error_message = AuthService.validate_request(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400
        
        # Get the bank code from the sender
        bank_code = data.get("sender", {}).get("bank_code")
        if not bank_code or bank_code not in Config.API_KEYS:
            return jsonify({"error": "Invalid bank code"}), 400
        
        # Validate HMAC
        expected_hmac = AuthService.generate_hmac(
            data["sender"]["account_number"],
            data["timestamp"],
            data["transaction_id"],
            data["amount"]["value"],
            Config.API_KEYS[bank_code]
        )
        
        if request.headers.get('X-HMAC') != expected_hmac:
            log_security_event('invalid_hmac', {
                'ip': request.remote_addr,
                'bank_code': bank_code
            })
            return jsonify({"error": "Invalid HMAC"}), 401
        
        return f(*args, **kwargs)
    return decorated_function 