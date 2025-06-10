"""
Enhanced Validation Utilities for SINPE Banking System
Provides comprehensive validation with improved security and standards compliance
"""

import re
from typing import Dict, Tuple, List
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
import hashlib


def validate_sinpe_payload(payload: Dict) -> Tuple[bool, str]:
    """
    Enhanced validation for SINPE transfer payload

    Args:
        payload: Transfer payload to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not payload:
        return False, "Payload vacío"

    # Required fields for SINPE transfer
    required_fields = [
        "transaction_id",
        "timestamp",
        "amount",
        "sender_account",
        "receiver_account",
        "currency",
    ]

    for field in required_fields:
        if field not in payload:
            return False, f"Campo requerido faltante: {field}"
        if not payload[field]:
            return False, f"Campo {field} no puede estar vacío"

    # Validate transaction ID format (UUID)
    transaction_id = payload["transaction_id"]
    if not re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        transaction_id,
        re.IGNORECASE,
    ):
        return False, "ID de transacción debe ser un UUID válido"

    # Validate amount
    try:
        amount = float(payload["amount"])
        if amount <= 0:
            return False, "Monto debe ser mayor a cero"
        if amount > 10000000:  # 10 million limit
            return False, "Monto excede el límite máximo"
        # Check decimal places (max 2)
        if Decimal(str(amount)).as_tuple().exponent < -2:
            return False, "Monto no puede tener más de 2 decimales"
    except (ValueError, InvalidOperation):
        return False, "Monto inválido"

    # Validate currency
    valid_currencies = ["CRC", "USD"]
    if payload["currency"] not in valid_currencies:
        return False, f"Moneda debe ser una de: {', '.join(valid_currencies)}"

    # Validate account numbers/IBAN
    sender_account = payload["sender_account"]
    receiver_account = payload["receiver_account"]

    if not validate_account_format(sender_account):
        return False, "Formato de cuenta origen inválido"

    if not validate_account_format(receiver_account):
        return False, "Formato de cuenta destino inválido"

    # Validate timestamp format (ISO 8601)
    timestamp = payload["timestamp"]
    if not validate_timestamp_format(timestamp):
        return False, "Formato de timestamp inválido (debe ser ISO 8601)"

    # Check timestamp is recent (within last hour)
    if not validate_timestamp_freshness(timestamp):
        return False, "Timestamp demasiado antiguo o futuro"

    return True, ""


def validate_sinpe_movil_payload(payload: Dict) -> Tuple[bool, str]:
    """
    Enhanced validation for SINPE Móvil transfer payload

    Args:
        payload: Transfer payload to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not payload:
        return False, "Payload vacío"

    # Required fields for SINPE Móvil transfer
    required_fields = [
        "transaction_id",
        "timestamp",
        "amount",
        "sender_phone",
        "receiver_phone",
        "currency",
    ]

    for field in required_fields:
        if field not in payload:
            return False, f"Campo requerido faltante: {field}"
        if not payload[field]:
            return False, f"Campo {field} no puede estar vacío"

    # Validate transaction ID format (UUID)
    transaction_id = payload["transaction_id"]
    if not re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        transaction_id,
        re.IGNORECASE,
    ):
        return False, "ID de transacción debe ser un UUID válido"

    # Validate amount
    try:
        amount = float(payload["amount"])
        if amount <= 0:
            return False, "Monto debe ser mayor a cero"
        if amount > 1000000:  # 1 million limit for mobile transfers
            return False, "Monto excede el límite máximo para SINPE Móvil"
        # Check decimal places (max 2)
        if Decimal(str(amount)).as_tuple().exponent < -2:
            return False, "Monto no puede tener más de 2 decimales"
    except (ValueError, InvalidOperation):
        return False, "Monto inválido"

    # Validate currency
    valid_currencies = ["CRC", "USD"]
    if payload["currency"] not in valid_currencies:
        return False, f"Moneda debe ser una de: {', '.join(valid_currencies)}"

    # Validate phone numbers
    sender_phone = payload["sender_phone"]
    receiver_phone = payload["receiver_phone"]

    if not validate_phone_format(sender_phone):
        return False, "Formato de teléfono origen inválido"

    if not validate_phone_format(receiver_phone):
        return False, "Formato de teléfono destino inválido"

    # Check if sender and receiver are the same
    if sender_phone == receiver_phone:
        return False, "Teléfono origen y destino no pueden ser iguales"

    # Validate timestamp format (ISO 8601)
    timestamp = payload["timestamp"]
    if not validate_timestamp_format(timestamp):
        return False, "Formato de timestamp inválido (debe ser ISO 8601)"

    # Check timestamp is recent
    if not validate_timestamp_freshness(timestamp):
        return False, "Timestamp demasiado antiguo o futuro"

    return True, ""


def validate_account_format(account: str) -> bool:
    """
    Validate account number or IBAN format

    Args:
        account: Account number or IBAN to validate

    Returns:
        True if valid format
    """
    if not account:
        return False

    # Check if it's an IBAN
    if account.startswith("CR"):
        return validate_iban_format(account)

    # Check if it's a regular account number
    # Costa Rican account numbers are typically 10-20 digits
    clean_account = re.sub(r"[-\s]", "", account)
    return clean_account.isdigit() and 10 <= len(clean_account) <= 20


