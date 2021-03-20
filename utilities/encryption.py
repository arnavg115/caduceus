from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
def getKey(password,salt):
    password = password.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend= default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key
def encrypt(key,unencrypted):
    Handler = Fernet(key)
    unencrypted = unencrypted.encode()
    return Handler.encrypt(unencrypted)
def decrypt(key, encrypted):
    Handler = Fernet(key)
    unencrypted = Handler.decrypt(encrypted)
    return unencrypted.decode()