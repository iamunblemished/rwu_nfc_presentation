import base64
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
# Import the model from the models file, don't define it here!
from .models import AccessLog, Keycard
import os
from dotenv import load_dotenv

load_dotenv()

# Use the key from the .env file. Note: AES needs the key in bytes.
raw_key = os.getenv('SHARED_SECRET_KEY')
SHARED_SECRET = raw_key.encode('utf-8')

def dashboard(request):
    logs = AccessLog.objects.all().order_by('-timestamp')[:10]
    return render(request, 'core/dashboard.html', {'logs': logs})

@csrf_exempt
def verify_access(request):
    if request.method == 'POST':
        try:
            encrypted_payload = request.POST.get('payload')
            raw_cipher = base64.b64decode(encrypted_payload)

            cipher = AES.new(SHARED_SECRET, AES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(raw_cipher), AES.block_size)
            uid = decrypted.decode('utf-8')

            is_authorized = Keycard.objects.filter(uid=uid, is_active=True).exists()
            AccessLog.objects.create(scanned_uid=uid, granted=is_authorized)

            return JsonResponse({"access": "granted" if is_authorized else "denied"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
