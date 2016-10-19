#!/usr/bin/env python3
import sys
import hashlib
from AESCipher import *

class SecureEncryption(object):
    def __init__(self, keys):
        assert len(keys) == 4
        self.keys = keys
        self.ciphers = []
        for i in range(4):
            self.ciphers.append(AESCipher(keys[i]))

    def enc(self, plaintext): # Because one encryption is not secure enough
        one        = self.ciphers[0].encrypt(plaintext)
        two        = self.ciphers[1].encrypt(one)
        three      = self.ciphers[2].encrypt(two)
        ciphertext = self.ciphers[3].encrypt(three)
        return ciphertext

    def dec(self, ciphertext):
        three      = AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))
        two        = AESCipher._unpad(self.ciphers[2].decrypt(three))
        one        = AESCipher._unpad(self.ciphers[1].decrypt(two))
        plaintext  = AESCipher._unpad(self.ciphers[0].decrypt(one))
        return plaintext

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./cryptolock.py file-you-want-to-encrypt password-to-use")
        exit()

    # Read file to be encrypted
    filename = sys.argv[1]
    plaintext = open(filename, "rb").read()

    user_input = sys.argv[2].encode('utf-8')
    assert len(user_input) == 8
    i = len(user_input) // 4
    keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
        hashlib.sha256(user_input[0:i]).digest(),
        hashlib.sha256(user_input[i:2*i]).digest(),
        hashlib.sha256(user_input[2*i:3*i]).digest(),
        hashlib.sha256(user_input[3*i:4*i]).digest(),
    ]
    s = SecureEncryption(keys)

    ciphertext = s.enc(plaintext)
    plaintext_ = s.dec(ciphertext)
    assert plaintext == plaintext_

    open(filename+".encrypted", "wb").write(ciphertext)
