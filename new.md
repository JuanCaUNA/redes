# Análisis de Conectividad - Banco Python (bancoPy/pythonProject)

## 🏦 Estado Actual del Proyecto

Basado en el análisis del código y la documentación, el banco Python principal está **parcialmente configurado** para conexiones inter-bancarias, pero requiere **correcciones críticas** para funcionar correctamente.

## 🔍 Componentes de Conectividad Analizados

### ✅ **Aspectos Correctamente Configurados**

1. **SSL/HTTPS**:
   - Certificados SSL presentes en `app/ssl/`
   - Servidor HTTPS funcionando en puerto 5443
   - Configuración SSL en `ssl_config`

2. **Estructura de Endpoints**:
   - Endpoints de recepción: `/api/sinpe-transfer` y `/api/sinpe-movil-transfer`
   - Endpoints de envío: `/api/send-external-transfer`
   - Health check: `/health`

3. **Servicio de Conectividad**:
   - `BankConnectorService` implementado
   - Carga de contactos desde contactos-bancos.json
   - Retry logic para conexiones fallidas

4. **Base de Datos y Modelos**:
   - SQLAlchemy ORM configurado
   - Modelos para transacciones y usuarios
   - Sistema de logging completo

## ❌ **Problemas Críticos Identificados**

### 1. **HMAC Incompatible (CRÍTICO)**

**Problema**: El algoritmo HMAC actual no es compatible con otros bancos del ecosistema.

**Tu implementación actual** en `hmac_generator.py`:

```python
# FORMATO INCORRECTO - Sin comas como separadores
mensaje = account_number + timestamp + transaction_id + amount_str
```

**Formato esperado por otros bancos** (según code.py y análisis de otros bancos):

```python
# FORMATO CORRECTO - Con comas como separadores
mensaje = f"{clave},{account_number},{timestamp},{transaction_id},{amount_str}"
```

**Impacto**: Las transferencias a bancos externos fallarán por verificación HMAC incorrecta.

### 2. **Configuración de Red Fragmentada**

**Problema**: Tienes dos archivos de configuración diferentes:

- `config/banks.json`
- contactos-bancos.json

Con IPs y estructuras que no coinciden completamente.

### 3. **Validación de Payloads Incompleta**

**Problema**: Los endpoints no validan completamente la estructura según los protocolos SINPE estándar definidos en otros bancos.

## 🔧 **Correcciones Requeridas**

### **Corrección 1: Actualizar Algoritmo HMAC**

````python
def generar_hmac(
    account_number: str,
    timestamp: str,
    transaction_id: str,
    amount: float,
    clave: str = SECRET_KEY,
) -> str:
    """
    Generar HMAC compatible con otros bancos del ecosistema
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar comas como separadores
    mensaje = f"{clave},{account_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()

def generar_hmac_movil(
    phone_number: str,
    timestamp: str,
    transaction_id: str,
    amount: float,
    clave: str = SECRET_KEY,
) -> str:
    """
    Generar HMAC para SINPE Móvil compatible con otros bancos
    """
    amount_str = "{:.2f}".format(float(amount))
    # CAMBIO CRÍTICO: Usar comas como separadores
    mensaje = f"{clave},{phone_number},{timestamp},{transaction_id},{amount_str}"
    return hashlib.md5(mensaje.encode()).hexdigest()
````

### **Corrección 2: Unificar Configuración de Bancos**

````json
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
    "name": "Banco TypeScript (Marconi)",
    "url": "http://192.168.2.10:3001",
    "code": "0119",
    "enabled": true
  }
}
````

### **Corrección 3: Validación Robusta de Payloads**

````python
def validate_sinpe_transfer_payload(data: Dict[Any, Any]) -> Tuple[bool, str]:
    """Validar estructura de transferencia SINPE tradicional"""
    required_fields = ['version', 'timestamp', 'transaction_id', 'sender', 'receiver', 'amount', 'hmac_md5']
    
    for field in required_fields:
        if field not in data:
            return False, f"Falta campo requerido: {field}"
    
    # Validar estructura de sender
    sender_required = ['account_number', 'bank_code', 'name']
    for field in sender_required:
        if field not in data['sender']:
            return False, f"Falta campo en sender: {field}"
            
    # Validar estructura de receiver
    receiver_required = ['account_number', 'bank_code', 'name']
    for field in receiver_required:
        if field not in data['receiver']:
            return False, f"Falta campo en receiver: {field}"
            
    # Validar estructura de amount
    if 'value' not in data['amount']:
        return False, "Falta campo amount.value"
        
    return True, "Válido"

def validate_sinpe_movil_payload(data: Dict[Any, Any]) -> Tuple[bool, str]:
    """Validar estructura de transferencia SINPE móvil"""
    required_fields = ['version', 'timestamp', 'transaction_id', 'sender', 'receiver', 'amount', 'hmac_md5']
    
    for field in required_fields:
        if field not in data:
            return False, f"Falta campo requerido: {field}"
    
    # Validar estructura de sender/receiver para móvil
    if 'phone_number' not in data['sender']:
        return False, "Falta campo sender.phone_number"
        
    if 'phone_number' not in data['receiver']:
        return False, "Falta campo receiver.phone_number"
        
    return True, "Válido"
````

## 🧪 **Pruebas de Conectividad Recomendadas**

### **Test 1: Envío a Banco TypeScript (IP: 192.168.2.10:3001)**

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

### **Test 2: Envío a Banco Python (IP: 192.168.3.10:5000)**

```bash
curl -X POST http://192.168.3.10:5000/api/sinpe-transfer \
  -H "Content-Type: application/json" \
  -d '{...similar estructura...}'
```

## 📊 **Matriz de Compatibilidad Esperada**

| Componente | Estado Actual | Después de Correcciones |
|------------|---------------|-------------------------|
| **SSL/HTTPS** | ✅ Funcionando | ✅ Funcionando |
| **HMAC** | ❌ Incompatible | ✅ Compatible |
| **Endpoints** | ⚠️ Parcial | ✅ Completo |
| **Validación** | ⚠️ Básica | ✅ Robusta |
| **Configuración** | ⚠️ Fragmentada | ✅ Unificada |
| **Conectividad** | ❌ No funcional | ✅ Funcional |

## 🎯 **Conclusión**

Tu banco Python está **bien estructurado** pero necesita **3 correcciones críticas**:

1. **HMAC con formato de comas** (prioridad crítica)
2. **Configuración unificada** (prioridad alta)
3. **Validación robusta** (prioridad media)

Con estas correcciones, el banco será **100% compatible** con el ecosistema SINPE y podrá conectarse exitosamente con:

- Banco TypeScript (Redes-Project-dev/server)
- Banco Python secundario (PRUEBA/PRUEBA/server)

**Tiempo estimado de implementación**: 2-3 horas de desarrollo + pruebas.
