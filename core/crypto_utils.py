import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# In production, move this to a .env file!
SECRET_KEY = b'1234567890123456' 

def encrypt_uid(uid_string):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(uid_string.encode(), AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

def decrypt_payload(encrypted_payload):
    raw_cipher = base64.b64decode(encrypted_payload)
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(raw_cipher), AES.block_size)
    return decrypted.decode('utf-8')
