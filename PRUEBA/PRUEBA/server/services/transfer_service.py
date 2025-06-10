from datetime import datetime
from server.utils.logger import logger, log_transaction
from server.config import Config

class TransferService:
    @staticmethod
    def process_sinpe_transfer(data):
        """Process a SINPE transfer."""
        try:
            # Validate sender
            if not TransferService._validate_account(data["sender"]):
                return False, "Invalid sender account information"
            
            # Validate receiver
            if not TransferService._validate_account(data["receiver"]):
                return False, "Invalid receiver account information"
            
            # Process the transfer (implement your business logic here)
            # This is where you would:
            # 1. Check account balances
            # 2. Update account balances
            # 3. Record the transaction
            # 4. Notify relevant parties
            
            # For now, we'll just simulate a successful transfer
            log_transaction('sinpe_transfer', data, 'success')
            
            return True, {
                "status": "success",
                "message": "Transfer processed successfully",
                "transaction_id": data["transaction_id"],
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
        except Exception as e:
            logger.error(f"Error processing SINPE transfer: {str(e)}")
            return False, str(e)

    @staticmethod
    def process_sinpe_movil_transfer(data):
        """Process a SINPE Móvil transfer."""
        try:
            # Validate sender phone
            if not TransferService._validate_phone(data["sender"]["phone_number"]):
                return False, "Invalid sender phone number"
            
            # Validate receiver phone
            if not TransferService._validate_phone(data["receiver"]["phone_number"]):
                return False, "Invalid receiver phone number"
            
            # Process the transfer (implement your business logic here)
            # This is where you would:
            # 1. Check phone number registrations
            # 2. Update account balances
            # 3. Record the transaction
            # 4. Send SMS notifications
            
            # For now, we'll just simulate a successful transfer
            log_transaction('sinpe_movil_transfer', data, 'success')
            
            return True, {
                "status": "success",
                "message": "SINPE Móvil transfer processed successfully",
                "transaction_id": data["transaction_id"],
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
        except Exception as e:
            logger.error(f"Error processing SINPE Móvil transfer: {str(e)}")
            return False, str(e)

    @staticmethod
    def _validate_account(account_data):
        """Validate account information."""
        required_fields = ["account_number", "bank_code", "name"]
        return all(field in account_data for field in required_fields)

    @staticmethod
    def _validate_phone(phone_number):
        """Validate phone number format."""
        # Basic validation for Costa Rican phone numbers
        # This should be enhanced based on actual requirements
        return phone_number.isdigit() and len(phone_number) == 8 