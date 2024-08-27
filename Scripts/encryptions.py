import os, re
from base64 import b64decode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding



def password_is_valid(password):
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    if len(password) <= 7:
        return False, "Password must be longer than 7 characters."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one numeric character."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase character."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase character."
    if not re.search(
        r"[@$!%*?&#]", password
    ):  # Adjust the symbols as per your requirement
        return False, "Password must contain at least one special character (@$!%*?&#)."
    return True, ""
