# Entorno y codigo

- este proyecto es para comunicacion entre bancos a un nivel basico
- el codigo no requiere complejidad
- se requiere el ssl
- se requiere hmac
- configurado en .venv de pyhon 3.12.4 en este proyecto
- en windows tengo tanto python 3.13 como el 3.12 pero solo usamos el del .venv que es el 3.12

***importante actualmente no se esta conectado con otros bancos por lo que no se puede probar la comunicacion entre bancos***

## Comandos útiles para Python

- Ejecutar un script Python:

    ```bash
    python archivo.py
    ```

- Instalar paquetes con pip:

    ```bash
    pip install nombre_paquete
    ```

- Crear un entorno virtual:

    ```bash
    python -m venv venv
    ```

- Activar entorno virtual:
  - En Windows:

    ```bash
    .\venv\Scripts\activate
    ```

  - En macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

## Comandos útiles para Ruff y Black

### Ruff

- Analizar código con Ruff:

    ```bash
    ruff .
    ```

- Corregir automáticamente problemas:

    ```bash
    ruff check . --fix
    ```

- Mostrar ayuda de Ruff:

    ```bash
    ruff --help
    ```

### Black

- Formatear todo el proyecto con Black:

    ```bash
    black .
    ```

- Formatear un archivo específico:

    ```bash
    black archivo.py
    ```

- Mostrar ayuda de Black:

    ```bash
    black --help
    ```
