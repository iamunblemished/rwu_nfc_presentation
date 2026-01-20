import os
import base64
import requests
from threading import Thread
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import AccessLog, Keycard
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from dotenv import load_dotenv

load_dotenv()

# AES Configuration
raw_key = os.getenv('SHARED_SECRET_KEY')
SHARED_SECRET = raw_key.encode('utf-8')

# --- NEW: GLOBAL STATES FOR THE APPLIANCE ---
is_authorized_state = False
current_appliance_msg = "System Idle"

# --- WEBHOOK DISPATCHER ---
def fire_webhooks(uid, status):
    """Sends a POST request to external appliances when access is granted."""
    appliance_urls = [
        "http://192.168.197.xx:5000/lights", # Update with your real IPs
        "http://192.168.197.xx:5000/coffee",
    ]
    payload = {
        "user": uid,
        "event": "access_granted",
        "timestamp": str(timezone.now()),
        "state": status
    }
    for url in appliance_urls:
        try:
            requests.post(url, json=payload, timeout=0.5)
        except Exception as e:
            print(f"Webhook failed for {url}: {e}")

# --- DASHBOARD VIEW ---
def dashboard(request):
    logs = AccessLog.objects.all().order_by('-timestamp')[:10]
    return render(request, 'core/dashboard.html', {
        'logs': logs,
        'is_authorized': is_authorized_state # Pass state to dashboard
    })

# --- NEW: REMOTE INPUT PAGE ---
def remote_input_page(request):
    """Renders the site page to type messages."""
    return render(request, 'core/remote.html')

# --- VERIFICATION VIEW (UPDATED) ---
@csrf_exempt
def verify_access(request):
    global is_authorized_state # Access the global switch
    if request.method == 'POST':
        try:
            encrypted_payload = request.POST.get('payload')
            if not encrypted_payload:
                return JsonResponse({"error": "No payload provided"}, status=400)

            # 2. Decrypt the UID
            raw_cipher = base64.b64decode(encrypted_payload)
            cipher = AES.new(SHARED_SECRET, AES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(raw_cipher), AES.block_size)
            uid = decrypted.decode('utf-8').strip()

            # 3. Check Database
            # This ensures only cards registered in your Django Admin work
            is_valid_user = Keycard.objects.filter(uid=uid, is_active=True).exists()

            if is_valid_user:
                is_authorized_state = True # UNLOCK THE SYSTEM
                Thread(target=fire_webhooks, args=(uid, "ON")).start()

            AccessLog.objects.create(scanned_uid=uid, granted=is_valid_user)

            return JsonResponse({
                "access": "granted" if is_valid_user else "denied",
                "uid_detected": uid,
                "authorized": is_authorized_state
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

# --- NEW: APPLIANCE ENDPOINT (FOR CLI) ---
@csrf_exempt
def send_to_appliance(request):
    """The CLI polls this to see if it should unlock or show a message."""
    global current_appliance_msg, is_authorized_state
    
    if request.method == 'POST':
        msg = request.POST.get('message', '')
        current_appliance_msg = msg
        return JsonResponse({"status": "Message Sent"})

    return JsonResponse({
        "authorized": is_authorized_state,
        "message": current_appliance_msg if is_authorized_state else "--- LOCKED ---"
    })

def clear_message(request):
    """Resets the appliance message after it has been processed."""
    global current_appliance_msg
    current_appliance_msg = "System Idle"
    return JsonResponse({"status": "cleared"})

# --- NEW: EMERGENCY RESET ---
def reset_system(request):
    """Call /unlock-cheat/ to lock the system back up."""
    global is_authorized_state
    is_authorized_state = False
    return JsonResponse({"status": "System Relocked"})
