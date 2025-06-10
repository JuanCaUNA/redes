import logging
import sys
from logging.handlers import RotatingFileHandler
from server.config import Config

def setup_logger():
    # Create logger
    logger = logging.getLogger('sinpe')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create file handler
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create logger instance
logger = setup_logger()

def log_transaction(transaction_type, data, status, error=None):
    """Log a transaction with all relevant information."""
    log_data = {
        'type': transaction_type,
        'data': data,
        'status': status,
        'error': str(error) if error else None
    }
    
    if status == 'success':
        logger.info(f"Transaction successful: {log_data}")
    else:
        logger.error(f"Transaction failed: {log_data}")

def log_error(error_type, error_message, context=None):
    """Log an error with context information."""
    log_data = {
        'error_type': error_type,
        'message': error_message,
        'context': context
    }
    logger.error(f"Error occurred: {log_data}")

def log_security_event(event_type, details):
    """Log security-related events."""
    log_data = {
        'event_type': event_type,
        'details': details
    }
    logger.warning(f"Security event: {log_data}") 