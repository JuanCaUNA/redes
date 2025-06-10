# SINPE API Implementation

This is a Python implementation of the SINPE (Sistema Nacional de Pagos Electrónicos) API for interbank transfers in Costa Rica.

## Features

- SINPE Transfer API endpoint
- SINPE Móvil Transfer API endpoint
- HMAC MD5 authentication
- SSL/TLS encryption
- Comprehensive logging
- Input validation
- Error handling

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
Edit the `API_KEYS` dictionary in `app.py` to add your bank's API key.

## Running the Server

```bash
python app.py
```

The server will start on `https://localhost:5000`

## API Endpoints

### 1. SINPE Transfer
- **URL**: `/api/sinpe-transfer`
- **Method**: `POST`
- **Headers**:
  - `X-API-Key`: Your bank's API key
  - `X-HMAC`: HMAC signature
  - `Content-Type`: `application/json`

Example request body:
```json
{
    "version": "1.0",
    "timestamp": "2025-06-06T16:24:00Z",
    "transaction_id": "TRX123456",
    "sender": {
        "account_number": "1234567890",
        "bank_code": "BANCO1",
        "name": "John Doe"
    },
    "receiver": {
        "account_number": "0987654321",
        "bank_code": "BANCO2",
        "name": "Jane Smith"
    },
    "amount": {
        "value": "1000.00",
        "currency": "CRC"
    },
    "description": "Payment for services"
}
```

### 2. SINPE Móvil Transfer
- **URL**: `/api/sinpe-movil-transfer`
- **Method**: `POST`
- **Headers**: Same as SINPE Transfer

Example request body:
```json
{
    "version": "1.0",
    "timestamp": "2025-06-06T16:24:00Z",
    "transaction_id": "TRX123456",
    "sender": {
        "phone_number": "88888888"
    },
    "receiver": {
        "phone_number": "77777777"
    },
    "amount": {
        "value": "1000.00",
        "currency": "CRC"
    },
    "description": "Payment for services"
}
```

## Security

- All endpoints require HMAC MD5 authentication
- SSL/TLS encryption is enabled by default
- API keys are required for all requests
- Input validation is performed on all requests
- All transactions are logged for audit purposes

## Logging

Transaction logs are stored in `sinpe_transactions.log` with the following format:
```
timestamp - level - message
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 400: Bad Request (missing or invalid fields)
- 401: Unauthorized (invalid API key or HMAC)
- 500: Internal Server Error 