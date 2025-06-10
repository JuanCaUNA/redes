"""
System Health Monitoring Service
Monitors database connections, API health, inter-bank connectivity, and system performance
"""

import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
import threading
from app.models import db, Transaction, Account
from app.services.logging_service import banking_logger
from sqlalchemy import text
import json
import os


class SystemHealthMonitor:
    """Comprehensive system health monitoring"""

    def __init__(self):
        self.monitoring_active = True
        self.health_data = {
            "last_check": None,
            "database": {"status": "unknown", "response_time": 0},
            "api": {"status": "unknown", "response_time": 0},
            "inter_bank": {"status": "unknown", "reachable_banks": 0},
            "system": {"cpu_percent": 0, "memory_percent": 0, "disk_percent": 0},
            "transactions": {"last_24h": 0, "success_rate": 0},
            "alerts": []
        }
        self.start_monitoring()

    def start_monitoring(self):
        """Start background health monitoring"""
        def monitor_loop():
            while self.monitoring_active:
                try:
                    self.perform_health_check()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    banking_logger.log_error("health_monitoring", str(e))
                    time.sleep(60)

        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        banking_logger.app_logger.info("System health monitoring started")

    def perform_health_check(self) -> Dict:
        """Perform comprehensive health check"""
        try:
            self.health_data["last_check"] = datetime.utcnow().isoformat()
            self.health_data["alerts"] = []

            # Check database health
            self._check_database_health()

            # Check system resources
            self._check_system_resources()

            # Check transaction health
            self._check_transaction_health()

            # Check inter-bank connectivity (less frequently)
            if datetime.utcnow().minute % 5 == 0:  # Every 5 minutes
                self._check_inter_bank_health()

            # Generate alerts if needed
            self._generate_alerts()

            return self.health_data

        except Exception as e:
            banking_logger.log_error("health_check", str(e))
            return {"error": str(e), "timestamp": datetime.utcnow().isoformat()}

    def _check_database_health(self):
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Simple query to test connection
            result = db.session.execute(text("SELECT 1")).fetchone()
            
            response_time = time.time() - start_time
            
            if result and response_time < 1.0:  # Less than 1 second
                self.health_data["database"] = {
                    "status": "healthy",
                    "response_time": round(response_time * 1000, 2)  # Convert to ms
                }
            else:
                self.health_data["database"] = {
                    "status": "slow",
                    "response_time": round(response_time * 1000, 2)
                }
                self.health_data["alerts"].append("Database response time is slow")

        except Exception as e:
            self.health_data["database"] = {
                "status": "error",
                "response_time": 0,
                "error": str(e)
            }
            self.health_data["alerts"].append(f"Database connection failed: {str(e)}")

    def _check_system_resources(self):
        """Check system CPU, memory, and disk usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100

            self.health_data["system"] = {
                "cpu_percent": round(cpu_percent, 1),
                "memory_percent": round(memory_percent, 1),
                "disk_percent": round(disk_percent, 1),
                "status": "healthy"
            }

            # Generate alerts for high resource usage
            if cpu_percent > 80:
                self.health_data["alerts"].append(f"High CPU usage: {cpu_percent:.1f}%")
                self.health_data["system"]["status"] = "warning"

            if memory_percent > 85:
                self.health_data["alerts"].append(f"High memory usage: {memory_percent:.1f}%")
                self.health_data["system"]["status"] = "warning"

            if disk_percent > 90:
                self.health_data["alerts"].append(f"High disk usage: {disk_percent:.1f}%")
                self.health_data["system"]["status"] = "critical"

        except Exception as e:
            self.health_data["system"] = {
                "status": "error",
                "error": str(e)
            }

    def _check_transaction_health(self):
        """Check transaction processing health"""
        try:
            # Get transactions from last 24 hours
            twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
            
            total_transactions = Transaction.query.filter(
                Transaction.created_at >= twenty_four_hours_ago
            ).count()

            successful_transactions = Transaction.query.filter(
                Transaction.created_at >= twenty_four_hours_ago,
                Transaction.status == "completed"
            ).count()

            success_rate = (successful_transactions / max(total_transactions, 1)) * 100

            self.health_data["transactions"] = {
                "last_24h": total_transactions,
                "successful": successful_transactions,
                "success_rate": round(success_rate, 2),
                "status": "healthy"
            }

            # Generate alerts for low success rate
            if success_rate < 95 and total_transactions > 10:
                self.health_data["alerts"].append(
                    f"Low transaction success rate: {success_rate:.1f}%"
                )
                self.health_data["transactions"]["status"] = "warning"

            # Alert if no transactions in last hour (during business hours)
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            recent_transactions = Transaction.query.filter(
                Transaction.created_at >= one_hour_ago
            ).count()

            if recent_transactions == 0 and 8 <= datetime.utcnow().hour <= 18:  # Business hours
                self.health_data["alerts"].append("No transactions in the last hour during business hours")

        except Exception as e:
            self.health_data["transactions"] = {
                "status": "error",
                "error": str(e)
            }

    def _check_inter_bank_health(self):
        """Check connectivity to other banks"""
        try:
            # Load bank contacts
            contacts_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "contactos-bancos.json"
            )
            
            reachable_banks = 0
            total_banks = 0
            
            if os.path.exists(contacts_file):
                with open(contacts_file, 'r', encoding='utf-8') as f:
                    banks = json.load(f)
                
                for bank in banks:
                    if bank.get("IP"):
                        total_banks += 1
                        try:
                            # Quick health check to bank
                            response = requests.get(
                                f"http://{bank['IP']}/health",
                                timeout=5
                            )
                            if response.status_code == 200:
                                reachable_banks += 1
                        except:
                            pass  # Bank unreachable

            self.health_data["inter_bank"] = {
                "status": "healthy" if reachable_banks == total_banks else "partial",
                "reachable_banks": reachable_banks,
                "total_banks": total_banks,
                "connectivity_rate": round((reachable_banks / max(total_banks, 1)) * 100, 1)
            }

            if reachable_banks < total_banks:
                unreachable = total_banks - reachable_banks
                self.health_data["alerts"].append(
                    f"{unreachable} bank(s) unreachable out of {total_banks}"
                )

        except Exception as e:
            self.health_data["inter_bank"] = {
                "status": "error",
                "error": str(e)
            }

    def _generate_alerts(self):
        """Generate system-wide alerts based on health data"""
        try:
            # Critical system alerts
            critical_alerts = []
            warning_alerts = []

            # Check for critical conditions
            if self.health_data["database"]["status"] == "error":
                critical_alerts.append("Database connection failed")

            if self.health_data["system"].get("disk_percent", 0) > 95:
                critical_alerts.append("Critical disk space - system may fail")

            if self.health_data["system"].get("memory_percent", 0) > 95:
                critical_alerts.append("Critical memory usage - system may fail")

            # Log critical alerts
            for alert in critical_alerts:
                banking_logger.log_security_event(
                    "system_critical_alert",
                    {"alert": alert, "health_data": self.health_data},
                    "CRITICAL"
                )

            # Log warning alerts
            for alert in warning_alerts:
                banking_logger.log_security_event(
                    "system_warning_alert",
                    {"alert": alert, "health_data": self.health_data},
                    "WARNING"
                )

        except Exception as e:
            banking_logger.log_error("alert_generation", str(e))

    def get_health_status(self) -> Dict:
        """Get current health status"""
        return self.health_data.copy()

    def get_detailed_report(self) -> Dict:
        """Get detailed health report"""
        try:
            # Get additional metrics
            detailed_report = self.health_data.copy()
            
            # Add process information
            process = psutil.Process()
            detailed_report["process"] = {
                "pid": process.pid,
                "cpu_percent": process.cpu_percent(),
                "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
                "open_files": len(process.open_files()),
                "connections": len(process.connections()),
                "threads": process.num_threads()
            }

            # Add database connection pool info (if using SQLAlchemy with connection pooling)
            try:
                engine = db.engine
                pool = engine.pool
                detailed_report["database"]["pool"] = {
                    "size": pool.size(),
                    "checked_in": pool.checkedin(),
                    "checked_out": pool.checkedout(),
                    "overflow": pool.overflow(),
                    "invalid": pool.invalid()
                }
            except:
                pass  # Connection pool info not available

            # Add recent error summary
            detailed_report["recent_errors"] = self._get_recent_error_summary()

            return detailed_report

        except Exception as e:
            return {"error": str(e), "timestamp": datetime.utcnow().isoformat()}

    def _get_recent_error_summary(self) -> Dict:
        """Get summary of recent errors from logs"""
        # This is a simplified version - in production, you'd analyze log files
        return {
            "last_hour": 0,
            "last_24h": 0,
            "most_common": "Log analysis not implemented",
            "note": "Implement log file analysis for production use"
        }

    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        banking_logger.app_logger.info("System health monitoring stopped")

    def force_health_check(self) -> Dict:
        """Force an immediate health check"""
        return self.perform_health_check()


# Global health monitor instance
health_monitor = SystemHealthMonitor()
