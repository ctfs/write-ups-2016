from Crypto.Cipher import AES
from bs4 import BeautifulSoup

import requests

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
    return text + (chr(pad) * pad)

def pkcs7_unpad(text, block_size=16):
    pad = ord(text[-1])
    if pad > block_size:
        raise PKCS7PaddingError("Given padding is not valid", text)

    pad_chars = text[-pad:]
    if (len(pad_chars) == 1 and ord(pad_chars[0]) == 0x01) or \
        all([pad_chars[0] == c for c in pad_chars[1:]]):
        return text[:-pad]
    else:
        raise PKCS7PaddingError("Given padding is not valid", text)

def break_into_blocks(text, block_size=16):
    return [text[i:i + block_size] for i in range(0, len(text), block_size)]

def aes_encrypt_chal17():
    r = requests.get("http://crypto.chal.csaw.io:8001")
    soup = BeautifulSoup(r.text, 'html.parser')

    data = soup.find_all("input")[0].get("value").decode("base64")
    return data[0:16], data[16:]

def aes_decrypt_chal17(IV, data):
    the_thing = IV+data
    r = requests.post("http://crypto.chal.csaw.io:8001", data={"matrix-id":the_thing.encode("base64")})
    soup = BeautifulSoup(r.text, 'html.parser')
    tmp = soup.find_all("center")
    if len(tmp) < 1:
        return True

    data = tmp[0].get_text()
    if data == "Caught exception during AES decryption...":
        return False
    else:
        return True

def challenge_17():
    IV, enc = aes_encrypt_chal17()
    print "Have IV:{} and encrypted data:{}".format(repr(IV), repr(enc))

    blocks = break_into_blocks(enc)
    actual_iv = IV
    decrypt_out = ""
    for n, block in enumerate(blocks):
        decrypt_block = ""
        pad_block = ""
        for i in range(1, len(block) + 1):
            tmp_pad_block = "".join([chr(ord(x) ^ i) for x in pad_block])
            for c in range(255):
                print "\tTesting [{}]".format(hex(c))
                test_iv = (chr(c) + tmp_pad_block).rjust(len(block), "\x00")
                if aes_decrypt_chal17(test_iv, block):
                    inter_byte = c ^ i
                    pad_block = chr(inter_byte) + pad_block
                    decrypt_byte = chr(inter_byte ^ ord(actual_iv[-i]))
                    decrypt_block = decrypt_byte + decrypt_block
                    break
            print "SUP"
        decrypt_out += decrypt_block
        print decrypt_out
        actual_iv = block

    decrypt_out = pkcs7_unpad(decrypt_out)
    print "[+] Decrypted:", decrypt_out

if __name__ == "__main__":
     challenge_17()
