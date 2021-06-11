import os, base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from CryptoList import RSAKey
from Crypto.PublicKey import RSA
import os, base64
from Crypto import Random

random_generator = Random.new().read
rsa = RSA.generate(1024, random_generator)
with open("RSA_key/private_key.pem", "wb") as f:
    f.write(rsa.exportKey())
with open("RSA_key/public_key.pem", "wb") as f:
    f.write(rsa.public_key().exportKey())
rsa = RSAKey()
t = rsa.encode("Hello World !")
print(t)
print(rsa.decode(t))


