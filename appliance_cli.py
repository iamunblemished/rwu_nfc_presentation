import requests
import time
import os

SERVER_URL = "http://192.168.197.11:8000/appliance-msg/"
last_msg = ""

def print_locked_ui():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("      [!] SECURITY ALERT: SYSTEM LOCKED [!]")
    print("="*50)
    print("\n  STATUS: WAITING FOR AUTHORIZED NFC SWIPE...")
    print("\n" + "="*50)

def print_unlocked_ui(content):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("      RWU APPLIANCE NODE - [UNLOCKED]      ")
    print("="*50)
    print(f"\n  >> INCOMING COMMAND: {content}")
    print("\n" + "="*50)

while True:
    try:
        response = requests.get(SERVER_URL)
        data = response.json()
        
        authorized = data.get('authorized', False)
        message = data.get('message', "")

        if not authorized:
            print_locked_ui()
        else:
            if message != last_msg:
                print_unlocked_ui(message)
                last_msg = message
            
    except Exception as e:
        print(f"Connection Error: {e}")
    
    time.sleep(2)