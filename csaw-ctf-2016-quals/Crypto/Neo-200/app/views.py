from flask import render_template, request
import hashlib, struct, json
from Crypto.Cipher import AES, DES
from Crypto import Random
import base64
import hashlib
import hmac
import os
import time
import random

IV = Random.new().read(AES.block_size)

challenge_flag = "flag{what_if_i_told_you_you_solved_the_challenge}"
challenge_key  = 'csawctf_uber_key'

class PKCS7PaddingError(Exception):
    def __init__(self, message, data):
        super(PKCS7PaddingError, self).__init__(message)
        self.data = data

    def __str__(self):
        return self.message + ": " + repr(self.data)

def pkcs7_padding(text, block_size=16):
    pad = len(text) % block_size
    if pad == 0:
        return text
    pad = block_size - pad
    return text + bytes(chr(pad) * pad, 'utf-8')

def pkcs7_unpad(text, block_size=16):
    pad = text[-1]
    if pad > block_size:
        raise PKCS7PaddingError("Given padding is not valid", text)

    pad_chars = text[-pad:]
    if (len(pad_chars) == 1 and pad_chars[0] == 0x01) or \
        all([pad_chars[0] == c for c in pad_chars[1:]]):
        return text[:-pad]
    else:
        raise PKCS7PaddingError("Given padding is not valid", text)

def aes_encrypt(key, string):
    global IV
    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext = pkcs7_padding(string, len(key))

    encrypt = cipher.encrypt(plaintext.decode("utf-8"))
    return_data = IV + encrypt
    return return_data

def aes_decrypt(key, data):
    IV = data[0:len(key)]
    data = data[len(key):]
    
    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypt = cipher.decrypt(data)
    return pkcs7_unpad(decrypt, len(key))

def init_views(app):
    @app.route('/', methods=['GET', 'POST'])
    def challenge():
        matrix_id = base64.b64encode(aes_encrypt(challenge_key, bytes(challenge_flag, "utf-8"))).decode("utf-8")

        if request.method == 'GET':
            return render_template('index.html', matrix_id=matrix_id)

        try:
            sid = base64.b64decode(bytes(request.form.get('matrix-id'), 'utf-8'))
        except:
            error = "Neo, that isn't base64. What are you thinking? How are we going to save humanity if you don't even know how to base64 encode something properly???"
            return render_template('index.html', matrix_id=matrix_id, error=error)

        if sid:
            try:
                ptext = aes_decrypt(challenge_key, sid)
            except:
                error = "Caught exception during AES decryption..."
                return render_template('index.html', matrix_id=request.form.get('matrix-id'), error=error)

            return render_template('index.html')
        else:
            return render_template('index.html', matrix_id=matrix_id)
