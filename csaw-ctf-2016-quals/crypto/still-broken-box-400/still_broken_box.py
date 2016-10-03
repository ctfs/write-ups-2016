from functools import wraps
import errno
import os
import signal
import SocketServer
import random, time

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(60)
def recv(req, bytes):
        return req.recv(bytes)

def sign(req):
    d = 72596297030027247088224441953116786228228821869766428209408803933205537023998505397353083159853232071634218962765810199687928871114871071437224958879899194322315727105732530760408149352537661939990489463013528377200061436727961572916826684795534376097377874541448076152549360494498557470018458506007946440429
    N = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
    bits = list(range(0, 300))
    random.shuffle(bits)
    while True:
        req.sendall("Input an number(0~9999) to be signed:")
        msg = recv(req, 5)
        try:
            g = int(msg)
            if g < 0 or g > 9999:
                raise Exception
        except:
            req.sendall("Wrong input, quitting...")
            return
            
        if random.random() < 0.5:
            if len(bits) == 0:
                req.sendall("Box is overheating, quitting...")
                return
            pos = bits.pop()
            enc = pow(g, d^(2**pos), N)
        else:
            enc = pow(g, d, N)
        req.sendall("signature:{0}, N:{1}".format(str(enc), N))
        req.sendall("\nSign more items?(yes, no):")
        choice = recv(req, 4).split('\n')[0]
        if choice == 'no':
            break

class incoming(SocketServer.BaseRequestHandler):
    def handle(self):
        random.seed(time.time())
        req = self.request
        sign(req)

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(("0.0.0.0", 8000), incoming)
server.timeout = 60
server.serve_forever()
