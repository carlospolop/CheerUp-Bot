import random
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import os


class MyAES:
    def __init__(self):
        self.msgs = [
            {'cipher_text': b'n3IHkXagScXWa+j9ko38rX9lLJksvJtj94pQ7PcUG41ZPF8q0HSc3BLKwg6R+TAT1NsLkyfZMaoG+XflvqaB6pmnHFSPfXcw/aiVivDr2R+j+rzt+hJV0kV4e8rt17E5e5RVs1OnkhtLxmiP68We2jDOu99Fe0SGJGoL4DIlVqTE4r47IQ21HguSq4FSbIK6Hordpt15kMdTvH9s96JvlfRBvK5uKMkkrLwXWiy2Fm8g/s/cq8/KbNINxBN+egM37C4Mv6kGR8xTmiowm1vaeySbz+0L8xoXHb2LBH5tcpMkD5NmLoMdF0XPotrcNdIXx7nLvRbUb3mhJHd0Ba3Qjce7uXxxvY8kQDo0r4rpM8P3r4ad5M+9QLOdml7XyA3zUXCA07yctIVtdobzLPOf0ffqIOJnFw3kFsQJ3hBcEcEVK9WlnH14F9RhTN6iPiJXs2FygJWVfbHcG27XYWGlksI2HTe/JsUXmmLxPyT8B3k5L56X5QJYI47pFZbXe3gx+Za3xSVdl294FEFg5FNT4pR7wTrrmhLtaGgrcDOLK1YUtrSjt3WfXt1G0qbfuIvBX+WWYv+gam2C7miunoSzmQ0yZHRGlZgpSZOziTOHZlBvxEmlyGX+C0Mbn3BDz0jdcgSIk5rA364VUr1Q135HfUwVbIn9NNoSPzs9+3/UhxixldmyEsbn+iFZ0N7T/SUWUaU9siSiUZ4K5HALHeAWD6rRLSYyPDLVsHKV8VIhff9Mq0BcIn8WqTYawQyAk9GpEdvXlU9YyzG7A7u9iywL2sKuxguck0mWH/rDQzrawhfJHogsS31fmON0Q6ckbBg9', 'salt': b'WmXt2nz4lonSdxmW3zhQ3Q==', 'iv': b'XRUHdmdH0ZglbSgdiHCIgQ=='}
        ]
        self.password = os.getenv('ENCRYPTION_PASSWD')
    
    # pad with spaces at the end of the text
    # beacuse AES needs 16 byte blocks
    def pad(self, s):
        block_size = 16
        remainder = len(s) % block_size
        padding_needed = block_size - remainder
        return s + padding_needed * b' '

    # remove the extra spaces at the end
    def unpad(self, s): 
        return s.rstrip()
    
    def encrypt(self, plain_text):
        # generate a random salt
        salt = os.urandom(AES.block_size)

        # generate a random iv
        iv = Random.new().read(AES.block_size)

        # use the Scrypt KDF to get a private key from the password
        private_key = hashlib.scrypt(self.password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

        # pad text with spaces to be valid for AES CBC mode
        padded_text = self.pad(plain_text)
        
        # create cipher config
        cipher_config = AES.new(private_key, AES.MODE_CBC, iv)

        # return a dictionary with the encrypted text
        return {
            'cipher_text': base64.b64encode(cipher_config.encrypt(padded_text)),
            'salt': base64.b64encode(salt),
            'iv': base64.b64encode(iv)
        }
    
    
    def decrypt(self, enc_dict):
        # decode the dictionary entries from base64
        salt = base64.b64decode(enc_dict['salt'])
        enc = base64.b64decode(enc_dict['cipher_text'])
        iv = base64.b64decode(enc_dict['iv'])

        # generate the private key from the password and salt
        private_key = hashlib.scrypt(self.password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

        # create the cipher config
        cipher = AES.new(private_key, AES.MODE_CBC, iv)

        # decrypt the cipher text
        decrypted = cipher.decrypt(enc)

        # unpad the text to remove the added spaces
        original = self.unpad(decrypted)

        return original.decode("utf-8")

    def get_random_decrypt(self):
        random_entry = random.choice(self.msgs)
        return self.decrypt(random_entry)


if __name__ == '__main__':
    ma = MyAES()
    text = """PUT HERE THE TEXT"""
    encrypted = ma.encrypt(bytes(text, "utf-8"))
    print(encrypted)
    print()
    print(ma.decrypt(encrypted))

