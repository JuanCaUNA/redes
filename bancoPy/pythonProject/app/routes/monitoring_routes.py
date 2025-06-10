"""
System Monitoring Routes - API endpoints for health monitoring and system status
"""

from flask import Blueprint, jsonify, request
from app.services.health_monitoring_service import health_monitor
from app.services.transaction_monitoring_service import transaction_monitor
from app.services.logging_service import banking_logger
from app.models import db, Transaction, Account, User
from datetime import datetime, timedelta
from sqlalchemy import func, and_

# Optional import for system monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

monitoring_bp = Blueprint("monitoring", __name__)


@monitoring_bp.route("/health", methods=["GET"])
def get_health_status():
    """Get basic health status"""
    try:
        health_status = health_monitor.get_health_status()
        
        # Determine overall system health
        overall_status = "healthy"
        if any(component.get("status") == "error" for component in [
            health_status.get("database", {}),
            health_status.get("system", {}),
            health_status.get("transactions", {})
        ]):
            overall_status = "error"
        elif any(component.get("status") == "warning" for component in [
            health_status.get("database", {}),
            health_status.get("system", {}),
            health_status.get("transactions", {})
        ]):
            overall_status = "warning"

        return jsonify({
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "SINPE Banking System",
            "components": health_status
        })

    except Exception as e:
        banking_logger.log_error("health_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Health check failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/health/detailed", methods=["GET"])
def get_detailed_health():
    """Get detailed health report"""
    try:
        detailed_report = health_monitor.get_detailed_report()
        return jsonify({
            "status": "success",
            "data": detailed_report,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        banking_logger.log_error("detailed_health_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Detailed health check failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/metrics/transactions", methods=["GET"])
def get_transaction_metrics():
    """Get transaction metrics and statistics"""
    try:
        hours = request.args.get("hours", 24, type=int)
        hours = min(hours, 168)  # Limit to 1 week max

        stats = transaction_monitor.get_transaction_statistics(hours)
        
        return jsonify({
            "status": "success",
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        banking_logger.log_error("transaction_metrics_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to get transaction metrics",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/metrics/system", methods=["GET"])
def get_system_metrics():
    """Get detailed system performance metrics"""
    try:
        # CPU information
        cpu_info = {
            "usage_percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }

        # Memory information
        memory = psutil.virtual_memory()
        memory_info = {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": memory.percent
        }

        # Disk information
        disk = psutil.disk_usage('/')
        disk_info = {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": round((disk.used / disk.total) * 100, 1)
        }

        # Network statistics
        network = psutil.net_io_counters()
        network_info = {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }

        return jsonify({
            "status": "success",
            "data": {
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info,
                "network": network_info,
                "timestamp": datetime.utcnow().isoformat()
            }
        })

    except Exception as e:
        banking_logger.log_error("system_metrics_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to get system metrics",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/metrics/database", methods=["GET"])
def get_database_metrics():
    """Get database performance metrics"""
    try:
        # Basic database statistics
        total_users = User.query.count()
        total_accounts = Account.query.count()
        total_transactions = Transaction.query.count()

        # Recent activity
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_transactions = Transaction.query.filter(
            Transaction.created_at >= one_hour_ago
        ).count()

        # Transaction status distribution
        status_distribution = db.session.query(
            Transaction.status,
            func.count(Transaction.id)
        ).group_by(Transaction.status).all()

        # Transaction type distribution (last 24 hours)
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        type_distribution = db.session.query(
            Transaction.transaction_type,
            func.count(Transaction.id),
            func.sum(Transaction.amount)
        ).filter(
            Transaction.created_at >= twenty_four_hours_ago
        ).group_by(Transaction.transaction_type).all()

        return jsonify({
            "status": "success",
            "data": {
                "totals": {
                    "users": total_users,
                    "accounts": total_accounts,
                    "transactions": total_transactions
                },
                "recent_activity": {
                    "transactions_last_hour": recent_transactions
                },
                "status_distribution": [
                    {"status": status, "count": count}
                    for status, count in status_distribution
                ],
                "type_distribution_24h": [
                    {
                        "type": tx_type,
                        "count": count,
                        "total_amount": float(amount or 0)
                    }
                    for tx_type, count, amount in type_distribution
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
        })

    except Exception as e:
        banking_logger.log_error("database_metrics_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to get database metrics",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/alerts", methods=["GET"])
def get_active_alerts():
    """Get current system alerts"""
    try:
        health_status = health_monitor.get_health_status()
        alerts = health_status.get("alerts", [])

        # Add severity levels to alerts
        categorized_alerts = []
        for alert in alerts:
            severity = "warning"
            if any(keyword in alert.lower() for keyword in ["critical", "failed", "error"]):
                severity = "critical"
            elif any(keyword in alert.lower() for keyword in ["high", "slow"]):
                severity = "warning"
            else:
                severity = "info"

            categorized_alerts.append({
                "message": alert,
                "severity": severity,
                "timestamp": health_status.get("last_check")
            })

        return jsonify({
            "status": "success",
            "data": {
                "alerts": categorized_alerts,
                "total_alerts": len(categorized_alerts),
                "critical_count": len([a for a in categorized_alerts if a["severity"] == "critical"]),
                "warning_count": len([a for a in categorized_alerts if a["severity"] == "warning"]),
                "timestamp": datetime.utcnow().isoformat()
            }
        })

    except Exception as e:
        banking_logger.log_error("alerts_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to get alerts",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/health/force-check", methods=["POST"])
def force_health_check():
    """Force an immediate health check"""
    try:
        health_data = health_monitor.force_health_check()
        
        return jsonify({
            "status": "success",
            "message": "Health check completed",
            "data": health_data,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        banking_logger.log_error("force_health_check_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Health check failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@monitoring_bp.route("/status/summary", methods=["GET"])
def get_status_summary():
    """Get a concise status summary for dashboard"""
    try:
        health_status = health_monitor.get_health_status()
        
        # Calculate uptime (simplified - in production, track actual start time)
        uptime_seconds = psutil.boot_time()
        uptime = datetime.utcnow() - datetime.fromtimestamp(uptime_seconds)

        # Get key metrics
        cpu_usage = health_status.get("system", {}).get("cpu_percent", 0)
        memory_usage = health_status.get("system", {}).get("memory_percent", 0)
        transactions_24h = health_status.get("transactions", {}).get("last_24h", 0)
        success_rate = health_status.get("transactions", {}).get("success_rate", 0)

        return jsonify({
            "status": "success",
            "data": {
                "uptime_days": uptime.days,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "transactions_24h": transactions_24h,
                "success_rate": success_rate,
                "active_alerts": len(health_status.get("alerts", [])),
                "database_status": health_status.get("database", {}).get("status", "unknown"),
                "last_check": health_status.get("last_check"),
                "timestamp": datetime.utcnow().isoformat()
            }
        })

    except Exception as e:
        banking_logger.log_error("status_summary_endpoint", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to get status summary",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500
