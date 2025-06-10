# Análisis: PRUEBA/PRUEBA/server - Banco Secundario Python

## 🏦 Resumen General

Banco secundario implementado en Python Flask, diseñado específicamente para recibir y procesar transferencias SINPE desde otros bancos. Arquitectura simplificada enfocada en procesamiento de transacciones entrantes.

## 📁 Estructura del Proyecto

```txt
PRUEBA/PRUEBA/server/
├── app.py                    # Aplicación Flask principal
├── config.py                 # Configuraciones del sistema
├── services/                 # Servicios de negocio
│   ├── auth_service.py       # Autenticación y autorización
│   └── transfer_service.py   # Procesamiento de transferencias
└── utils/
    └── logger.py             # Sistema de logging
```

## 🔧 Arquitectura Simplificada

### Componentes Core

- **Flask App**: Servidor HTTP básico con endpoints SINPE
- **Transfer Service**: Lógica de procesamiento de transferencias
- **Auth Service**: Validación de requests inter-banco
- **Logger**: Sistema de logging para auditoría

## 📡 Endpoints de Recepción

```txt
POST /api/sinpe-transfer         # Recibir SINPE tradicional
POST /api/sinpe-movil-transfer   # Recibir SINPE móvil
GET  /health                     # Health check
POST /api/auth/validate          # Validación de autenticación
```

## 🔐 Protocolo de Seguridad

### Validación HMAC

```python
def verify_hmac(payload, received_hmac):
    secret = "supersecreta123"
    # Reconstruir mensaje según tipo de transferencia
    if "phone_number" in payload["sender"]:
        # SINPE Móvil
        message = f"{secret},{payload['sender']['phone_number']},{payload['timestamp']},{payload['transaction_id']},{payload['amount']['value']}"
    else:
        # SINPE Tradicional  
        message = f"{secret},{payload['sender']['account_number']},{payload['timestamp']},{payload['transaction_id']},{payload['amount']['value']}"
    
    expected_hmac = hashlib.md5(message.encode()).hexdigest()
    return expected_hmac == received_hmac
```

## 🔄 Flujo de Procesamiento

### Recepción de Transferencias

1. **Recepción**: POST en endpoint SINPE correspondiente
2. **Validación Estructural**: Verificar campos requeridos
3. **Autenticación**: Validar HMAC signature
4. **Verificación de Cuenta**: Confirmar existencia de cuenta destino
5. **Procesamiento**: Acreditar fondos a cuenta local
6. **Registro**: Crear transacción en base de datos
7. **Respuesta**: Retornar confirmación o error

### Formato de Respuesta Estándar

```json
{
    "success": true,
    "message": "Transferencia procesada exitosamente",
    "transaction_id": "UUID",
    "timestamp": "ISO_TIMESTAMP",
    "details": {
        "amount": 50000.00,
        "currency": "CRC",
        "receiver_account": "CR21..."
    }
}
```

## 🗄️ Gestión de Datos

- **Base de Datos Local**: Probablemente SQLite
- **Registro de Transacciones**: Todas las transferencias entrantes
- **Log de Comunicaciones**: Historial de requests inter-banco
- **Estados de Transferencias**: Pending, Completed, Failed

## ⚙️ Configuración del Sistema

```python
# config.py - Configuraciones típicas
BANK_CODE = "XXX"  # Código asignado por BCCR
SECRET_KEY = "supersecreta123"
DATABASE_URL = "sqlite:///bank_secondary.db"
ALLOWED_ORIGINS = [
    "192.168.1.10:5000",  # Banco principal
    "192.168.2.10:3001"   # Otros bancos autorizados
]
HMAC_SECRET = "supersecreta123"
```

## 🧪 Casos de Uso Principales

1. **Recibir transferencias del banco principal (152)**
2. **Validar usuarios locales por número de teléfono**
3. **Procesar SINPE móvil entrante**
4. **Mantener historial completo de transacciones**
5. **Responder health checks para monitoreo**
6. **Manejar errores de red y timeouts**

## 🔧 Integración y Compatibilidad

- **Protocolo Compatible**: Misma estructura de payloads que banco principal
- **HMAC Idéntico**: Mismo algoritmo MD5 para validación
- **Endpoints Estándar**: Naming consistente con otros bancos
- **Error Handling**: Códigos HTTP estándar
- **JSON Responses**: Formato estructurado para respuestas

## 🔍 Características de Operación

- **Modo Receptor**: Principalmente para recibir transferencias
- **Validación Robusta**: Verificación completa de payloads
- **Logging Detallado**: Registro de todas las operaciones
- **Manejo de Errores**: Respuestas claras para debugging
- **Health Monitoring**: Disponibilidad para otros bancos
