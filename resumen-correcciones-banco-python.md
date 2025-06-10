# Resumen de Correcciones - Banco Python (bancoPy/pythonProject)

## 🏦 Estado Actual del Banco

Tu banco principal Python está bien implementado pero necesita algunas correcciones críticas para garantizar la conectividad completa con los otros bancos del ecosistema SINPE.

## 🚨 Problemas Críticos Identificados

### 1. **HMAC Inconsistente entre Bancos**

**Problema**: Los otros bancos utilizan un formato diferente para generar HMAC:

**Tu banco actual:**

```python
# Tu implementación actual
mensaje = account_number + timestamp + transaction_id + amount_str
```

**Bancos externos esperan:**

```python
# Formato esperado por otros bancos
mensaje = f"{secret},{account_number},{timestamp},{transaction_id},{amount}"
```

**Solución**: Actualizar `app/utils/hmac_generator.py` para usar comas como separadores.

### 2. **Endpoints Duplicados y Confusos**

**Problema**: Tienes múltiples archivos de rutas con endpoints similares:

- `sinpe_routes.py` (principal)
- `sinpe_routes_backup.py` (backup)
- `sinpe_routes_new.py` (nuevo)

**Solución**: Consolidar en un solo archivo con endpoints estándar.

### 3. **Configuración de Red Inconsistente**

**Problema**: Dos archivos de configuración diferentes:

- `config/banks.json`
- `contactos-bancos.json`

Con IPs y puertos que no coinciden entre sí.

**Solución**: Unificar configuración y usar IPs consistentes.

### 4. **Validación de Payloads Incompleta**

**Problema**: Los endpoints no validan completamente la estructura según los protocolos SINPE estándar.

**Solución**: Implementar validación robusta de esquemas JSON.

## 🔧 Correcciones Requeridas

### A. **Corrección del Algoritmo HMAC**

```python
# ACTUALIZAR: app/utils/hmac_generator.py
def generar_hmac(account_number: str, timestamp: str, transaction_id: str, amount: float, clave: str = SECRET_KEY) -> str:
    """
    Generar HMAC compatible con otros bancos del ecosistema
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar comas como separadores
    mensaje = f"{clave},{account_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()

def generar_hmac_movil(phone_number: str, timestamp: str, transaction_id: str, amount: float, clave: str = SECRET_KEY) -> str:
    """
    Generar HMAC para SINPE Móvil compatible con otros bancos
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar comas como separadores
    mensaje = f"{clave},{phone_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()
```

### B. **Endpoints Estándar Requeridos**

Tu banco DEBE tener exactamente estos endpoints para compatibilidad:

```python
# REQUERIDOS para recibir transferencias
POST /api/sinpe-transfer              # Transferencias SINPE tradicionales
POST /api/sinpe-movil-transfer        # Transferencias SINPE móvil

# REQUERIDOS para enviar transferencias  
POST /api/send-external-transfer      # Enviar a bancos externos
POST /api/send-external-movil-transfer # Enviar móvil a bancos externos

# REQUERIDOS para operación
GET  /api/validate/{phone}            # Validar números de teléfono
GET  /api/bank-contacts               # Directorio de bancos
GET  /health                          # Health check
```

### C. **Configuración de Red Unificada**

```json
// ACTUALIZAR: config/banks.json (archivo único)
{
  "152": {
    "name": "Tu Banco Local",
    "url": "http://192.168.1.10:5000",
    "code": "0152",
    "enabled": true
  },
  "876": {
    "name": "Banco Josue", 
    "url": "http://192.168.3.10:5000",
    "code": "0876",
    "enabled": true
  },
  "119": {
    "name": "Banco TypeScript",
    "url": "http://192.168.2.10:3001", 
    "code": "0119",
    "enabled": true
  }
}
```

### D. **Validación de Payloads Robusta**

