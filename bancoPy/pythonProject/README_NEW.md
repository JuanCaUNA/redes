# SINPE Banking System - Python Implementation

Sistema bancario integral basado en Python que replica la funcionalidad del sistema de pagos SINPE de Costa Rica. El sistema presenta una interfaz de terminal rica e interactiva con backend API Flask.

## ✨ Características

- **💻 Interfaz Terminal Rica**: Terminal interactiva con menús coloridos y formularios
- **🌐 API REST Completa**: Backend Flask con todos los endpoints SINPE
- **🔐 SSL/HTTPS**: Servidor seguro con certificados SSL (<https://127.0.0.1:5443>)
- **🗄️ Base de Datos**: SQLite con SQLAlchemy ORM
- **💸 Transferencias SINPE**: Transferencias por teléfono y cuenta con verificación HMAC
- **👥 Gestión de Usuarios**: Autenticación completa y gestión de cuentas
- **📱 Enlaces Telefónicos**: Vincular números de teléfono a cuentas bancarias
- **📊 Historial de Transacciones**: Seguimiento completo de transacciones
- **⚙️ Panel de Administración**: Gestión de base de datos y estadísticas
- **🔍 Monitoreo de Sistema**: Monitoreo de salud y logging completo

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.12.4 (configurado en .venv)
- Entorno virtual activado

### Ejecutar el Sistema

```powershell
# En Windows (PowerShell)
cd pythonProject

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar la aplicación principal
python main.py
```

Alternativamente, si tienes problemas con la política de ejecución:

```powershell
# Ejecutar directamente con el Python del entorno virtual
.\.venv\Scripts\python.exe main.py
```

### Al Iniciar el Sistema

1. **Base de datos**: Se inicializa automáticamente con datos de ejemplo
2. **Servidor API**: Se inicia en <https://127.0.0.1:5443> (SSL) o <http://127.0.0.1:5000> (HTTP)
3. **Interfaz Terminal**: Menú interactivo con opciones numeradas

## 🎮 Uso del Sistema

### Menú Principal

```txt
┌──────┬────────────────────────────┐
│ 1    │ 🔐 Login / User Management │
│ 2    │ 💰 Account Management      │
│ 3    │ 💸 SINPE Transfers         │
│ 4    │ 📱 Phone Link Management   │
│ 5    │ 📊 Transaction History     │
│ 6    │ ⚙️ Admin Panel             │
│ 0    │ 🚪 Exit                    │
└──────┴────────────────────────────┘
```

### Datos de Ejemplo

El sistema crea automáticamente usuarios de prueba:

**Usuarios** (contraseña: `password123`):

- `juan_perez` - Teléfono: 88887777
- `maria_rodriguez` - Teléfono: 88886666
- `carlos_gonzalez` - Teléfono: 88885555
- `ana_lopez` - Teléfono: 88884444

## 🏗️ Estructura del Proyecto

```txt
pythonProject/
├── main.py                 # 🚀 Punto de entrada principal
├── requirements.txt        # 📦 Dependencias
├── README.md              # 📖 Documentación
├── MisNotas.md            # 📝 Notas del usuario
├── .env                   # ⚙️ Variables de entorno
├── app/                   # 🏢 Aplicación principal
│   ├── __init__.py        # Flask app factory
│   ├── models/            # 🗃️ Modelos de base de datos
│   ├── routes/            # 🛣️ Rutas de API
│   ├── services/          # 🔧 Lógica de negocio
│   ├── ssl/               # 🔐 Certificados SSL
│   └── utils/             # 🛠️ Utilidades
├── config/                # ⚙️ Configuración
├── database/              # 🗄️ Base de datos SQLite
├── logs/                  # 📋 Archivos de log
└── tests/                 # 🧪 Pruebas unitarias
```

## 🔌 API Endpoints

### Endpoints Principales

- **Health Check**: `GET /health`
- **SINPE Transfers**: `POST /api/sinpe-movil`
- **User Management**: `GET|POST|PUT|DELETE /api/users`
- **Account Management**: `GET|POST /api/accounts`
- **Phone Links**: `GET|POST /api/phone-links`
- **Transactions**: `GET|POST /api/transactions`
- **Authentication**: `POST /api/auth/login`

### Ejemplo de Transferencia SINPE

```bash
curl -X POST https://127.0.0.1:5443/api/sinpe-movil \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "88887777",
    "amount": 5000,
    "hmac": "generated_hmac_signature",
    "timestamp": "2025-06-10T10:30:00Z"
  }'
```

## 🔒 Seguridad

### HMAC Verification

Todas las transferencias requieren firma HMAC-MD5:

```python
# Para transferencias por teléfono
message = f"{secret},{phone},{timestamp},{transaction_id},{amount}"

# Para transferencias por cuenta
message = f"{secret},{account_number},{timestamp},{transaction_id},{amount}"
```

**Secret Key**: `supersecreta123`

### SSL/HTTPS

- Certificados SSL incluidos en `app/ssl/`
- Servidor HTTPS en puerto 5443
- Fallback HTTP en puerto 5000 si SSL no está disponible

## 🧪 Pruebas

```powershell
# Ejecutar todas las pruebas
.\.venv\Scripts\python.exe -m pytest tests/ -v

# Resultado esperado: 4/4 tests pasando
```

### Pruebas Incluidas

- **test_hmac.py**: Verificación de firmas HMAC
  - ✅ Generación de HMAC para transferencias por teléfono
  - ✅ Generación de HMAC para transferencias por cuenta
  - ✅ Verificación de firmas válidas
  - ✅ Validación de estructura de mensajes

## 🛠️ Comandos Útiles

### Gestión del Entorno

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python -c "import rich; print('✅ Rich installed')"
```

### Linting y Formateo

```powershell
# Analizar código con Ruff
.\.venv\Scripts\ruff.exe check .

# Formatear código con Black
.\.venv\Scripts\black.exe .

# Corregir problemas automáticamente
.\.venv\Scripts\ruff.exe check . --fix
```

## 📊 Monitoreo y Logs

### Archivos de Log

- `logs/banking_app.log` - Log principal de la aplicación
- `logs/transactions.log` - Log de transacciones
- `logs/security.log` - Log de seguridad
- `logs/errors.log` - Log de errores
- `logs/api_access.log` - Log de acceso a API

### Health Check

```bash
curl https://127.0.0.1:5443/health
```

Respuesta esperada:

```json
{
  "status": "healthy",
  "message": "SINPE Banking System API"
}
```

## ⚡ Funcionalidades Principales

### 1. Gestión de Usuarios

- Crear, editar, eliminar usuarios
- Autenticación segura
- Gestión de sesiones

### 2. Gestión de Cuentas

- Crear cuentas bancarias
- Consultar saldos
- Historial de movimientos

### 3. Transferencias SINPE

- Transferencias por número de teléfono
- Transferencias por número de cuenta
- Verificación HMAC obligatoria
- Validación de saldos

### 4. Enlaces Telefónicos

- Vincular teléfonos a cuentas
- Gestionar múltiples enlaces
- Validación de números

### 5. Panel de Administración

- Estadísticas del sistema
- Gestión de base de datos
- Monitoreo de salud

## 🚨 Limitaciones Actuales

⚠️ **IMPORTANTE**: Actualmente no se puede conectar con otros bancos, por lo que no se pueden probar transferencias interbancarias. Sin embargo, todas las funciones internas del banco funcionan correctamente mientras el servidor esté activo.

### Funcionalidades Operativas ✅

- ✅ Transferencias dentro del mismo banco
- ✅ Gestión de usuarios y cuentas
- ✅ Validación HMAC
- ✅ API REST completa
- ✅ Interfaz terminal interactiva
- ✅ SSL/HTTPS
- ✅ Base de datos SQLite
- ✅ Logging completo

### Funcionalidades Pendientes ⏳

- ⏳ Conexión con otros bancos
- ⏳ Transferencias interbancarias
- ⏳ Integración con BCCR real

## 🆘 Solución de Problemas

### Error: "No module named 'rich'"

```powershell
# Usar el Python del entorno virtual
.\.venv\Scripts\python.exe main.py
```

### Error: "SSL certificates not available"

- El sistema funcionará en HTTP (puerto 5000)
- No afecta la funcionalidad principal

### Error en activación del entorno virtual

```powershell
# Ejecutar directamente
.\.venv\Scripts\python.exe main.py
```

## 📝 Notas de Desarrollo

- **Python**: 3.12.4 (del .venv)
- **Framework**: Flask con SQLAlchemy
- **Base de datos**: SQLite (development)
- **Interfaz**: Rich terminal UI
- **Seguridad**: HMAC-MD5, SSL/HTTPS
- **Testing**: pytest

## 📄 Licencia

Este proyecto es para fines educativos y demuestra la implementación de un sistema bancario SINPE en Python.
