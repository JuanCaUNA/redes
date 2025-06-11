Collecting workspace information# Estructura del Proyecto SINPE Banking System

Basado en la información de tu workspace, el proyecto bancoPy/pythonProject tiene la siguiente estructura:

## 🏗️ Estructura Principal

```
bancoPy/pythonProject/
├── main.py                 # 🚀 Punto de entrada principal
├── gui_basica.py           # 🖥️ Interfaz gráfica con Tkinter
├── ejecutar_gui.bat        # 🔄 Script para iniciar la GUI en Windows
├── requirements.txt        # 📦 Dependencias Python
├── README.md               # 📖 Documentación principal
├── README_GUI.md           # 📖 Documentación de la interfaz gráfica
├── MisNotas.md             # 📝 Notas del usuario
├── .env                    # ⚙️ Variables de entorno
├── contactos-bancos.json   # 🏦 Configuración de bancos externos
├── IBAN-estructure.json    # 🔄 Estructura IBAN
├── app/                    # 🏢 Aplicación principal
│   ├── __init__.py         # Flask app factory
│   ├── models/             # 🗃️ Modelos de base de datos
│   ├── routes/             # 🛣️ Rutas de API
│   ├── services/           # 🔧 Lógica de negocio
│   ├── ssl/                # 🔐 Certificados SSL
│   └── utils/              # 🛠️ Utilidades
├── config/                 # ⚙️ Configuración
│   ├── settings.py         # Configuraciones generales
│   └── banks.json          # Mapeo de bancos
├── database/               # 🗄️ Base de datos
│   └── banking.db          # SQLite (auto-creado)
├── logs/                   # 📋 Archivos de log
└── tests/                  # 🧪 Pruebas unitarias
```

## 🔌 Componentes Principales

1. **Interfaces de Usuario**:
   - `gui_basica.py` - Interfaz gráfica con Tkinter
   - `main.py` - Interfaz de terminal y punto de entrada principal

2. **Documentación**:
   - `README.md` - Documentación general del sistema
   - `README_GUI.md` - Documentación específica de la GUI

3. **Configuración**:
   - `contactos-bancos.json` - Configuración de bancos externos
   - `config/banks.json` - Configuración de bancos (alternativa)

4. **Seguridad**:
   - `app/ssl/` - Certificados SSL para comunicación segura

5. **Backend API**:
   - `app/routes/` - Endpoints API para transferencias SINPE

## 🔧 Problemas Estructurales Identificados

Como se menciona en tus archivos de análisis, hay algunos problemas estructurales:

1. **Configuración Duplicada**:
   - contactos-bancos.json
   - `config/banks.json`

2. **Rutas Duplicadas**:
   - Múltiples archivos en `app/routes/` con endpoints similares

Estos problemas necesitan ser corregidos para tener una estructura de proyecto más consistente y mantenible.
