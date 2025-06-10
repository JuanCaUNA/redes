"""
Transaction Monitoring Service - Real-time monitoring and fraud detection
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from sqlalchemy import and_, or_, func
from app.models import db, Transaction, Account, PhoneLink
import threading
import time

logger = logging.getLogger(__name__)


class TransactionMonitoringService:
    """Service for monitoring transactions and detecting suspicious activity"""

    def __init__(self):
        self.fraud_rules = self._load_fraud_rules()
        self.monitoring_enabled = True
        self._start_background_monitoring()

    def _load_fraud_rules(self) -> Dict:
        """Load fraud detection rules"""
        return {
            "max_daily_amount": {
                "sinpe_movil": 500000,  # CRC
                "sinpe_transfer": 10000000,  # CRC
                "internal": 50000000  # CRC
            },
            "max_hourly_transactions": 10,
            "max_single_transaction": {
                "sinpe_movil": 100000,  # CRC
                "sinpe_transfer": 5000000,  # CRC
                "internal": 10000000  # CRC
            },
            "velocity_thresholds": {
                "transactions_per_minute": 5,
                "amount_per_minute": 200000  # CRC
            },
            "suspicious_patterns": {
                "round_amounts": True,  # Flag round amounts like 100000, 500000
                "rapid_succession": 60,  # Seconds between transactions
                "account_jumping": 5  # Max different accounts per hour
            }
        }

    def monitor_transaction(self, transaction_data: Dict) -> Dict:
        """
        Monitor a transaction in real-time for fraud detection

        Args:
            transaction_data: Transaction data to monitor

        Returns:
            Dict with monitoring results and risk score
        """
        try:
            risk_score = 0
            alerts = []

            # Extract key information
            amount = Decimal(str(transaction_data.get("amount", 0)))
            transaction_type = transaction_data.get("transaction_type", "unknown")
            sender_phone = transaction_data.get("sender_phone")
            receiver_phone = transaction_data.get("receiver_phone")
            from_account_id = transaction_data.get("from_account_id")
            to_account_id = transaction_data.get("to_account_id")

            # Rule 1: Check single transaction limits
            single_limit_check = self._check_single_transaction_limit(amount, transaction_type)
            if not single_limit_check["passed"]:
                risk_score += 50
                alerts.append(single_limit_check["message"])

            # Rule 2: Check daily transaction limits
            daily_limit_check = self._check_daily_limits(from_account_id, amount, transaction_type)
            if not daily_limit_check["passed"]:
                risk_score += 30
                alerts.append(daily_limit_check["message"])

            # Rule 3: Check transaction velocity
            velocity_check = self._check_velocity_limits(from_account_id, sender_phone)
            if not velocity_check["passed"]:
                risk_score += 40
                alerts.append(velocity_check["message"])

            # Rule 4: Check for suspicious patterns
            pattern_check = self._check_suspicious_patterns(transaction_data)
            if not pattern_check["passed"]:
                risk_score += pattern_check["risk_score"]
                alerts.extend(pattern_check["alerts"])

            # Rule 5: Check for unusual recipient behavior
            recipient_check = self._check_recipient_patterns(receiver_phone, to_account_id)
            if not recipient_check["passed"]:
                risk_score += 20
                alerts.append(recipient_check["message"])

            # Determine overall risk level
            risk_level = self._calculate_risk_level(risk_score)

            result = {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "alerts": alerts,
                "allow_transaction": risk_score < 70,
                "requires_review": 40 <= risk_score < 70,
                "monitoring_timestamp": datetime.utcnow().isoformat()
            }

            # Log high-risk transactions
            if risk_score >= 50:
                logger.warning(
                    f"High-risk transaction detected: Score={risk_score}, "
                    f"Type={transaction_type}, Amount={amount}, Alerts={alerts}"
                )

            return result

        except Exception as e:
            logger.error(f"Error in transaction monitoring: {str(e)}")
            return {
                "risk_score": 0,
                "risk_level": "unknown",
                "alerts": ["Error en monitoreo"],
                "allow_transaction": True,
                "requires_review": False,
                "error": str(e)
            }

    def _check_single_transaction_limit(self, amount: Decimal, transaction_type: str) -> Dict:
        """Check if transaction exceeds single transaction limits"""
        limits = self.fraud_rules["max_single_transaction"]
        limit = limits.get(transaction_type, limits.get("internal", 10000000))

        if amount > limit:
            return {
                "passed": False,
                "message": f"Transacción excede límite individual ({limit:,.0f} CRC)"
            }
        
        return {"passed": True, "message": ""}

    def _check_daily_limits(self, account_id: Optional[int], amount: Decimal, transaction_type: str) -> Dict:
        """Check daily transaction limits for account"""
        if not account_id:
            return {"passed": True, "message": ""}

        try:
            # Get today's transactions
            today = datetime.utcnow().date()
            daily_transactions = Transaction.query.filter(
                and_(
                    Transaction.from_account_id == account_id,
                    func.date(Transaction.created_at) == today,
                    Transaction.status == "completed"
                )
            ).all()

            # Calculate daily total
            daily_total = sum(tx.amount for tx in daily_transactions)
            new_total = daily_total + amount

            # Check limit
            limits = self.fraud_rules["max_daily_amount"]
            daily_limit = limits.get(transaction_type, limits.get("internal", 50000000))

            if new_total > daily_limit:
                return {
                    "passed": False,
                    "message": f"Excede límite diario ({daily_limit:,.0f} CRC). Actual: {new_total:,.0f} CRC"
                }

            return {"passed": True, "message": ""}

        except Exception as e:
            logger.error(f"Error checking daily limits: {str(e)}")
            return {"passed": True, "message": ""}

    def _check_velocity_limits(self, account_id: Optional[int], phone: Optional[str]) -> Dict:
        """Check transaction velocity (frequency)"""
        try:
            # Check last minute activity
            one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
            
            # Check by account
            if account_id:
                recent_by_account = Transaction.query.filter(
                    and_(
                        Transaction.from_account_id == account_id,
                        Transaction.created_at >= one_minute_ago
                    )
                ).count()

                if recent_by_account >= self.fraud_rules["velocity_thresholds"]["transactions_per_minute"]:
                    return {
                        "passed": False,
                        "message": "Demasiadas transacciones por minuto desde esta cuenta"
                    }

            # Check by phone
            if phone:
                recent_by_phone = Transaction.query.filter(
                    and_(
                        Transaction.sender_phone == phone,
                        Transaction.created_at >= one_minute_ago
                    )
                ).count()

                if recent_by_phone >= self.fraud_rules["velocity_thresholds"]["transactions_per_minute"]:
                    return {
                        "passed": False,
                        "message": "Demasiadas transacciones por minuto desde este teléfono"
                    }

            return {"passed": True, "message": ""}

        except Exception as e:
            logger.error(f"Error checking velocity limits: {str(e)}")
            return {"passed": True, "message": ""}

    def _check_suspicious_patterns(self, transaction_data: Dict) -> Dict:
        """Check for suspicious transaction patterns"""
        alerts = []
        risk_score = 0

        amount = Decimal(str(transaction_data.get("amount", 0)))

        # Check for round amounts
        if self.fraud_rules["suspicious_patterns"]["round_amounts"]:
            if amount % 10000 == 0 and amount >= 50000:  # Round amounts like 50k, 100k, etc.
                alerts.append("Monto redondo sospechoso")
                risk_score += 10

        # Check for rapid succession (if timestamp provided)
        timestamp = transaction_data.get("timestamp")
        if timestamp and transaction_data.get("from_account_id"):
            try:
                recent_transactions = Transaction.query.filter(
                    and_(
                        Transaction.from_account_id == transaction_data["from_account_id"],
                        Transaction.created_at >= datetime.utcnow() - timedelta(seconds=60)
                    )
                ).count()

                if recent_transactions > 0:
                    alerts.append("Transacciones en sucesión rápida")
                    risk_score += 15

            except Exception:
                pass

        return {
            "passed": risk_score == 0,
            "alerts": alerts,
            "risk_score": risk_score
        }

    def _check_recipient_patterns(self, receiver_phone: Optional[str], to_account_id: Optional[int]) -> Dict:
        """Check for unusual recipient patterns"""
        try:
            if not receiver_phone and not to_account_id:
                return {"passed": True, "message": ""}

            # Check if recipient receives unusually high volume
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            
            received_count = 0
            if receiver_phone:
                received_count += Transaction.query.filter(
                    and_(
                        Transaction.receiver_phone == receiver_phone,
                        Transaction.created_at >= one_hour_ago,
                        Transaction.status == "completed"
                    )
                ).count()

            if to_account_id:
                received_count += Transaction.query.filter(
                    and_(
                        Transaction.to_account_id == to_account_id,
                        Transaction.created_at >= one_hour_ago,
                        Transaction.status == "completed"
                    )
                ).count()

            if received_count > 20:  # More than 20 transactions per hour
                return {
                    "passed": False,
                    "message": "Receptor con volumen inusualmente alto"
                }

            return {"passed": True, "message": ""}

        except Exception as e:
            logger.error(f"Error checking recipient patterns: {str(e)}")
            return {"passed": True, "message": ""}

    def _calculate_risk_level(self, risk_score: int) -> str:
        """Calculate risk level based on score"""
        if risk_score >= 70:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        elif risk_score >= 20:
            return "LOW"
        else:
            return "MINIMAL"

    def get_transaction_statistics(self, hours: int = 24) -> Dict:
        """Get transaction statistics for monitoring dashboard"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            # Total transactions
            total_transactions = Transaction.query.filter(
                Transaction.created_at >= cutoff_time
            ).count()

            # Total amount
            total_amount = db.session.query(
                func.sum(Transaction.amount)
            ).filter(
                Transaction.created_at >= cutoff_time
            ).scalar() or 0

            # Transactions by type
            transactions_by_type = db.session.query(
                Transaction.transaction_type,
                func.count(Transaction.id),
                func.sum(Transaction.amount)
            ).filter(
                Transaction.created_at >= cutoff_time
            ).group_by(Transaction.transaction_type).all()

            # Failed transactions
            failed_transactions = Transaction.query.filter(
                and_(
                    Transaction.created_at >= cutoff_time,
                    Transaction.status != "completed"
                )
            ).count()

            return {
                "period_hours": hours,
                "total_transactions": total_transactions,
                "total_amount": float(total_amount),
                "failed_transactions": failed_transactions,
                "success_rate": (total_transactions - failed_transactions) / max(total_transactions, 1) * 100,
                "transactions_by_type": [
                    {
                        "type": tx_type,
                        "count": count,
                        "amount": float(amount or 0)
                    }
                    for tx_type, count, amount in transactions_by_type
                ],
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating transaction statistics: {str(e)}")
            return {"error": str(e)}

    def _start_background_monitoring(self):
        """Start background monitoring thread"""
        def background_monitor():
            while self.monitoring_enabled:
                try:
                    self._periodic_checks()
                    time.sleep(300)  # Check every 5 minutes
                except Exception as e:
                    logger.error(f"Error in background monitoring: {str(e)}")
                    time.sleep(60)  # Wait 1 minute before retrying

        monitor_thread = threading.Thread(target=background_monitor, daemon=True)
        monitor_thread.start()
        logger.info("Transaction monitoring background service started")

    def _periodic_checks(self):
        """Perform periodic fraud detection checks"""
        try:
            # Check for accounts with unusual activity in last hour
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            
            suspicious_accounts = db.session.query(
                Transaction.from_account_id,
                func.count(Transaction.id).label('tx_count'),
                func.sum(Transaction.amount).label('total_amount')
            ).filter(
                and_(
                    Transaction.created_at >= one_hour_ago,
                    Transaction.from_account_id.isnot(None)
                )
            ).group_by(Transaction.from_account_id).having(
                or_(
                    func.count(Transaction.id) > 15,  # More than 15 transactions
                    func.sum(Transaction.amount) > 1000000  # More than 1M CRC
                )
            ).all()

            if suspicious_accounts:
                logger.warning(f"Found {len(suspicious_accounts)} accounts with unusual activity")
                for account_id, tx_count, total_amount in suspicious_accounts:
                    logger.warning(
                        f"Account {account_id}: {tx_count} transactions, "
                        f"{total_amount:,.0f} CRC in last hour"
                    )

        except Exception as e:
            logger.error(f"Error in periodic checks: {str(e)}")

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring_enabled = False
        logger.info("Transaction monitoring stopped")

    def update_fraud_rules(self, new_rules: Dict):
        """Update fraud detection rules"""
        self.fraud_rules.update(new_rules)
        logger.info("Fraud detection rules updated")


# Global instance
transaction_monitor = TransactionMonitoringService()
