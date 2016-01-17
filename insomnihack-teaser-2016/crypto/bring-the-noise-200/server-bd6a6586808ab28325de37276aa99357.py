#!/usr/bin/env python

import SocketServer as ss
import struct
import os
from binascii import hexlify
import hashlib

FLAG = open('flag').read()
POWLEN = 5


def randint(bound):
    return struct.unpack('<L', os.urandom(4))[0] % bound


def learn_with_vibrations():
    q, n, eqs = 8, 6, 40
    solution = [randint(q) for i in range(n)]
    equations = []
    for i in range(eqs):
        coefs = [randint(q) for i in range(n)]
        result = sum([solution[i]*coefs[i] for i in range(n)]) % q
        vibration = randint(3) - 1
        result = (result + q + vibration) % q
        equations.append('%s, %d' % (str(coefs)[1:-1], result))
    return equations, solution


class Handler(ss.StreamRequestHandler):

    def handle(self):
        put = self.wfile.write

        challenge = hexlify(os.urandom(1+POWLEN/2))[:POWLEN]
        put('Challenge = %s\n' % challenge)
        response = self.rfile.readline()[:-1]
        responsehash = hashlib.md5(response).hexdigest().strip()
        if responsehash[:POWLEN] != challenge:
            put('Wrong\n')
            return

        equations, solution = learn_with_vibrations()
        for equation in  equations:
            put(equation + '\n')

        put('Enter solution as "1, 2, 3, 4, 5, 6"\n')

        sol = self.rfile.readline().strip()
        if sol != str(solution)[1:-1]:
            put('Wrong\n')
            return
        put('%s\n' % FLAG)


class ReusableTCPServer(ss.ForkingMixIn, ss.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    HOST, PORT = ('0.0.0.0', 1111)
    ss.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer((HOST, PORT), Handler)
    server.serve_forever()
