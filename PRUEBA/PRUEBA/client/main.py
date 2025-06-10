import argparse
import json
from client.utils.api_client import APIClient
from client.config import Config

def parse_args():
    parser = argparse.ArgumentParser(description='SINPE Transfer Client')
    parser.add_argument('--type', choices=['sinpe', 'movil'], required=True,
                      help='Type of transfer (sinpe or movil)')
    parser.add_argument('--amount', type=float, required=True,
                      help='Amount to transfer')
    parser.add_argument('--description', required=True,
                      help='Transfer description')
    
    # SINPE transfer specific arguments
    parser.add_argument('--sender-account', help='Sender account number (for SINPE)')
    parser.add_argument('--sender-name', help='Sender name (for SINPE)')
    parser.add_argument('--receiver-account', help='Receiver account number (for SINPE)')
    parser.add_argument('--receiver-bank', help='Receiver bank code (for SINPE)')
    parser.add_argument('--receiver-name', help='Receiver name (for SINPE)')
    
    # SINPE Móvil specific arguments
    parser.add_argument('--sender-phone', help='Sender phone number (for SINPE Móvil)')
    parser.add_argument('--receiver-phone', help='Receiver phone number (for SINPE Móvil)')
    
    return parser.parse_args()

def main():
    args = parse_args()
    client = APIClient()
    
    try:
        if args.type == 'sinpe':
            # Validate SINPE transfer arguments
            if not all([args.sender_account, args.sender_name, 
                       args.receiver_account, args.receiver_bank, args.receiver_name]):
                print("Error: All SINPE transfer arguments are required")
                return
            
            # Create sender and receiver account objects
            sender_account = {
                "account_number": args.sender_account,
                "name": args.sender_name
            }
            
            receiver_account = {
                "account_number": args.receiver_account,
                "bank_code": args.receiver_bank,
                "name": args.receiver_name
            }
            
            # Make the transfer
            response = client.make_sinpe_transfer(
                sender_account,
                receiver_account,
                args.amount,
                args.description
            )
            
        else:  # SINPE Móvil
            # Validate SINPE Móvil arguments
            if not all([args.sender_phone, args.receiver_phone]):
                print("Error: All SINPE Móvil arguments are required")
                return
            
            # Make the transfer
            response = client.make_sinpe_movil_transfer(
                args.sender_phone,
                args.receiver_phone,
                args.amount,
                args.description
            )
        
        # Print the response
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 