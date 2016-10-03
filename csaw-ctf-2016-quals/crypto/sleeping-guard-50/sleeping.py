import base64
from twisted.internet import reactor, protocol
import os

PORT = 8000

import struct
def get_bytes_from_file(filename):  
    return open(filename, "rb").read()  
    
# remove this for distribution of server
KEY = "WoAh_A_Key!?"

def length_encryption_key():
    return len(KEY)

def get_magic_png():
    image = get_bytes_from_file("./sleeping.png")
    encoded_string = base64.b64encode(image)
    key_len = length_encryption_key()
    print 'Sending magic....'
    if key_len != 12:
        return ''
    return encoded_string 
    

class MyServer(protocol.Protocol):
    def connectionMade(self):
        resp = get_magic_png()
        self.transport.write(resp)

class MyServerFactory(protocol.Factory):
    protocol = MyServer

factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
