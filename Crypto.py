import abc
from abc import ABC

class CryptoKey(ABC):
    @abc.abstractmethod
    def encode(self, content) -> str:
        return "encoded"

    @abc.abstractmethod
    def decode(self, content) -> str:
        return "decoded"

class RSA(CryptoKey):
    pass

class SymmetricKey(CryptoKey):
    pass

class CaesarCipher(CryptoKey):
    def __init__(self, offset):
        self.offset = offset

    def encode(self, content):
        return ''.join([chr((ord(c) - 33 + self.offset) % (126 - 33) + 33) for c in content])
    
    def decode(self, content):
        return ''.join([chr((ord(c) - 33 - self.offset) % (126 - 33) + 33) for c in content])
