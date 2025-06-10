# Entorno y codigo

- este proyecto es para comunicacion entre bancos a un nivel basico
- el codigo no requiere complejidad
- se requiere el ssl ✅ (FUNCIONANDO - certificados en app/ssl/)
- se requiere hmac ✅ (FUNCIONANDO - todas las pruebas pasan)
- configurado en .venv de python 3.12.4 en este proyecto ✅ (FUNCIONANDO)
- en windows tengo tanto python 3.13 como el 3.12 pero solo usamos el del .venv que es el 3.12

***IMPORTANTE: actualmente no se esta conectado con otros bancos por lo que no se puede probar la comunicacion entre bancos, pero todas las funciones internas funcionan correctamente***

## Estado Actual del Sistema ✅

- **Servidor API**: Funciona en <https://127.0.0.1:5443> (SSL habilitado)
- **Base de datos**: SQLite funcionando con datos de ejemplo
- **Interfaz terminal**: Totalmente funcional con Rich UI
- **Pruebas**: 4/4 tests pasando (HMAC y validaciones)
- **SSL**: Certificados funcionando correctamente
- **Funciones internas**: Todas operativas (usuarios, cuentas, transferencias internas)

## Comandos útiles para este proyecto

### Ejecutar el sistema

- **Interfaz Gráfica (NUEVA - Recomendada)**:

    ```batch
    run-GUI.bat
    ```

    *O alternativamente:*

    ```powershell
    .\.venv\Scripts\python.exe gui_simple.py
    ```

- **Terminal/Consola (Anterior)**:

    ```batch
    run-app.bat
    ```

    *O alternativamente:*

    ```powershell
    .\.venv\Scripts\python.exe main.py
    ```

### Comandos de desarrollo

- **Ejecutar pruebas**:

    ```powershell
    .\.venv\Scripts\python.exe -m pytest tests/ -v
    ```

- **Instalar dependencias**:

    ```powershell
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    ```

## URLs importantes

- **API Server (SSL)**: <https://127.0.0.1:5443>
- **API Health Check**: <https://127.0.0.1:5443/health>
- **API Monitoring**: <https://127.0.0.1:5443/api/monitoring/health>
