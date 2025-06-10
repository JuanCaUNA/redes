"""
Comprehensive Logging Service for SINPE Banking System
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import json
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class BankingLoggerService:
    """Enhanced logging service for banking operations"""

    def __init__(self):
        self.setup_loggers()

    def setup_loggers(self):
        """Setup different loggers for different purposes"""

        # Create logs directory if it doesn't exist
        log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
        )
        os.makedirs(log_dir, exist_ok=True)

        # Configure formatters
        detailed_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )

        json_formatter = JsonFormatter()

        # Main application logger
        self.app_logger = logging.getLogger("banking_app")
        self.app_logger.setLevel(logging.INFO)

        app_handler = RotatingFileHandler(
            os.path.join(log_dir, "banking_app.log"),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        app_handler.setFormatter(detailed_formatter)
        self.app_logger.addHandler(app_handler)

        # Transaction logger (for audit trail)
        self.transaction_logger = logging.getLogger("transactions")
        self.transaction_logger.setLevel(logging.INFO)

        transaction_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, "transactions.log"),
            when="D",
            interval=1,
            backupCount=30,  # Keep 30 days
        )
        transaction_handler.setFormatter(json_formatter)
        self.transaction_logger.addHandler(transaction_handler)

        # Security logger (for fraud detection and security events)
        self.security_logger = logging.getLogger("security")
        self.security_logger.setLevel(logging.WARNING)

        security_handler = RotatingFileHandler(
            os.path.join(log_dir, "security.log"),
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=10,
        )
        security_handler.setFormatter(detailed_formatter)
        self.security_logger.addHandler(security_handler)

        # API access logger
        self.api_logger = logging.getLogger("api_access")
        self.api_logger.setLevel(logging.INFO)

        api_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, "api_access.log"),
            when="H",
            interval=1,
            backupCount=24,  # Keep 24 hours
        )
        api_handler.setFormatter(json_formatter)
        self.api_logger.addHandler(api_handler)

        # Error logger
        self.error_logger = logging.getLogger("errors")
        self.error_logger.setLevel(logging.ERROR)

        error_handler = RotatingFileHandler(
            os.path.join(log_dir, "errors.log"),
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=10,
        )
        error_handler.setFormatter(detailed_formatter)
        self.error_logger.addHandler(error_handler)

    def log_transaction(
        self, transaction_data: Dict[str, Any], event_type: str = "transaction"
    ):
        """Log transaction events with structured data"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "transaction_id": transaction_data.get("transaction_id"),
            "amount": transaction_data.get("amount"),
            "currency": transaction_data.get("currency", "CRC"),
            "transaction_type": transaction_data.get("transaction_type"),
            "sender_phone": transaction_data.get("sender_phone"),
            "receiver_phone": transaction_data.get("receiver_phone"),
            "from_account": transaction_data.get("from_account_id"),
            "to_account": transaction_data.get("to_account_id"),
            "status": transaction_data.get("status"),
            "description": transaction_data.get("description", "")[
                :100
            ],  # Truncate long descriptions
        }

        self.transaction_logger.info("", extra={"json_data": log_entry})

    def log_security_event(
        self, event_type: str, details: Dict[str, Any], severity: str = "WARNING"
    ):
        """Log security-related events"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "details": details,
            "source_ip": details.get("source_ip", "unknown"),
            "user_agent": details.get("user_agent", "unknown"),
        }

        if severity.upper() == "CRITICAL":
            self.security_logger.critical(
                f"Security Event: {event_type}", extra={"json_data": log_entry}
            )
        elif severity.upper() == "ERROR":
            self.security_logger.error(
                f"Security Event: {event_type}", extra={"json_data": log_entry}
            )
        else:
            self.security_logger.warning(
                f"Security Event: {event_type}", extra={"json_data": log_entry}
            )

    def log_api_access(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        request_data: Optional[Dict] = None,
    ):
        """Log API access for monitoring and analytics"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "request_size": len(json.dumps(request_data)) if request_data else 0,
            "success": 200 <= status_code < 300,
        }

        self.api_logger.info("", extra={"json_data": log_entry})

    def log_fraud_detection(
        self, transaction_id: str, risk_score: int, alerts: list, action_taken: str
    ):
        """Log fraud detection events"""
        self.log_security_event(
            "fraud_detection",
            {
                "transaction_id": transaction_id,
                "risk_score": risk_score,
                "alerts": alerts,
                "action_taken": action_taken,
            },
            "WARNING" if risk_score >= 50 else "INFO",
        )

    def log_inter_bank_communication(
        self, bank_code: str, operation: str, success: bool, details: Dict
    ):
        """Log inter-bank communication events"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "inter_bank_communication",
            "bank_code": bank_code,
            "operation": operation,
            "success": success,
            "details": details,
        }

        if success:
            self.app_logger.info(
                f"Inter-bank communication successful: {operation} with bank {bank_code}"
            )
        else:
            self.error_logger.error(
                f"Inter-bank communication failed: {operation} with bank {bank_code}",
                extra={"json_data": log_entry},
            )

    def log_balance_update(
        self,
        account_number: str,
        previous_balance: float,
        new_balance: float,
        transaction_id: str,
        update_type: str,
    ):
        """Log account balance updates for audit trail"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "balance_update",
            "account_number": account_number,
            "previous_balance": previous_balance,
            "new_balance": new_balance,
            "change": new_balance - previous_balance,
            "transaction_id": transaction_id,
            "update_type": update_type,
        }

        self.transaction_logger.info("", extra={"json_data": log_entry})

    def log_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict] = None,
        exception: Optional[Exception] = None,
    ):
        """Log application errors with context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "exception_type": type(exception).__name__ if exception else None,
            "exception_details": str(exception) if exception else None,
        }

        self.error_logger.error(
            f"{error_type}: {error_message}", extra={"json_data": log_entry}
        )

    def log_system_startup(self, version: str, config: Dict):
        """Log system startup events"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "system_startup",
            "version": version,
            "config": {
                "database_url": (
                    config.get("database_url", "").replace(
                        config.get("database_url", "").split("://")[1].split("@")[0],
                        "***",
                    )
                    if "@" in config.get("database_url", "")
                    else config.get("database_url", "")
                ),
                "debug_mode": config.get("debug", False),
                "port": config.get("port", 5000),
            },
        }

        self.app_logger.info("System startup", extra={"json_data": log_entry})

    def get_log_summary(self, hours: int = 24) -> Dict:
        """Get summary of recent log activity"""
        # This is a simplified version - in production, you'd query log files or use a log aggregation service
        return {
            "period_hours": hours,
            "summary": "Log analysis would require parsing log files",
            "recommendation": "Use ELK stack or similar for production log analysis",
        }


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record):
        if hasattr(record, "json_data"):
            return json.dumps(record.json_data, ensure_ascii=False)
        else:
            # Fallback to standard formatting
            return super().format(record)


# Global logger instance
banking_logger = BankingLoggerService()
