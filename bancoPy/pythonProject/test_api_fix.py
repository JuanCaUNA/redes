#!/usr/bin/env python3
"""
Test script to verify API endpoints work after database schema update
"""

import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://127.0.0.1:5443/api"


def test_transactions_api():
    """Test transactions API endpoint"""
    print("Testing transactions API...")

    try:
        response = requests.get(f"{BASE_URL}/transactions", verify=False)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('data', []))} transactions")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_accounts_api():
    """Test accounts API endpoint"""
    print("\nTesting accounts API...")

    try:
        response = requests.get(f"{BASE_URL}/accounts", verify=False)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            accounts = data.get("data", [])
            print(f"✅ Success! Found {len(accounts)} accounts")

            # Show first account details
            if accounts:
                first_account = accounts[0]
                print(
                    f"Sample account: ID={first_account.get('id')}, IBAN={first_account.get('iban')}"
                )
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


if __name__ == "__main__":
    print("🔍 Testing API endpoints after database schema update\n")

    # Test both endpoints
    transactions_ok = test_transactions_api()
    accounts_ok = test_accounts_api()

    print(f"\n📊 Results:")
    print(f"Transactions API: {'✅ Working' if transactions_ok else '❌ Failed'}")
    print(f"Accounts API: {'✅ Working' if accounts_ok else '❌ Failed'}")

    if transactions_ok and accounts_ok:
        print("\n🎉 All tests passed! The database schema update was successful.")
    else:
        print("\n⚠️ Some tests failed. Please check the server logs.")
