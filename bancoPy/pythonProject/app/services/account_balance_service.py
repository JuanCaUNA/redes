"""
Account Balance Service - Manages account balances and transaction history
"""

from app.models import db, Account, Transaction
from decimal import Decimal
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class AccountBalanceService:
    """Service for managing account balances with proper transaction handling"""

    @staticmethod
    def get_account_balance(account_number: str) -> Optional[Decimal]:
        """
        Get current balance for an account

        Args:
            account_number: Account number to check

        Returns:
            Current balance or None if account doesn't exist
        """
        account = Account.query.filter_by(number=account_number).first()
        return account.balance if account else None

    @staticmethod
    def update_balance_atomic(
        account_number: str, amount: Decimal, transaction_type: str = "adjustment"
    ) -> Dict:
        """
        Update account balance atomically with validation

        Args:
            account_number: Account number to update
            amount: Amount to add/subtract (negative for debits)
            transaction_type: Type of transaction for audit

        Returns:
            Dict with success status and new balance
        """
        try:
            account = Account.query.filter_by(number=account_number).first()
            if not account:
                return {"success": False, "error": "Cuenta no encontrada"}

            # Check for sufficient funds on debits
            if amount < 0 and account.balance + amount < 0:
                return {
                    "success": False,
                    "error": "Fondos insuficientes",
                    "current_balance": float(account.balance),
                    "requested_amount": float(amount),
                }

            # Update balance
            previous_balance = account.balance
            account.balance += amount

            # Commit the change
            db.session.commit()

            logger.info(
                f"Balance updated for account {account_number}: "
                f"{previous_balance} -> {account.balance} (change: {amount})"
            )

            return {
                "success": True,
                "previous_balance": float(previous_balance),
                "new_balance": float(account.balance),
                "change": float(amount),
            }

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating balance for {account_number}: {str(e)}")
            return {"success": False, "error": f"Error interno: {str(e)}"}

    @staticmethod
    def transfer_between_accounts(
        from_account: str,
        to_account: str,
        amount: Decimal,
        description: str = "",
        transaction_id: str = None,
    ) -> Dict:
        """
        Transfer money between two accounts atomically

        Args:
            from_account: Source account number
            to_account: Destination account number
            amount: Transfer amount
            description: Transfer description
            transaction_id: Optional transaction ID

        Returns:
            Dict with transfer result
        """
        if amount <= 0:
            return {"success": False, "error": "Monto debe ser mayor a cero"}

        try:
            # Get both accounts
            source_acc = Account.query.filter_by(number=from_account).first()
            dest_acc = Account.query.filter_by(number=to_account).first()

            if not source_acc:
                return {"success": False, "error": "Cuenta origen no encontrada"}
            if not dest_acc:
                return {"success": False, "error": "Cuenta destino no encontrada"}

            # Check sufficient funds
            if source_acc.balance < amount:
                return {
                    "success": False,
                    "error": "Fondos insuficientes",
                    "available": float(source_acc.balance),
                    "requested": float(amount),
                }

            # Perform atomic transfer
            source_acc.balance -= amount
            dest_acc.balance += amount

            # Create transaction record if transaction_id provided
            if transaction_id:
                transaction = Transaction(
                    transaction_id=transaction_id,
                    from_account_id=source_acc.id,
                    to_account_id=dest_acc.id,
                    amount=amount,
                    description=description,
                    status="completed",
                    transaction_type="internal_transfer",
                )
                db.session.add(transaction)

            db.session.commit()

            logger.info(
                f"Transfer completed: {from_account} -> {to_account}, "
                f"Amount: {amount}, Transaction ID: {transaction_id}"
            )

            return {
                "success": True,
                "transaction_id": transaction_id,
                "from_account": from_account,
                "to_account": to_account,
                "amount": float(amount),
                "source_new_balance": float(source_acc.balance),
                "dest_new_balance": float(dest_acc.balance),
            }

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in transfer {from_account} -> {to_account}: {str(e)}")
            return {"success": False, "error": f"Error en transferencia: {str(e)}"}

    @staticmethod
    def get_transaction_history(
        account_number: str, limit: int = 50, transaction_type: str = None
    ) -> List[Dict]:
        """
        Get transaction history for an account

        Args:
            account_number: Account number
            limit: Maximum number of transactions to return
            transaction_type: Filter by transaction type

        Returns:
            List of transaction dictionaries
        """
        try:
            account = Account.query.filter_by(number=account_number).first()
            if not account:
                return []

            # Get both sent and received transactions
            query_sent = Transaction.query.filter_by(from_account_id=account.id)
            query_received = Transaction.query.filter_by(to_account_id=account.id)

            if transaction_type:
                query_sent = query_sent.filter_by(transaction_type=transaction_type)
                query_received = query_received.filter_by(
                    transaction_type=transaction_type
                )

            sent_transactions = query_sent.limit(limit // 2).all()
            received_transactions = query_received.limit(limit // 2).all()

            all_transactions = sent_transactions + received_transactions
            all_transactions.sort(key=lambda x: x.created_at, reverse=True)

            return [tx.to_dict() for tx in all_transactions[:limit]]

        except Exception as e:
            logger.error(
                f"Error getting transaction history for {account_number}: {str(e)}"
            )
            return []

    @staticmethod
    def validate_account_integrity(account_number: str) -> Dict:
        """
        Validate account balance against transaction history

        Args:
            account_number: Account to validate

        Returns:
            Dict with validation results
        """
        try:
            account = Account.query.filter_by(number=account_number).first()
            if not account:
                return {"valid": False, "error": "Cuenta no encontrada"}

            # Calculate balance from transactions
            sent_transactions = Transaction.query.filter_by(
                from_account_id=account.id, status="completed"
            ).all()

            received_transactions = Transaction.query.filter_by(
                to_account_id=account.id, status="completed"
            ).all()

            calculated_balance = Decimal("0.00")

            # Subtract sent amounts
            for tx in sent_transactions:
                calculated_balance -= tx.amount

            # Add received amounts
            for tx in received_transactions:
                calculated_balance += tx.amount

            # Compare with stored balance
            balance_matches = abs(account.balance - calculated_balance) < Decimal(
                "0.01"
            )

            return {
                "valid": balance_matches,
                "stored_balance": float(account.balance),
                "calculated_balance": float(calculated_balance),
                "difference": float(account.balance - calculated_balance),
                "total_transactions": len(sent_transactions)
                + len(received_transactions),
            }

        except Exception as e:
            logger.error(f"Error validating account {account_number}: {str(e)}")
            return {"valid": False, "error": f"Error en validación: {str(e)}"}
