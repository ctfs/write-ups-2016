from gmpy2 import mpz, invert
import os
import hashlib
import struct
import socket
import SocketServer
import logging
import base64
import shlex
import subprocess


"""
    params
"""

ADDRESS = '0.0.0.0'
PORT = 8889
TIMEOUT = 60.0
MAX_DATA_TO_RECEIVE_LENGTH = 8196
logger = None
keys_file_path = '.'


"""
    utils
"""

def data_to_int(s):
    return mpz(s.encode('hex'), 16)

def SHA1(data):
    return data_to_int(hashlib.sha1(data).hexdigest())


def import_public_key(keys_path):
    key_public = os.path.join(keys_path, 'key.public')
    assert (os.path.exists(key_public))
    with open(key_public, 'r') as f:
        data = f.read()
        d = data.split('\n')
        p = mpz(d[0])
        q = mpz(d[1])
        g = mpz(d[2])
        y = mpz(d[3])
        return (p, q, g, y)

def import_private_key(keys_path):
    key_private = os.path.join(keys_path, 'key.private')
    assert (os.path.exists(key_private))
    with open(key_private, 'r') as f:
        data = f.read()
        d = data.split('\n')
        p = mpz(d[0])
        q = mpz(d[1])
        g = mpz(d[2])
        x = mpz(d[3])
        y = mpz(d[4])
        return (p, q, g, x, y)


def import_cmd_signature(cmd, keys_path):
    f = os.path.join(keys_path, '{0}.sig'.format(cmd))
    with open(f, 'r') as f:
        data = f.read()
        d = data.split('\n')
        (r, s) = (mpz(d[0]), mpz(d[1]))
        return (r, s)


"""
    sign data
"""

def sign(data, p, q, g, x, k):
    r = pow(g, k, p) % q
    s = (invert(k, q) * (SHA1(data) + x * r)) % q
    return (r, s)

def verify(data, p, q, g, y, r, s):
    if not (r > 0 and r < q): return False
    if not (s > 0 and s < q): return False
    w = invert(s, q)
    u1 = (SHA1(data) * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    if v == r:
        return True
    else:
        return False


"""
    server
"""

def read_message(s):
    received_buffer = s.recv(4)
    if len(received_buffer) < 4:
        raise Exception('Error while receiving data')
    to_receive = struct.unpack('>I', received_buffer[0:4])[0]
    if to_receive > MAX_DATA_TO_RECEIVE_LENGTH:
        raise Exception('Too many bytes to receive')
    received_buffer = ''
    while (len(received_buffer) < to_receive):
        received_buffer += s.recv(to_receive - len(received_buffer))
    return received_buffer

def send_message(s, message):
    send_buffer = struct.pack('>I', len(message)) + message
    s.sendall(send_buffer)

def run_cmd(cmd):
    try:
        args = shlex.split(cmd)
        return subprocess.check_output(args)
    except Exception as ex:
        return str(ex)


class ForkingTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketServer.TCPServer.server_bind(self)

class ServiceServerHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def do_challenge(self):
        proof = base64.b64encode(os.urandom(12))
        proof_len = len(proof)+5
        message = 'Solve a puzzle first: find an x such that ' \
                    'SHA1(x)[-3:]==\'\\xff\\xff\\xff\' and len(x)=={0} and x[:{1}]=={2}'.format(proof_len, len(proof), proof)
        send_message(self.request, message)
        test = read_message(self.request)
        ha = hashlib.sha1()
        ha.update(test)
        if (len(test) != proof_len
            or test[:-5] != proof or
            ha.digest()[-3:] != '\xff\xff\xff'):
            send_message(self.request, 'Your solution is incorrect')
            return False
        return True

    def handle(self):
        logger.info('Accepted  connection from {0}'.format(self.client_address[0]))
        self.request.settimeout(TIMEOUT)
        try:
            if not self.do_challenge():
                raise Exception('Failed to pass the test')
            (p, q, g, x, y) = import_private_key(keys_file_path)
            while True:
                message = read_message(self.request)
                (r_str, s_str, cmd_exp) = message.split('\n')
                logger.debug('Accepting command {0}'.format(cmd_exp))
                (r, s) = (mpz(r_str), mpz(s_str))
                if not verify(cmd_exp, p, q, g, y, r, s):
                    raise Exception('Signature verification check failed')
                cmd = shlex.split(cmd_exp)[0]
                if cmd == 'ls':
                    ret_str = run_cmd(cmd_exp)
                    send_message(self.request, ret_str)
                elif cmd == 'dir':
                    ret_str = run_cmd(cmd_exp)
                    send_message(self.request, ret_str)
                elif cmd == 'cd':
                    try:
                        path = ''.join(shlex.split(cmd_exp)[1:])
                        os.chdir(path)
                        send_message(self.request, '')
                    except Exception as ex:
                        send_message(self.request, str(ex))
                elif cmd == 'cat':
                    try:
                        files = shlex.split(cmd_exp)
                        if len(files) == 1:
                            raise Exception('Nothing to cat')
                        ret_str = run_cmd(cmd_exp)
                        send_message(self.request, ret_str)
                    except Exception as ex:
                        send_message(self.request, str(ex))
                elif cmd == 'exit':
                    break
                elif cmd == 'leave':
                    break
                else:
                    send_message(self.request, 'Unknown command {0}'.format(cmd))
                    break
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        finally:
            logger.info('Processed connection from {0}'.format(self.client_address[0]))
        return


"""
    checks
"""

def check_cmd_signatures(keys_path):
    cmd1 = 'exit'
    cmd2 = 'leave'
    (p, q, g, y) = import_public_key(keys_path)
    (r1, s1) = import_cmd_signature(cmd1, keys_path)
    assert (verify(cmd1, p, q, g, y, r1, s1))
    (r2, s2) = import_cmd_signature(cmd2, keys_path)
    assert (verify(cmd2, p, q, g, y, r2, s2))


"""
    main
"""

if __name__ == '__main__':
    check_cmd_signatures(keys_file_path)
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    address = (ADDRESS, PORT)
    server = ForkingTCPServer(address, ServiceServerHandler)
    server.timeout = 5
    server.serve_forever()
