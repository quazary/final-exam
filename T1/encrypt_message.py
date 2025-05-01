from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from os import urandom
import sys

# Load message
with open("message.txt", "rb") as f:
    message = f.read()
# Generate AES key and IV
aes_key = urandom(32)  # AES-256
iv = urandom(16)
# Pad and encrypt message
padder = sym_padding.PKCS7(128).padder()
padded_message = padder.update(message) + padder.finalize()
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_message) + encryptor.finalize()
# Save encrypted message
with open("encrypted_message.bin", "wb") as f:
    f.write(iv + ciphertext)
# Load RSA public key
with open("public_key.pem", "rb") as f:
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
print("[+] Message encrypted and AES key secured with RSA.")