```python
# AGREGAR: app/utils/validators.py
def validate_sinpe_payload(data):
    """Validar estructura de transferencia SINPE"""
    required_fields = ['version', 'timestamp', 'transaction_id', 'sender', 'receiver', 'amount', 'hmac_md5']
    
    for field in required_fields:
        if field not in data:
            return False, f"Falta campo requerido: {field}"
    
    # Validar estructura de sender/receiver
    if 'account_number' not in data['sender'] and 'phone_number' not in data['sender']:
        return False, "Sender debe tener account_number o phone_number"
        
    return True, "Válido"
```

### E. **Manejo de Errores Estandarizado**

```python
# ESTANDARIZAR respuestas de error
def standard_error_response(error_message, status_code=400):
    return jsonify({
        'success': False,
        'error': error_message,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code

def standard_success_response(message, data=None):
    response = {
        'success': True,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    if data:
        response['data'] = data
    return jsonify(response)
```

## 🔄 Protocolo de Integración

### Estructura SINPE Tradicional (Estándar)

```json
{
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00Z",
    "transaction_id": "uuid-v4-here",
    "sender": {
        "account_number": "CR21-0152-0001-XX-XXXX-XXXX-XX",
        "bank_code": "152",
        "name": "Usuario Sender"
    },
    "receiver": {
        "account_number": "CR21-0876-0001-XX-XXXX-XXXX-XX", 
        "bank_code": "876",
        "name": "Usuario Receiver"
    },
    "amount": {
        "value": 50000.00,
        "currency": "CRC"
    },
    "description": "Transferencia de prueba",
    "hmac_md5": "hash_con_formato_correcto"
}
```

### Estructura SINPE Móvil (Estándar)

```json
{
    "version": "1.0", 
    "timestamp": "2024-01-15T10:30:00Z",
    "transaction_id": "uuid-v4-here",
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
    "description": "SINPE Móvil",
    "hmac_md5": "hash_con_formato_correcto"
}
```

## 🧪 Pruebas de Conectividad

### Casos de Prueba Requeridos

1. **Envío a Banco TypeScript (119)**
   - IP: `192.168.2.10:3001`
   - Endpoint: `POST /api/sinpe/transfer`

2. **Envío a Banco Python Secundario (876)**
   - IP: `192.168.3.10:5000`
   - Endpoint: `POST /api/sinpe-transfer`

3. **Recepción desde Bancos Externos**
   - Validar HMAC con formato correcto
   - Procesar según estructura estándar

## 📝 Lista de Tareas de Corrección

### Prioridad Alta (Crítico)

- [ ] **Corregir algoritmo HMAC** - Usar formato con comas
- [ ] **Consolidar endpoints** - Un solo archivo de rutas
- [ ] **Unificar configuración** - Un solo archivo de bancos
- [ ] **Implementar validación robusta** - Esquemas JSON

### Prioridad Media

- [ ] **Mejorar manejo de errores** - Respuestas estándar
- [ ] **Actualizar documentación** - API endpoints
- [ ] **Optimizar logging** - Mejor trazabilidad

### Prioridad Baja

- [ ] **Interfaz terminal** - Mejoras de UX
- [ ] **Tests automatizados** - Cobertura completa
- [ ] **Métricas** - Monitoreo de performance

## 🎯 Objetivo Final

Después de estas correcciones, tu banco podrá:

✅ **Enviar transferencias** a bancos TypeScript y Python externos  
✅ **Recibir transferencias** desde cualquier banco del ecosistema  
✅ **Validar correctamente** todas las firmas HMAC  
✅ **Comunicarse de forma estándar** con endpoints compatibles  
✅ **Manejar errores** de manera consistente y trazable  

## 🚀 Pasos de Implementación

1. **Actualizar HMAC** → Compatibilidad inmediata
2. **Consolidar endpoints** → Estructura limpia
3. **Unificar configuración** → Red consistente
4. **Probar conectividad** → Validar funcionamiento
5. **Documentar cambios** → Facilitar mantenimiento

Con estas correcciones, tu banco será completamente compatible con el ecosistema SINPE y podrá conectarse exitosamente con todos los demás bancos.
