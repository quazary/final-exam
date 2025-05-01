from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import serialization  # Corrected import
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
# Load private RSA key
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)
# Load encrypted AES key
with open("aes_key_encrypted.bin", "rb") as f:
    encrypted_aes_key = f.read()
# Decrypt AES key
aes_key = private_key.decrypt(
    encrypted_aes_key,
    rsa_padding.OAEP(
        mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
# Load encrypted message
with open("encrypted_message.bin", "rb") as f:
    data = f.read()
iv = data[:16]  # First 16 bytes = IV
ciphertext = data[16:]  # Rest = Encrypted message
# Decrypt message
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
decryptor = cipher.decryptor()
padded_message = decryptor.update(ciphertext) + decryptor.finalize()
# Unpad the message
unpadder = sym_padding.PKCS7(128).unpadder()
message = unpadder.update(padded_message) + unpadder.finalize()
# Save the plaintext
with open("decrypted_message.txt", "wb") as f:
    f.write(message)
print("[+] Message decrypted successfully.")
