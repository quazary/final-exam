from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.hashes import SHA256
from os import urandom
import hashlib

# Load message and compute hash
with open("alice_message.txt", "rb") as f:
    message = f.read()
    original_hash = hashlib.sha256(message).hexdigest()
    print(f"Original SHA-256 hash: {original_hash}")

# Generate random AES key and IV
aes_key = urandom(32)  # 256-bit key
iv = urandom(16)       # 128-bit IV

# Pad and encrypt message
padder = padding.PKCS7(128).padder()
padded_data = padder.update(message) + padder.finalize()

cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_data) + encryptor.finalize()

# Save encrypted message (IV + ciphertext)
with open("encrypted_file.bin", "wb") as f:
    f.write(iv + ciphertext)

# Load Bob's public key
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Encrypt AES key with RSA
encrypted_aes_key = public_key.encrypt(
    aes_key,
    rsa_padding.OAEP(
        mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save encrypted AES key
with open("aes_key_encrypted.bin", "wb") as f:
    f.write(encrypted_aes_key)

print("[+] Message encrypted and AES key secured with Bob's public key") 
