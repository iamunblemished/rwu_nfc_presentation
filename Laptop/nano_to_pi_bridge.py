import serial
import requests
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# --- CONFIGURATION ---
SERIAL_PORT = 'COM5' 
BAUD_RATE = 115200   
PI_IP = "192.168.197.11" 
URL = f"http://{PI_IP}:8000/verify/"
SHARED_SECRET = b"1234567890123456" 

# Timing variables
last_server_check = 0
server_check_interval = 1.0  # Poll server every 1.0 seconds

def encrypt_uid(uid):
    cipher = AES.new(SHARED_SECRET, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(uid.encode('utf-8'), AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

try:
    # Use a very short timeout so read operations don't hang the loop
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01) 
    print(f"Connected to Nano. System Responsive...")
except Exception as e:
    print(f"Error: {e}")
    exit()

while True:
    current_time = time.time()

    # --- 1. HIGH SPEED SERIAL CHECK (NFC SWIPE) ---
    # We check this every single loop iteration (very fast)
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "Physical UID:" in line:
                uid = line.split("Physical UID:")[-1].strip()
                print(f"Raw UID: {uid} [Processing...]")

                encrypted_payload = encrypt_uid(uid)
                # Note: This is a blocking call, but only happens on a swipe
                response = requests.post(URL, data={'payload': encrypted_payload}, timeout=2)
                print(f"Sent. Server Response: {response.status_code}")
        except Exception as e:
            print(f"Serial Error: {e}")

    # --- 2. ASYNCHRONOUS SERVER CHECK (REMOTE MSG) ---
    # This block only runs once per second, without slowing down the serial check

    
    if current_time - last_server_check > server_check_interval:
        try:
            remote_res = requests.get(f"http://{PI_IP}:8000/appliance-msg/", timeout=1)
            if remote_res.status_code == 200:
                data = remote_res.json()
                server_msg = data.get('message')
                is_auth = data.get('authorized', False)

                if server_msg and server_msg != "System Idle":
                    print(f"Forwarding to Nano: {server_msg}")
                    ser.write(f"MSG:{server_msg}\n".encode())
                    # time.sleep(1)
                    # # ONLY CLEAR AFTER SUCCESSFUL FORWARDING
                    # try:
                    #     requests.get(f"http://{PI_IP}:8000/clear_message/", timeout=1)
                    # except Exception as e:
                    #     print(f"Clear Failed: {e}")
        except Exception:
            pass # Keep terminal clean if server is briefly unreachable
        
        last_server_check = current_time

    # Minimal sleep to prevent 100% CPU usage, but fast enough for serial
    time.sleep(0.01)