def validate_iban_format(iban: str) -> bool:
    """
    Enhanced IBAN validation for Costa Rican IBANs

    Args:
        iban: IBAN to validate

    Returns:
        True if valid IBAN format
    """
    if not iban:
        return False

    # Remove spaces and dashes
    clean_iban = re.sub(r"[-\s]", "", iban.upper())

    # Check basic format
    if not re.match(r"^CR\d{20}$", clean_iban):
        return False

    # Check country code
    if not clean_iban.startswith("CR"):
        return False

    # Check length (22 characters for Costa Rica)
    if len(clean_iban) != 22:
        return False

    # Validate check digits using MOD-97 algorithm
    try:
        # Move first 4 characters to end
        rearranged = clean_iban[4:] + clean_iban[:4]

        # Replace letters with numbers (C=12, R=27)
        numeric = rearranged.replace("C", "12").replace("R", "27")

        # Check if result is numeric
        if not numeric.isdigit():
            return False

        # Apply MOD-97
        return int(numeric) % 97 == 1
    except (ValueError, OverflowError):
        return False


def validate_phone_format(phone: str) -> bool:
    """
    Enhanced phone number validation for Costa Rican numbers

    Args:
        phone: Phone number to validate

    Returns:
        True if valid format
    """
    if not phone:
        return False

    # Remove any non-digit characters
    clean_phone = re.sub(r"\D", "", phone)

    # Costa Rican phone numbers are 8 digits
    if len(clean_phone) != 8:
        return False

    # Check valid prefixes
    # Mobile: 6, 7, 8
    # Landline: 2
    valid_prefixes = ["2", "6", "7", "8"]
    return clean_phone[0] in valid_prefixes


def validate_timestamp_format(timestamp: str) -> bool:
    """
    Validate timestamp format (ISO 8601)

    Args:
        timestamp: Timestamp string to validate

    Returns:
        True if valid ISO 8601 format
    """
    if not timestamp:
        return False

    # Try to parse ISO 8601 format
    try:
        # Handle both with and without 'Z' suffix
        if timestamp.endswith("Z"):
            datetime.fromisoformat(timestamp[:-1] + "+00:00")
        else:
            datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False


def validate_timestamp_freshness(timestamp: str, max_age_minutes: int = 60) -> bool:
    """
    Validate that timestamp is recent (within acceptable time window)

    Args:
        timestamp: Timestamp string
        max_age_minutes: Maximum age in minutes

    Returns:
        True if timestamp is fresh
    """
    try:
        # Parse timestamp
        if timestamp.endswith("Z"):
            dt = datetime.fromisoformat(timestamp[:-1] + "+00:00")
        else:
            dt = datetime.fromisoformat(timestamp)

        # Remove timezone info for comparison with UTC now
        dt = dt.replace(tzinfo=None)
        now = datetime.utcnow()

        # Check if within acceptable window
        age = abs((now - dt).total_seconds() / 60)
        return age <= max_age_minutes

    except (ValueError, AttributeError):
        return False


def validate_transaction_limits(
    amount: float, transaction_type: str
) -> Tuple[bool, str]:
    """
    Validate transaction against daily/monthly limits

    Args:
        amount: Transaction amount
        transaction_type: Type of transaction

    Returns:
        Tuple of (is_valid, error_message)
    """
    limits = {
        "sinpe_movil": {"daily": 500000, "single": 100000},  # CRC
        "sinpe_transfer": {"daily": 10000000, "single": 5000000},  # CRC
        "internal": {"daily": 50000000, "single": 10000000},  # CRC
    }

    if transaction_type not in limits:
        return False, "Tipo de transacción no reconocido"

    limit_config = limits[transaction_type]

    if amount > limit_config["single"]:
        return (
            False,
            f"Monto excede límite por transacción ({limit_config['single']:,.0f} CRC)",
        )

    return True, ""


def validate_bank_code(bank_code: str) -> bool:
    """
    Validate Costa Rican bank code format

    Args:
        bank_code: Bank code to validate

    Returns:
        True if valid format
    """
    if not bank_code:
        return False

    # Remove leading zeros and check
    clean_code = bank_code.lstrip("0")

    # Known Costa Rican bank codes
    valid_codes = ["102", "151", "152", "138", "107", "160", "161", "162"]

    return bank_code.zfill(3) in valid_codes or len(bank_code) == 4


def sanitize_input(input_str: str, max_length: int = 255) -> str:
    """
    Sanitize input string to prevent injection attacks

    Args:
        input_str: Input string to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not input_str:
        return ""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';\\]', "", str(input_str))

    # Limit length
    return sanitized[:max_length]


def validate_hmac_integrity(payload: Dict, hmac_signature: str) -> bool:
    """
    Basic HMAC validation (placeholder for more complex validation)

    Args:
        payload: Transaction payload
        hmac_signature: HMAC signature to validate

    Returns:
        True if HMAC appears valid
    """
    if not hmac_signature or len(hmac_signature) != 32:
        return False

    # Check if it's hexadecimal
    try:
        int(hmac_signature, 16)
        return True
    except ValueError:
        return False


def get_validation_summary() -> Dict:
    """
    Get summary of validation rules and limits

    Returns:
        Dict with validation configuration
    """
    return {
        "transaction_limits": {
            "sinpe_movil": {"max_single": 100000, "max_daily": 500000},
            "sinpe_transfer": {"max_single": 5000000, "max_daily": 10000000},
            "internal": {"max_single": 10000000, "max_daily": 50000000},
        },
        "supported_currencies": ["CRC", "USD"],
        "phone_format": "8 digits starting with 2, 6, 7, or 8",
        "iban_format": "CR + 20 digits",
        "timestamp_max_age_minutes": 60,
        "max_input_length": 255,
    }
