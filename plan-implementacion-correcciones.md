# Plan de Implementación de Correcciones - Banco Python

## 🎯 Objetivo

Hacer que tu banco Python sea 100% compatible con los bancos TypeScript y Python externos en el ecosistema SINPE.

## 📋 Correcciones por Implementar

### 1. **Corrección Crítica: HMAC**

**Archivo a modificar**: `app/utils/hmac_generator.py`

**Problema actual**:

```python
# Formato actual (INCORRECTO)
mensaje = account_number + timestamp + transaction_id + amount_str
```

**Solución requerida**:

```python
# Formato correcto con comas
mensaje = f"{secret},{account_number},{timestamp},{transaction_id},{amount_str}"
```

### 2. **Consolidación de Endpoints**

**Archivos a limpiar**:

- Mantener: `app/routes/sinpe_routes.py` (principal)
- Eliminar: `app/routes/sinpe_routes_backup.py`
- Eliminar: `app/routes/sinpe_routes_new.py`

**Endpoints requeridos**:

```txt
POST /api/sinpe-transfer         # SINPE tradicional
POST /api/sinpe-movil-transfer   # SINPE móvil  
POST /api/send-external-transfer      # Enviar externo
POST /api/send-external-movil-transfer # Enviar móvil externo
GET  /api/validate/{phone}       # Validar teléfono
GET  /api/bank-contacts          # Directorio bancos
GET  /health                     # Health check
```

### 3. **Unificación de Configuración**

**Problema**: Tienes dos archivos:

- `config/banks.json`
- `contactos-bancos.json`

**Solución**: Usar solo `config/banks.json` con formato estándar.

### 4. **Validación de Payloads**

**Crear**: `app/utils/validators.py`

```python
def validate_sinpe_transfer(data):
    """Validar transferencia SINPE tradicional"""
    required = ['version', 'timestamp', 'transaction_id', 'sender', 'receiver', 'amount', 'hmac_md5']
    # Implementar validación completa

def validate_sinpe_movil_transfer(data):
    """Validar transferencia SINPE móvil"""
    required = ['version', 'timestamp', 'transaction_id', 'sender', 'receiver', 'amount', 'hmac_md5']
    # Implementar validación completa
```

## 🔧 Configuración de Red

### IPs y Puertos Estándar

```json
{
  "152": {
    "name": "Tu Banco Local",
    "url": "http://localhost:5000",
    "code": "0152"
  },
  "876": {
    "name": "Banco Python Secundario", 
    "url": "http://192.168.3.10:5000",
    "code": "0876"
  },
  "119": {
    "name": "Banco TypeScript",
    "url": "http://192.168.2.10:3001",
    "code": "0119"
  }
}
```

## 🧪 Pruebas de Conectividad

### Test 1: Envío a Banco TypeScript

```bash
curl -X POST http://192.168.2.10:3001/api/sinpe/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00Z",
    "transaction_id": "test-uuid",
    "sender": {
      "account_number": "CR21-0152-0001-XX-XXXX-XXXX-XX",
      "bank_code": "152",
      "name": "Test User"
    },
    "receiver": {
      "account_number": "CR21-0119-0001-XX-XXXX-XXXX-XX",
      "bank_code": "119", 
      "name": "Receiver"
    },
    "amount": {
      "value": 1000.00,
      "currency": "CRC"
    },
    "description": "Test transfer",
    "hmac_md5": "HMAC_CALCULADO_CORRECTAMENTE"
  }'
```

### Test 2: Envío a Banco Python Secundario

```bash
curl -X POST http://192.168.3.10:5000/api/sinpe-transfer \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00Z", 
    "transaction_id": "test-uuid",
    "sender": {
      "account_number": "CR21-0152-0001-XX-XXXX-XXXX-XX",
      "bank_code": "152",
      "name": "Test User"
    },
    "receiver": {
      "account_number": "CR21-0876-0001-XX-XXXX-XXXX-XX",
      "bank_code": "876",
      "name": "Receiver"
    },
    "amount": {
      "value": 1000.00,
      "currency": "CRC"
    },
    "description": "Test transfer",
    "hmac_md5": "HMAC_CALCULADO_CORRECTAMENTE"
  }'
```

## 📊 Matriz de Compatibilidad Esperada

| Operación | Banco TypeScript (119) | Banco Python (876) | Estado |
|-----------|------------------------|-------------------|---------|
| Envío SINPE | ✅ Después corrección | ✅ Después corrección | 🔄 Pendiente |
| Recepción SINPE | ✅ Compatible | ✅ Compatible | ✅ Listo |
| Envío SINPE Móvil | ✅ Después corrección | ✅ Después corrección | 🔄 Pendiente |
| Recepción SINPE Móvil | ✅ Compatible | ✅ Compatible | ✅ Listo |
| Health Check | ✅ Compatible | ✅ Compatible | ✅ Listo |
| Validación Phone | ✅ Compatible | ✅ Compatible | ✅ Listo |

## 🚀 Orden de Implementación

1. **HMAC Fix** - Prioridad crítica
2. **Cleanup endpoints** - Prioridad alta  
3. **Config unificada** - Prioridad media
4. **Validadores** - Prioridad media
5. **Tests** - Prioridad baja

## ✅ Criterio de Éxito

Tu banco estará completamente funcional cuando:

- [x] Estructura de proyecto bien organizada
- [ ] HMAC compatible con todos los bancos
- [ ] Endpoints limpios y estándar
- [ ] Configuración unificada
- [ ] Validación robusta implementada
- [ ] Conectividad probada con bancos externos
- [ ] Manejo de errores estandarizado

## 📝 Notas Importantes

- **No modificar** bancos externos - solo tu implementación
- **Mantener** compatibilidad con protocolos SINPE existentes
- **Probar** cada corrección individualmente
- **Documentar** cambios realizados
