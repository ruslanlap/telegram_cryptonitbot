# handlers/__init__.py

from .start import register_start_handlers
from .language import register_language_handlers
from .encrypt import register_encrypt_handlers
from .decrypt import register_decrypt_handlers
from .hello import register_hello_handlers

def register_handlers(dp):
    register_start_handlers(dp)
    register_language_handlers(dp)
    register_encrypt_handlers(dp)
    register_decrypt_handlers(dp)
    register_hello_handlers(dp)