#!/usr/bin/env python3
"""
SINPE Banking System - Main Entry Point (Optimized)
Terminal-based banking application with Flask API backend
"""

import os
import sys
import threading
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app import create_app
from app.models import db
from app.services.database_service import DatabaseService
from app.services.terminal_service import TerminalService

console = Console()


class SinpeBankingSystem:
    """Optimized SINPE Banking System with SSL support"""

    def __init__(self):
        self.app = create_app()
        self.terminal_service = TerminalService()
        self.current_user = None
        self.server_thread = None
        self.server_running = False

    def initialize_database(self):
        """Initialize database with sample data"""
        console.print("[yellow]Initializing database...[/yellow]")

        with self.app.app_context():
            db.create_all()
            db_service = DatabaseService()
            db_service.create_sample_data()

        console.print("[green]✓ Database initialized successfully[/green]")

    def start_api_server(self):
        """Start Flask API server with SSL support"""
        console.print("[yellow]Starting API server...[/yellow]")

        def run_server():
            ssl_context = getattr(self.app, "ssl_context", None)

            if ssl_context:
                console.print("🔐 [green]SSL certificates loaded successfully[/green]")
                port = 5443  # Standard HTTPS port for development
                self.app.run(
                    host="127.0.0.1",
                    port=port,
                    debug=False,
                    use_reloader=False,
                    ssl_context=ssl_context,
                    threaded=True,
                )
            else:
                console.print(
                    "⚠️ [yellow]SSL certificates not available - using HTTP[/yellow]"
                )
                port = 5000
                self.app.run(
                    host="127.0.0.1",
                    port=port,
                    debug=False,
                    use_reloader=False,
                    threaded=True,
                )

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        self.server_running = True

        # Wait for server to start
        time.sleep(1)
        ssl_context = getattr(self.app, "ssl_context", None)
        port = 5443 if ssl_context else 5000
        protocol = "https" if ssl_context else "http"
        console.print(
            f"✓ [green]API server started on {protocol}://127.0.0.1:{port}[/green]"
        )

    def show_welcome_screen(self):
        """Display welcome screen with SSL status"""
        console.clear()

        welcome_text = Text()
        welcome_text.append("SINPE", style="bold blue")
        welcome_text.append(" Banking System", style="bold white")

        panel = Panel(
            welcome_text,
            title="🏦 Welcome",
            title_align="center",
            border_style="blue",
            padding=(1, 2),
        )

        console.print(panel)
        console.print("\n[dim]Costa Rican Payment System - Python Implementation[/dim]")

        # Show appropriate URL based on SSL availability
        ssl_context = getattr(self.app, "ssl_context", None)
        if ssl_context:
            console.print(
                "[dim]🔐 API Server: https://127.0.0.1:5443 (SSL Enabled)[/dim]\n"
            )
        else:
            console.print(
                "[dim]⚠️ API Server: http://127.0.0.1:5000 (SSL Not Available)[/dim]\n"
            )

    def show_main_menu(self):
        """Display main menu options"""
        table = Table(show_header=False, box=box.ROUNDED)
        table.add_column("Option", style="cyan", width=4)
        table.add_column("Description", style="white")

        table.add_row("1", "🔐 Login / User Management")
        table.add_row("2", "💰 Account Management")
        table.add_row("3", "💸 SINPE Transfers")
        table.add_row("4", "📱 Phone Link Management")
        table.add_row("5", "📊 Transaction History")
        table.add_row("6", "⚙️ Admin Panel")
        table.add_row("0", "🚪 Exit")

        console.print(table)

    def handle_menu_choice(self, choice):
        """Handle menu choice selection"""
        try:
            if choice == "0":
                return False
            elif choice == "1":
                self.terminal_service.handle_user_management()
            elif choice == "2":
                self.terminal_service.handle_account_management()
            elif choice == "3":
                self.terminal_service.handle_sinpe_transfers()
            elif choice == "4":
                self.terminal_service.handle_phone_links()
            elif choice == "5":
                self.terminal_service.handle_transaction_history()
            elif choice == "6":
                self.terminal_service.handle_admin_panel()
            else:
                console.print("[red]Invalid option. Please try again.[/red]")

            return True

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return True

    def run(self):
        """Main application loop"""
        try:
            # Initialize system
            console.print("[cyan]Starting SINPE Banking System...[/cyan]")
            self.initialize_database()
            self.start_api_server()

            # Show welcome screen
            self.show_welcome_screen()

            # Main menu loop
            while True:
                console.print("\n" + "=" * 60)
                self.show_main_menu()

                choice = Prompt.ask(
                    "\n[bold cyan]Select an option[/bold cyan]", default="0"
                )

                if not self.handle_menu_choice(choice):
                    break

        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            console.print("[green]Thank you for using SINPE Banking System![/green]")


if __name__ == "__main__":
    system = SinpeBankingSystem()
    system.run()
