"""
HMAC Generation Utilities for SINPE Banking System
FORMATO CORREGIDO: Compatible con ecosistema inter-banco usando comas como separadores
"""

import hashlib
import hmac

SECRET_KEY = "supersecreta123"


def generate_hmac_for_account_transfer(
    account_number: str,
    timestamp: str,
    transaction_id: str,
    amount: float,
    clave: str = SECRET_KEY,
) -> str:
    """
    Generate HMAC MD5 for account-to-account transfers
    FORMATO CORREGIDO: Con comas como separadores para compatibilidad inter-banco

    Args:
        account_number: Account number of sender
        timestamp: ISO 8601 timestamp
        transaction_id: UUID of transaction
        amount: Transfer amount
        clave: Secret key for HMAC generation

    Returns:
        HMAC in hexadecimal format
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar formato con comas como esperan otros bancos
    mensaje = f"{clave},{account_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()


def generate_hmac_for_phone_transfer(
    phone_number: str,
    timestamp: str,
    transaction_id: str,
    amount: float,
    clave: str = SECRET_KEY,
) -> str:
    """
    Generate HMAC MD5 for SINPE mobile transfers (phone-based)
    FORMATO CORREGIDO: Con comas como separadores para compatibilidad inter-banco

    Args:
        phone_number: Phone number of recipient
        timestamp: ISO 8601 timestamp
        transaction_id: UUID of transaction
        amount: Transfer amount
        clave: Secret key for HMAC generation

    Returns:
        HMAC in hexadecimal format
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar formato con comas como esperan otros bancos
    mensaje = f"{clave},{phone_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()


def generar_hmac(
    account_number: str,
    timestamp: str,
    transaction_id: str,
    amount: float,
    clave: str = SECRET_KEY,
) -> str:
    """
    Función compatible con code.py - Generate HMAC for validation
    FORMATO CORREGIDO: Con comas como separadores para compatibilidad inter-banco

    Args:
        account_number: Account number
        timestamp: Transaction timestamp
        transaction_id: Transaction ID
        amount: Amount value
        clave: Secret key

    Returns:
        HMAC in hexadecimal format
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar formato con comas como esperan otros bancos
    mensaje = f"{clave},{account_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()


def verify_hmac(payload: dict, provided_hmac: str, clave: str = SECRET_KEY) -> bool:
    """
    Verify HMAC signature for incoming transfer requests with improved validation

    Args:
        payload: Transfer payload containing all fields
        provided_hmac: HMAC provided in request
        clave: Secret key for verification

    Returns:
        True if HMAC is valid, False otherwise
    """
    if not payload or not provided_hmac:
        return False

    try:
        # Extract required fields based on transfer type
        if "receiver_phone" in payload:
            # SINPE Móvil transfer
            phone = payload.get("receiver_phone", "")
            timestamp = payload.get("timestamp", "")
            transaction_id = payload.get("transaction_id", "")
            amount = payload.get("amount", 0)
            
            expected_hmac = generate_hmac_for_phone_transfer(
                phone, timestamp, transaction_id, amount, clave
            )
        elif "receiver_account" in payload:
            # Traditional SINPE transfer
            account = payload.get("receiver_account", "")
            timestamp = payload.get("timestamp", "")
            transaction_id = payload.get("transaction_id", "")
            amount = payload.get("amount", 0)
            
            expected_hmac = generate_hmac_for_account_transfer(
                account, timestamp, transaction_id, amount, clave
            )
        else:
            # Try legacy format
            sender = payload.get("sender", {})
            if sender.get("phone_number"):
                # Phone-based transfer (SINPE Móvil)
                expected_hmac = generate_hmac_for_phone_transfer(
                    sender["phone_number"],
                    payload["timestamp"],
                    payload["transaction_id"],
                    payload["amount"]["value"] if isinstance(payload["amount"], dict) else payload["amount"],
                    clave,
                )
            elif sender.get("account_number"):
                # Account-based transfer (SINPE)
                expected_hmac = generate_hmac_for_account_transfer(
                    sender["account_number"],
                    payload["timestamp"],
                    payload["transaction_id"],
                    payload["amount"]["value"] if isinstance(payload["amount"], dict) else payload["amount"],
                    clave,
                )
            else:
                return False

        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected_hmac.lower(), provided_hmac.lower())
        
    except Exception:
        return False


def extract_bank_code_from_iban(iban: str) -> str:
    """
    Extract bank code from IBAN (positions 4-7 in clean IBAN)

    Args:
        iban: IBAN string

    Returns:
        Bank code (4 digits)
    """
    if not iban:
        return ""
    
    # Remove dashes and ensure we have enough characters
    clean_iban = iban.replace("-", "")
    if len(clean_iban) < 8:
        return ""
    
    # Bank code is at positions 4-7 in Costa Rican IBAN
    return clean_iban[4:8]


def is_external_transfer(bank_code: str) -> bool:
    """
    Determine if transfer is to external bank (not our bank code "152")

    Args:
        bank_code: Bank code to check

    Returns:
        True if external bank, False if internal
    """
    LOCAL_BANK_CODE = "0152"  # Updated to 4-digit format
    return bank_code != LOCAL_BANK_CODE
