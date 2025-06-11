#!/usr/bin/env python3
"""
Test de Conectividad Inter-Bancaria
Prueba la conectividad y compatibilidad HMAC con otros bancos del ecosistema
"""

import requests
import json
import uuid
from datetime import datetime
from app.utils.hmac_generator import (
    generate_hmac_for_account_transfer,
    generate_hmac_for_phone_transfer,
)
import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# Configuración de bancos para pruebas
BANCOS_ACTIVOS = {
    "876": {
        "name": "Banco Josue",
        "url": "http://192.168.3.10:5000",
        "endpoint_sinpe": "/api/sinpe-transfer",
        "endpoint_movil": "/api/sinpe-movil-transfer",
        "enabled": True,
    },
    "119": {
        "name": "Banco TypeScript (Marconi)",
        "url": "http://192.168.2.10:3001",
        "endpoint_sinpe": "/api/sinpe/transfer",
        "endpoint_movil": "/api/sinpe/movil-transfer",
        "enabled": True,
    },
    "241": {
        "name": "Banco Brayan",
        "url": "http://192.168.4.10:5050",
        "endpoint_sinpe": "/api/sinpe-transfer",
        "endpoint_movil": "/api/sinpe-movil-transfer",
        "enabled": True,
    },
    "223": {
        "name": "Banco Kendall",
        "url": "http://192.168.5.10:3001",
        "endpoint_sinpe": "/api/sinpe-transfer",
        "endpoint_movil": "/api/sinpe-movil-transfer",
        "enabled": True,
    },
}


def test_health_endpoint(bank_code: str, bank_config: dict) -> bool:
    """Test health endpoint de un banco"""
    try:
        url = f"{bank_config['url']}/health"
        print(f"🔍 Probando health check: {url}")
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ {bank_config['name']} - Health OK")
            try:
                data = response.json()
                print(f"   Status: {data.get('status', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")
                print(f"   Bank Code: {data.get('bank_code', 'N/A')}")
            except:
                print(f"   Respuesta: {response.text[:100]}")
            return True
        else:
            print(f"❌ {bank_config['name']} - Health FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {bank_config['name']} - Connection FAILED: {str(e)}")
        return False


def test_sinpe_transfer(bank_code: str, bank_config: dict) -> bool:
    """Test transferencia SINPE tradicional"""
    try:
        # Generar datos de prueba
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Payload de transferencia
        payload = {
            "version": "1.0",
            "timestamp": timestamp,
            "transaction_id": transaction_id,
            "sender": {
                "account_number": "CR21-0152-0001-00-0000-0001-23",
                "bank_code": "152",
                "name": "Test Sender"
            },
            "receiver": {
                "account_number": f"CR21-{bank_code}-0001-00-0000-0001-23",
                "bank_code": bank_code,
                "name": "Test Receiver"
            },
            "amount": {
                "value": 1000.00,
                "currency": "CRC"
            },
            "description": "Test transfer - Conectividad Inter-Bancaria"
        }
        
        # Generar HMAC con formato corregido
        hmac_signature = generate_hmac_for_account_transfer(
            payload["sender"]["account_number"],
            timestamp,
            transaction_id,
            payload["amount"]["value"]
        )
        payload["hmac_md5"] = hmac_signature
        
        # Hacer request
        url = f"{bank_config['url']}{bank_config['endpoint_sinpe']}"
        print(f"🔍 Probando SINPE transfer: {url}")
        
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ {bank_config['name']} - SINPE Transfer OK")
            try:
                data = response.json()
                print(f"   Transaction ID: {data.get('transaction_id', 'N/A')}")
                print(f"   Status: {data.get('success', 'N/A')}")
            except:
                print(f"   Respuesta: {response.text[:100]}")
            return True
        else:
            print(f"❌ {bank_config['name']} - SINPE Transfer FAILED (Status: {response.status_code})")
            try:
                data = response.json()
                print(f"   Error: {data.get('error', 'Unknown error')}")
            except:
                print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {bank_config['name']} - SINPE Transfer Connection FAILED: {str(e)}")
        return False


