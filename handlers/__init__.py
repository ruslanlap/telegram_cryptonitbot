# handlers/__init__.py
from .start import register_start_handlers
from .hello import register_hello_handlers
from .encrypt import register_encrypt_handlers
from .decrypt import register_decrypt_handlers

def register_handlers(dp):
    register_start_handlers(dp)
    register_hello_handlers(dp)
    register_encrypt_handlers(dp)
    register_decrypt_handlers(dp)
