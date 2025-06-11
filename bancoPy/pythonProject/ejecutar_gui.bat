@echo off
echo =========================================
echo  SINPE Banking System - Interfaz Grafica
echo =========================================
echo.

REM Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo Entorno virtual no encontrado, usando Python del sistema...
)

echo.
echo Iniciando servidor...
echo.

REM Ejecutar servidor
python main.py

echo.
echo Iniciando interfaz grafica...
echo.

REM Ejecutar la interfaz gráfica
python gui_basica.py

echo.
echo Interfaz cerrada. Presiona cualquier tecla para salir...
pause > nul