def test_sinpe_movil_transfer(bank_code: str, bank_config: dict) -> bool:
    """Test transferencia SINPE Móvil"""
    try:
        # Generar datos de prueba
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Payload de transferencia móvil
        payload = {
            "version": "1.0",
            "timestamp": timestamp,
            "transaction_id": transaction_id,
            "sender": {
                "phone_number": "88887777"
            },
            "receiver": {
                "phone_number": "88886666"
            },
            "amount": {
                "value": 500.00,
                "currency": "CRC"
            },
            "description": "Test SINPE Móvil - Conectividad Inter-Bancaria"
        }
        
        # Generar HMAC móvil con formato corregido
        hmac_signature = generate_hmac_for_phone_transfer(
            payload["sender"]["phone_number"],
            timestamp,
            transaction_id,
            payload["amount"]["value"]
        )
        payload["hmac_md5"] = hmac_signature
        
        # Hacer request
        url = f"{bank_config['url']}{bank_config['endpoint_movil']}"
        print(f"🔍 Probando SINPE Móvil: {url}")
        
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ {bank_config['name']} - SINPE Móvil OK")
            try:
                data = response.json()
                print(f"   Transaction ID: {data.get('transaction_id', 'N/A')}")
                print(f"   Status: {data.get('success', 'N/A')}")
            except:
                print(f"   Respuesta: {response.text[:100]}")
            return True
        else:
            print(f"❌ {bank_config['name']} - SINPE Móvil FAILED (Status: {response.status_code})")
            try:
                data = response.json()
                print(f"   Error: {data.get('error', 'Unknown error')}")
            except:
                print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {bank_config['name']} - SINPE Móvil Connection FAILED: {str(e)}")
        return False


def main():
    """Ejecutar todas las pruebas de conectividad"""
    print("=" * 60)
    print("🏦 PRUEBAS DE CONECTIVIDAD INTER-BANCARIA")
    print("   Sistema SINPE - Banco Python Principal (152)")
    print("=" * 60)
    print()
    
    resultados = {
        "health": {},
        "sinpe": {},
        "movil": {}
    }
    
    for bank_code, bank_config in BANCOS_ACTIVOS.items():
        if not bank_config["enabled"]:
            continue
            
        print(f"\n📋 Probando banco: {bank_config['name']} (Código: {bank_code})")
        print("-" * 50)
        
        # Test Health
        resultados["health"][bank_code] = test_health_endpoint(bank_code, bank_config)
        print()
        
        # Test SINPE Transfer
        resultados["sinpe"][bank_code] = test_sinpe_transfer(bank_code, bank_config)
        print()
        
        # Test SINPE Móvil
        resultados["movil"][bank_code] = test_sinpe_movil_transfer(bank_code, bank_config)
        print()
    
    # Resumen final
    print("=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    for bank_code, bank_config in BANCOS_ACTIVOS.items():
        if not bank_config["enabled"]:
            continue
            
        health_ok = resultados["health"].get(bank_code, False)
        sinpe_ok = resultados["sinpe"].get(bank_code, False)
        movil_ok = resultados["movil"].get(bank_code, False)
        
        status = "✅" if all([health_ok, sinpe_ok, movil_ok]) else "⚠️" if any([health_ok, sinpe_ok, movil_ok]) else "❌"
        
        print(f"{status} {bank_config['name']} (Código: {bank_code})")
        print(f"   Health: {'✅' if health_ok else '❌'}")
        print(f"   SINPE: {'✅' if sinpe_ok else '❌'}")
        print(f"   Móvil: {'✅' if movil_ok else '❌'}")
        print()
    
    print("\n💡 Nota: Estas pruebas requieren que los bancos estén ejecutándose")
    print("   en sus respectivas IPs y que la red esté configurada correctamente.")


if __name__ == "__main__":
    main()
