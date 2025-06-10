# 🖥️ Interfaz Gráfica SINPE Banking System

## 🎉 ¡NUEVA FUNCIONALIDAD

Se ha agregado una **interfaz gráfica simple** para facilitar la interacción con el sistema bancario.

---

## 🚀 CÓMO USAR LA INTERFAZ GRÁFICA

### **Método 1: Script Batch (Más Fácil)**

```batch
run-GUI.bat
```

### **Método 2: PowerShell**

```powershell
.\.venv\Scripts\python.exe gui_simple.py
```

---

## ✨ CARACTERÍSTICAS DE LA GUI

### 🎯 **Funcionalidades Disponibles**

- **🔐 Gestión de Usuarios**: Login, crear usuarios, ver lista
- **💰 Gestión de Cuentas**: Crear cuentas, ver saldos, detalles
- **💸 Transferencias SINPE**: Por cuenta e IBAN y por teléfono
- **📱 Enlaces Telefónicos**: Vincular números con cuentas
- **📊 Historial**: Ver transacciones con filtros
- **⚙️ Control del Servidor**: Iniciar/detener desde la GUI

### 🎨 **Interfaz Intuitiva**

- **Pestañas organizadas** por funcionalidad
- **Formularios simples** para todas las operaciones
- **Tablas visuales** para mostrar datos
- **Mensajes claros** de éxito y error
- **Control de servidor integrado**

---

## 📋 GUÍA DE USO

### **1. Iniciar la Aplicación**

- Ejecuta `run-GUI.bat`
- La ventana de la aplicación se abrirá

### **2. Iniciar el Servidor (si no está corriendo)**

- Haz clic en "Iniciar Servidor"
- Espera unos segundos hasta ver "🟢 Servidor conectado"

### **3. Usar las Funcionalidades**

#### **👥 Usuarios**

- **Login**: Ingresa usuario y PIN, luego "Iniciar Sesión"
- **Crear Usuario**: Botón "Crear Usuario" → llenar formulario
- **Ver Lista**: Se actualiza automáticamente

#### **💰 Cuentas**

- **Ver Cuentas**: Lista automática con IBAN, saldo, tipo
- **Crear Cuenta**: Botón "Crear Cuenta" (requiere login)
- **Ver Detalles**: Seleccionar cuenta → "Ver Detalles"

#### **💸 Transferencias**

- **Por Cuenta**: IBAN origen → IBAN destino → monto → "Transferir"
- **Por Teléfono**: IBAN origen → teléfono → monto → "Transferir"
- **Validación automática** de campos

#### **📱 Enlaces Telefónicos**

- **Crear Enlace**: IBAN + teléfono → "Crear Enlace"
- **Ver Enlaces**: Lista automática de enlaces activos

#### **📊 Historial**

- **Filtrar por IBAN**: Opcional
- **Buscar**: Botón "Buscar Transacciones"
- **Ver todas**: Botón "Actualizar Lista"

---

## ⚙️ CARACTERÍSTICAS TÉCNICAS

### **🔄 Auto-Actualización**

- Los datos se actualizan automáticamente
- Botones "Actualizar" disponibles en cada pestaña

### **🛡️ Validaciones**

- Campos obligatorios verificados
- Montos validados (números positivos)
- Mensajes de error claros

### **🔗 Integración Completa**

- Usa la **misma API** que la interfaz de terminal
- **Servidor SSL** en <https://127.0.0.1:5443>
- **Misma base de datos** SQLite

### **💾 Control del Servidor**

- **Iniciar/Detener** servidor desde la GUI
- **Detección automática** del estado del servidor
- **Proceso en segundo plano** no bloquea la GUI

---

## 🆚 COMPARACIÓN: GUI vs Terminal

| Característica | GUI (Nueva) | Terminal (Anterior) |
|---------------|-------------|-------------------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ Muy fácil | ⭐⭐⭐ Moderado |
| **Visualización** | ⭐⭐⭐⭐⭐ Tablas y formularios | ⭐⭐⭐ Texto colorido |
| **Navegación** | ⭐⭐⭐⭐⭐ Pestañas y botones | ⭐⭐ Menús numerados |
| **Control servidor** | ⭐⭐⭐⭐⭐ Integrado | ⭐⭐⭐⭐ Manual |
| **Multitarea** | ⭐⭐⭐⭐⭐ Múltiples ventanas | ⭐⭐ Una operación |

---

## 🎯 RECOMENDACIÓN

### **Usar GUI para**

- ✅ **Usuarios nuevos** o no técnicos
- ✅ **Operaciones frecuentes** (transferencias, consultas)
- ✅ **Visualización de datos** (cuentas, historial)
- ✅ **Trabajo productivo** diario

### **Usar Terminal para**

- ✅ **Usuarios técnicos** que prefieren CLI
- ✅ **Automatización** o scripts
- ✅ **Servidores** sin GUI

---

## 🐛 RESOLUCIÓN DE PROBLEMAS

### **"No se puede iniciar el servidor"**

- Verifica que no haya otro proceso usando el puerto
- Revisa que `.venv` esté configurado correctamente

### **"Error de conexión a la API"**

- Asegúrate de que el servidor esté iniciado (🟢)
- Espera unos segundos después de iniciar el servidor

### **"Error al crear usuario/cuenta"**

- Verifica que todos los campos estén llenos
- Para cuentas: asegúrate de haber iniciado sesión

---

## ✅ VENTAJAS DE LA NUEVA GUI

1. **🎯 Más fácil de usar** - No necesitas memorizar comandos
2. **👀 Mejor visualización** - Tablas claras con datos organizados
3. **⚡ Más eficiente** - Múltiples operaciones sin reiniciar
4. **🔄 Tiempo real** - Datos actualizados automáticamente
5. **🛡️ Menos errores** - Validación visual de campos
6. **🎨 Intuitiva** - Interfaz familiar estilo Windows

**¡La GUI hace el sistema mucho más accesible y productivo!** 🚀
