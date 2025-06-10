from flask import Flask, request, jsonify
import hmac
import hashlib
import json
from datetime import datetime
import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    filename='sinpe_transactions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Configuration
API_KEYS = {
    "BANCO1": "secret_key_1",
    "BANCO2": "secret_key_2",
    # Add more banks as needed
}

def validate_hmac(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'X-API-Key' not in request.headers:
            return jsonify({"error": "API key missing"}), 401
        
        api_key = request.headers['X-API-Key']
        if api_key not in API_KEYS.values():
            return jsonify({"error": "Invalid API key"}), 401
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Get the bank code from the sender
        bank_code = data.get("sender", {}).get("bank_code")
        if not bank_code or bank_code not in API_KEYS:
            return jsonify({"error": "Invalid bank code"}), 400
            
        # Generate HMAC for validation
        expected_hmac = generar_hmac(
            data["sender"]["account_number"],
            data["timestamp"],
            data["transaction_id"],
            data["amount"]["value"],
            API_KEYS[bank_code]
        )
        
        if request.headers.get('X-HMAC') != expected_hmac:
            return jsonify({"error": "Invalid HMAC"}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def generar_hmac(account_number, timestamp, transaction_id, amount, clave):
    amount_str = "{:.2f}".format(float(amount))
    mensaje = account_number + timestamp + transaction_id + amount_str
    return hmac.new(clave.encode(), mensaje.encode(), hashlib.md5).hexdigest()

@app.route('/api/sinpe-transfer', methods=['POST'])
@validate_hmac
def receive_sinpe_transfer():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["version", "timestamp", "transaction_id", "sender", "receiver", "amount", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate sender fields
        sender_fields = ["account_number", "bank_code", "name"]
        for field in sender_fields:
            if field not in data["sender"]:
                return jsonify({"error": f"Missing required sender field: {field}"}), 400
        
        # Validate receiver fields
        receiver_fields = ["account_number", "bank_code", "name"]
        for field in receiver_fields:
            if field not in data["receiver"]:
                return jsonify({"error": f"Missing required receiver field: {field}"}), 400
        
        # Validate amount fields
        if "value" not in data["amount"]:
            return jsonify({"error": "Missing amount value"}), 400
        
        # Log the transaction
        logging.info(f"Received SINPE transfer: {json.dumps(data)}")
        
        # Process the transaction (implement your business logic here)
        # For now, we'll just return a success response
        return jsonify({
            "status": "success",
            "message": "Transfer received successfully",
            "transaction_id": data["transaction_id"]
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing SINPE transfer: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/sinpe-movil-transfer', methods=['POST'])
@validate_hmac
def receive_sinpe_movil_transfer():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["version", "timestamp", "transaction_id", "sender", "receiver", "amount", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate sender phone number
        if "phone_number" not in data["sender"]:
            return jsonify({"error": "Missing sender phone number"}), 400
        
        # Validate receiver phone number
        if "phone_number" not in data["receiver"]:
            return jsonify({"error": "Missing receiver phone number"}), 400
        
        # Validate amount
        if "value" not in data["amount"]:
            return jsonify({"error": "Missing amount value"}), 400
        
        # Log the transaction
        logging.info(f"Received SINPE Móvil transfer: {json.dumps(data)}")
        
        # Process the transaction (implement your business logic here)
        # For now, we'll just return a success response
        return jsonify({
            "status": "success",
            "message": "SINPE Móvil transfer received successfully",
            "transaction_id": data["transaction_id"]
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing SINPE Móvil transfer: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc') 