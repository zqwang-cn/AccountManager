import base64
import hashlib


def xor(text, key):
    if not key:
        return text
    r = ''
    for i in range(len(text)):
        r += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return r


def encrypt(text, password):
    cipher = base64.encodebytes(xor(text, password).encode()).decode()
    return cipher


def decrypt(text, password):
    plain = xor(base64.decodebytes(text.encode()).decode(), password)
    return plain


def hash(text):
    return hashlib.new('md5', text.encode()).hexdigest()
