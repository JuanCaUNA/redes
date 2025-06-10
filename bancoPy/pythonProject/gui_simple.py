#!/usr/bin/env python3
"""
Interfaz Gráfica Simple para SINPE Banking System
Interfaz amigable que utiliza la API REST del sistema
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import requests
import json
import subprocess
import sys
import os
from urllib3.exceptions import InsecureRequestWarning

# Suprimir advertencias SSL para desarrollo
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SinpeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SINPE Banking System - Interfaz Gráfica")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables del sistema
        self.api_base = "https://127.0.0.1:5443/api"
        self.server_process = None
        self.server_running = False
        self.current_user = None
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Verificar si el servidor está corriendo
        self.check_server_status()

    def setup_styles(self):
        """Configurar estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Header.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background='#f0f0f0',
                       foreground='#2c3e50')
        
        style.configure('Status.TLabel',
                       font=('Arial', 10),
                       background='#f0f0f0')
        
        style.configure('Success.TLabel',
                       font=('Arial', 10),
                       background='#f0f0f0',
                       foreground='#27ae60')
        
        style.configure('Error.TLabel',
                       font=('Arial', 10),
                       background='#f0f0f0',
                       foreground='#e74c3c')

    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="🏦 SINPE Banking System", 
                               style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Estado del servidor
        self.server_frame = ttk.LabelFrame(main_frame, text="Estado del Servidor", padding="10")
        self.server_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.status_label = ttk.Label(self.server_frame, 
                                     text="🔴 Servidor desconectado", 
                                     style='Error.TLabel')
        self.status_label.grid(row=0, column=0, padx=(0, 20))
        
        self.start_server_btn = ttk.Button(self.server_frame, 
                                          text="Iniciar Servidor",
                                          command=self.start_server)
        self.start_server_btn.grid(row=0, column=1, padx=5)
        
        self.stop_server_btn = ttk.Button(self.server_frame, 
                                         text="Detener Servidor",
                                         command=self.stop_server,
                                         state='disabled')
        self.stop_server_btn.grid(row=0, column=2, padx=5)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Pestaña de Usuarios
        self.create_users_tab()
        
        # Pestaña de Cuentas
        self.create_accounts_tab()
        
        # Pestaña de Transferencias
        self.create_transfers_tab()
        
        # Pestaña de Enlaces Telefónicos
        self.create_phone_links_tab()
        
        # Pestaña de Historial
        self.create_history_tab()
        
        # Frame de información
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        info_text = "Sistema bancario local - Solo funciones internas disponibles"
        ttk.Label(info_frame, text=info_text, style='Status.TLabel').grid(row=0, column=0)
        
        # Configurar redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def create_users_tab(self):
        """Crear pestaña de gestión de usuarios"""
        users_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(users_frame, text="👥 Usuarios")
        
        # Login section
        login_frame = ttk.LabelFrame(users_frame, text="Iniciar Sesión", padding="10")
        login_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(login_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.username_entry = ttk.Entry(login_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(login_frame, text="PIN:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.pin_entry = ttk.Entry(login_frame, width=10, show="*")
        self.pin_entry.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Button(login_frame, text="Iniciar Sesión", 
                  command=self.login_user).grid(row=0, column=4)
        
        # Usuario actual
        self.current_user_label = ttk.Label(users_frame, 
                                           text="No hay sesión activa", 
                                           style='Status.TLabel')
        self.current_user_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Lista de usuarios
        users_list_frame = ttk.LabelFrame(users_frame, text="Usuarios del Sistema", padding="10")
        users_list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview para usuarios
        self.users_tree = ttk.Treeview(users_list_frame, 
                                      columns=('ID', 'Nombre', 'Email', 'Teléfono'), 
                                      show='headings', height=8)
        
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Nombre', text='Nombre Completo')
        self.users_tree.heading('Email', text='Email')
        self.users_tree.heading('Teléfono', text='Teléfono')
        
        self.users_tree.column('ID', width=50)
        self.users_tree.column('Nombre', width=200)
        self.users_tree.column('Email', width=200)
        self.users_tree.column('Teléfono', width=100)
        
        self.users_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para usuarios
        users_scrollbar = ttk.Scrollbar(users_list_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        users_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)
        
        # Botones de usuario
        users_buttons_frame = ttk.Frame(users_frame)
        users_buttons_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(users_buttons_frame, text="Actualizar Lista", 
                  command=self.refresh_users).grid(row=0, column=0, padx=5)
        ttk.Button(users_buttons_frame, text="Crear Usuario", 
                  command=self.create_user).grid(row=0, column=1, padx=5)
        
        users_frame.columnconfigure(1, weight=1)
        users_frame.rowconfigure(2, weight=1)
        users_list_frame.columnconfigure(0, weight=1)
        users_list_frame.rowconfigure(0, weight=1)

    def create_accounts_tab(self):
        """Crear pestaña de gestión de cuentas"""
        accounts_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(accounts_frame, text="💰 Cuentas")
        
        # Lista de cuentas
        accounts_list_frame = ttk.LabelFrame(accounts_frame, text="Cuentas Bancarias", padding="10")
        accounts_list_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview para cuentas
        self.accounts_tree = ttk.Treeview(accounts_list_frame, 
                                         columns=('Usuario', 'IBAN', 'Saldo', 'Tipo'), 
                                         show='headings', height=10)
        
        self.accounts_tree.heading('Usuario', text='Usuario')
        self.accounts_tree.heading('IBAN', text='IBAN')
        self.accounts_tree.heading('Saldo', text='Saldo (₡)')
        self.accounts_tree.heading('Tipo', text='Tipo')
        
        self.accounts_tree.column('Usuario', width=150)
        self.accounts_tree.column('IBAN', width=250)
        self.accounts_tree.column('Saldo', width=120)
        self.accounts_tree.column('Tipo', width=100)
        
        self.accounts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para cuentas
        accounts_scrollbar = ttk.Scrollbar(accounts_list_frame, orient=tk.VERTICAL, command=self.accounts_tree.yview)
        accounts_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.accounts_tree.configure(yscrollcommand=accounts_scrollbar.set)
        
        # Botones de cuentas
        accounts_buttons_frame = ttk.Frame(accounts_frame)
        accounts_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(accounts_buttons_frame, text="Actualizar Lista", 
                  command=self.refresh_accounts).grid(row=0, column=0, padx=5)
        ttk.Button(accounts_buttons_frame, text="Crear Cuenta", 
                  command=self.create_account).grid(row=0, column=1, padx=5)
        ttk.Button(accounts_buttons_frame, text="Ver Detalles", 
                  command=self.view_account_details).grid(row=0, column=2, padx=5)
        
        accounts_frame.columnconfigure(1, weight=1)
        accounts_frame.rowconfigure(0, weight=1)
        accounts_list_frame.columnconfigure(0, weight=1)
        accounts_list_frame.rowconfigure(0, weight=1)

    def create_transfers_tab(self):
        """Crear pestaña de transferencias"""
        transfers_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(transfers_frame, text="💸 Transferencias")
        
        # Transferencia SINPE por cuenta
        sinpe_account_frame = ttk.LabelFrame(transfers_frame, text="Transferencia SINPE (Cuenta)", padding="10")
        sinpe_account_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(sinpe_account_frame, text="IBAN Origen:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.origin_iban_entry = ttk.Entry(sinpe_account_frame, width=30)
        self.origin_iban_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(sinpe_account_frame, text="IBAN Destino:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.dest_iban_entry = ttk.Entry(sinpe_account_frame, width=30)
        self.dest_iban_entry.grid(row=0, column=3)
        
        ttk.Label(sinpe_account_frame, text="Monto (₡):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.amount_account_entry = ttk.Entry(sinpe_account_frame, width=15)
        self.amount_account_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        ttk.Label(sinpe_account_frame, text="Descripción:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10))
        self.desc_account_entry = ttk.Entry(sinpe_account_frame, width=30)
        self.desc_account_entry.grid(row=1, column=3, pady=(10, 0))
        
        ttk.Button(sinpe_account_frame, text="Transferir por Cuenta", 
                  command=self.transfer_by_account).grid(row=2, column=0, columnspan=4, pady=(15, 0))
        
        # Transferencia SINPE Móvil
        sinpe_mobile_frame = ttk.LabelFrame(transfers_frame, text="Transferencia SINPE Móvil", padding="10")
        sinpe_mobile_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(sinpe_mobile_frame, text="IBAN Origen:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.origin_iban_mobile_entry = ttk.Entry(sinpe_mobile_frame, width=30)
        self.origin_iban_mobile_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(sinpe_mobile_frame, text="Teléfono Destino:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.dest_phone_entry = ttk.Entry(sinpe_mobile_frame, width=15)
        self.dest_phone_entry.grid(row=0, column=3)
        
        ttk.Label(sinpe_mobile_frame, text="Monto (₡):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.amount_mobile_entry = ttk.Entry(sinpe_mobile_frame, width=15)
        self.amount_mobile_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        ttk.Label(sinpe_mobile_frame, text="Descripción:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10))
        self.desc_mobile_entry = ttk.Entry(sinpe_mobile_frame, width=30)
        self.desc_mobile_entry.grid(row=1, column=3, pady=(10, 0))
        
        ttk.Button(sinpe_mobile_frame, text="Transferir por Teléfono", 
                  command=self.transfer_by_phone).grid(row=2, column=0, columnspan=4, pady=(15, 0))
        
        transfers_frame.columnconfigure(1, weight=1)

    def create_phone_links_tab(self):
        """Crear pestaña de enlaces telefónicos"""
        phone_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(phone_frame, text="📱 Enlaces")
        
        # Crear enlace telefónico
        create_link_frame = ttk.LabelFrame(phone_frame, text="Crear Enlace Telefónico", padding="10")
        create_link_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(create_link_frame, text="IBAN:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.link_iban_entry = ttk.Entry(create_link_frame, width=30)
        self.link_iban_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(create_link_frame, text="Teléfono:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.link_phone_entry = ttk.Entry(create_link_frame, width=15)
        self.link_phone_entry.grid(row=0, column=3)
        
        ttk.Button(create_link_frame, text="Crear Enlace", 
                  command=self.create_phone_link).grid(row=1, column=0, columnspan=4, pady=(15, 0))
        
        # Lista de enlaces
        links_list_frame = ttk.LabelFrame(phone_frame, text="Enlaces Telefónicos Activos", padding="10")
        links_list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview para enlaces
        self.links_tree = ttk.Treeview(links_list_frame, 
                                      columns=('Teléfono', 'IBAN', 'Usuario', 'Estado'), 
                                      show='headings', height=8)
        
        self.links_tree.heading('Teléfono', text='Teléfono')
        self.links_tree.heading('IBAN', text='IBAN')
        self.links_tree.heading('Usuario', text='Usuario')
        self.links_tree.heading('Estado', text='Estado')
        
        self.links_tree.column('Teléfono', width=120)
        self.links_tree.column('IBAN', width=250)
        self.links_tree.column('Usuario', width=150)
        self.links_tree.column('Estado', width=100)
        
        self.links_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para enlaces
        links_scrollbar = ttk.Scrollbar(links_list_frame, orient=tk.VERTICAL, command=self.links_tree.yview)
        links_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.links_tree.configure(yscrollcommand=links_scrollbar.set)
        
        # Botones
        links_buttons_frame = ttk.Frame(phone_frame)
        links_buttons_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(links_buttons_frame, text="Actualizar Lista", 
                  command=self.refresh_phone_links).grid(row=0, column=0, padx=5)
        
        phone_frame.columnconfigure(1, weight=1)
        phone_frame.rowconfigure(1, weight=1)
        links_list_frame.columnconfigure(0, weight=1)
        links_list_frame.rowconfigure(0, weight=1)

    def create_history_tab(self):
        """Crear pestaña de historial"""
        history_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(history_frame, text="📊 Historial")
        
        # Filtros
        filter_frame = ttk.LabelFrame(history_frame, text="Filtros", padding="10")
        filter_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(filter_frame, text="IBAN:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.filter_iban_entry = ttk.Entry(filter_frame, width=30)
        self.filter_iban_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Button(filter_frame, text="Buscar Transacciones", 
                  command=self.search_transactions).grid(row=0, column=2)
        
        # Lista de transacciones
        transactions_frame = ttk.LabelFrame(history_frame, text="Historial de Transacciones", padding="10")
        transactions_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview para transacciones
        self.transactions_tree = ttk.Treeview(transactions_frame, 
                                             columns=('Fecha', 'Tipo', 'Origen', 'Destino', 'Monto', 'Estado'), 
                                             show='headings', height=10)
        
        self.transactions_tree.heading('Fecha', text='Fecha')
        self.transactions_tree.heading('Tipo', text='Tipo')
        self.transactions_tree.heading('Origen', text='Origen')
        self.transactions_tree.heading('Destino', text='Destino')
        self.transactions_tree.heading('Monto', text='Monto (₡)')
        self.transactions_tree.heading('Estado', text='Estado')
        
        self.transactions_tree.column('Fecha', width=120)
        self.transactions_tree.column('Tipo', width=100)
        self.transactions_tree.column('Origen', width=150)
        self.transactions_tree.column('Destino', width=150)
        self.transactions_tree.column('Monto', width=100)
        self.transactions_tree.column('Estado', width=80)
        
        self.transactions_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para transacciones
        transactions_scrollbar = ttk.Scrollbar(transactions_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        transactions_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.transactions_tree.configure(yscrollcommand=transactions_scrollbar.set)
        
        # Botones
        history_buttons_frame = ttk.Frame(history_frame)
        history_buttons_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(history_buttons_frame, text="Actualizar Lista", 
                  command=self.refresh_transactions).grid(row=0, column=0, padx=5)
        
        history_frame.columnconfigure(1, weight=1)
        history_frame.rowconfigure(1, weight=1)
        transactions_frame.columnconfigure(0, weight=1)
        transactions_frame.rowconfigure(0, weight=1)

    # Métodos del servidor
    def check_server_status(self):
        """Verificar si el servidor está corriendo"""
        try:
            response = requests.get(f"{self.api_base.replace('/api', '')}/health", 
                                  verify=False, timeout=2)
            if response.status_code == 200:
                self.server_running = True
                self.status_label.config(text="🟢 Servidor conectado", style='Success.TLabel')
                self.start_server_btn.config(state='disabled')
                self.stop_server_btn.config(state='normal')
                self.refresh_all_data()
            else:
                raise requests.RequestException()
        except:
            self.server_running = False
            self.status_label.config(text="🔴 Servidor desconectado", style='Error.TLabel')
            self.start_server_btn.config(state='normal')
            self.stop_server_btn.config(state='disabled')

    def start_server(self):
        """Iniciar el servidor en segundo plano"""
        try:
            # Cambiar al directorio del proyecto
            project_dir = os.path.dirname(os.path.abspath(__file__))
            python_exe = os.path.join(project_dir, '.venv', 'Scripts', 'python.exe')
            main_py = os.path.join(project_dir, 'main.py')
            
            # Iniciar el servidor en un proceso separado
            self.server_process = subprocess.Popen(
                [python_exe, main_py],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # Esperar un momento y verificar el estado
            def check_server_startup():
                time.sleep(3)  # Esperar a que el servidor inicie
                self.root.after(0, self.check_server_status)
            
            threading.Thread(target=check_server_startup, daemon=True).start()
            
            messagebox.showinfo("Servidor", "Iniciando servidor... Por favor espera unos segundos.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")

    def stop_server(self):
        """Detener el servidor"""
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process = None
            
            self.server_running = False
            self.status_label.config(text="🔴 Servidor desconectado", style='Error.TLabel')
            self.start_server_btn.config(state='normal')
            self.stop_server_btn.config(state='disabled')
            
            messagebox.showinfo("Servidor", "Servidor detenido correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al detener el servidor: {e}")

    # Métodos de API
    def api_request(self, method, endpoint, data=None):
        """Realizar petición a la API"""
        if not self.server_running:
            messagebox.showerror("Error", "El servidor no está conectado")
            return None
        
        try:
            url = f"{self.api_base}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, verify=False, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, verify=False, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, verify=False, timeout=10)
            else:
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                messagebox.showerror("Error API", f"Error {response.status_code}: {response.text}")
                return None
                
        except requests.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la API: {e}")
            return None

    # Métodos de usuarios
    def login_user(self):
        """Iniciar sesión de usuario"""
        username = self.username_entry.get().strip()
        pin = self.pin_entry.get().strip()
        
        if not username or not pin:
            messagebox.showerror("Error", "Por favor ingrese usuario y PIN")
            return
        
        data = {"username": username, "pin": pin}
        result = self.api_request('POST', '/auth/login', data)
        
        if result and result.get('success'):
            self.current_user = result.get('user')
            self.current_user_label.config(
                text=f"Sesión activa: {self.current_user.get('full_name', username)}",
                style='Success.TLabel'
            )
            messagebox.showinfo("Éxito", f"Bienvenido, {self.current_user.get('full_name', username)}")
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", result.get('message', 'Error al iniciar sesión') if result else 'Error de conexión')

    def refresh_users(self):
        """Actualizar lista de usuarios"""
        result = self.api_request('GET', '/users')
        
        if result and result.get('success'):
            # Limpiar lista actual
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Agregar usuarios
            for user in result.get('users', []):
                self.users_tree.insert('', 'end', values=(
                    user.get('id', ''),
                    user.get('full_name', ''),
                    user.get('email', ''),
                    user.get('phone', '')
                ))

    def create_user(self):
        """Crear nuevo usuario"""
        # Diálogo simple para crear usuario
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Usuario")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos del formulario
        ttk.Label(dialog, text="Nombre completo:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        phone_entry = ttk.Entry(dialog, width=30)
        phone_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="PIN:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        pin_entry = ttk.Entry(dialog, width=30, show="*")
        pin_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def submit_user():
            data = {
                "full_name": name_entry.get().strip(),
                "email": email_entry.get().strip(),
                "phone": phone_entry.get().strip(),
                "pin": pin_entry.get().strip()
            }
            
            if not all(data.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            result = self.api_request('POST', '/users', data)
            
            if result and result.get('success'):
                messagebox.showinfo("Éxito", "Usuario creado exitosamente")
                dialog.destroy()
                self.refresh_users()
            else:
                messagebox.showerror("Error", result.get('message', 'Error al crear usuario') if result else 'Error de conexión')
        
        ttk.Button(dialog, text="Crear Usuario", command=submit_user).grid(row=4, column=0, columnspan=2, pady=20)

    # Métodos de cuentas
    def refresh_accounts(self):
        """Actualizar lista de cuentas"""
        result = self.api_request('GET', '/accounts')
        
        if result and result.get('success'):
            # Limpiar lista actual
            for item in self.accounts_tree.get_children():
                self.accounts_tree.delete(item)
            
            # Agregar cuentas
            for account in result.get('accounts', []):
                self.accounts_tree.insert('', 'end', values=(
                    account.get('user_name', ''),
                    account.get('iban', ''),
                    f"{account.get('balance', 0):,.2f}",
                    account.get('account_type', '')
                ))

    def create_account(self):
        """Crear nueva cuenta"""
        if not self.current_user:
            messagebox.showerror("Error", "Debe iniciar sesión primero")
            return
        
        # Diálogo para crear cuenta
        account_type = simpledialog.askstring("Crear Cuenta", 
                                             "Tipo de cuenta (ahorros/corriente):",
                                             initialvalue="ahorros")
        
        if account_type:
            data = {
                "user_id": self.current_user.get('id'),
                "account_type": account_type,
                "initial_balance": 0
            }
            
            result = self.api_request('POST', '/accounts', data)
            
            if result and result.get('success'):
                messagebox.showinfo("Éxito", f"Cuenta creada: {result.get('account', {}).get('iban', '')}")
                self.refresh_accounts()
            else:
                messagebox.showerror("Error", result.get('message', 'Error al crear cuenta') if result else 'Error de conexión')

    def view_account_details(self):
        """Ver detalles de cuenta seleccionada"""
        selection = self.accounts_tree.selection()
        if not selection:
            messagebox.showinfo("Información", "Por favor seleccione una cuenta")
            return
        
        item = self.accounts_tree.item(selection[0])
        iban = item['values'][1]
        
        result = self.api_request('GET', f'/accounts/{iban}')
        
        if result and result.get('success'):
            account = result.get('account', {})
            details = f"""
IBAN: {account.get('iban', '')}
Usuario: {account.get('user_name', '')}
Tipo: {account.get('account_type', '')}
Saldo: ₡{account.get('balance', 0):,.2f}
Estado: {account.get('status', '')}
Fecha de creación: {account.get('created_at', '')}
            """
            messagebox.showinfo("Detalles de la Cuenta", details)

    # Métodos de transferencias
    def transfer_by_account(self):
        """Realizar transferencia por cuenta"""
        origin_iban = self.origin_iban_entry.get().strip()
        dest_iban = self.dest_iban_entry.get().strip()
        amount = self.amount_account_entry.get().strip()
        description = self.desc_account_entry.get().strip() or "Transferencia SINPE"
        
        if not all([origin_iban, dest_iban, amount]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("El monto debe ser positivo")
        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
            return
        
        data = {
            "origin_iban": origin_iban,
            "destination_iban": dest_iban,
            "amount": amount,
            "description": description
        }
        
        result = self.api_request('POST', '/sinpe/transfer-account', data)
        
        if result and result.get('success'):
            messagebox.showinfo("Éxito", f"Transferencia exitosa. ID: {result.get('transaction_id', '')}")
            self.clear_transfer_fields()
            self.refresh_accounts()
        else:
            messagebox.showerror("Error", result.get('message', 'Error en la transferencia') if result else 'Error de conexión')

    def transfer_by_phone(self):
        """Realizar transferencia por teléfono"""
        origin_iban = self.origin_iban_mobile_entry.get().strip()
        dest_phone = self.dest_phone_entry.get().strip()
        amount = self.amount_mobile_entry.get().strip()
        description = self.desc_mobile_entry.get().strip() or "Transferencia SINPE Móvil"
        
        if not all([origin_iban, dest_phone, amount]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("El monto debe ser positivo")
        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
            return
        
        data = {
            "origin_iban": origin_iban,
            "destination_phone": dest_phone,
            "amount": amount,
            "description": description
        }
        
        result = self.api_request('POST', '/sinpe/transfer-phone', data)
        
        if result and result.get('success'):
            messagebox.showinfo("Éxito", f"Transferencia exitosa. ID: {result.get('transaction_id', '')}")
            self.clear_transfer_mobile_fields()
            self.refresh_accounts()
        else:
            messagebox.showerror("Error", result.get('message', 'Error en la transferencia') if result else 'Error de conexión')

    def clear_transfer_fields(self):
        """Limpiar campos de transferencia por cuenta"""
        self.origin_iban_entry.delete(0, tk.END)
        self.dest_iban_entry.delete(0, tk.END)
        self.amount_account_entry.delete(0, tk.END)
        self.desc_account_entry.delete(0, tk.END)

    def clear_transfer_mobile_fields(self):
        """Limpiar campos de transferencia móvil"""
        self.origin_iban_mobile_entry.delete(0, tk.END)
        self.dest_phone_entry.delete(0, tk.END)
        self.amount_mobile_entry.delete(0, tk.END)
        self.desc_mobile_entry.delete(0, tk.END)

    # Métodos de enlaces telefónicos
    def create_phone_link(self):
        """Crear enlace telefónico"""
        iban = self.link_iban_entry.get().strip()
        phone = self.link_phone_entry.get().strip()
        
        if not iban or not phone:
            messagebox.showerror("Error", "IBAN y teléfono son obligatorios")
            return
        
        data = {
            "iban": iban,
            "phone_number": phone
        }
        
        result = self.api_request('POST', '/phone-links', data)
        
        if result and result.get('success'):
            messagebox.showinfo("Éxito", "Enlace telefónico creado exitosamente")
            self.link_iban_entry.delete(0, tk.END)
            self.link_phone_entry.delete(0, tk.END)
            self.refresh_phone_links()
        else:
            messagebox.showerror("Error", result.get('message', 'Error al crear enlace') if result else 'Error de conexión')

    def refresh_phone_links(self):
        """Actualizar lista de enlaces telefónicos"""
        result = self.api_request('GET', '/phone-links')
        
        if result and result.get('success'):
            # Limpiar lista actual
            for item in self.links_tree.get_children():
                self.links_tree.delete(item)
            
            # Agregar enlaces
            for link in result.get('phone_links', []):
                self.links_tree.insert('', 'end', values=(
                    link.get('phone_number', ''),
                    link.get('iban', ''),
                    link.get('user_name', ''),
                    link.get('status', '')
                ))

    # Métodos de historial
    def search_transactions(self):
        """Buscar transacciones"""
        iban = self.filter_iban_entry.get().strip()
        
        endpoint = '/transactions'
        if iban:
            endpoint += f'?iban={iban}'
        
        result = self.api_request('GET', endpoint)
        
        if result and result.get('success'):
            # Limpiar lista actual
            for item in self.transactions_tree.get_children():
                self.transactions_tree.delete(item)
            
            # Agregar transacciones
            for trans in result.get('transactions', []):
                self.transactions_tree.insert('', 'end', values=(
                    trans.get('created_at', '')[:16],  # Solo fecha y hora
                    trans.get('transaction_type', ''),
                    trans.get('origin_iban', '')[-8:] if trans.get('origin_iban') else '',  # Últimos 8 dígitos
                    trans.get('destination_info', ''),
                    f"₡{trans.get('amount', 0):,.2f}",
                    trans.get('status', '')
                ))

    def refresh_transactions(self):
        """Actualizar lista de transacciones"""
        self.search_transactions()

    # Método para actualizar todos los datos
    def refresh_all_data(self):
        """Actualizar todos los datos de la interfaz"""
        if self.server_running:
            self.refresh_users()
            self.refresh_accounts()
            self.refresh_phone_links()
            self.refresh_transactions()

    def run(self):
        """Iniciar la interfaz gráfica"""
        self.root.mainloop()


if __name__ == "__main__":
    app = SinpeGUI()
    app.run()
