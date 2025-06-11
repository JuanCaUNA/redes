#!/usr/bin/env python3
"""
Interfaz Gráfica Básica para SINPE Banking System
Una GUI simple usando Tkinter para interactuar con el sistema bancario
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import urllib3
import threading
import json
from datetime import datetime

# Deshabilitar advertencias SSL para desarrollo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SinpeGUIBasica:
    """Interfaz gráfica básica para el sistema bancario SINPE"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SINPE Banking System - Interfaz Básica")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # URL base de la API
        self.api_base = "https://127.0.0.1:5443/api"

        # Variables
        self.current_user = None

        # Configurar estilos
        self.setup_styles()

        # Crear la interfaz
        self.create_widgets()

        # Verificar si el servidor está corriendo
        self.check_server_status()

    def setup_styles(self):
        """Configurar estilos básicos"""
        style = ttk.Style()
        style.theme_use("clam")

        # Configurar colores
        self.colors = {
            "primary": "#2196F3",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336",
            "bg": "#F5F5F5",
        }

        self.root.configure(bg=self.colors["bg"])

    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""

        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame, text="🏦 SINPE Banking System", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Estado del servidor
        self.server_status_label = ttk.Label(
            main_frame, text="🔄 Verificando servidor...", foreground="orange"
        )
        self.server_status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # Panel izquierdo - Menú de opciones
        self.create_menu_panel(main_frame)

        # Panel derecho - Área de contenido
        self.create_content_panel(main_frame)

        # Panel inferior - Log de actividad
        self.create_log_panel(main_frame)

    def create_menu_panel(self, parent):
        """Crear panel de menú"""
        menu_frame = ttk.LabelFrame(parent, text="📋 Opciones", padding="10")
        menu_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Botones del menú
        buttons = [
            ("👥 Usuarios", self.show_users),
            ("💰 Cuentas", self.show_accounts),
            ("📱 Enlaces Teléfono", self.show_phone_links),
            ("📊 Transacciones", self.show_transactions),
            ("➕ Crear Usuario", self.create_user_dialog),
            ("🏦 Crear Cuenta", self.create_account_dialog),
            ("💸 Transferir", self.transfer_dialog),
            ("🔄 Actualizar", self.refresh_all),
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(menu_frame, text=text, command=command, width=20)
            btn.grid(row=i, column=0, pady=2, sticky=tk.W + tk.E)

        menu_frame.columnconfigure(0, weight=1)

    def create_content_panel(self, parent):
        """Crear panel de contenido principal"""
        self.content_frame = ttk.LabelFrame(parent, text="📄 Información", padding="10")
        self.content_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # Área de texto con scroll
        self.content_text = scrolledtext.ScrolledText(
            self.content_frame, width=60, height=20, wrap=tk.WORD
        )
        self.content_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Mensaje inicial
        self.show_welcome_message()

    def create_log_panel(self, parent):
        """Crear panel de log"""
        log_frame = ttk.LabelFrame(parent, text="📋 Log de Actividad", padding="5")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def log_message(self, message):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def check_server_status(self):
        """Verificar estado del servidor"""

        def check():
            try:
                response = requests.get(
                    f"{self.api_base}/users", verify=False, timeout=3
                )
                if response.status_code == 200:
                    self.server_status_label.config(
                        text="✅ Servidor conectado", foreground="green"
                    )
                    self.log_message("✅ Conexión con servidor establecida")
                else:
                    self.server_status_label.config(
                        text="⚠️ Servidor con problemas", foreground="orange"
                    )
                    self.log_message("⚠️ Servidor responde pero hay problemas")
            except Exception as e:
                self.server_status_label.config(
                    text="❌ Servidor desconectado", foreground="red"
                )
                self.log_message(f"❌ Error de conexión: {str(e)}")

        threading.Thread(target=check, daemon=True).start()

    def api_request(self, method, endpoint, data=None):
        """Realizar petición a la API"""
        try:
            url = f"{self.api_base}{endpoint}"
            self.log_message(f"🔄 {method} {endpoint}")

            if method == "GET":
                response = requests.get(url, verify=False, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, verify=False, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, verify=False, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, verify=False, timeout=10)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            if response.status_code in [200, 201]:
                self.log_message(f"✅ {method} {endpoint} - Éxito")
                return response.json()
            else:
                self.log_message(
                    f"❌ {method} {endpoint} - Error {response.status_code}"
                )
                return None

        except Exception as e:
            self.log_message(f"❌ Error en {method} {endpoint}: {str(e)}")
            return None

    def show_welcome_message(self):
        """Mostrar mensaje de bienvenida"""
        welcome_text = """
🏦 BIENVENIDO AL SISTEMA BANCARIO SINPE

Esta es una interfaz gráfica básica para interactuar con el sistema bancario.

FUNCIONALIDADES DISPONIBLES:
• Ver y gestionar usuarios
• Ver y crear cuentas bancarias  
• Gestionar enlaces de teléfono para SINPE
• Ver historial de transacciones
• Realizar transferencias
• Crear nuevos usuarios y cuentas

INSTRUCCIONES:
1. Usa los botones del menú izquierdo para navegar
2. La información se mostrará en esta área
3. El log inferior muestra la actividad del sistema

¡Comienza seleccionando una opción del menú!
        """
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, welcome_text)

    def show_users(self):
        """Mostrar lista de usuarios"""
        self.content_frame.config(text="👥 Lista de Usuarios")
        data = self.api_request("GET", "/users")

        if data and data.get("success"):
            users = data.get("data", [])
            content = "📋 USUARIOS REGISTRADOS\n" + "=" * 50 + "\n\n"

            if users:
                for i, user in enumerate(users, 1):
                    content += f"{i}. {user.get('name', 'N/A')}\n"
                    content += f"   📧 Email: {user.get('email', 'N/A')}\n"
                    content += f"   📱 Teléfono: {user.get('phone', 'N/A')}\n"
                    content += f"   📅 Creado: {user.get('created_at', 'N/A')[:10]}\n"
                    content += "-" * 40 + "\n"
            else:
                content += "📭 No hay usuarios registrados\n"

            content += f"\n📊 Total: {len(users)} usuarios"
        else:
            content = "❌ Error al cargar usuarios"

        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, content)

    def show_accounts(self):
        """Mostrar lista de cuentas"""
        self.content_frame.config(text="💰 Lista de Cuentas")
        data = self.api_request("GET", "/accounts")

        if data and data.get("success"):
            accounts = data.get("data", [])
            content = "🏦 CUENTAS BANCARIAS\n" + "=" * 50 + "\n\n"

            if accounts:
                for i, account in enumerate(accounts, 1):
                    content += f"{i}. Cuenta ID: {account.get('id', 'N/A')}\n"
                    content += f"   🏦 IBAN: {account.get('iban', 'N/A')}\n"
                    content += f"   📄 Número: {account.get('number', 'N/A')}\n"
                    content += f"   💰 Saldo: {account.get('balance', 0):,.2f} {account.get('currency', 'CRC')}\n"
                    content += f"   👤 Usuario: {account.get('user_id', 'N/A')}\n"
                    content += f"   📅 Creada: {account.get('created_at', 'N/A')[:10]}\n"
                    content += "-" * 40 + "\n"
            else:
                content += "📭 No hay cuentas registradas\n"

            content += f"\n📊 Total: {len(accounts)} cuentas"
        else:
            content = "❌ Error al cargar cuentas"

        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, content)

    def show_phone_links(self):
        """Mostrar enlaces de teléfono"""
        self.content_frame.config(text="📱 Enlaces de Teléfono")
        data = self.api_request("GET", "/phone-links")

        if data and data.get("success"):
            links = data.get("data", [])
            content = "📱 ENLACES SINPE MÓVIL\n" + "=" * 50 + "\n\n"

            if links:
                for i, link in enumerate(links, 1):
                    content += f"{i}. Enlace ID: {link.get('id', 'N/A')}\n"
                    content += f"   📱 Teléfono: {link.get('phone', 'N/A')}\n"
                    content += f"   🏦 Cuenta: {link.get('account_number', 'N/A')}\n"
                    content += f"   📅 Creado: {link.get('created_at', 'N/A')[:10]}\n"
                    content += "-" * 40 + "\n"
            else:
                content += "📭 No hay enlaces de teléfono\n"

            content += f"\n📊 Total: {len(links)} enlaces"
        else:
            content = "❌ Error al cargar enlaces de teléfono"

        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, content)

    def show_transactions(self):
        """Mostrar transacciones"""
        self.content_frame.config(text="📊 Historial de Transacciones")
        data = self.api_request("GET", "/transactions")

        if data and data.get("success"):
            transactions = data.get("data", [])
            content = "💸 HISTORIAL DE TRANSACCIONES\n" + "=" * 50 + "\n\n"

            if transactions:
                for i, trans in enumerate(transactions, 1):
                    content += f"{i}. ID: {trans.get('transaction_id', 'N/A')[:8]}...\n"
                    content += f"   💰 Monto: {trans.get('amount', 0):,.2f} {trans.get('currency', 'CRC')}\n"
                    content += (
                        f"   📤 Desde: Cuenta {trans.get('from_account_id', 'N/A')}\n"
                    )
                    content += (
                        f"   📥 Hacia: Cuenta {trans.get('to_account_id', 'N/A')}\n"
                    )
                    content += f"   📋 Estado: {trans.get('status', 'N/A')}\n"
                    content += f"   📝 Descripción: {trans.get('description', 'N/A')}\n"
                    content += f"   📅 Fecha: {trans.get('created_at', 'N/A')[:10]}\n"
                    content += "-" * 40 + "\n"
            else:
                content += "📭 No hay transacciones registradas\n"

            content += f"\n📊 Total: {len(transactions)} transacciones"
        else:
            content = "❌ Error al cargar transacciones"

        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, content)

    def create_user_dialog(self):
        """Diálogo para crear usuario"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nuevo Usuario")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrar diálogo
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50)
        )

        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos
        ttk.Label(frame, text="👤 Crear Nuevo Usuario", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame, width=30)
        name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(frame, width=30)
        email_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(frame, width=30)
        phone_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(frame, width=30, show="*")
        password_entry.grid(row=4, column=1, pady=5)

        def create_user():
            data = {
                "name": name_entry.get(),
                "email": email_entry.get(),
                "phone": phone_entry.get(),
                "password": password_entry.get(),
            }

            if not all(data.values()):
                messagebox.showwarning(
                    "Datos Incompletos", "Todos los campos son obligatorios"
                )
                return

            result = self.api_request("POST", "/users", data)
            if result and result.get("success"):
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                dialog.destroy()
                self.show_users()  # Actualizar lista
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario")

        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="✅ Crear", command=create_user).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy).grid(
            row=0, column=1, padx=5
        )

    def create_account_dialog(self):
        """Diálogo para crear cuenta"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nueva Cuenta")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrar diálogo
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50)
        )

        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos
        ttk.Label(frame, text="🏦 Crear Nueva Cuenta", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        ttk.Label(frame, text="ID de Usuario:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        user_id_entry = ttk.Entry(frame, width=30)
        user_id_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Moneda:").grid(row=2, column=0, sticky=tk.W, pady=5)
        currency_combo = ttk.Combobox(frame, values=["CRC", "USD", "EUR"], width=27)
        currency_combo.set("CRC")
        currency_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Saldo Inicial:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        balance_entry = ttk.Entry(frame, width=30)
        balance_entry.insert(0, "0.00")
        balance_entry.grid(row=3, column=1, pady=5)

        def create_account():
            try:
                data = {
                    "user_id": int(user_id_entry.get())
                    if user_id_entry.get()
                    else None,
                    "currency": currency_combo.get(),
                    "balance": float(balance_entry.get()),
                }

                result = self.api_request("POST", "/accounts", data)
                if result and result.get("success"):
                    messagebox.showinfo("Éxito", "Cuenta creada correctamente")
                    dialog.destroy()
                    self.show_accounts()  # Actualizar lista
                else:
                    messagebox.showerror("Error", "No se pudo crear la cuenta")
            except ValueError:
                messagebox.showwarning(
                    "Datos Inválidos", "Verifique que los valores sean correctos"
                )

        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="✅ Crear", command=create_account).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy).grid(
            row=0, column=1, padx=5
        )

    def transfer_dialog(self):
        """Diálogo para realizar transferencia"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Realizar Transferencia")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrar diálogo
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50)
        )

        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos
        ttk.Label(
            frame, text="💸 Realizar Transferencia", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(frame, text="Cuenta Origen (ID):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        from_entry = ttk.Entry(frame, width=30)
        from_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Cuenta Destino (ID):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        to_entry = ttk.Entry(frame, width=30)
        to_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Monto:").grid(row=3, column=0, sticky=tk.W, pady=5)
        amount_entry = ttk.Entry(frame, width=30)
        amount_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Descripción:").grid(row=4, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(frame, width=30)
        desc_entry.grid(row=4, column=1, pady=5)

        def make_transfer():
            try:
                data = {
                    "from_account_id": int(from_entry.get()),
                    "to_account_id": int(to_entry.get()),
                    "amount": float(amount_entry.get()),
                    "description": desc_entry.get() or "Transferencia GUI",
                }

                result = self.api_request("POST", "/transactions", data)
                if result and result.get("success"):
                    messagebox.showinfo(
                        "Éxito", "Transferencia realizada correctamente"
                    )
                    dialog.destroy()
                    self.show_transactions()  # Actualizar lista
                else:
                    messagebox.showerror(
                        "Error", "No se pudo realizar la transferencia"
                    )
            except ValueError:
                messagebox.showwarning(
                    "Datos Inválidos", "Verifique que los valores sean correctos"
                )

        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="💸 Transferir", command=make_transfer).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy).grid(
            row=0, column=1, padx=5
        )

    def refresh_all(self):
        """Refrescar toda la información"""
        self.log_message("🔄 Actualizando información...")
        self.check_server_status()
        self.show_welcome_message()
        self.log_message("✅ Información actualizada")

    def run(self):
        """Ejecutar la interfaz gráfica"""
        try:
            self.log_message("🚀 Iniciando interfaz gráfica SINPE...")
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_message("👋 Cerrando aplicación...")
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")


def main():
    """Función principal"""
    print("🏦 Iniciando Interfaz Gráfica Básica SINPE...")

    # Crear y ejecutar la aplicación
    app = SinpeGUIBasica()
    app.run()


if __name__ == "__main__":
    main()
