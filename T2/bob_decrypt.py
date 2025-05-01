from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.hashes import SHA256
import hashlib

# Load private key
with open("private.pem", "rb") as f:
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
with open("encrypted_file.bin", "rb") as f:
    data = f.read()
iv = data[:16]
ciphertext = data[16:]

# Decrypt message
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
decryptor = cipher.decryptor()
padded_message = decryptor.update(ciphertext) + decryptor.finalize()

# Unpad message
unpadder = padding.PKCS7(128).unpadder()
message = unpadder.update(padded_message) + unpadder.finalize()

# Save decrypted message
with open("decrypted_message.txt", "wb") as f:
    f.write(message)

# Verify integrity
with open("alice_message.txt", "rb") as f:
    original_hash = hashlib.sha256(f.read()).hexdigest()

decrypted_hash = hashlib.sha256(message).hexdigest()

print(f"Original hash: {original_hash}")
print(f"Decrypted hash: {decrypted_hash}")

if original_hash == decrypted_hash:
    print("[+] Message decrypted successfully and integrity verified!")
else:
    print("[-] Integrity check failed! The message may have been tampered with.") 
