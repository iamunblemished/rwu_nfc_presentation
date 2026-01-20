import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Use the EXACT same key you put in your Pi's core/views.py
SHARED_SECRET = b'1234567890123456' 
URL = "http://192.168.197.11:8000/verify/"

def simulate_card_swipe(card_uid):
    # 1. Encrypt the UID
    cipher = AES.new(SHARED_SECRET, AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(pad(card_uid.encode(), AES.block_size))
    payload = base64.b64encode(encrypted_bytes).decode('utf-8')

    # 2. Send to the Pi
    print(f"Sending encrypted UID: {payload}")
    response = requests.post(URL, data={'payload': payload})
    
    print(f"Server Response: {response.json()}")

# Try a random ID
simulate_card_swipe("TEST_CARD_001")