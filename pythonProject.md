# Análisis: bancoPy/pythonProject - Banco Principal SINPE

## 🏦 Resumen General

Este es el banco principal del sistema SINPE implementado en Python con Flask. Actúa como hub central para transferencias SINPE y comunicación con bancos externos.

## 📁 Estructura del Proyecto

```txt
bancoPy/pythonProject/
├── main.py                    # Punto de entrada principal
├── run.sh                     # Script de startup
├── requirements.txt           # Dependencias Python
├── app/                       # Aplicación Flask
│   ├── __init__.py           # Factory de aplicación
│   ├── models/               # Modelos SQLAlchemy
│   ├── routes/               # Endpoints API
│   ├── services/             # Lógica de negocio
│   └── utils/                # Utilidades
├── config/                   # Configuración
│   ├── settings.py           # Configuraciones
│   └── banks.json            # Mapeo de bancos
├── database/                 # Base de datos
│   └── banking.db            # SQLite (auto-creado)
└── tests/                    # Suite de pruebas
```

## 🔧 Stack Tecnológico

- **Backend**: Python 3.8+ con Flask
- **Base de Datos**: SQLite con SQLAlchemy ORM
- **Interfaz**: Terminal UI con Rich library
- **API**: REST JSON con CORS habilitado
- **Seguridad**: HMAC-MD5 para autenticación

## 📡 API Endpoints Principales

```txt
POST /api/sinpe-transfer              # Recibir transferencias SINPE
POST /api/sinpe-movil-transfer        # Recibir SINPE móvil
POST /api/send-external-transfer      # Enviar a bancos externos
POST /api/send-external-movil-transfer # Enviar móvil externo
GET  /api/validate/{phone}            # Validar teléfonos
GET  /api/bank-contacts               # Contactos de bancos
GET  /health                          # Health check
```

## 🗄️ Modelo de Datos

### Entidades Principales

- **User**: Usuarios del sistema
- **Account**: Cuentas bancarias  
- **PhoneLink**: Enlaces teléfono-cuenta para SINPE
- **Transaction**: Registro de transacciones
- **SinpeSubscription**: Suscripciones BCCR
- **Currency**: Monedas soportadas

## 🔐 Protocolo de Comunicación

### Estructura SINPE Tradicional

```json
{
    "version": "1.0",
    "timestamp": "ISO_TIMESTAMP",
    "transaction_id": "UUID",
    "sender": {
        "account_number": "CR21...",
        "bank_code": "152",
        "name": "Usuario"
    },
    "receiver": {
        "account_number": "CR21...",
        "bank_code": "876", 
        "name": "Destinatario"
    },
    "amount": {
        "value": 50000.00,
        "currency": "CRC"
    },
    "description": "Descripción",
    "hmac_md5": "hash_signature"
}
```

### Estructura SINPE Móvil  

```json
{
    "version": "1.0",
    "timestamp": "ISO_TIMESTAMP",
    "transaction_id": "UUID",
    "sender": {
        "phone_number": "88887777"
    },
    "receiver": {
        "phone_number": "99998888"
    },
    "amount": {
        "value": 25000.00,
        "currency": "CRC"
    },
    "description": "Transferencia móvil",
    "hmac_md5": "hash_signature"
}
```

## 🔒 Seguridad HMAC

```python
# Algoritmo HMAC-MD5 (FORMATO ACTUAL - NECESITA CORRECCIÓN)
def generar_hmac(account_number, timestamp, transaction_id, amount):
    secret = "supersecreta123"
    # PROBLEMA: Formato actual sin comas como separadores
    message = account_number + timestamp + transaction_id + amount_str
    return hashlib.md5(message.encode()).hexdigest()

# FORMATO CORRECTO REQUERIDO para compatibilidad:
def generar_hmac_correcto(account_number, timestamp, transaction_id, amount):
    secret = "supersecreta123"
    amount_str = "{:.2f}".format(float(amount))
    message = f"{secret},{account_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(message.encode()).hexdigest()
```

## 🌐 Configuración de Bancos Externos

```json
// contactos-bancos.json
[
    {
        "contacto": "josue",
        "codigo": "876",
        "IP": "192.168.3.10:5000",
        "IBAN": "CR21-0876-0001-00-0000-0121-87"
    },
    {
        "contacto": "marconi", 
        "codigo": "119",
        "IP": "192.168.2.10:3001",
        "IBAN": "CR21-0119-0001-71-3176-4383-40"
    }
]
```

## 🔄 Flujo de Transferencias

### Transferencia Saliente

1. Validar datos de entrada
2. Generar transaction_id y timestamp
3. Crear payload con HMAC
4. Buscar IP del banco destino en contactos-bancos.json
5. Enviar POST al banco externo
6. Procesar respuesta y registrar

### Transferencia Entrante

1. Recibir payload en endpoint correspondiente
2. Validar estructura y campos requeridos
3. Verificar HMAC signature
4. Buscar cuenta destino local
5. Acreditar fondos y crear transacción
6. Retornar confirmación

## 🧪 Datos de Prueba

### Usuarios (password: password123)

- juan_perez (88887777)
- maria_rodriguez (88886666)
- carlos_gonzalez (88885555)
- ana_lopez (88884444)

### Configuración

- **Código de Banco**: 152
- **Puerto API**: 5000
- **HMAC Secret**: supersecreta123
- **Base de Datos**: SQLite local

## 🔧 Características Especiales

- **Terminal UI Rica**: Interfaz colorida con Rich library
- **API REST Completa**: Endpoints para todas las operaciones
- **Conectividad Inter-banco**: Cliente HTTP para comunicación
- **Validación IBAN**: Extracción automática de códigos de banco
- **Logging Completo**: Registro de todas las operaciones
- **Health Monitoring**: Endpoints de monitoreo

## ⚠️ Problemas Identificados que Requieren Corrección

1. **HMAC Incompatible**: Formato actual no coincide con otros bancos
2. **Endpoints Duplicados**: Múltiples archivos de rutas (sinpe_routes.py, sinpe_routes_backup.py)
3. **Configuración Fragmentada**: Dos archivos de configuración diferentes
4. **Validación Incompleta**: Falta validación robusta de payloads
5. **Manejo de Errores**: Respuestas no estandarizadas

## 🎯 Estado de Conectividad

- ❌ **Envío a Banco TypeScript (119)**: HMAC incompatible
- ❌ **Envío a Banco Python (876)**: HMAC incompatible  
- ✅ **Recepción Básica**: Estructura endpoint correcta
- ⚠️ **Validación**: Parcialmente funcional
