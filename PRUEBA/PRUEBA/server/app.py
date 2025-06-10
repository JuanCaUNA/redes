from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from server.config import Config
from server.services.auth_service import require_auth
from server.services.transfer_service import TransferService
from server.utils.logger import logger, log_error

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{Config.RATE_LIMIT} per minute"]
)

@app.route('/api/sinpe-transfer', methods=['POST'])
@limiter.limit(f"{Config.RATE_LIMIT} per minute")
@require_auth
def receive_sinpe_transfer():
    """Handle SINPE transfer requests."""
    try:
        data = request.get_json()
        success, response = TransferService.process_sinpe_transfer(data)
        
        if success:
            return jsonify(response), 200
        else:
            return jsonify({"error": response}), 400
            
    except Exception as e:
        log_error('sinpe_transfer_error', str(e), {'data': data})
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/sinpe-movil-transfer', methods=['POST'])
@limiter.limit(f"{Config.RATE_LIMIT} per minute")
@require_auth
def receive_sinpe_movil_transfer():
    """Handle SINPE Móvil transfer requests."""
    try:
        data = request.get_json()
        success, response = TransferService.process_sinpe_movil_transfer(data)
        
        if success:
            return jsonify(response), 200
        else:
            return jsonify({"error": response}), 400
            
    except Exception as e:
        log_error('sinpe_movil_transfer_error', str(e), {'data': data})
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    return jsonify({"error": "Rate limit exceeded"}), 429

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    try:
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG,
            ssl_context=(Config.SSL_CERT, Config.SSL_KEY)
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise 