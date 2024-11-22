# utils/encryption.py

import os
import base64
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(message, password):
    backend = default_backend()
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(salt + iv + ciphertext).decode('utf-8')

def decrypt(encrypted_message, password):
    backend = default_backend()
    encrypted = base64.b64decode(encrypted_message.encode('utf-8'))
    salt = encrypted[:16]
    iv = encrypted[16:32]
    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext_padded = decryptor.update(encrypted[32:]) + decryptor.finalize()
    try:
        plaintext = unpadder.update(plaintext_padded) + unpadder.finalize()
    except ValueError as e:
        logger.error(f"Error during decryption: {e}")
        raise ValueError("Invalid padding bytes")
    return plaintext.decode('utf-8')

def escape_markdown_v2(text):
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + char if char in escape_chars else char for char in text])