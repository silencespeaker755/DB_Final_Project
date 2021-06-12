import abc
from abc import ABC
import os, base64
from dotenv import load_dotenv
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Protocol.KDF import PBKDF2

load_dotenv()

class CryptoKey(ABC):
    @abc.abstractmethod
    def encode(self, content) -> str:
        return "encoded"

    @abc.abstractmethod
    def decode(self, content) -> str:
        return "decoded"

class RSAKey(CryptoKey):
    def __init__(self):
        RSA_KEY_DIR = os.getenv('RSA_KEY_DIR', 'Test_data/RSA_key')
        with open(f'{RSA_KEY_DIR}/private_key.pem', "rb") as f:
            self.private_key = RSA.import_key(f.read())
        with open(f'{RSA_KEY_DIR}/public_key.pem', "rb") as f:
            self.public_key = RSA.import_key(f.read())

    def encode(self, content):
        cipher = PKCS1_OAEP.new(self.public_key)
        return base64.b64encode(cipher.encrypt(content.encode()))

    def decode(self, content):
        content = base64.b64decode(content)
        cipher = PKCS1_OAEP.new(self.private_key)
        return cipher.decrypt(content).decode()
        
        

class SymmetricKey(CryptoKey):
    def __init__(self, key): 
        hash_text = b'\xe3^\xad{\x89\xef\xe9\x0bK\x1c\x10\x08/Xp\xc3\x90\rb\xd2\xe2\xa7N\x81b#\xba\xb2\x8d\xbeaN'
        self.key = PBKDF2(key, hash_text, dkLen=32)
        self.block_size = AES.block_size

    def encode(self, content):
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(self._padding(content).encode('utf-8')))

    def decode(self, content):
        content = base64.b64decode(content)
        iv = content[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpadding(cipher.decrypt(content[self.block_size:])).decode('utf-8')

    def _padding(self, text):
        s = self.block_size
        return text + (s - len(text) % s) * (chr(s - len(text) % s))

    def _unpadding(self, text):
        return text[:-ord(text[-2:-1])]

class CaesarCipher(CryptoKey):
    def __init__(self, offset):
        self.offset = offset

    def encode(self, content):
        return ''.join([self.shift(c, self.offset) for c in content])
    
    def decode(self, content):
        return ''.join([self.shift(c, -self.offset) for c in content])

    def shift(self, character, offset):
        return chr((ord(character) - 33 + offset) % (126 - 33) + 33)
