# 🏦 Interfaz Gráfica Básica - SINPE Banking System

## Descripción

Esta es una interfaz gráfica básica desarrollada desde cero usando Tkinter para el sistema bancario SINPE. Proporciona una manera visual y fácil de interactuar con todas las funcionalidades del sistema.

## 🚀 Cómo usar

### Método 1: Ejecutar directamente

```bash
# Activar entorno virtual
.\.venv\Scripts\activate

# Ejecutar la GUI
python gui_basica.py
```

### Método 2: Usar el archivo batch (Windows)

```bash
# Doble clic en el archivo o ejecutar desde terminal
ejecutar_gui.bat
```

## 📋 Funcionalidades

### Panel de Menú (Izquierda)

- **👥 Usuarios**: Ver lista completa de usuarios registrados
- **💰 Cuentas**: Ver todas las cuentas bancarias con sus saldos
- **📱 Enlaces Teléfono**: Ver enlaces SINPE móvil configurados
- **📊 Transacciones**: Ver historial completo de transacciones
- **➕ Crear Usuario**: Diálogo para registrar nuevos usuarios
- **🏦 Crear Cuenta**: Diálogo para crear nuevas cuentas bancarias
- **💸 Transferir**: Realizar transferencias entre cuentas
- **🔄 Actualizar**: Refrescar toda la información

### Panel Principal (Centro)

- Muestra la información detallada de la opción seleccionada
- Área de texto con scroll para visualizar datos
- Información formateada y fácil de leer

### Panel de Log (Inferior)

- Muestra todas las actividades y operaciones en tiempo real
- Incluye timestamps y estados de las operaciones
- Ayuda a monitorear el funcionamiento del sistema

### Indicador de Estado

- **✅ Servidor conectado**: API funcionando correctamente
- **⚠️ Servidor con problemas**: API responde pero hay errores
- **❌ Servidor desconectado**: No se puede conectar a la API

## 🔧 Requisitos Previos

1. **Servidor ejecutándose**: La API debe estar corriendo en `https://127.0.0.1:5443`
2. **Python con Tkinter**: Viene incluido con Python por defecto
3. **Librerías**: requests, urllib3 (instaladas con requirements.txt)

## 📝 Uso Paso a Paso

### 1. Iniciar el Sistema

```bash
# Terminal 1: Iniciar el servidor principal
python main.py

# Terminal 2: Iniciar la interfaz gráfica
python gui_basica.py
```

### 2. Verificar Conexión

- Al abrir la GUI, verifica que aparezca "✅ Servidor conectado"
- Si aparece error, asegúrate de que el servidor esté ejecutándose

### 3. Explorar Datos Existentes

- Haz clic en "👥 Usuarios" para ver los usuarios de prueba
- Haz clic en "💰 Cuentas" para ver las cuentas disponibles
- Haz clic en "📊 Transacciones" para ver el historial

### 4. Crear Nuevos Elementos

- **Crear Usuario**: Completa todos los campos obligatorios
- **Crear Cuenta**: Especifica el ID de usuario y saldo inicial
- **Realizar Transferencia**: Usa los IDs de cuentas existentes

## 💡 Tips de Uso

### Datos de Prueba Disponibles

El sistema incluye datos de ejemplo:

- **Usuarios**: juan_perez, maria_rodriguez, carlos_gonzalez, ana_lopez
- **Contraseña**: password123 (para todos)
- **Cuentas**: 6 cuentas con diferentes saldos
- **Enlaces**: Números de teléfono configurados para SINPE

### IDs Útiles para Pruebas

- **Usuarios**: IDs 1, 2, 3, 4
- **Cuentas**: IDs 1, 2, 3, 4, 5, 6
- **Teléfonos**: 88887777, 88886666, 88885555, 88884444

### Transferencias de Ejemplo

```
Cuenta Origen: 1 (juan_perez - Saldo: 50,000)
Cuenta Destino: 3 (maria_rodriguez - Saldo: 100,000)
Monto: 1000.00
Descripción: Prueba de transferencia
```

## 🎨 Características de la Interfaz

### Diseño

- **Colores**: Esquema azul profesional
- **Iconos**: Emojis para mejor identificación visual
- **Layout**: Distribución en 3 paneles para máxima usabilidad
- **Responsive**: Se adapta al redimensionar la ventana

### Experiencia de Usuario

- **Diálogos**: Ventanas modales para operaciones específicas
- **Validación**: Verificación de datos en tiempo real
- **Feedback**: Mensajes claros de éxito/error
- **Log**: Registro completo de actividades

### Seguridad

- **SSL**: Conexiones seguras con el servidor
- **Validación**: Verificación de datos antes de enviar
- **Manejo de Errores**: Gestión robusta de excepciones

## 🔍 Resolución de Problemas

### "❌ Servidor desconectado"

1. Verifica que `main.py` esté ejecutándose
2. Confirma que el puerto 5443 esté disponible
3. Revisa que no haya errores en el log del servidor

### "Error al cargar datos"

1. Verifica la conexión a internet
2. Confirma que la base de datos esté inicializada
3. Revisa el log de actividad en la GUI

### "Datos Incompletos" al crear elementos

1. Completa todos los campos obligatorios
2. Verifica el formato de los datos (números, emails)
3. Usa IDs existentes para referencias

## 🛠️ Personalización

### Modificar Colores

Edita el diccionario `self.colors` en la clase `SinpeGUIBasica`:

```python
self.colors = {
    'primary': '#2196F3',    # Azul principal
    'success': '#4CAF50',    # Verde éxito
    'warning': '#FF9800',    # Naranja advertencia
    'error': '#F44336',      # Rojo error
    'bg': '#F5F5F5'         # Fondo gris claro
}
```

### Añadir Nuevas Funciones

1. Crea el método en la clase `SinpeGUIBasica`
2. Añade el botón correspondiente en `create_menu_panel`
3. Implementa la lógica de la API en `api_request`

## 📞 Soporte

Si encuentras problemas:

1. Revisa el log de actividad en la GUI
2. Verifica que el servidor principal esté funcionando
3. Consulta los logs del sistema en la carpeta `logs/`

---

**¡Disfruta usando la interfaz gráfica del sistema bancario SINPE!** 🏦✨
