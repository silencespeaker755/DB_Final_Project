class CaesarCipher:
    def __init__(self, offset):
        self.offset = offset

    def encode(self, content):
        return ''.join([chr((ord(c) - 33 + self.offset) % (126 - 33) + 33) for c in content])

    def decode(self, content):
        return ''.join([chr((ord(c) - 33 - self.offset) % (126 - 33) + 33) for c in content])
